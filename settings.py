SEARCH_KEY = "AIzaSyACcXuQ7K7XcSlYiUfEabdejtJ75zKucT4"
SEARCH_ID = "940397e3c4ef24464"
COUNTRY = "ke"
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&gl=" + COUNTRY
RESULT_COUNT = 10

import os
if os.path.exists("private.py"):
    from private import *