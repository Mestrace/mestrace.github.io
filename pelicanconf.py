from datetime import datetime

AUTHOR = "Mestrace"
SITENAME = "mestrace.github.io"
SITEURL = "https://mestrace.github.io."
SITETITLE = "Mestrace"
SITESUBTITLE = "Software Developer"
SITEDESCRIPTION = "My Thoughts"
SITELOGO = "https://avatars.githubusercontent.com/u/26028388?v=4"
BROWSER_COLOR = "#333"
PYGMENTS_STYLE = "monokai"


PATH = "content"

TIMEZONE = "Asia/Singapore"

DEFAULT_LANG = "zh"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "themes/Flex"

# # Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)


STATIC_PATHS = ["images", "static"]
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

I18N_TEMPLATES_LANG = "en"
DEFAULT_LANG = "en"
OG_LOCALE = "en_US"
LOCALE = "en_US"

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {"linenos": "table"}

# there is no other HTML content
READERS = {"html": None}

GITHUB_URL = "http://github.com/Mestrace/"
GITHUB_CORNER_URL = GITHUB_URL
MAIN_MENU = True
SOCIAL = (("github", GITHUB_URL),)


ARTICLE_URL = "posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html"

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike 4.0 International License",
    "version": "4.0",
    "slug": "by-sa",
    "icon": True,
    "language": "en_US",
}

COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 10

PLUGINS = [
    "simple_footnotes",
    # "i18n_subsites"
]
# # Enable Jinja2 i18n extension used to parse translations.
# JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
    },
}


THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True

CUSTOM_CSS = "static/custom.css"
EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
}
