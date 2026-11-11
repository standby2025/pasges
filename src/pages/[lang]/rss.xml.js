import { createFeed } from '../../lib/feed';
import { languages } from '../../lib/languages';
export function getStaticPaths() {
 return languages.filter((lang) => lang !== 'zh').map((lang) => ({ params: { lang } }));
}
export async function GET(context) {
 return createFeed(context.params.lang, context.site);
}
