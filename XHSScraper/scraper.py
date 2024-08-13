import os
import pandas as pd
from tqdm import tqdm
import time
from DrissionPage import ChromiumPage
from .config import LOGIN_URL, SEARCH_URL_TEMPLATE, DEFAULT_WAIT_TIME, DEFAULT_CRAWL_TIMES, LOG_FORMAT, LOG_LEVEL, KEYWORD
from .utils import setup_logging, wait_random_time, encode_keyword

class XHSScraper:
    def __init__(self):
        self.page = None
        self.page2 = None
        self.logger = setup_logging(LOG_FORMAT, LOG_LEVEL)       
    


    def _perform_login(self):
        self.page = ChromiumPage()
        self.page.get(LOGIN_URL)
        if self.page.ele('.login-container'):  # only first time 
            self.logger.info("Scan the QR code to login.")
            time.sleep(DEFAULT_WAIT_TIME)
        else:
            self.logger.info("Already logged in.")



    def search(self, keyword_encoded):
        self.page.get(SEARCH_URL_TEMPLATE + keyword_encoded)


    def extract_user_info(self):
        # Basic profile
        container = self.page.ele('.onebox')
        if container:
            username = self.page.ele('.user-name').text
            userupdate = self.page.ele('.user-tag').text
            userid = self.page.ele('.user-desc').text
            userid = userid.replace('小红书号：', '')
            userlink = container.ele('tag:a').link
            userdesc = self.page.eles('.user-desc-box')
            # may have different situation
            if len(userdesc) > 2:
                usertype = userdesc[0].text
                usernote = userdesc[2].text
            else:
                usertype = ''
                usernote = userdesc[1].text
            usernote = usernote.replace('笔记・', '')
        else:
            self.logger.info("Cannot be searched. Please check the keyword.")
            username, userupdate, userid, userlink, usernote, usertype = '', '', '', '', '', ''
        return username, userupdate, userid, userlink, usernote, usertype



    def extract_additional_info(self, userlink):
        # Check if userlink is valid
        if not userlink:
            self.logger.info("User link is invalid, skipping additional info extraction.")
            return '', '', '', '', '', ''
        # Additional profile
        self.page2 = ChromiumPage()
        self.page2.get(userlink)

        avatar = self.page2.ele('.avatar-wrapper').ele('tag:img').link
        usertags = self.extract_user_tags()
        usersign = self.page2.ele('.user-desc').text

        counts = self.page2.eles('.count')
        follower = counts[0].text
        fans = counts[1].text
        like_collect = counts[2].text

        return avatar, usertags, usersign, follower, fans, like_collect



    def extract_user_tags(self):
        user_tags = self.page2.eles('.tag-item')
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
        sections = page.eles('.note-item') if page else []
        post_data = []

        for session in sections:
            try:
                note_link = session.ele('tag:a').link
                footer = session.ele('.footer')
                title = footer.ele('.title').text
                like = footer.ele('.like-wrapper like-active').text
                post_data.append([note_link, title, like])
            except Exception as e:
                self.logger.error(f"Error occurred while processing session: {e}")

        return post_data


    
    def page_scroll_down(self, page):
        # Scroll down the page
        if page:
            wait_random_time()
            page.scroll.to_bottom()


    
    def craw(self, times):
        # Crawl the posts
        all_posts = []

        if not self.page2:
            self.logger.error("User profile link is not initialized or keyword search returned no results.")
            return pd.DataFrame(columns=['post_link', 'post_title', 'post_like']) # Return an empty DataFrame

        for _ in tqdm(range(times)):
            post_info = self.get_post_info(self.page2)
            all_posts.extend(post_info)
            self.page_scroll_down(self.page2)

        df = pd.DataFrame(all_posts, columns=['post_link', 'post_title', 'post_like'])
        return df



    def run(self, times, keyword_encoded):
        # Run the whole process
        self._perform_login()
        self.search(keyword_encoded)
        kol_combined_info = self.combine_kol_info()
        result_df = self.craw(times)
        return kol_combined_info, result_df



    def get_data(self, keyword):
        # Get the data and save it to an Excel file
        keyword_encoded = encode_keyword(keyword)
        kol_combined_info, result_df = self.run(DEFAULT_CRAWL_TIMES, keyword_encoded) # Default is 5. Be free to change it.
        with pd.ExcelWriter(f'{keyword}_{time.strftime("%Y-%m-%d")}.xlsx') as writer:
            kol_combined_info.to_excel(writer, sheet_name='kol_info', index=False)
            result_df.to_excel(writer, sheet_name='post_info', index=False)
        print("Crawling finished. Data saved.")


    
if __name__ == "__main__":
    xhs = XHSScraper()
    xhs.get_data(KEYWORD)

