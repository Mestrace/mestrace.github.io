Title: 我是如何做SEO优化的 - 持续更新中
Slug: myblog-seo
Date: 2023-03-11
Category: MISC

一开始，我的写博客是出于对自己成长的记录，但时间推移后，我希望更多人能够阅读我的文章。虽然与同事和朋友分享文章可以带来满足感，但如果能吸引更多读者并获得他们的认可和反馈，那将会极大地推动我的进步并让我更加热爱写作。因此，让陌生人发现我的博客已成为我的首要问题。

众所周知，搜索引擎使用网络爬虫遍历整个互联网。然而，随着互联网站点的急剧增加，即使几十年前，现有的搜索引擎也已经无法完成对所有网站的遍历。因此，如何进行搜索引擎优化（Search Engine Optimization，SEO）已逐渐成为备受关注的研究领域。其目的是解决如何使搜索引擎更好地“阅读”我的网站，从而使我的博客文章在用户输入特定关键词时排在前列。在这篇文章中，我将逐步描述我如何对我的博客网站进行SEO，并提供相应的参考资料，希望能够对写博客的朋友提供帮助。

首先，让我简单介绍一下我是如何搭建自己的博客的。如果你使用与我相似的工具链，那么本文将更有助于你。为了减少麻烦的事情，我主要使用GitHub Pages来部署和托管我的博客，这样就省去了很多麻烦。在框架方面，我使用的是[Pelican](https://getpelican.com)，一个Python的静态文档站框架，并使用[Flex主题](https://github.com/alexandrevicenzi/Flex)。Pelican支持Markdown写作，并且可以内嵌HTML。使用这套工具链，我几乎不需要担心部署和配置的问题，只需专注于写作即可。

## 获取访问数据

数据分析是进行优化的重要依据。即使你还没有开始优化，也应该了解如何获取有关你网站访问的数据。在本节中，我将介绍我如何查看访问数据，并提供一些我会用到的工具。

### Google Analytics

使用[Google Analytics](https://analytics.google.com/analytics/web/#/)，可以直观地查看网站的访问数据和高级浏览数据。我使用的Flex框架原生支持Google Analytics 4，只需要配置测量ID，即可在发布网站时自动添加相关的跟踪代码。

首先，需要在Google Analytics后台配置网站跟踪，跟着步骤操作即可，可以参考[官方指南](https://support.google.com/analytics/answer/1008080)。

然后，在你的网站页面中进行配置，才能收集数据，可以跟着这份[官方教程](https://support.google.com/analytics/answer/9539598)拿到你的gtag。如果你使用Flex框架，可以直接在配置文件`pelicanconf.py`中添加以下行：

```Python
# pelicanconf.py
# Google analytics
GOOGLE_GLOBAL_SITE_TAG = 'G-XXXXXXXXXX' # Your Google Analytics 4 Property ID
```
原理也比较简单，就是在需要追踪的每个页面的HTML `<head>`里面加上google的信息。即使你没有跟我用一样的技术栈，你也可以用类似的方式处理，具体可以参考官方文档。这里给出一份模版代码：

```html
<head>
    <!-- Other heads -->

    {% if GOOGLE_GLOBAL_SITE_TAG %}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ GOOGLE_GLOBAL_SITE_TAG }}"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', '{{ GOOGLE_GLOBAL_SITE_TAG }}');
    </script>
    {% endif %}
</head>
```

这样过一阵子就可以看到你的网站放完数据了。

### Google Search Console

> **_NOTE:_** 建议生成好sitemap之后再进行这一步

[Google Search Console](https://search.google.com/search-console/about) 是一个进阶的免费工具，可以用来查看网站在Google搜索结果中的排名和可见性，也包括了能指出网站问题的SEO工具等。

跟着Google Search Console的配置器走，就会要求你[验证你是这个网站的拥有者](https://support.google.com/webmasters/answer/9008080?hl=en)。验证的方式有很多种，这里我选择了最简单的一种，在网址根目录下放置提供的文件`/googleXXXXXXXXXXXX.html`，里面就只有一行
```html
google-site-verification: googleXXXXXXXXXXXX.html
```

在Pelican配置中也比较简单，直接讲这个文件加到配置文件`pelicanconf.py`的`EXTRA_PATH_METADATA`里面就好，比如这样
```Python
EXTRA_PATH_METADATA = {
    "static/google72cb1b82695f07e2.html": {"path": "google72cb1b82695f07e2.html"},
}
```
发布之后就可以继续在Google Search Console里面完成配置。之后过几个小时就可以查看被搜索和点击到的次数了。

当然，Google Search Console只针对Google的搜索，如果你想要配置其他搜索引擎，就需要另外配置了。比如

- [Bing Webmaster](https://www.bing.com/webmasters)
- [百度搜索平台](https://ziyuan.baidu.com/)

## 我的优化策略

### Pelican seo插件

顾名思义，[`pelican-plugin/seo`](https://github.com/pelican-plugins/seo)插件就是用来做Pelican框架下的SEO优化的。这个插件主要有两个功能
- SEO Report: 根据编译后的文章生成一个SEO报告，报告中包含SEO的几个关键点以及如何进行优化。
- SEO Enhancer：在文章编译时添加一些SEO元素，使得文章能够更好地被解析。

安装`pelican-plugin/seo`后，需要在`pelicanconf.py`中增加相应的配置，包括：

```python
PLUGINS = [
    # ...
    "seo",
]
# SEO Settings
SEO_REPORT = False  # SEO report is enabled by default
SEO_ENHANCER = True  # SEO enhancer is disabled by default
SEO_ENHANCER_OPEN_GRAPH = True  # Subfeature of SEO enhancer
SEO_ENHANCER_TWITTER_CARDS = True  # Subfeature of SEO enhancer
```

简单介绍一下这几个选项：

- `SEO_REPORT`：生成上述提到的SEO报告，并以HTML形式输出在项目根目录。
- `SEO_ENHANCER`：添加一些默认的SEO元素，例如生成robots.txt，增加Canonical标签以及增加页面结构标签等。
- `SEO_ENHANCER_OPEN_GRAPH`：开启Open Graph协议，能够在社交媒体上分享你的内容时显示额外的信息。
- `SEO_ENHANCER_TWITTER_CARDS`：开启Twitter卡片，能够在推特上分享你的内容时显示额外的信息。

### Pelican sitemap插件

[`pelican-plugin/sitemap`](https://github.com/pelican-plugins/sitemap)能帮助你在生成Pelican静态网站的同时生成站点地图文件。这个文件可以向搜索引擎提供一些提示，帮助爬虫找到页面的路径并规划何时重新访问你的页面。一旦启用该插件，站点地图文件将在 `output/sitemap.<format>` 路径下生成。
0
当你发布你的站点后，你需要将站点地图提交到搜索引擎后台。下面是一个在 Google Search Console 中添加站点地图的示例：

<p align="center">
  <img src="{static}/images/7/search_console_sitemap.png" />
</p>


## 参考资料

本文主要参考了[Pelican Static sites - SEO Optimization](https://blog.kmonsoor.com/pelican-how-to-make-seo-friendly/)中聊的一些思路。

如果你想变得更强的话，可以延伸看看

1. [SEO - denzildoyle](https://gist.github.com/denzildoyle/31fe294065f606b4f612)
2. [為了 SEO！我離開了 Medium，改在 GitHub 上自架個人網站](https://kucw.github.io/blog/2021/1/from-medium-to-github/)