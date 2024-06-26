from datetime import datetime
import os
import pathlib

AUTHOR = "Mestrace"
SITENAME = "Mestrace的个人博客"
SITEURL = "http://127.0.0.1:8000"
SITETITLE = "Mestrace"
SITESUBTITLE = "Software Developer"
SITEDESCRIPTION = "我的个人博客，记录我的成长历程"
SITELOGO = "http://github.com/Mestrace.png?size=460"
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

CUSTOM_CSS = "static/custom.css"
EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
    "static/google72cb1b82695f07e2.html": {"path": "google72cb1b82695f07e2.html"},
    "static/808470c28b824e33920b126802a692f6.txt": {
        "path": "808470c28b824e33920b126802a692f6.txt"
    },
    "static/yandex_be29935b91989956.html": {"path": "yandex_be29935b91989956.html"},
}

favico_path = "content/static/favico"
for file in os.listdir(os.fsencode(favico_path)):
    filename = os.fsdecode(file)
    path = pathlib.PurePath().joinpath("static", "favico", filename)
    EXTRA_PATH_METADATA[path.as_posix()] = {"path": filename}

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
    "seo",
    "sitemap",
    "pelican.plugins.precompress",
    "render_math",
    "md_include",
    "photos",
]

# # Enable Jinja2 i18n extension used to parse translations.
# JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
    },
    "output_format": "html5",
}


THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True

# Remove URL Hash
DISABLE_URL_HASH = True

# Math Jax
MATH_JAX = {"tex_extensions": ["color.js", "mhchem.js"]}

# Sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.8, "indexes": 0.3, "pages": 0.5},
    "changefreqs": {"articles": "weekly", "indexes": "weekly", "pages": "weekly"},
}

# Pelican Photos
PHOTO_LIBRARY = "content/images"
PHOTO_RESIZE_JOBS = 3
PHOTO_EXIF_REMOVE_GPS = True
