Title: 一些有趣的HTTPS和TCP面试题
Slug: interesting-interview-questions-about-tcp-and-http
Category: Computer Science
Date: 2024-04-22 20:00
Summary: 分享一些有趣的TCP和HTTP面试题，并给出一些解答。

今日在闲来无事的时候，刷到了这条推特，其中涉及了一些常见但又容易让人犯迷糊的问题。笔者想着如果自己在面试中遇到相关的问题，可能也不一定能够答上来，因此本篇文章将结合笔者之前做的一些面试准备，来回答一下这些问题。学艺不精，望各位读者斧正。

<blockquote class="twitter-tweet" data-lang="en" data-theme="light"><p lang="zh" dir="ltr">分享一下我遇到的网络面试题：<br>1、Https 如何保证数据的安全<br>2、TCP 建立连接需要3 次握手？为什么不是 2和4 <br>3、UDP 需要握手吗<br>4、TIME_WAIT 的作用<br>5、TCP拆包粘包这种说法对吗<br>6、TCP是可靠传输吗？如果是还需要在业务层保证幂等吗<br>7、QQ 使用的是 TCP 还是 UDP <br>8、Linux…</p>&mdash; Nextify (@nextify2024) <a href="https://twitter.com/nextify2024/status/1782218309213315146?ref_src=twsrc%5Etfw">April 22, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## 1、HTTPS 如何保证数据的安全

HTTPS在原有的明文HTTP协议上附加了一个TLS加密层来保证传输层的信息不被任何中间方窃听。

<figure align="center">
  <img src="https://cf-assets.www.cloudflare.com/slt3lc6tev37/5aYOr5erfyNBq20X5djTco/3c859532c91f25d961b2884bf521c1eb/tls-ssl-handshake.png"/>
  <figcaption>Source: A10 Networks</figcaption>
</figure>

在整个TLS的握手阶段，客户端和服务端通过多次交互来确认以下信息：

1. 双方确认使用的TLS版本，如TLS 1.2, 1.3。
2. 双方选择使用的加密模式，包括对应的对称加密和非对称加密算法
3. 客户端通过服务端提供的公钥和服务器数字证书来确认自己连接的是正确的服务器。
4. 客户端选定会话密钥后，通过非对称加密算法传输给服务端


相较于TLS 1.2，TLS 1.3 主要做了以下改进：

1. 更快的握手过程: TLS 1.3通过减少握手过程中的往返次数，加快了连接建立的速度，从而提高了性能。
1. 更强的加密算法: TLS 1.3移除了一些安全性较弱的加密算法，只支持更安全的加密套件，如ChaCha20-Poly1305和AES-GCM。
1. 减少了协议握手过程中的延迟: TLS 1.3减少了协议握手中的往返次数，从而减少了连接建立的延迟。

<figure align="center">
  <img src="https://www.a10networks.com/wp-content/uploads/differences-between-tls-1.2-and-tls-1.3-full-handshake.png"/>
  <figcaption>Source: Cloudflare</figcaption>
</figure>

参考：

- [Cloudflare - 什么是 TLS（传输层安全性）？](https://www.cloudflare.com/zh-cn/learning/ssl/transport-layer-security-tls/)
- [Cloudflare - What happens in a TLS handshake? | SSL handshake](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/)
- [Cloudflare - Keyless SSL: The Nitty Gritty Technical Details](https://blog.cloudflare.com/keyless-ssl-the-nitty-gritty-technical-details/)
- [A10 Networks - Key differences Between TLS 1.2 and TLS 1.3](https://www.a10networks.com/glossary/key-differences-between-tls-1-2-and-tls-1-3/)

## 2、TCP 建立连接需要3 次握手？为什么不是 2 或 4？

TCP的3次握手本质上是建立一个可靠的全双工通道，此外还同步了双方的滑动窗口大小。

为什么不是2次：客户端SYN，服务端ACK的2次握手只能建立一个客户端到服务端的单工通道。

为什么不是4次：3次握手本质上就是4次，只是将服务端ACK和服务端SYN合并为SYNACK。

参考：

- [Willam Johnson - Medium Post - Why does TCP connection establishment require three-way handshake?](https://medium.com/@relieved_gold_mole_613/why-does-tcp-connection-establishment-require-three-way-handshake-2f9e2c5da1ce)

## 3、UDP 需要握手吗？

从协议层面没有限制，不需要握手。但是应用层可能需要约定好一个传输方式，常见的策略有固定端口，原路返回，或者通过其他交互方式确认好端口之后再进行传输。

参考：

- [Cloudflare - 什么是UDP？](https://www.cloudflare.com/zh-cn/learning/ddos/glossary/user-datagram-protocol-udp/)

## 4、TIME_WAIT 的作用

TIME_WAIT是在TCP关闭连接时，在完成四次挥手之后，主动关闭连接的一方应等待TIME_WAIT = 2MSL的时间之后，才重复使用同一个端口进行连接。

1. 保证最后的ACK能到达被动关闭连接方，确保全双工连接正常关闭。否则的话，对方可能会因为收不到ACK包，而请求重传，导致进行一些非法的状态，如RST之类的。
2. 在下一次连接重复使用同一套端口进行连接时，确保不会有丢失在网络里的包重新到达这一套新的连接中。

参考：

- [昀溪 - 解读TIME_WAIT--你在网上看到的大多数帖子可能都是错误的](https://www.cnblogs.com/rexcheny/p/11143128.html)

## 5、TCP拆包粘包这种说法对吗

对也不对。本质上对于定义的问题。代码使用方认为在应用层发送数据包时数据包是有边界的，因此在接收方时也应该读到边界。但是实际上TCP是基于字节流的，因此所有通过TCP传输的数据都被视作一个字节流。TCP只保证传输的内容的顺序性，但是应用是否应该将接收到的信息视作是同一个或者不同的包，TCP是管不着的。举个例子，当接收方使用某种带Buffer的机制读取时，就会读到连续的内容，而没有边界，从而可能导致解析发生错误。或者说换种说法，应用层需要自己定义协议内容，确保解析是正确的。

让我们来看看HTTP是怎么处理的。HTTP约定使用`\r\n`来区分Header和Body，此外在Header中附加的`Content-Length`确定了客户端应读取的内容长度。以下是一段示例代码。

```python
import socket

def send_http_request(host, port, path):
    # 创建 socket 对象
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    sock.connect((host, port))

    # 发送 HTTP 请求
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    sock.sendall(request.encode('utf-8'))

    # 接收 HTTP 响应
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    # 解析 HTTP 响应
    status_line, headers, body = response.split(b'\r\n\r\n')

    # 获取 Content-Length
    content_length = None
    for header in headers.split(b'\r\n'):
        if header.startswith(b'Content-Length:'):
            content_length = int(header.split(b':')[1].strip())
            break

    # 打印 HTTP 响应状态码
    print(status_line.decode('utf-8'))

    # 打印 HTTP 响应头
    for header in headers.split(b'\r\n'):
        if header:
            print(header.decode('utf-8'))

    # 读取 HTTP 响应正文
    if content_length is not None:
        body = body[:content_length]
        print(body.decode('utf-8'))
    else:
        print('Content-Length header not found')


# 使用示例
send_http_request('www.example.com', 80, '/')
```

参考：

- [github/source-code-hunter - TCP 粘包/拆包](https://github.com/doocs/source-code-hunter/blob/main/docs/Netty/TCP粘拆包/TCP粘拆包问题及Netty中的解决方案.md)

## 6、TCP是可靠传输吗？如果是还需要在业务层保证幂等吗


TCP只保证数据链路层的可靠性，至于传输的内容是怎么处理的，TCP无法保证。比如对于一个数据库进行写入，而发生了某种硬件上的失败导致写入失败，这种情况TCP就无法处理。

更多的情况是，我们要保证业务上的操作是幂等的。一个写入操作可能会跨越多个机房，数据库和网络链路，远远不是TCP能够解决的，而这需要研发工程师不断的努力去优化可靠性。TCP只是为了能准确送达业务消息而生的，具体的幂等，及对应的补偿机制还是需要开发人员自己实现。但是TCP能做的事情是帮开发人员屏蔽掉更底层，如IP端口的一些实现细节。

参考：

- [小林coding - 用了 TCP 协议，数据一定不会丢吗？](https://www.xiaolincoding.com/network/3_tcp/tcp_drop.html#用了tcp协议就一定不会丢包吗) 这篇文章介绍了更多关于TCP可能丢包的场景
- [融极 - CSDN - 幂等性详解与示例](https://blog.csdn.net/tianzhonghaoqing/article/details/121180153)


## 7、QQ 使用的是 TCP 还是 UDP 

只针对消息场景来说，UDP较为合适。

对比起来有哪些优势？
- TCP由于其的一些本身特性过于通用（如阻塞控制，保证有序，及TIME_WAIT等），基于消息的场景下对于带宽的利用率不够，因此在早期通常都基于UDP开发一套更简便的可靠传输协议来处理QQ这种场景。
- TCP由于需要使用很多连接符（Socket），在操作系统层面没有优化的情况下，每台服务器可以支持的连接数受到一定的限制。但是后来有了epoll之后也可以实现。

但是，最重要的是，我们要根据不同的场景使用不同的技术框架和选型。此外，对于一个大的项目来说，不同的模块会需要应用不同的技术。

1. UDP：PC客户端的心跳和上线检测，消息内容下载 & 推送，内网P2P文件传输
2. TCP：Android & IOS 的 图，文，小视频发送
3. HTTP/S：基于Web技术的一些内容。

参考：

- [博客园/Jessica程序猿 - 高并发网络编程之epoll详解](https://www.cnblogs.com/wuchanming/p/4349743.html)
- [知乎/QQ 为什么以 UDP 协议为主，以 TCP 协议为辅？](https://www.zhihu.com/question/20292749)有一些野史，看看就好。
- [github/chungchi300/reading-book - 1.4亿在线背后的故事-——-腾讯-QQ-IM后台架构的演化与启示.ppt](https://github.com/chungchi300/reading-book/blob/master/architecture/1.4亿在线背后的故事-——-腾讯-QQ-IM后台架构的演化与启示.ppt)
- [博客园/xiaoyongyoong - 聊天系统设计 how to design a chat system](https://www.cnblogs.com/cynrjy/p/15336100.html)

## 8、Linux 已经提供了Keep-Alive，为什么还需要应用层做心跳检测



> The UNIX, Linux and Windows operating systems use a 'keepalive' setting to test idle TCP connections and ensure they are still active. By default, 'keepalive' is set to 7200000ms (2 hours). This means that every 2 hours the server machine tests the idle TCP connection by pinging the client machine from where the connection is coming. If the server gets no response back from the client, then 'keepalive' terminates the idle connection. The 'keepalive' interval can be modified by configuring the operating system to reduce the time from 2 hours to 5 minutes.
> Source: Esri

Keep-Alive机制可以设置为5分钟到2小时，主要是服务端用来关闭一些无用的连接的，如客户端不主动关闭连接但是已经不响应了。
此外，可能会有各种原因让Keep-Alive数据包失效，比如Socks Proxy。

参考：

- [Esri - Change the operating system's 'keepalive' settings](https://support.esri.com/en-us/knowledge-base/change-the-operating-system-s-keepalive-settings-146247-000006285)
- [横云断岭/hengyunabc - 为什么基于TCP的应用需要心跳包（TCP keep-alive原理分析）](https://hengyun.tech/why-we-need-heartbeat/)

