# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://mestrace.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

# Precompress Plugin
PRECOMPRESS_ZOPFLI = True

# Addthis
ADD_THIS_ID = "ra-64172c2607a4b50c"
ADD_THIS_SHARING_PROMPT = "如果你觉得这篇文章很赞，不要忘记分享给你的小伙伴们！"

# Google analytics
GOOGLE_GLOBAL_SITE_TAG = "G-07WBTMQT81"

# SEO Settings
SEO_REPORT = False  # SEO report is enabled by default
SEO_ENHANCER = True  # SEO enhancer is disabled by default
SEO_ENHANCER_OPEN_GRAPH = True  # Subfeature of SEO enhancer
SEO_ENHANCER_TWITTER_CARDS = False  # Subfeature of SEO enhancer

# Sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.8, "indexes": 0.3, "pages": 0.5},
    "changefreqs": {"articles": "weekly", "indexes": "weekly", "pages": "weekly"},
}