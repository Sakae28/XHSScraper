# Configuration for XHSScraper

# URLs
LOGIN_URL = 'https://www.xiaohongshu.com/explore'
SEARCH_URL_TEMPLATE = 'https://www.xiaohongshu.com/search_result?keyword='

# Default settings
DEFAULT_WAIT_TIME = 20
DEFAULT_CRAWL_TIMES = 5

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'

# User input. MUST CHANGE BEFORE RUNNING
# CANNOT BE EMPTY
KEYWORD = ['麦当劳', '索尼'] 

# Switch the mode to decide whether to crawl extra info for notes and posts
# Default is False. Turn it to True to get extra info.
EXTRA_NOTE_INFO = False
EXTRA_POST_INFO = False