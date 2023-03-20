Title: 手把手教你在树莓派4B上运行LLaMA 7B模型
Slug: llama-rpi
Date: 2023-03-15
Category: MISC
Summary: 本文详细描述了我是如何一步步在树莓派4B上运行LLaMA模型。LLaMA是由Meta AI发布的一个大语言模型。ggerganov/llama.cpp是一个由C++实现的LLaMA移植版本，并使用4-bit量化技术以将模型适配至个人设备上。超大型语料模型从未如此唾手可得。在树莓派上获得你的个人chatgpt。如果你对树莓派、LLaMA模型或大型语言模型感兴趣，那么本文一定会对你有帮助。How I run the LLaMA model step by step on a Raspberry Pi 4B. LLaMA is a large language model released by Meta AI. ggerganov/llama.cpp is a C++ implementation of the LLaMA port, which uses 4-bit quantization techniques to adapt the model to personal devices. A large-scale Machine Learning model has never been so readily available for normal people. If you are interested in Raspberry Pi, LLaMA model, or large-scale language models, this article will provide you with useful information.

## 引言

LLaMA全称是Large Language Model Meta AI，是由Meta AI研究人员发布的一个预训练语言模型。与最近爆火的ChatGPT相比，LLaMA架构更小，但训练过程和单GPU推理速度更快，成本更低。今天在刷推特的时候无意中看到了这样一条消息，[@ggerganov](https://github.com/ggerganov)在GitHub上发布了[llama.cpp](https://github.com/ggerganov/llama.cpp)，使用了4-bit量化将模型尽可能缩小，并能在多种移动设备上运行。这我就不淡定了，正好手里有个闲置的Raspberry Pi 4B 4GB版本，赶紧搞起。

<blockquote class="twitter-tweet" data-conversation="none"><p lang="en" dir="ltr">Added a new section to my post highlighting the advances we&#39;ve already seen in the last two days: LLaMA runs on a 4GB RaspberryPi and a Pixel 6 phone now! <a href="https://t.co/pWOv6PP85b">https://t.co/pWOv6PP85b</a></p>&mdash; Simon Willison (@simonw) <a href="https://twitter.com/simonw/status/1635314097318395904?ref_src=twsrc%5Etfw">March 13, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


## 配置树莓派

> 如果你已经配置好了树莓派，且gcc版本为10以上的就可以跳过这一部分了

以下是我配置树莓派的步骤

首先通过[Raspberry Pi Imager]()刷入系统至SD卡
- 系统版本为Ubuntu Server 22.10 (64 bit)
- 注意这里一定要使用64 bit的系统，不然后续可能无法编译

配置系统

直接用命令行升级软件包并安装相关依赖，这里给出参考命令
```bash
sudo su
apt-get update
apt-get upgrade

# 一些会用到的工具
apt-get install gcc g++ python3 python3-pip

# 安装python依赖
python3 -m pip install torch numpy sentencepiece
```

## `llama.cpp`

首先可以先下载LLaMa模型，7B的模型大概是28GB左右，网速不好的同学可以提前开始下载，以免到时候还需要苦等。可以在网上搜索到泄漏的下载磁力链接，用你喜欢的任意P2P / Torrent软件下载即可。

接下来就可以进入[`llama.cpp`](https://github.com/ggerganov/llama.cpp)按照里面的教程进行操作了。虽然看似比较简单，但里面还是有一些小坑的地方的。我在这里简单阐述下我遇到的问题以及我是怎么解决的。

### 构建二进制

```bash
# build this repo
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```

首先需要克隆仓库到本地，并进行make。我在这一步发现两个问题

1. Rasbian Buster自带的gcc版本较老（gcc 8）且无法升级，因此才需要在前面重装系统并安装最新版本的。目前我使用的是gcc 12。
1. `make`的时候提示不支持的选项。

    `makefile`里面处理一些平台特定的flag的时候是读取系统平台并储存到`UNAME_S`,`UNAME_P`和`UNAME_M`里面，之后通过这三个参数判断编译器相关的选项。如果这里通过不了的话可以考虑看看`makefile`里相近平台的参数并指定。`make UNAME_P=armv7 UNAME_M=armv7`就可以指定为`armv7`的编译选项。

    
1. `make`的时候提示內联错误`‘always_inline’ ‘vdotq_s32’`

    这个问题比较坑爹。我一开始以为是编译器的问题，换了好几种选项都不行。后来发现是作者在03.14针对Apple Sillicon做的一个优化 [Use vdotq_s32 to improve performance #67 - Merged](https://github.com/ggerganov/llama.cpp/pull/67)。目前暂不清楚为什么树莓派无法处理这个，已经向作者反馈了。既然无法针对性的做处理，我尝试了直接revert对应的commit。之后就没有编译错误可以继续了。在我报出这个问题之后两小时，另一位贡献者[@Ronsor](https://github.com/Ronsor)已经提出了一个PR去修复这个问题了 [Don't use vdotq_s32 if it's not available #139](https://github.com/ggerganov/llama.cpp/pull/139)，点赞。

### 预处理模型

```bash
# obtain the original LLaMA model weights and place them in ./models
ls ./models
65B 30B 13B 7B tokenizer_checklist.chk tokenizer.model

# install Python dependencies
python3 -m pip install torch numpy sentencepiece

# convert the 7B model to ggml FP16 format
python3 convert-pth-to-ggml.py models/7B/ 1

# quantize the model to 4-bits
./quantize.sh 7B
```

我们将前面下载下来的模型放到`llama.cpp/models`文件夹，主要包含`7B`模型文件夹和`tokenizer.model`分词器模型。然后使用`convert-pth-to-ggml.py`进行预处理转换成FP16精度，最后使用`./quantize.sh`脚本进行4 bit量化以进一步缩小。

这一步主要遇到的这么两个问题

1. 使用`scp`从Mac上传文件到pi上，稍微配置了一会儿，主要是等待时间较长。
1. 在`pi`上运行`convert-pth-to-ggml.py`这一步的时候，消耗内存太大OOM进程直接被系统kill掉了。

简单看了下`convert-pth-to-ggml.py`，似乎都是做一些浮点精度的转换，最后生成的也是通用的模型格式`ggml`。于是我决定尝试先用Mac做`ggml`转换，然后拷贝到Pi上作进一步的处理`ggml-model-f16.bin`。实操发现这样是可行的，Pi也可以成功的运行`quantize.sh`量化脚本。


## 使用`llama.cpp`

到这里我们的安装就已经结束了，紧张又兴奋的使用时间开始了。先来跑一个简单的Hello World。

```bash
./main -m ./models/7B/ggml-model-q4_0.bin -p "Hello world!" -t 8 -n 512
```

```text
main: seed = 167882008main: seed = 167882008main: seed = 1678820083
llama_model_load: loading model from './models/7B/ggml-model-q4_0.bin' - please wait ...
llama_model_load: n_vocab = 32000
llama_model_load: n_ctx   = 512
llama_model_load: n_embd  = 4096
llama_model_load: n_mult  = 256
llama_model_load: n_head  = 32
llama_model_load: n_layer = 32
llama_model_load: n_rot   = 128
llama_model_load: f16     = 2
llama_model_load: n_ff    = 11008
llama_model_load: n_parts = 1
llama_model_load: ggml ctx size = 4529.34 MB
llama_model_load: memory_size =   512.00 MB, n_mem = 16384
llama_model_load: loading model part 1/1 from './models/7B/ggml-model-q4_0.bin'
llama_model_load: .................................... done
llama_model_load: model size =  4017.27 MB / num tensors = 291

system_info: n_threads = 4 / 4 | AVX = 0 | AVX2 = 0 | AVX512 = 0 | FMA = 0 | NEON = 1 | ARM_FMA = 1 | F16C = 0 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 0 | SSE3 = 0 | VSX = 0 | 

main: prompt: 'Hello world'
main: number of tokens in prompt = 3
     1 -> ''
 10994 -> 'Hello'
  3186 -> ' world'

sampling parameters: temp = 0.800000, top_k = 40, top_p = 0.950000, repeat_last_n = 64, repeat_penalty = 1.300000


Hello world! | Welcome to the new site.
We've been working hard on a few updates around here and it feels really great to finally share this

main: mem per token = 14368644 bytes
main:     load time = 113492.53 ms
main:   sample time =   987.31 ms
main:  predict time = 3881120.50 ms / 121285.02 ms per token
main:    total time = 4215260.00 ms
```

我们可以看到，生成了这句30词的回复，Pi用了1小时10分钟，生成速度约为`121 s/Token`。有可能是我编译出了问题，这个后续再修复一下吧。当然由于时间太慢了，我后面的几个用例都直接在Mac上运行了。

再跑一个官方例子
```bash
./main -m ./models/7B/ggml-model-q4_0.bin -p "Building a website can be done in 10 simple steps:" -t 8 -n 512
```

```
Building a website can be done in 10 simple steps:
Start with the end goal. Think about what your audience wants to achieve before they ever visit you site – and once there, how do these users interact on it? This is an important step as it will help formulate all of those great ideas into something that makes sense for their target marketplace!
2) Get Inspired & Develop a Mood Board: It's always good to have some kinda inspiration board. If you’re thinking about starting from scratch, use Pinterest or other sources (like Behance and Dribbble), as they will give your ideas a direction when it comes time for the visual design phase!
3) Strategize Your Content: Here's where things start to get tricky. You need some kinda content strategy in place here – do you have all of that information ready at hand? Now is also a good time as any to think about wireframes and how users will interact with your site once its built!
4) Do It With A Purpose: Are there particular goals for the user’s journey on this website, or simply trying to build an online presence? If so you may want to consider using marketing automation software like Hubspot that allows marketers and salespeople to work together better. This will help them organize your content into a more logical hierarchy – which is one of those things we love doing!
5) Visual Design: It's time for the fun part, where you think about colors (orange!) layout & typography, etcetera - and then start to design it using Illustrator or Photoshop. At this point in your project its important that all parties involved have a clear understanding of what needs to be done!
6) User Interface Design: This is when the UI designer comes into play – they should know how things interact with one another, understand user goals and create an experience so seamless it feels like second nature. The better this step goes down, you will end up having a much more engaging website at hand!
7) Coding Starts: After all of that planning is done here’s where the coding process begins – usually with HTML & CSS first and then followed by Javascript to make sure your site works flawlessly across multiple browsers.
8 ) Test, Test Again And Then Test Some More…: This phase can go on for a while (we know this from experience

main: mem per token = 14434244 bytes
main:     load time =  4570.61 ms
main:   sample time =   448.29 ms
main:  predict time = 138987.47 ms / 271.99 ms per token
main:    total time = 146495.30 ms
```

在Mac上运行的速度还是非常快的（废话），生成512个词的回复用了2分26秒，平均`0.27 s/Token`。

此外，仓库里还包含了一个对于android设备的编译选项和实际运行的视频，有兴趣的读者可以自己研究下。也有人尝试在三星Galaxy S22 Ultra上运行这个模型，速度竟然可以达到`1.2s/Token`。


## 小结

目前整个项目还是处于一个比较初级的形态，在RPi上生成速度相当慢，几乎不可用。此外，作者也在README中提到了一些限制

1. 目前很难判断量化是否影响了模型生成的质量，需要一些更严谨的基准测试。
1. 目前模型并没有使用MacOS提供的Accelerate框架，因为对于整个解码器中大部分张量形状来说，使用ARM_NEON的内部实现和使用Accelerate框架并没有什么性能差别。

除开性能之外，项目的指引还需要更加完善一些才能够更好的帮到大家。


但无论如何，在训练和运行语言模型逐渐要求海量算力的今天，能有这样一个模型让个人设备也能跑起来一个甚至还挺好用的模型，还是挺让人感动的。不知道是巧合还是什么，第一个跑通的老兄在[Raspberry Pi 4 4GB #58](https://github.com/ggerganov/llama.cpp/issues/58)里面展示的例句是：“The first man on the moon was Neil Armstrong..." 总要有人尝试，去发现，去做第一个登上月球的人，不是吗？

## 参考文献

如果你想进一步了解相关内容的话，可以阅读下面的文章

- [ChatGPT论文阅读系列-LLaMA: Open and Efficient Foundation Language Models - 知乎](https://zhuanlan.zhihu.com/p/612002642)
- [LLaMA快速上手指南: 便捷构建“本地版ChatGPT” - 知乎](https://zhuanlan.zhihu.com/p/613111988)
