import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { languages } from './lib/languages';

const blog = defineCollection({
	loader: glob({
		base: './src/content/blog',
		pattern: '**/*.{md,mdx}',
		generateId: ({ entry }) => entry.replace(/\.(md|mdx)$/, ''),
	}),
	schema: z.object({
		lang: z.enum(languages).default('zh'),
		translationKey: z.string().optional(),
		translationStatus: z.enum(['original', 'machine', 'reviewed']).default('original'),
		title: z.string(),
		description: z.string(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		tags: z.array(z.string()).default([]),
		// draft: true 的文章在构建时会被跳过
		draft: z.boolean().default(false),
	}),
});

export const collections = { blog };
