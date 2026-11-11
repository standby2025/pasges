import { getCollection } from 'astro:content';
import type { Language } from './languages';

/** 给站内路径加上 base 前缀,兼容项目站点的子路径部署。 */
export function withBase(path: string) {
	const base = import.meta.env.BASE_URL.replace(/\/$/, '');
	return `${base}/${path.replace(/^\//, '')}`;
}

/** 已发布文章,按发布时间倒序。 */
export async function getPosts(lang?: Language) {
	const posts = await getCollection('blog', ({ data }) => !data.draft && (!lang || data.lang === lang));
	return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}
