import rss from '@astrojs/rss';
import { siteUI, type Language } from './languages';
import { getPosts, withBase } from './site';

export async function createFeed(lang: Language, site: URL | undefined) {
 const posts = await getPosts(lang);
 return rss({
  title: siteUI[lang].title,
  description: siteUI[lang].description,
  site: site!,
  customData: `<language>${lang}</language>`,
  items: posts.map((post) => ({
   title: post.data.title,
   description: post.data.description,
   pubDate: post.data.pubDate,
   link: withBase(`/blog/${post.id}/`),
  })),
 });
}
