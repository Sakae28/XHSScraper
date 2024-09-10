# XHSScraper

XHSScraper is a Python package to scrape user profile, posts and replies from 小红书.

# Introduction

This project is inspired by [DrissionPage](https://github.com/g1879/DrissionPage) which is a very user-friendly and easy-to-handle tool. The functionality of this package is not yet comprehensive, but will be improved over time.

**THIS IS ONLY FOR LEARNING AND PRACTICING.*

| Functions | Status | Future Plan |
| --- | --- | --- |
| Get user’s profile | ✔ |  |
| Get user’s posts | ✔ | Continue from where you last stopped |
| Get notes related to keyword | ✔ |  |
| Get detailed stats from posts | In Progress |  |
| Get all the replies from posts | In Progress |  |

# Updates

- The `KEYWORD` now is set to a list. You can retrieve multiple users' profiles and posts in batches.
- Add a new function: if the user is not found, the tool will extract notes related to the keyword and store them in the `note_list`.
- Add a switch mode. You can determine whether to turn it on to get extra information of posts or notes.

# File Structure

```
.          
├── XHSScraper
│   ├── scraper.py     # main script
│   ├── config.py      # configuration, you have to change this file!
│   ├── utils.py       # several sub functions
│   └── _init_.py
├── requires.txt       # pip install -r requires.txt
├── test.py            # run the test script
├── LICENSE
├── .gitignore
└── readme.md		
```

# Reminder

The overall crawling time depends on the number of pages to be crawled and whether the additional information mode is enabled. The more pages there are, the longer the crawling time will be; if the additional information mode is enabled, it will also significantly increase the crawling time.

# Installation

- Cloning the Repository
    
    To use this package, you can clone the repository directly from GitHub:
    
    ```bash
    git clone https://github.com/Sakae28/XHSScraper.git
    ```
    
    Then, navigate to the directory and install the required dependencies:
    
    ```bash
    cd XHSScraper
    pip install -r requires.txt
    ```
    
- Manual Installation
    
    If you prefer, you can also manually copy the files to your project directory.
    

# Prerequisites

1. Chrome browser is necessary.
2. Make sure you already have the app “小红书” in your phone because it needs you to scan the QR code for the first time.
3. Edit `config.py`
    
    ```python
    # Configuration for XHSScraper
    
    # URLs
    LOGIN_URL = 'https://www.xiaohongshu.com/explore'
    SEARCH_URL_TEMPLATE = 'https://www.xiaohongshu.com/search_result?keyword='
    
    # Default settings. You could edit it or keep the default value.
    DEFAULT_WAIT_TIME = 20
    DEFAULT_CRAWL_TIMES = 5
    
    # Logging configuration
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'DEBUG'
    
    # User input. MUST CHANGE BEFORE RUNNING
    # Make sure the name is correct and can be searched
    KEYWORD = ["麦当劳", "索尼"]

    # Switch the mode to decide whether to crawl extra info for notes and posts
    # Default is False. Turn it to True to get extra info.
    EXTRA_NOTE_INFO = False
    EXTRA_POST_INFO = False
    ```


# Run the script

Run the `test.py` in your Python compiler.

```python
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
```

# Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you want to contribute code, please fork the repository and submit a pull request.
