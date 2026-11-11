import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const languages = ['zh', 'en', 'fr', 'es', 'ru', 'ar'];
const locales = { zh: 'zh-CN', en: 'en-US', fr: 'fr-FR', es: 'es-ES', ru: 'ru-RU', ar: 'ar' };
const base = (process.env.BASE_PATH || '').replace(/\/$/, '');
const errors = [];
for (const lang of languages) {
 const prefix = lang === 'zh' ? '' : `/${lang}`;
 for (const page of ['', '/blog', '/about']) {
  const file = resolve('dist', `.${prefix}${page}/index.html`);
  try {
   const html = await readFile(file, 'utf8');
   const expectedDir = lang === 'ar' ? 'rtl' : 'ltr';
   if (!html.includes(`lang="${locales[lang]}"`) || !html.includes(`dir="${expectedDir}"`)) errors.push(`${file}: wrong page language/direction`);
   for (const path of ['/', '/blog/', '/about/']) {
    if (!html.includes(`href="${base}${prefix}${path}"`)) errors.push(`${file}: missing current-language navigation ${path}`);
   }
   if (!html.includes(`href="${base}${prefix}/rss.xml"`)) errors.push(`${file}: missing localized RSS`);
   if (!html.includes('id="language-picker"')) errors.push(`${file}: missing global language switcher`);
   const alternates = [...html.matchAll(/<link\b[^>]*hreflang="(zh|en|fr|es|ru|ar)"[^>]*>/g)];
   if (new Set(alternates.map((m) => m[1])).size !== 6) errors.push(`${file}: missing global hreflang`);
   const postList = html.match(/<ul\b[^>]*class="post-list[^"]*"[^>]*>([\s\S]*?)<\/ul>/)?.[1] || '';
   for (const item of postList.matchAll(/<a\b[^>]*href="([^"]+)"/g)) {
    if (!item[1].endsWith(`.${lang}/`)) errors.push(`${file}: article list contains another language: ${item[1]}`);
   }
  } catch (e) { errors.push(`${file}: ${e.message}`); }
 }
 try {
  const rss = await readFile(resolve('dist', `.${prefix}/rss.xml`), 'utf8');
  if (!rss.includes(`<language>${lang}</language>`)) errors.push(`${lang}: wrong RSS language`);
  for (const item of rss.matchAll(/<item>([\s\S]*?)<\/item>/g)) {
   if (!item[1].includes(`.${lang}/`)) errors.push(`${lang}: RSS item points to another language`);
  }
 } catch (e) { errors.push(`${lang}: missing RSS: ${e.message}`); }
}
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log('Global localization verified: 18 home/archive/about pages and 6 language-specific feeds.');
