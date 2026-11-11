// @ts-check
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// 部署时由 GitHub Actions 注入(见 .github/workflows/deploy.yml),本地开发用默认值。
// 用户站点 (<user>.github.io 仓库):base 为 '/';项目站点 (<user>.github.io/<repo>):base 为 '/<repo>'。
export default defineConfig({
	site: process.env.SITE_URL || 'http://localhost:4321',
	base: process.env.BASE_PATH || '/',
	integrations: [mdx(), sitemap()],
	markdown: {
		shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' } },
	},
});
