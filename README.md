# 个人博客模板 (Astro + GitHub Pages)

知识类博客：宋体标题、五套可选配色、代码高亮、RSS、sitemap，以及六语文章和本地化独立图片。

## 写文章

**导入前必须阅读 [文章导入核心规则](docs/ARTICLE_IMPORT_RULES.md)**。所有后续 agent 都受此规则约束。

正式文章保留完整 Markdown，默认创建 `zh/en/fr/es/ru/ar` 六个版本，例如 `src/content/blog/homebrew-ai-toolbox.en.md`。各版本填写 `lang`、共享的 `translationKey` 和真实的 `translationStatus`；`draft: true` 不会发布。模板草稿 `hello-world.md` 不对外展示。

图表优先用独立 SVG，其次 WebP、PNG、JPEG。图中文字须随文章语言重新出图，每张图的 alt 保存内容描述和重建 prompt。图片放 `src/assets/blog/<slug>/`，原始 HTML 只保存在 `archives/articles/<slug>/`，不作为展示来源。

首页展示中文文章组；文章页提供六语入口，阿拉伯文支持 RTL。机器翻译版本会明确标记，校对后才可改为 `reviewed`。

```bash
npm install
npm run dev      # 本地预览 http://localhost:4321
npm run validate:articles # 核查六语、图片、alt prompt 和原始归档
npm run build    # 先校验，再构建到 dist/
```

站点名、简介、作者、GitHub 链接在 `src/consts.ts`;关于页在 `src/pages/about.astro`;配色在 `src/styles/global.css` 顶部变量。

## 发布:push tag 触发

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 一次性设置

1. 仓库 **Settings → Pages → Source** 选 **GitHub Actions**。
2. 仓库 **Settings → Environments → github-pages → Deployment branches and tags**,
   添加一条 **Tag** 规则 `v*`。否则 tag 触发的部署会被环境保护规则拒绝。
3. 仓库名为 `<用户名>.github.io` 时站点在根路径;其他仓库名会部署到 `/<仓库名>/`。
   两种情况工作流会自动处理 `site` 与 `base`,无需手改。

也可以在 Actions 页面选默认分支手动运行 workflow(`workflow_dispatch`)。

## 配色

页头可选暖纸、晴雾、松林、蔷薇、深海五套配色。未选择时每次加载页面随机抽取；手动选择后用浏览器 localStorage 的 `blog-theme` 保存，刷新和切换页面都会沿用。选「每次随机」可清除固定偏好。浏览器禁用存储时仍可在当前页面切换。

## 重建首篇文章

`python3 scripts/import_homebrew.py` 从归档 HTML 和已缓存的机器翻译离线重建六份完整 Markdown 与 42 张独立 SVG。原始 HTML/Markdown 不会被修改。仅显式加 `--translate` 才会向 Google Translate 请求缺失译文；机器翻译尚未人工审核。

归档的 `manifest.json` 保存原文件 SHA-256、来源、翻译方式和遗留编辑项；图片目录的 `manifest.json` 保存每种语言的重建 prompt。原稿待核实标记与截图占位图仍保留，不能视为已完成核实或已补齐截图。
