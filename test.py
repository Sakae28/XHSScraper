
# for test
from XHSScraper.scraper import XHSScraper
from XHSScraper.config import (
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

xhs = XHSScraper()
xhs.get_data(KEYWORD, EXTRA_NOTE_INFO, EXTRA_POST_INFO)





