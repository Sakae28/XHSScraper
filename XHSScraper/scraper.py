import os
import pandas as pd
from tqdm import tqdm
import time
from DrissionPage import ChromiumPage
from .config import (
    LOGIN_URL,
    SEARCH_URL_TEMPLATE,
    DEFAULT_WAIT_TIME,
    DEFAULT_CRAWL_TIMES,
    LOG_FORMAT,
    LOG_LEVEL,
    KEYWORD,
    EXTRA_NOTE_INFO,
    EXTRA_POST_INFO
)
from .utils import setup_logging, wait_random_time, encode_keyword

class XHSScraper:
    def __init__(self):
        self.loginpage = None
        self.searchpage = None
        self.userpage = None
        self.detailpage = None
        self.logger = setup_logging(LOG_FORMAT, LOG_LEVEL)       
    


    def _perform_login(self):
        self.loginpage = ChromiumPage()
        self.loginpage.get(LOGIN_URL)
        if self.loginpage.ele('.login-container'):  # only first time 
            self.logger.info("Scan the QR code to login.")
            time.sleep(DEFAULT_WAIT_TIME)
        else:
            self.logger.info("Already logged in.")



    def search(self, keyword_encoded):
        search_url = SEARCH_URL_TEMPLATE + keyword_encoded
        self.searchpage = ChromiumPage()
        self.searchpage.get(search_url)
        self.searchpage_url = self.searchpage.url


    def check_container(self):
        container = self.searchpage.ele('.onebox')
        return container


    def diff_line(self, times, container):
        if container: # if the element exists, it means the keyword is correct
            kol_info = self.combine_kol_info()
            userlink = kol_info['user link'][0]
            note_df = self.crawl_notes(times)
            post_df = self.crawl_posts(times, userlink)
        else: # if not, return empty dataframes for kol_info and post_df but still crawl notes
            kol_info = pd.DataFrame()
            self.logger.warning("Keyword is not correct. No user found.")
            note_df = self.crawl_notes(times)
            post_df = pd.DataFrame()
            self.logger.warning("No post found.")
        return kol_info, note_df, post_df


    def extract_user_info(self):
        # Basic profile
        username = self.searchpage.ele('.user-name').text
        userupdate = self.searchpage.ele('.user-tag').text
        userid = self.searchpage.ele('.user-desc').text
        userid = userid.replace('小红书号：', '')
        userlink = self.searchpage.ele('.onebox').ele('tag:a').link
        userdesc = self.searchpage.eles('.user-desc-box')
        # may have different situation
        if len(userdesc) > 2:
            usertype = userdesc[0].text
            usernote = userdesc[2].text
        else:
            usertype = ''
            usernote = userdesc[1].text
        usernote = usernote.replace('笔记・', '')

        return username, userupdate, userid, userlink, usernote, usertype   
            
        

    def extract_additional_info(self, userlink):
        # Additional profile
        self.userpage = ChromiumPage()
        self.userpage.get(userlink)

        avatar = self.userpage.ele('.avatar-wrapper').ele('tag:img').link
        usertags = self.extract_user_tags()
        usersign = self.userpage.ele('.user-desc').text

        counts = self.userpage.eles('.count')
        follower = counts[0].text
        fans = counts[1].text
        like_collect = counts[2].text

        return avatar, usertags, usersign, follower, fans, like_collect



    def extract_user_tags(self):
        user_tags = self.userpage.eles('.tag-item')
        tag_str = ''
        
        if user_tags:
            icon = user_tags[0].ele('.reds-icon') # If the user has the gender icon, it must has the element
            
            if icon:
                # Get the gender information
                gender_element = icon.children()[0].attrs.get('xlink:href', '')
                gender_str = gender_element.replace('#', '') if gender_element else ''
                
                if len(user_tags) > 1:
                    tag_str = ' | '.join([tag.text for tag in user_tags[1:]])
                    tag_str = f"{gender_str} | {tag_str}" if gender_str else tag_str # Join all the tags together
                else:
                    tag_str = gender_str
            else:
                # Directly join other tags together
                tag_str = ' | '.join([tag.text for tag in user_tags])
        
        return tag_str



    def combine_kol_info(self):
        # Combine all information
        username, userupdate, userid, userlink, usernote, usertype = self.extract_user_info()
        avatar, usertags, usersign, follower, fans, like_collect = self.extract_additional_info(userlink)
        kol_info = {
            'user name': username,
            'user update': userupdate,
            'user id': userid,
            'user link': userlink,
            'user type': usertype,
            'user note': usernote,
            'avatar': avatar,
            'user tags': usertags,
            'user sign': usersign,
            'follower': follower,
            'fans': fans,
            'like_collect': like_collect
        }
        kol_info = pd.DataFrame(kol_info, index=[0])
        return kol_info



    def get_post_info(self, page):
        # Retrieve each post
        sections = page.eles('.note-item')
        post_data = []

        for session in sections:
            try:
                note_link = session.ele('.cover ld mask').link
                footer = session.ele('.footer')
                title = footer.ele('.title').text
                username = footer.ele('.name').text
                like = footer.ele('.like-wrapper like-active').text
                post_data.append([note_link, title, username, like])
            except Exception as e:
                self.logger.error(f"Error occurred while processing session: {e}")

        return post_data


    
    def page_scroll_down(self, page):
        # Scroll down the searchpage
        page.set.scroll.smooth(on_off=False) # turn off smooth scroll
        wait_random_time()
        page.scroll.to_bottom()


    
    def crawl_notes(self, times):
        all_notes = []

        # Make sure we start crawling notes on the search searchpage
        if hasattr(self, 'searchpage_url') and self.searchpage_url:
            self.searchpage.get(self.searchpage_url)
        else:
            self.logger.error("Searchpage URL is not initialized. Please run the search function first.")
            return None, None

        # Always crawl related notes from search searchpage
        for _ in tqdm(range(times), desc='Crawling notes'):
            note_info = self.get_post_info(self.searchpage)
            all_notes.extend(note_info)
            self.page_scroll_down(self.searchpage)

        note_df = pd.DataFrame(all_notes, columns=['note_link', 'note_title', 'note_user', 'note_like'])
        note_df.drop_duplicates(subset=['note_link'], inplace=True)

        return note_df


    def crawl_posts(self, times, userlink):
        all_posts = []

        # If the keyword is correct, crawl the user's posts
        self.userpage.get(userlink)
        for _ in tqdm(range(times), desc='Crawling posts'):
            post_info = self.get_post_info(self.userpage)
            all_posts.extend(post_info)
            self.page_scroll_down(self.userpage)
        
        post_df = pd.DataFrame(all_posts, columns=['post_link', 'post_title', 'post_user', 'post_like'])
        post_df.drop_duplicates(subset=['post_link'], inplace=True)

        return post_df



    def run(self, keyword_encoded):
        self._perform_login()
        self.search(keyword_encoded)
        container = self.check_container()
        kol_combined_info, note_df, post_df = self.diff_line(DEFAULT_CRAWL_TIMES, container)
        return kol_combined_info, note_df, post_df


    def get_note_post_detail(self, row):
        self.detailpage = ChromiumPage()
    
        # get note_link or post_link
        link = row.get('note_link') or row.get('post_link')
        if not link:
            return pd.Series([None]*5, index=['date', 'collect', 'comment', 'desc', 'hashtag'])
        
        self.detailpage.get(link)
        date = self.detailpage.ele('.date').text
        collect = self.detailpage.ele('.collect-wrapper').ele('.count').text
        collect = "0" if collect == '收藏' else collect
        comment = self.detailpage.ele('.chat-wrapper').ele('.count').text
        comment = "0" if collect == '评论' else comment
        desc = self.detailpage.ele('tag:div@class=desc').ele('tag:span').text
        desc = desc.replace("\n", "")

        # process hashtags and description
        hashtags = self.detailpage.eles('#hash-tag')
        if hashtags:
            hashtag = ' '.join([tag.text for tag in hashtags]).replace("\n", "")
        else:
            hashtag = ''
        
        return pd.Series([date, collect, comment, desc, hashtag], index=['date', 'collect', 'comment', 'desc', 'hashtag'])


    def get_data(self, keyword, extra_note_info, extra_post_info):
        # Get the data and save it to an Excel file
        if not keyword:
            self.logger.error("Keyword list is empty. Exiting the process.")
            return None
        
        for kw in keyword:
            keyword_encoded = encode_keyword(kw)
            kol_combined_info, note_df, post_df = self.run(keyword_encoded)
            
            if extra_note_info:
                self.logger.info("Fetching extra note information...")
                note_df[['date', 'collect', 'comment', 'desc', 'hashtag']] = note_df.apply(self.get_note_post_detail, axis=1)           
            if extra_post_info:
                self.logger.info("Fetching extra post information...")
                post_df[['date', 'collect', 'comment', 'desc', 'hashtag']] = post_df.apply(self.get_note_post_detail, axis=1)
            
            filename = f'{kw}_{time.strftime("%Y-%m-%d")}.xlsx'
            with pd.ExcelWriter(filename) as writer:
                kol_combined_info.to_excel(writer, sheet_name='kol_info', index=False)
                note_df.to_excel(writer, sheet_name='note_list', index=False)
                post_df.to_excel(writer, sheet_name='post_list', index=False)
        
            print(f"Crawling finished for {kw}. Data saved.")




if __name__ == "__main__":
    xhs = XHSScraper()
    xhs.get_data(KEYWORD, EXTRA_NOTE_INFO, EXTRA_POST_INFO)

