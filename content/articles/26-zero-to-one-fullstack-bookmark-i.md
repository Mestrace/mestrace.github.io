Title: 从无到有做全栈，实现一个书签应用（一）
Slug: zero-to-one-fullstack-bookmark-i
Category: Computer Science
Tags: Fullstack
Date: 2025-05-09
Summary: 本文将带你从零开始，一步步构建一个全栈书签应用。无论你是经验丰富的后端开发者，还是对 javascript 生态系统知之甚少的小白，都能从这个教程中获益。我们将学习 javascript 语言，使用 Express.js 和 React 等常见框架搭建前后端，并通过 MongoDB 实现数据存储。最终目标是部署一个简单易用的在线书签管理器。这篇教程将侧重于实践操作，帮助你快速掌握全栈开发的核心概念和流程。


我过去的开发经验都聚焦于后端开发，也使用过很多后端框架，如Gin (Golang) 和 Django (Python)。但是由于工作需求限制，我几乎从来没有接触过javascript。但是从网上的经验，我也大概了解过整个基于javascript生态的全栈开发，非常适合独立开发者和小团队进行开发。现在有了更多的空闲时间去探索，我决定学习这个新的体系。但是我在网上搜索的时候，很难找到一个真正适合我这种既是专业人士，有同时是小白的人士。因此我觉得自己动手写一个。当然，说是自己动手写也不准确。我期望能够利用现在的LLM技术，更快的帮我掌握这个领域的基本知识。本文所涉及的代码约80%是由AI写出来的，并经由我进行调试和反馈。

我最初关于这个项目的想法是从非常简单的主意开始。这个系统不应该涉及任何支付，认证，安全和其他需要花费大量时间进行开发和调试的复杂问题。因此，我设定了以下学习目标：

1. 学习javascript语言，使用一些常见框架开发一个前后端的完整项目。
1. 部署到互联网上的任意平台，能够进行在线使用。
1. 尽量运用最佳实践。

带着这些想法，我进行了一些头脑风暴。最终，我设定了这个想法：开发一个**书签管理器**。

概念：一个可以保存，分类和分享网页链接的地方。
核心功能：书签的CRUD，列表和筛选。
学习要点：一些基础的Javascript前后端功能，连接数据库。

在开始这个项目之前，我假设你：

* 熟悉 git 操作。
* 熟悉 HTTP 及其最佳实践。
* 能够 ( 非常概括地 ) 理解 javascript ( 或 typescript ) 。
* 能够熟练使用 docker 命令。
* 能够熟练使用终端。
* 当出现意想不到的情况时，能够阅读并进行搜索来调查问题。

即使你不满足其中某些要求，也可以继续阅读。当遇到不熟悉的内容时，你可以进一步研究。我们将采用自下而上的方法来实现和运行。但你也可以选择自上而下的方法：只需完成数据库配置，然后跳到后面的章节，先体验一下这个项目，然后再回头阅读任何代码。无论哪种方式，都由你选择。话不多说，我们开始吧。

# 从无到有启动Bookmark项目

我一直想尝试这种 monorepo 的概念，即前后端都用类似的语言，并在同一个目录下进行开发。

```bash
mkdir bookmark-app
cd bookmark-app
# then 
mkdir server
mkdir client
```

接着进入 `server` 文件夹并设置项目结构。这个项目的选型主要会使用 `express.js` ，数据层使用 `Mongoose` ，然后使用 `dotenv` 来为这个项目设置不同的配置。


```bash
cd server

# 初始化Node项目
npm init -y

# 安装核心依赖
npm install express mongoose dotenv

# 安装开发依赖
npm install --save-dev nodemon

# 创建基本的服务器文件
touch server.js

# 创建一个简单的.gitignore文件
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
```

打开 `package.json` 并编辑 `scripts` 部分，加入以下内容。这部分内容的意思是是使用`nodemon`来启动服务。`nodemon`能帮助我们边开发边重启服务。

```json
"scripts": {
   "test": "echo \"Error: no test specified\" && exit 1",
   "dev": "nodemon server.js"
},
```

接下来我们来创建一个React项目。这里我们使用了Vite提供的React模版，并安装安装了`axios`用于给后端发送API请求。

```bash
# 使用 Vite 在 client 文件夹内创建一个新的 React 项目
# 被提示安装 'create-vite'，输入 'y'。
# 选择 'React' 和  'TypeScript' 。
npm create vite@latest client --template react

cd client

# 安装项目依赖
npm install

# 安装 axios
npm install axios
```

完成这些之后，项目结构应该像下面这样 [ref] 你可以使用 `tree bookmark-app --gitignore` 来可视化这个结构。在 MacOS 上安装可以使用这个命令 `brew install tree` [/ref] 。

```
bookmark-app
├── client
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── assets
│   │   │   └── react.svg
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── server
    ├── package-lock.json
    ├── package.json
    └── server.js
```

## 简单启用一下服务端

如果我们将以下代码放入 server/server.js 文件中，我们就拥有了一个可运行的 API 端点。现在我们可以在 server 文件夹中运行 npm run dev 来启动后端服务器。因为我们是用了`nodemon`，当代码发生改变的时候，它还具备自动重新加载的功能。我们在浏览器中直接访问`localhost:3000` 应该能够访问该页面并看到 `Bookmark API is running! `。


```javascript
// Example server.js start
require('dotenv').config(); // Load environment variables from .env file
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Bookmark API is running!');
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

# 设置数据库

在这个项目中，我选择了 mongodb 来作为数据库，因为它文档模型提供了极佳的易用性。获取 mongodb 的方式有很多种。如果你已经安装了 mongodb，可以跳过这部分。我选择通过 docker 来安装，也同样是因为它简单易用。我同时安装了Docker Desktop来进行可视化操作。

<figure align="center">
  <img src="{static}/images/26/docker-mongo.png" />
</figure>

```bash
# 拉取镜像
docker pull mongodb/mongodb-community-server:latest

# 启动mongodb
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest


# 安装 mongosh
brew install mongosh

# 通过 mongosh 连接到数据库
mongosh --port 27017
```

如果一切顺利，我们现在已经连接到 mongodb shell 。我们简单测试一下，应该会得到类似下面的输出。


```
test> db.runCommand(
...    {
...       hello: 1
...    }
... )
{
  isWritablePrimary: true,
  topologyVersion: {
    processId: ObjectId('6812ad7c13fca01873314556'),
    counter: Long('0')
  },
  maxBsonObjectSize: 16777216,
  maxMessageSizeBytes: 48000000,
  maxWriteBatchSize: 100000,
  localTime: ISODate('2025-04-30T23:09:40.733Z'),
  logicalSessionTimeoutMinutes: 30,
  connectionId: 4,
  minWireVersion: 0,
  maxWireVersion: 25,
  readOnly: false,
  ok: 1
}
```

# 实现服务端逻辑

回到 `server` 文件夹，创建一个 `.env` 文件并添加以下行：

```bash
DATABASE_URL = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.0"
```

在 server.js 文件中，添加以下代码：

```javascript
// Connect to MongoDB
const mongoose = require('mongoose');
mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB Connected'))
    .catch(err => console.error('MongoDB Connection Error:', err));
```

让我们创建一个代表书签的模型。 Mongoose 提供了一种与数据交互的抽象方式。在 models/bookmark.js 文件中，我们定义书签表的结构 ( schema ) 。

```javascript
const mongoose = require('mongoose');

const isValidUrl = (url) => {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
};

const bookmarkSchema = new mongoose.Schema({
    url: {
        type: String,
        required: true,
        validate: {
            validator: isValidUrl,
            message: 'Invalid URL format'
        }
    },
    title: {
        type: String,
        required: true,
        maxlength: 200
    },
    description: {
        type: String,
        maxlength: 1000
    },
    tags: {
        type: [String],
        default: [],
        validate: {
            validator: (tags) => tags.length <= 10,
            message: 'Maximum 10 tags allowed'
        }
    },
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Bookmark', bookmarkSchema);
```
该模型包含一个 URL 、一个标题、一些字符串描述以及一个字符串列表形式的标签。并且增加了一些校验和限制的逻辑。

在 routes/bookmark.js 中创建一个新文件，让我们添加第一个用于查询书签的 api 端点。

```javascript
const express = require('express');
const router = express.Router(); 
const Bookmark = require('../models/Bookmark');

router.get('/', async (req, res) => {
    try {
        const bookmarks = await Bookmark.find().sort({ createdAt: -1 });
        res.json(bookmarks);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});
```

这个方法使用了书签的 schema ，查询了所有的书签并按创建时间排序。然后，我们可以添加一个创建书签的方法。这里我们只添加了基本的验证，并暴露了所有的路由函数。

```javascript
router.post('/', async (req, res) => {
    const { url, title, description, tags } = req.body;

    if (!url || !title) {
        return res.status(400).json({ msg: 'Please include a URL and Title' });
    }

    try {
        const newBookmark = new Bookmark({
            url,
            title,
            description,
            tags
        });

        const bookmark = await newBookmark.save();
        res.status(201).json(bookmark);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});
```

我们还需要让服务器在特定的端点使用这些 api 定义。在 `server.js` 中，在 `/api/v1/bookmarks` 路径添加路由。

```javascript
app.use('/api/v1/bookmarks', require('./routes/bookmark'));
```

这样，我们就可以使用 npm run dev 来启动服务器了。我使用了 Postman 来测试这些 api 端点。我附上了 `cURL` 请求以供参考，可以直接在终端中使用它们，或者作为请求导入到 Postman 中。


这个请求创建一个新的书签。

```bash
curl --location '127.0.0.1:3000/api/v1/bookmark' \
--header 'Content-Type: application/json' \
--data '{
    "url": "http://google.com",
    "title": "Google",
    "description": "Put google as a bookmark",
    "tags": [
        "abc",
        "def",
        "ghi"
    ]
}'
```

响应会是这样的：

```json
{
    "url": "http://google.com",
    "title": "Google",
    "description": "Put google as a bookmark",
    "tags": [
        "abc",
        "def",
        "ghi"
    ],
    "_id": "68153dfd10539ed8509c8576",
    "createdAt": "2025-05-02T21:49:49.817Z",
    "__v": 0
}
```

以下请求应该会查询数据库中所有现存的书签，并按创建时间排序。

```bash
curl --location '127.0.0.1:3000/api/v1/bookmark'
```

响应会是这样的：

```json
[
    {
        "_id": "68153dfd10539ed8509c8576",
        "url": "http://google.com",
        "title": "Google",
        "description": "Put google as a bookmark",
        "tags": [
            "abc",
            "def",
            "ghi"
        ],
        "createdAt": "2025-05-02T21:49:49.817Z",
        "__v": 0
    }
]
```

让我们在 mongodb shell 中检查一下。在命令行中使用 `mongosh -port 27017` 启动mongodb shell，并使用下面命令。

```javascript
test> db.getCollectionNames()
[ 'bookmarks' ]
test> db.bookmarks.find({})
[
  {
    _id: ObjectId('68153dfd10539ed8509c8576'),
    url: 'http://google.com',
    title: 'Google',
    description: 'Put google as a bookmark',
    tags: [ 'abc', 'def', 'ghi' ],
    createdAt: ISODate('2025-05-02T21:49:49.817Z'),
    __v: 0
  }
]
```

到目前为止，我们已经实现了创建和查询书签列表的基本逻辑。我还是用同样的方式，创建了修改和删除的逻辑，但在这里我们就不一一赘述了。你可以进入本项目的代码目录进行更细致的研究。


# Implement client logic

对于客户端逻辑，我们将主要使用基本的 React 来实现。由于客户端代码相当复杂，我不会从仓库中复制粘贴到本文的正文内容中。但我会给你一个高层次的概述。首先，客户端的文件树结构如下所示。

```
client
├── README.md
├── eslint.config.js
├── index.html
├── package-lock.json
├── package.json
├── public
│   └── vite.svg
├── src
│   ├── App.css
│   ├── App.tsx
│   ├── assets
│   │   └── react.svg
│   ├── components
│   │   ├── AddBookmarkModal.module.css
│   │   ├── AddBookmarkModal.tsx
│   │   ├── BookmarkItem.module.css
│   │   ├── BookmarkItem.tsx
│   │   ├── BookmarkList.module.css
│   │   ├── BookmarkList.tsx
│   │   ├── Toast.module.css
│   │   ├── Toast.tsx
│   │   └── ToastContainer.tsx
│   ├── config
│   ├── main.tsx
│   ├── types
│   │   └── bookmark.ts
│   └── vite-env.d.ts
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

每个文件都有其独特的功能，我会尽力解释它们的作用。我会跳过 vite 生成的样板代码，因为它们不是我们主要关注的内容。它们只是为了简化开发过程而存在的。

* `main.tsx` 是应用程序的主要入口点。它很简单。目前，它只包含对 `App.tsx` 的引用。除此之外，通常它只用于导入一些通用的东西，例如导入和应用全局样式、设置全局上下文提供者，或者为整个应用程序初始化国际化。
* `App.tsx` 是书签应用程序样式的主要入口点。它定义了应用程序的结构。 `App.tsx` 中的所有内容都应该引用 `components` 文件夹中的各个组件。
* `components` 文件夹包含了为应用程序定义的所有基本模块。对于每个组件，我们定义了主要的模块文件 `*.tsx `和相关的样式表文件 `*.module.css`( 如果有的话 ) 。
  * `AddBookmarkModal.tsx` 是一个处理用户创建新书签输入的组件。它呈现一个表单，并调用相关的后端 api 来处理表单上传。此外，它的抽象程度较高，可以同时处理编辑和添加新书签的逻辑。
  * `BookmarkItem.tsx` 是用于显示每个单独书签卡片的主要组件。它还包括用于正确显示链接和图标的验证逻辑。
  * `BookmarkList.tsx` 是查询和显示所有书签项的核心逻辑，以及调用 `AddBookmarkModal` 的逻辑。
  * `Toast.tsx` 用于在右上角显示单个的提示信息。
  * `ToastContainer.tsx` 用于控制所有正在显示和已关闭的提示信息。


什么是 Modal ( 模态框 ) ？

可以把 Modal ( 模态框 ) 看作是显示在用户屏幕上的一个临时的、集中的覆盖层。它主要用于中断用户当前的工作流程，并引导用户进行特定操作。在我们的例子中，当用户点击添加或编辑按钮后，我们的 `AddBookmarkModal` 会在屏幕中央创建一个输入表单，并向相应的后端 api 发送请求。

什么是 Toast ( 吐司提示 ) ？

可以把 Toast 看作是一种简短的、非侵入式的弹出方式，用于向用户显示重要的通知。在我们的例子中，我们用它来显示错误信息。


## Fire up the project

让我们把一切都启动起来。

首先，你需要克隆项目。在运行 `git clone git@github.com:Mestrace/bookmark-app.git` 之后。你需要将代码库切换到 `192ef0c` 这个分支，使用 `git checkout 192ef0c` 命令。

首先，使用我们之前展示的 mongosh 命令来验证你的数据库是否正在运行。

在一个新的命令行界面中，进入 `server` 文件夹，通过运行 `npm install` 安装所有依赖项。然后，你可以运行 `npm run dev` 来在端口 3000 启动服务器。目前这个端口号在前端项目中是硬编码的，所以你要么不做任何更改，要么必须同时更改 `client` 和 `server` 文件夹中的设置。你应该等待并查看你的 `server shell` 中是否有任何错误信息。

在一个新的命令行界面中，进入 `client` 文件夹，通过运行 `npm install` 安装所有依赖项。然后，你可以运行 `npm run dev` 来在端口 5173 启动客户端。你可以点击终端中显示的链接，它会自动在浏览器中打开。然后你就可以体验所有的功能了。

## Summary

这基本上就是整个项目了，完全从零开始。恭喜你，我和你都走到了这一步。从实践的角度来看，这个项目并不完美。我们没有忽略了生产环境中的很多事情，比如性能和安全性。我认为核心理念是，我们一开始就有一个可以动手实践的东西，所有的不完美都可以在后续的优化中处理。如果你和我一样是初学者，那么理解整个项目全貌至关重要，我不会让你我陷入各种元素的细枝末节中，因为在短时间理解项目的所有组成部分并不现实。

在接下来的文章中，我将继续解决前后端存在的一些问题。然后我们会把它部署到某个网络平台，让它正式上线。
