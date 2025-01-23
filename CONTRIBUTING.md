# 贡献

该项目欢迎世界各地的开发者和组织的贡献。我们的目标是培育一个协作和包容的社区，在这里，不同的观点和专业知识可以推动创新并增强项目的能力。无论您是个人贡献者还是代表组织，我们邀请您加入我们，共同塑造该项目的未来。可能的贡献包括但不限于：

* Pushing patches.
* Pushing patches.
* Code review of pull requests.
* Documentation, examples and test cases.
* Readability improvement, e.g., improvement on docstr and comments.
* Community participation in [issues](https://github.com/langfarm/langfarm/issues), [discussions](https://github.com/langfarm/langfarm/discussions).
* Tutorials, blog posts, talks that promote the project.
* Sharing application scenarios and/or related research.

如果您是 GitHub 新手，[这里 English](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests) / [中文](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests) 有关于参与 GitHub 开发的详细帮助资源。

## 版本号

版本号，按 [语义化版本](https://semver.org/lang/zh-CN/) 标准。

版本格式：主版本号.次版本号.修订号 （MAJOR.MINOR.PATCH），版本号递增规则如下：

* MAJOR - 主版本号：当你做了不兼容的 API 修改，
* MINOR - 次版本号：当你做了向下兼容的功能性新增，
* PATCH - 修订号：当你做了向下兼容的问题修正。

## commit 规范

提交约定：[Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)

* **fix**: 类型 为 fix 的提交表示在代码库中修复了一个 bug（这和语义化版本中的 ```PATCH``` 相对应）。
* **feat**: 类型 为 feat 的提交表示在代码库中新增了一个功能（这和语义化版本中的 ```MINOR``` 相对应）。
* **BREAKING CHANGE**: 在脚注中包含 BREAKING CHANGE: 或 <类型>(范围) 后面有一个 ! 的提交，表示引入了破坏性 API 变更（这和语义化版本中的 ```MAJOR``` 相对应）。 破坏性变更可以是任意 类型 提交的一部分。
* 其它：
  * build: 用于修改项目构建系统，例如修改依赖库、外部接口或者升级 Node 版本等；
  * chore: 用于对非业务性代码进行修改，例如修改构建流程或者工具配置等；
  * ci: 用于修改持续集成流程，例如修改 Travis、Jenkins 等工作流配置；
  * docs: 用于修改文档，例如修改 README 文件、API 文档等；
  * style: 用于修改代码的样式，例如调整缩进、空格、空行等；
  * refactor: 用于重构代码，例如修改代码结构、变量名、函数名等但不修改功能逻辑；
  * perf: 用于优化性能，例如提升代码的性能、减少内存占用等；
  * test: 用于修改测试用例，例如添加、删除、修改代码的测试用例等。
* 脚注中除了 ```BREAKING CHANGE: <description>``` ，其它条目应该采用类似 git trailer format 这样的惯例。
