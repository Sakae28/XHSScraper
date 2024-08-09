# XHSScraper/utils.py

import time
import random
import logging
from urllib.parse import quote

def setup_logging(log_format, log_level):
    logging.basicConfig(format=log_format, level=log_level)
    return logging.getLogger()

def wait_random_time(min_seconds=0.5, max_seconds=1.5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def encode_keyword(keyword):
    return quote(quote(keyword.encode('utf-8')).encode('gb2312'))