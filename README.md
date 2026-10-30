# 半山

一个用 [Hugo](https://gohugo.io/) + [Stack](https://github.com/CaiJimmy/hugo-theme-stack) 搭的博客。

## 五分钟上手

日常只有三件事:开着预览、写文章、推上去。

```bash
cd C:/Project/blog
hugo server -D
```

浏览器打开 http://localhost:1313 。`-D` 让草稿也渲染,这样新建的文章不用先改状态就能看见。改文件保存即刷新,停就按 `Ctrl+C`。

**一次只开一个预览。** 端口被占说明已经有一个在跑,先用那个,或者 `Ctrl+C` 关掉重开,不要用 `--port 1314` 另起一个。两个实例长得一模一样,其实是两份独立的内存副本:文件变了,A 窗口重编译了 B 窗口未必,现象就是"明明改了却没生效",而你因为地址栏端口不同,还以为看的是同一个站。

写一篇:

```bash
hugo new content post/hello-world/index.md
```

生成 `content/post/hello-world/index.md`,front matter 已经填好。文件夹名会被拿去当 `slug`(也就是网址),所以写英文;大标题在文件里改成中文。写完把 `draft: true` 改成 `false`,否则推上去线上也不会出现。

发布:

```bash
git add -A && git commit -m "新文章" && git push
```

GitHub Actions 会自己构建部署,几十秒后线上可见。**前提是仓库 Settings → Pages 的 Source 选的是 `GitHub Actions`**;选成 `Deploy from a branch` 的话,push 上去什么都不会发生,也不报错,只是站点一直停在旧版本。

## 地址和标题,是两个名字

这是最容易卡住的地方。一篇文章有两个标识:

```yaml
title: "第一篇"     # 页面上印出来的大标题
slug: "hello"       # 地址栏里那一段
```

配合 `hugo.yaml` 里的 `permalinks: post: "/p/:slug/"`,它最终落在 `/p/hello/`。所以打开 http://localhost:1313/p/hello/ ,看到的文章叫《第一篇》——页面上根本不会出现 "hello" 这个词。这不是丢文章,是它本来就这样。

反过来也成立:想找某篇,按标题找(首页卡片、`/archives/`);想手敲地址,按 slug 敲。两者对不上是正常的。

## 写了文章却看不到,按这个顺序查

1. **front matter 里有没有 `build:` 块** —— 从别处拷来的模板常带着这个:

   ```yaml
   build:
     render: never
     list: never
   ```

   这是"别生成这个页面、也别列出来",优先级高于 `draft`,而且**不报错**。症状是文件明明在、`hugo` 也不报错、就是哪都没有。删掉整块即可。

2. **`draft: true`** —— 本地带 `-D` 能看见,但 push 上线时草稿一律不发布。要发就改成 `false`。
3. **文件位置** —— 必须是一个目录:`content/post/名字/index.md`。直接把 `.md` 扔进 `content/` 或 `content/post/` 根下,不会变成文章。
4. **你看的是线上还是本地** —— 线上只认已 push 的提交。本地草稿、未推送的改动都不会出现。`git status` 有 `ahead` 就说明线上还是旧的。
5. **首页只列最近 8 篇** —— `pagination.pagerSize: 8`。更早的文章不在首页,去 `/archives/`。

五条都排除了还不显示,跑一次 `hugo --quiet`,报错会直接指到文件和行号。

## 确认这些是你自己的

`hugo.yaml` 里这几行现在是这样,确实是你自己的信息就不用动:

```yaml
baseURL: "https://lzl114105.github.io/"   # 仓库叫别的名字时,要写成 .../仓库名/
title: "半山"
```

还想调的:

- `params.sidebar.subtitle` —— 侧边栏那句副标题
- `menu.social` 里的 `url` —— 换成你的 GitHub 主页

头像换成 `assets/img/avatar.png`(建议 400×400 的正方形)。
关于页改 `content/page/about/index.md`。

## 图片:全部在配置里

所有图片入口都集中在 `hugo.yaml` 的 `params.images` 一段,换图只改一行,不用碰模板:

```yaml
params:
  images:
    hero: "img/hero.png"          # ① 首页门头横幅,建议 1600×640 以上的横图
    categories:                   # ② 分类卡片封面,键名与分类名一字不差
      技术: "img/cat-tech.png"
      随笔: "img/cat-life.png"
      备忘: "img/cat-note.png"
    postFallback: ""              # ③ 文章没封面时用的兜底图,留空就不出图
  sidebar:
    avatar: "img/avatar.png"      # ④ 头像,正方形
  favicon: "img/avatar.png"       # ⑤ 站点图标(一般是同一张)
```

路径都相对 `assets/img/`,把图丢进这个目录就行。构建时会自动转 WebP 并按需要切尺寸,所以原图多大都能用(单张建议不超过 2MB)。

**留空就等于不用图**,页面会自己换成渐变占位:门头变成暮色天空加山峦,分类卡片变成彩色色块,不会出现破图。所以你可以先把图删掉,以后再慢慢补。

文章的封面不在这配,写在文章自己的 front matter 里:

```yaml
image: "cover.png"     # 图片放在文章同一目录
```

不写 `image` 就用 `postFallback`;两个都没有,首页那张卡片就只显示文字。

## 写一篇的完整流程

```bash
hugo new content post/2026-10-26-我的题目/index.md
```

生成的文件长这样,每个字段都有用处:

```yaml
---
title: "2026 10 26 我的题目"      # 站上显示的大标题,直接改成中文
slug: "2026-10-26-我的题目"       # URL 用这个,所以别用中文
description: ""                  # 首页卡片和搜索结果里的一句话摘要
date: 2026-10-26T21:30:00+08:00
image: ""                        # 封面,填同目录下的文件名
categories: [随笔]                # 决定它归到首页哪个书架上
tags: []                         # 自由打标签,不填也不影响
draft: true                      # 改成 false 才发布
---
```

正文从 `<!--more-->` 下面开始写。这行是摘要切点:它上面的内容会出现在首页卡片里,下面的要进文章才看得见,所以第一段别写"本文介绍……",直接给结论。

图片有两种放法,都指向文章自己的目录:

- 封面 —— 图片丢进文章目录,`image: "cover.png"`
- 正文插图 —— 同样丢进文章目录,正文里写 `![](photo.jpg)`,相对路径就够了

文章是"一个目录一篇"(`content/post/名字/index.md`),不是散装的 `.md`。这样图片跟着文章走,改名、复制、备份都不会散架。

## 新建一个分类

分类不是"建"出来的,是**文章写出来的**。front matter 里写一个新名字,`/categories/新名字/` 这个页面就存在了,首页「分册」也会自动多一张卡片——不用改任何配置,也不用先声明。

想让这个分类像个正经栏目,再补一个文件:

```bash
# 目录名 = 分类名,一字不差
content/categories/读书/_index.md
```

```yaml
---
title: "读书"                              # 显示名,书架和分类页标题都用它
slug: "reading"                           # 网址用这个
description: "读过的、正在读的、读不下去的。"   # 书架上那行小字
---
```

三个字段各管一件事。`slug` 尤其值得写:不写的话网址是 `/categories/%E8%AF%BB%E4%B9%A6/`,写了就是 `/categories/reading/`。

配封面(可选):

```yaml
params:
  images:
    categories:
      读书: "img/cat-read.png"    # 键名是分类名,不是 slug
```

图放 `assets/img/`。键名要和文章里 `categories:` 写的那串字一模一样,差一个字就取不到,然后静默退回渐变——不报错,但你会以为图没生效。

删分类:把文章里那行删掉,它自己就消失;`_index.md` 留着不影响,清掉更干净。

## 在手机上写

手机上不跑 Hugo,思路反过来:**你只管改文件,GitHub Actions 替你构建**。手机浏览器登录 github.com,进 `lzl114105/lzl114105.github.io` 仓库,就够用了。

**改一篇**:进 `content/post/文章名/index.md` → 右上铅笔图标 → 改完拉到底 **Commit changes**(直接提交到 `main`)→ 等 Actions 跑完,一分钟内线上生效。

**新写一篇**:仓库页 **Add file → Create new file**,文件名一栏直接输路径,斜杠会自动变成目录:

```
content/post/my-new-post/index.md
```

粘贴这段开头,然后写正文:

```yaml
---
title: "标题写中文"
slug: "my-new-post"
description: "一句话摘要"
date: 2026-10-30
categories:
    - 随笔
tags:
draft: false        # 手机上最容易忘的一行
---

正文从这开始。
```

**发照片**:文章目录里 **Add file → Upload files**,传完在正文用 `![](photo.jpg)` 引用,文件名对上就行。

**最大的一条纪律:手机提交后,电脑必须先 `git pull` 再干活。** 两边各改各的,后 push 的那个会被拒,新手上手最容易被这个吓到。养成"坐下先 pull,起身已推送"的习惯,冲突就永远不会发生。

嫌网页编辑器糙的话,下一步可以给站里加 Decap CMS(一个 `/admin/` 后台页面,手机浏览器打开就是像样的编辑器,能建文章、传图、发布),需要配一次 GitHub 授权,想做说一声。

## 目录结构

```
hugo.yaml                 全站配置,图片入口也在里面(params.images)
content/
  post/文章名/index.md     文章。图片丢进同目录,用 ![x](photo.jpg) 引用
  page/about/index.md     关于页
  page/archives/index.md  归档页
  page/search/index.md    搜索页
assets/
  img/hero.png            首页门头横幅
  img/cat-*.png           分类卡片封面
  img/avatar.png          头像 + 站点图标
  css/custom.css          皮肤:配色、字体、卡片、门头样式(顶部是色板变量)
  js/custom.js            阅读进度条、列表入场动画
layouts/
  home.html               首页结构(门头 / 文章流 / 分类书架)
  _partials/custom/img.html   统一取图助手(配置里的路径 → Hugo 图片资源)
themes/hugo-theme-stack/  主题(直接放在仓库里,不依赖外网)
.github/workflows/hugo.yaml  自动部署流水线
```

## 想改样子改哪里

| 想改的 | 改哪 |
|---|---|
| 主色、强调色、深色模式配色 | `assets/css/custom.css` 顶部 `:root` 和 `[data-scheme="dark"]` 两个色块 |
| 标题字体 / 正文字体 | 同文件 `--font-serif` / `--font-body` |
| 首页门头文案、文章流、分类书架的结构 | `layouts/home.html` |
| 卡片圆角、阴影、间距 | `custom.css` 里的 `--radius` / `--shadow` / `--section-separation` |
| 开场的文字 / 关掉开场 | `hugo.yaml` 的 `params.intro` |
| 开场速度、斜切角度、辉光颜色 | `custom.css` 末尾「开场」那一段 |

## 首页开场:一个字被切开

进首页时先黑屏，中间浮出一个词，接着一道 -11.5° 的斜光把它划开，幕布顺着这道缝撕向两侧，露出页面。它由四层东西叠着演，时间轴错开：

| 层 | 动作 | 起 |
|---|---|---|
| 幕布两片 | 用 `clip-path` 沿斜线各留一半，撕开时朝相反方向平移并旋转 | 1.95s |
| 光刃 | 一条 150vmax 长的细线，从中心向两端扫出去 | 1.45s |
| 切口 | 标题身上那条 1.55em 的亮线，扫过字身 | 1.2s |
| 标题 | 从模糊里浮出、放大，再被淡出吃掉 | 0s |

改文案和开关:

```yaml
params:
  intro:
    enable: true
    text: "半山"      # 幕布中央那个词
    tagline: ""       # 下面一行小字,留空不显示
```

三个约束,都是刻意的:**只在首页**播(文章页来回跳不打断阅读);**一个会话只播一次**,靠 `sessionStorage` 记标记,刷新不重播,关掉标签页重开才会再演一次;**系统开了「减少动态效果」就直接不注入**,不给这类用户塞黑屏。

要调节奏就改 `custom.css` 里 `@keyframes introLeft/introRight` 的位移和 `intro*` 的 `animation-delay`,别去动 JS。

## 部署到 GitHub Pages 的完整步骤

1. 在 GitHub 建仓库,名字用 `你的用户名.github.io`(这样网址就是 `https://你的用户名.github.io/`,最省事);如果仓库叫别的名字,`baseURL` 要写成 `https://你的用户名.github.io/仓库名/`
2. 本地 `git init && git add -A && git commit -m init`
3. `git remote add origin git@github.com:你的用户名/仓库名.git`
4. `git branch -M main && git push -u origin main`
5. 仓库页面 → Settings → Pages → **Source 选 `GitHub Actions`**(不是 Deploy from a branch)
6. 等 Actions 跑完,访问你的网址

## 几个容易踩的坑

**日期格式写错会静默出问题。** front matter 里 `date: 2026-10-26` 最稳,别写 `2026/10/26`。写错了不报错,只是排序乱。

**中文标题会生成中文 URL。** 已经在 archetypes 里给新文章自动加了 `slug` 字段,取文件夹名。想让某篇换地址,改它 front matter 里的 `slug`。

**想换主题。** 把新主题放进 `themes/`,`hugo.yaml` 里 `theme:` 改成新目录名。文章在 `content/` 下与主题无关,不受影响;但主题自定义的短代码、配色变量要重做。

**评论默认是关的。** 要开就去 [giscus.app](https://giscus.app/) 拿到 `repo` 和 `repoID`,填进 `hugo.yaml` 的 `params.comments.giscus`,再把 `params.comments.enabled` 改成 `true`。

**Hugo 装在哪。** 二进制在 `~/bin/hugo.exe`(已在 PATH 里),版本 v0.168.0 extended。这个站点必须用 **extended** 版,普通版编译不了主题的 SCSS。
