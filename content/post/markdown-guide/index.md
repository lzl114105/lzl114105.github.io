---
title: "写作用的 Markdown 速查"
slug: "markdown-guide"
description: "这个主题支持的语法,以及几个容易忘的写法。留着当备忘。"
date: 2026-10-26
image: "cover.png"
categories:
    - 备忘
tags:
    - Markdown
    - 写作
math: true
---

平时写文章用不到多少语法,真正高频的只有标题、加粗、链接、代码块、引用这五六样。剩下的是偶尔想起来"这个主题支不支持"时来查一下。这篇就是那份清单。

<!--more-->

## 基本结构

```markdown
# 这是 H1,一般只给标题用,正文从 ## 开始

## H2 会进右侧目录
### H3 也进目录
#### H4 是目录最深一级

**加粗**  *斜体*  ~~删除线~~  `行内代码`

[链接文字](https://example.com)

> 引用。多行引用每行前面都要有 >
```

## 代码块

三个反引号后面写上语言名,就会有语法高亮和行号:

````markdown
```java
public record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) throw new IllegalArgumentException();
    }
}
```
````

实际效果:

```java
public record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) throw new IllegalArgumentException();
    }
}
```

不写语言名也能高亮,Hugo 会猜。但猜错了反而不如不猜,建议还是写上。

## 表格

```markdown
| 左边 | 中间 | 右边 |
|:-----|:----:|-----:|
| 左对齐 | 居中 | 右对齐 |
```

| 左边 | 中间 | 右边 |
|:-----|:----:|-----:|
| 左对齐 | 居中 | 右对齐 |

## 图片

文章放在 `content/post/文章名/index.md` 这种"文件夹 + index"的结构里时,图片直接丢进同一个文件夹,引用相对路径就行:

```markdown
![描述文字](photo.jpg)
```

这样图片会跟着文章走,以后换主题、搬家都不会断。

## 折叠后面的内容

首页列表里的摘要,默认取正文开头。想手动控制在哪里断开,插一行:

```markdown
<!--more-->
```

`<!--more-->` 之后的内容不会出现在列表页的摘要里。

## 数学公式

文章的 front matter 里加 `math: true` 才会加载公式渲染,然后:

```markdown
行内公式 $O(n\log n)$,独立公式:

$$
T(n) = 2T\left(\frac{n}{2}\right) + O(n)
$$
```

行内公式 $O(n\log n)$,独立公式:

$$
T(n) = 2T\left(\frac{n}{2}\right) + O(n)
$$

## 流程图

这个主题内置了 Mermaid,直接写代码块,语言标 `mermaid`:

````markdown
```mermaid
graph LR
    A[写 md] --> B[hugo 构建]
    B --> C[推 GitHub]
    C --> D[Actions 发布]
```
````

```mermaid
graph LR
    A[写 md] --> B[hugo 构建]
    B --> C[推 GitHub]
    C --> D[Actions 发布]
```

## 提示块

主题支持三种提示样式,用短代码写:

```markdown
{{</* alert "note" */>}}
普通提示,用来补充说明。
{{</* /alert */>}}

{{</* alert "warning" */>}}
警告,写"这里有个坑"。
{{</* /alert */>}}

{{</* alert "important" */>}}
重点,一篇文章最多用一个。
{{</* /alert */>}}
```

> 上面代码块里的 `{{</* */>}}` 是为了不被 Hugo 当成短代码执行,真实写的时候去掉 `<*` 和 `*>`。

## Front matter 字段

新文章顶部的这一段,这个主题认这些字段:

```yaml
---
title: "标题"          # 必填
description: "摘要"    # 列表页和搜索结果里显示
date: 2026-10-26      # 必填,格式别写错,写错了排序会乱
image: "cover.jpg"    # 封面,不写就是纯色卡片
categories:           # 分类,会出现在首页卡片上
    - 技术
tags:                 # 标签,可以多写
    - Hugo
math: false           # 这篇要不要公式
comments: true        # 这篇要不要评论
draft: true           # true 时只有加 -D 才看得到
---
```

最容易出问题的是 `date`。写成 `2026-10-26 20:00` 没问题,写成 `2026/10/26` 就可能被解析成别的东西,而且不会报错 —— 只是文章排序莫名其妙不对。
