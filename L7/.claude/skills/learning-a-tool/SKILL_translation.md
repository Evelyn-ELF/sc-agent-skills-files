---
name: learning-a-tool
description: 为编程工具创建学习路径，并定义创建学习指南时应研究哪些信息。当用户想要学习、理解或上手任何编程工具、库或框架时使用。
---

# Learning a Tool

为编程工具创建全面的学习路径。

## Workflow

### Phase 1: Research

从三个来源收集信息。分别研究每个来源，然后汇总发现。

#### From Official Documentation

- 官方文档 URL 和当前版本
- 工具背后的动机
- 它解决什么问题 / 它帮助完成什么
- 可以使用该工具构建哪些类型的应用
- 使用场景
- 安装步骤和前置条件
- 核心概念（3-5 个基本理念）
- 官方代码示例
- Getting started 或 tutorial 内容
- API reference 要点
- 已知限制或注意事项

#### From the Repository

- 仓库 URL 和元数据（stars、最后提交、license）
- 核心系统架构（配置、数据处理流程等）
- README 快速入门部分
- Examples 文件夹内容（每个示例演示什么）
- 项目主要功能及所用技术的简要总结

#### From Community Content

- 优质教程（标题、作者、URL、为何有价值）
- 视频资源（标题、频道、时长）
- 对比文章（与替代方案对比、关键权衡）
- 人们常提到的常见陷阱和错误
- 社区渠道（Discord、Reddit、论坛）
- 真实世界的使用场景和用户评价

### Phase 2: Structure

将内容组织为渐进式层级。`references/progressive-learning.md` 是权威参考。

你必须按以下顺序创建恰好 5 个 level：

1. Level 1: Overview & Motivation
2. Level 2: Installation & Hello World
3. Level 3: Core Concepts
4. Level 4: Practical Patterns
5. Level 5: Next Steps

不要合并、跳过或重命名 level。每个 level 的内容要求定义在参考文件中。

### Phase 3: Output

生成学习路径文件夹。

## Output Format

在当前工作目录（`./learning-{tool-name}/`）中创建文件夹，包含：

```
learning-{tool-name}/
├── README.md           # 概述及如何使用此学习路径
├── resources.md        # 按来源组织的所有链接（官方、社区）
├── learning-path.md    # 遵循五个 level 的主要内容
└── code-examples/      # 各章节的可运行代码
    ├── 01-hello-world/
    ├── 02-core-concepts/
    └── 03-patterns/
```
