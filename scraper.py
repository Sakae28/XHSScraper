import os
import pandas as pd
from tqdm import tqdm
import time
from DrissionPage import ChromiumPage
from .config import LOGIN_URL, SEARCH_URL_TEMPLATE, DEFAULT_WAIT_TIME, DEFAULT_CRAWL_TIMES, LOG_FORMAT, LOG_LEVEL, KEYWORD
from .utils import setup_logging, wait_random_time, encode_keyword

class XHSScraper:
    def __init__(self, keyword):
        self.keyword = keyword
        self.keyword_encoded = encode_keyword(keyword)
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


    def search(self):
        self.page.get(SEARCH_URL_TEMPLATE + self.keyword_encoded)


    def extract_user_info(self):
        # Basic profile
        username = self.page.ele('.user-name').text
        userupdate = self.page.ele('.user-tag').text
        userid = self.page.ele('.user-desc').text

        container = self.page.ele('.onebox')
        userlink = container.ele('tag:a').link
        userdesc = self.page.eles('.user-desc-box')
        usernote = userdesc[1].text

        return username, userupdate, userid, userlink, usernote

    def extract_additional_info(self, userlink):
        # Additional profile
        self.page2 = ChromiumPage()
        self.page2.get(userlink)

        avatar = self.page2.ele('.avatar-wrapper').ele('tag:img').link
        usertags = self.page2.eles('.tag-item')
        horoscope = usertags[0].text
        location = usertags[1].text
        usersign = self.page2.ele('.user-desc').text

        counts = self.page2.eles('.count')
        follower = counts[0].text
        fans = counts[1].text
        like_collect = counts[2].text

        return avatar, horoscope, location, usersign, follower, fans, like_collect


    def combine_kol_info(self):
        # Combine all information
        username, userupdate, userid, userlink, usernote = self.extract_user_info()
        avatar, horoscope, location, usersign, follower, fans, like_collect = self.extract_additional_info(userlink)
        kol_info = {
            'user name': username,
            'user update': userupdate,
            'user id': userid,
            'user link': userlink,
            'user note': usernote,
            'avatar': avatar,
            'horoscope': horoscope,
            'location': location,
            'user sign': usersign,
            'follower': follower,
            'fans': fans,
            'like_collect': like_collect
        }
        return kol_info

    def get_post_info(self, page):
        # Retrieve each post
        sections = page.eles('.note-item')
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
        wait_random_time()
        page.scroll.to_bottom()

    def craw(self, times):
        all_posts = []
        for _ in tqdm(range(times)):
            post_info = self.get_post_info(self.page2)
            all_posts.extend(post_info)
            self.page_scroll_down(self.page2)

        df = pd.DataFrame(all_posts, columns=['post_link', 'post_title', 'post_like'])
        return df

    def run(self, times):
        self._perform_login()
        self.search()
        kol_combined_info = self.combine_kol_info()
        result_df = self.craw(times)
        return kol_combined_info, result_df


def main():
    scraper = XHSScraper(KEYWORD) #Change the keyword in config.py
    kol_combined_info, result_df = scraper.run(DEFAULT_CRAWL_TIMES) # Default is 5. Be free to change it.
    with pd.ExcelWriter(f'{KEYWORD}_{time.strftime("%Y-%m-%d")}.xlsx') as writer:
        kol_combined_info.to_excel(writer, sheet_name='kol_info', index=False)
        result_df.to_excel(writer, sheet_name='post_info', index=False)
    print("Crawling finished. Data saved.")

if __name__ == "__main__":
    main()

