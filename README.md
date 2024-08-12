# XHSScraper
XHSScraper is a Python package to scrape KOL information from Xiaohongshu.

# Before start
This project is inspired by [DrissionPage](https://github.com/g1879/DrissionPage) which is a very user-friendly and easy-to-handle tool. The functionality of this package is not yet comprehensive, but will be improved over time.

| Functions | Status | Future Plan |
| --- | --- | --- |
| Get user’s profile | ✔ | Batch retrieve |
| Get user’s posts | ✔ | Continue from where you last stopped |
| Get detailed stats from posts | In Progress |  |
| Get all the replies from posts | In Progress |  |

# **Installation**

The `XHSSraper` script can be installed using two methods:

- **Using pip**

It is the preferred method for installing it. 

1. **Create a virtual environment (Recommended):**
    
    ```
    python3 -m venv venv
    ```
    
    This creates a virtual environment named `venv` to isolate project dependencies from your system-wide Python installation (**recommended**).
    
2. **Activate the virtual environment:**
    
    **Linux/macOS:**
    
    ```
    source venv/bin/activate
    ```
    
    **Windows:**
    
    ```
    venv\Scripts\activate
    ```
    
3. **Install using pip:**
    
    ```
    pip install XHSScraper
    ```
    
    This will download and install the `XHSScraper` package and its dependencies into your Python environment.
    
- **Manual Installation**

For an alternative installation method, clone the source code from the project repository and install it manually.

1. **Clone the repository:**
    
    ```
    git clone https://github.com/Sakae28/XHSScraper
    ```
    
2. **Navigate to the project directory:**
    
    ```
    cd XHSScraper
    ```
    
3. **Create a virtual environment (Recommended):**
    
    ```
    python3 -m venv venv
    ```
    
    This creates a virtual environment named `venv` to isolate project dependencies from your system-wide Python installation (**recommended**).
    
4. **Activate the virtual environment:**
    
    **Linux/macOS:**
    
    ```
    source venv/bin/activate
    ```
    
    **Windows:**
    
    ```
    venv\Scripts\activate
    ```

# Prerequisites

1. Make sure you already have the app “小红书” in your phone because it needs you to scan the QR code for the first time.
2. Edit `config.py`
    
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
    KEYWORD = "麦当劳" 
    ```
    
3. Install required packages
    
    Open CMD/Terminal, key in below command:
    
    `pip install -r requires.txt`
    

# Run the script

Open CMD/Terminal, key in below command:

`python XHSScraper.py`
