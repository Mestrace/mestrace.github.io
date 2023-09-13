Title: Tron的手续费模型和质押2.0
Slug: git-cherry-pick
Date: 2023-08-16
Category: MISC
Status: draft


在开发过程中，总会遇到一些非正常的开发流程之外的代码提交操作，因此我们会使用cherry-pick来完成需求。
虽然网上已经有很多文章聊`git`的使用方法了，但是我觉得大家讲的都不太深入，因此想要写一篇博文来讨论。
我想讨论的大纲是这样的
1. `git cherry-pick`的通常使用方法
2. 进阶中我们怎么使用`cherry-pick`，包括如何筛选两个分支之间的差别提交，以及如何把revert的东西再次提交
3. cherry-pick & rebase vs. merge