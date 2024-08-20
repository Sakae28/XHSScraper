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
    ```


# Run the script

Run the `test.py` in your Python compiler.

```python
from XHSScraper.scraper import XHSScraper
from XHSScraper.config import KEYWORD, DEFAULT_CRAWL_TIMES, DEFAULT_WAIT_TIME, LOG_FORMAT, LOG_LEVEL, LOGIN_URL, SEARCH_URL_TEMPLATE

xhs = XHSScraper()
xhs.get_data(KEYWORD)
```

# Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you want to contribute code, please fork the repository and submit a pull request.
