# 半山

一个用 [Hugo](https://gohugo.io/) + [Stack](https://github.com/CaiJimmy/hugo-theme-stack) 搭的博客。

## 先改这三处

打开 `hugo.yaml`,把占位的改成你自己的:

```yaml
baseURL: "https://YOURNAME.github.io/"   # 你的 GitHub 用户名
title: "半山"                             # 站名
```

再改这两个地方:

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

## 日常三件事

**写新文章**

```bash
hugo new content post/文章名/index.md
```

会生成 `content/post/文章名/index.md`,里面已经填好 front matter。`draft: true` 改成 `false` 才会发布。

**本地预览**

```bash
cd 到博客目录
hugo server -D
```

打开 http://localhost:1313 。`-D` 表示草稿也显示。改文件保存即刷新,不用重启。

**发布**

```bash
git add -A && git commit -m "新文章" && git push
```

推上去之后 GitHub Actions 自动构建发布,大概十几秒到一分钟。

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
