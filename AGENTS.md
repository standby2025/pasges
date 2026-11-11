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

## Core article import rules (mandatory)

Before importing, editing, translating, or publishing any article, read and follow [docs/ARTICLE_IMPORT_RULES.md](docs/ARTICLE_IMPORT_RULES.md). This is a core project requirement: retain full Markdown, archive original HTML without displaying it, produce all six UN official languages with filename suffixes, externalize charts/images using SVG > WebP > PNG > JPEG priority, localize text inside images, and include a reconstruction prompt in every image alt. Do not omit these requirements to save time.

Read `README.md` for commands and publication workflow. Run `npm run validate:articles` and `npm run build` before publishing. Keep `hello-world.md` as a hidden draft example. The Homebrew article is the first example of the six-language import format. Its source includes pending fact checks and screenshots; do not silently remove those markers.

Repository: https://github.com/standby2025/pasges. Publish using a unique `v*` tag or `gh workflow run deploy.yml --repo standby2025/pasges --ref main`, then check the Actions result and live articles.
