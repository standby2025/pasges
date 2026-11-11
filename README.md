# 个人博客模板 (Astro + GitHub Pages)

沉稳的中文知识类博客:米色纸张底 + 宋体标题、明暗主题、代码高亮、RSS、sitemap。

## 写文章

在 `src/content/blog/` 新建 `.md` / `.mdx`,参考 `hello-world.md` 的头信息。`draft: true` 不会发布。

```bash
npm install
npm run dev      # 本地预览 http://localhost:4321
npm run build    # 产物在 dist/
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
