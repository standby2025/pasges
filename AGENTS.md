## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

## Writing and publishing articles

Read `README.md` and the frontmatter in `src/content/blog/hello-world.md` before adding articles. Add `.md` or `.mdx` files to `src/content/blog/`; the filename becomes `/blog/<filename>/`. Required fields: `title`, `description`, `pubDate` (YYYY-MM-DD). Optional: `tags`, `updatedDate`, `draft`. Drafts are excluded from pages, lists, RSS, and sitemap. Keep the Hello World article as a draft example.

The first article, `homebrew-ai-toolbox.md`, was imported from the sibling `../a1/Homebrew-AI工具箱-成品.html`, preserving its figures and editorial placeholders. Its article-specific CSS is nested under `.homebrew-article` and uses the site's theme variables. The source includes pending fact checks and screenshots; do not silently remove their markers.

Run `npm run build` before publishing. Repository: https://github.com/standby2025/pasges. Publish by pushing a unique `v*` tag or running `gh workflow run deploy.yml --repo standby2025/pasges --ref main`. Check the Actions result and live article after deployment.
