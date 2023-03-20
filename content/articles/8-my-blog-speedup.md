Title: 我是如何提升博客加载速度的
Slug: myblog-speed-up
Category: MISC
Status: draft

## 数据

1. Developer tools
1. Google PageSpeed Insights

## 优化

1. pelican precompress: serve gzip 
    
    https://webmasters.stackexchange.com/questions/56561/is-gzip-compression-available-for-github-pages

    before
    timeline-before-precompress
    pagespeed-before-preprocess-mobile
    pagespeed-before-preprocess-desktop

    after
    timeline-after-precompress
    pagespeed-after-precompress-mobile
    pagespeed-after-preprocess-desktop

    cons
    编译速度肉眼可见的下降了，2.2s -> 8.9s。注意应该加到publish conf里面，这样本地就不需要忍受编译速度变慢了。
