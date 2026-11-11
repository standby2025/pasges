import { createFeed } from '../lib/feed';
export async function GET(context) {
 return createFeed('zh', context.site);
}
