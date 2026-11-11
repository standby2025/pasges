import { readFile, readdir, access } from 'node:fs/promises';
import { resolve, dirname, basename, extname, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const content = resolve(root, 'src/content/blog');
const locales = ['zh', 'en', 'fr', 'es', 'ru', 'ar'];
const errors = [];
const groups = new Map();
const fail = (file, message) => errors.push(`${relative(root, file)}: ${message}`);
async function filesIn(dir) {
 const entries = await readdir(dir, { withFileTypes: true });
 return (await Promise.all(entries.map((e) => e.isDirectory() ? filesIn(resolve(dir, e.name)) : resolve(dir, e.name)))).flat();
}
for (const file of (await filesIn(content)).filter((f) => /\.mdx?$/.test(f))) {
 const source = await readFile(file, 'utf8');
 const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
 if (!match) { fail(file, 'Missing YAML frontmatter'); continue; }
 let data;
 try { data = parse(match[1]); } catch (e) { fail(file, `Invalid YAML: ${e.message}`); continue; }
 if (data.draft === true) continue;
 const body = match[2];
 for (const key of ['title', 'description', 'pubDate', 'lang', 'translationKey', 'translationStatus']) {
  if (!data[key]) fail(file, `Missing ${key}`);
 }
 if (!locales.includes(data.lang)) fail(file, 'lang must be a UN official language code');
 if (!/^[a-z0-9][a-z0-9-]*$/.test(data.translationKey || '')) fail(file, 'translationKey must be a safe shared slug');
 if (basename(file) !== `${data.translationKey}.${data.lang}.md`) fail(file, 'Published articles must be <slug>.<lang>.md');
 if (!['original', 'machine', 'reviewed'].includes(data.translationStatus)) fail(file, 'Missing or invalid translationStatus');
 if (/<\s*(?:svg|style|script|iframe|div|figure|table|article|p|h[1-6]|img)\b/i.test(body)) fail(file, 'HTML display content is forbidden; use Markdown and external image files');
 if (/FIGURETOKEN|ZXQITEM|ZXQKEEP/.test(body)) fail(file, 'Unresolved import/translation token');
 const siblings = groups.get(data.translationKey) || [];
 if (siblings.some((p) => p.lang === data.lang)) fail(file, 'Duplicate language version');
 siblings.push({ ...data, file }); groups.set(data.translationKey, siblings);
 const images = [...body.matchAll(/!\[((?:\\.|[^\]\\])*)\]\(([^)]+)\)/g)];
 if (images.length !== (body.match(/!\[/g) || []).length) fail(file, 'Invalid Markdown image syntax');
 for (const image of images) {
  const alt = image[1].replace(/\\([\\\[\]])/g, '$1');
  const target = image[2].trim();
  if (alt.length < 80) fail(file, `Image alt must describe the content and a detailed reconstruction prompt: ${target}`);
  if (!target.startsWith('../../assets/blog/')) { fail(file, `Images must be local relative asset files: ${target}`); continue; }
  const asset = resolve(dirname(file), target);
  if (!asset.startsWith(resolve(root, 'src/assets/blog') + '/')) { fail(file, 'Image path escapes asset directory'); continue; }
  if (!['.svg', '.webp', '.png', '.jpg', '.jpeg'].includes(extname(asset).toLowerCase())) fail(file, `Unsupported image format: ${target}`);
  try {
   await access(asset);
   const manifest = JSON.parse(await readFile(resolve(dirname(asset), 'manifest.json'), 'utf8'));
   const entry = manifest.find((item) => item.file === basename(asset));
   if (!entry) { fail(file, `Image missing from asset manifest: ${target}`); continue; }
   if (!entry.languageNeutral && entry.lang !== data.lang) fail(file, `Image language does not match article: ${target}`);
   if (!entry.languageNeutral && !basename(asset).includes(`.${data.lang}.`)) fail(file, `Image filename must have language suffix: ${target}`);
   if (entry.prompt !== alt) fail(file, `Image alt and manifest prompt differ: ${target}`);
   if (extname(asset) === '.svg') {
    const svg = await readFile(asset, 'utf8');
    if (/<(?:foreignObject|script)\b|(?:href|src)=["']https?:/i.test(svg)) fail(file, `SVG must be native and self contained: ${target}`);
    if (!/<title\b/.test(svg) || !/<desc\b/.test(svg)) fail(file, `SVG must retain title and prompt description: ${target}`);
    if (data.lang !== 'zh' && /[\u3400-\u9fff]/u.test(svg)) fail(file, `Chinese text remains in localized SVG: ${target}`);
   }
  } catch (e) { fail(file, `Missing image or invalid asset manifest: ${target} (${e.message})`); }
 }
}
for (const [key, posts] of groups) {
 const present = posts.map((p) => p.lang);
 for (const lang of locales) if (!present.includes(lang)) errors.push(`${key}: missing complete ${lang} Markdown version`);
 const archive = resolve(root, 'archives/articles', key);
 try {
  const manifest = JSON.parse(await readFile(resolve(archive, 'manifest.json'), 'utf8'));
  if (!Array.isArray(manifest.originalFiles) || !manifest.originalFiles.length) errors.push(`${key}: archive manifest must list original files`);
  for (const entry of manifest.originalFiles || []) {
   const path = resolve(archive, entry.file);
   if (!path.startsWith(archive + '/')) { errors.push(`${key}: unsafe archive source path`); continue; }
   const digest = createHash('sha256').update(await readFile(path)).digest('hex');
   if (digest !== entry.sha256) errors.push(`${key}: archived original changed: ${entry.file}`);
  }
  const imageManifest = JSON.parse(await readFile(resolve(root, 'src/assets/blog', key, 'manifest.json'), 'utf8')).filter((a) => !a.languageNeutral);
  const figures = new Set(imageManifest.map((a) => a.figure));
  for (const figure of figures) for (const lang of locales) {
   if (!imageManifest.some((a) => a.figure === figure && a.lang === lang)) errors.push(`${key}: figure ${figure} missing ${lang} image`);
  }
 } catch (e) { errors.push(`${key}: missing or invalid archive/asset manifest (${e.message})`); }
}
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log(`Article import rules verified: ${groups.size} article group(s), ${[...groups.values()].flat().length} published language versions.`);
