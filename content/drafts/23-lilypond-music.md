Title: Lilypond 做乐谱
Slug: lilypond-music
Category: Photography
Date: 2025-02-27
Status: draft
Summary: 

因为在Homebrew部署了镜像，所以安装Lilypond相当无脑: `brew install lilypond`


先使用教程中的代码运行一下，保存以下代码到文件
```
\version "2.24.4"
{
  c' e' g' e'
}
```
运行`lilypond --svg <lilypond-example-compile-a-file>.ly`后输出的图片为
<figure align="center">
  <img src="{static}/images/23/lilypond-example-compile-a-file.svg" />
</figure>