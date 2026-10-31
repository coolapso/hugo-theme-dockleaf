# Dockleaf

A lightweight, dark Hugo documentation theme with built-in search. Plain CSS,
plain JavaScript, and Markdown: no Node.js, package manager, or frontend build step.

Features include responsive navigation, nested sections, a table of contents,
syntax highlighting, hint boxes, configurable homepage cards, and local search.
System fonts are the default; no external font or search services are used.

## Live example

See [Searchbase Documentation](https://docs.searchbase.md/) for a live example
of the documentation layout Dockleaf was extracted from.

## Install

Requires Hugo **0.168.0 or newer** (standard edition is sufficient).
From your Hugo site, after this repository is published:

```sh
git submodule add https://github.com/coolapso/dockleaf.git themes/dockleaf
```

Or copy the theme into `themes/dockleaf`. A copied installation needs `layouts/`,
`static/`, `i18n/`, `hugo.toml`, `theme.toml`, `LICENSE`, and `NOTICE`.
Set this in the site's `hugo.toml`:

```toml
baseURL = 'https://example.org/'
locale = 'en-us'
title = 'My Project Documentation'
theme = 'dockleaf'

[outputs]
  home = ['HTML', 'JSON']

[markup.tableOfContents]
  startLevel = 2
  endLevel = 3

[markup.highlight]
  style = 'onedark'
  lineNos = true

[params]
  brand = 'My Project'
  description = 'Documentation for my project.'
  # Optional paths relative to static/:
  # logo = 'images/logo.svg'
  # favicon = 'images/favicon.svg'
  footer = 'Copyright My Project contributors.'

[[menus.main]]
  name = 'Start'
  pageRef = '/guide/getting-started'
  weight = 1

[[menus.footer]]
  name = 'Source'
  url = 'https://github.com/example/project'
```

`pageRef` resolves internal menu destinations using Hugo's content tree. For card
and image URLs use paths such as `guide/getting-started/` or `images/logo.svg`;
these work with subdirectory hosting too. External URLs are also supported.

The site configuration above enables the homepage JSON output required for search,
a level 2–3 table of contents, and onedark code highlighting. Hugo does not inherit
these settings from theme configuration. Include both `HTML` and `JSON` home outputs.

## Content and navigation

Create `content/guide/_index.md` for a section and Markdown pages beneath it.
Sidebar sections and pages sort by Hugo `weight` and title. Nested sections work
recursively. Front matter supports `navTitle` for sidebar labels and
`hideFromNav: true` to hide a page or entire subtree from navigation. This does
not make content private or exclude it from search. Section landing pages render
Markdown content; write an introduction or links there as appropriate.

The homepage (`content/_index.md`) supports:

```yaml
---
title: My Project
heading: My Project Docs
description: Learn to install and use My Project.
eyebrow: Documentation
# Optional banner, bannerAlt, bannerWidth, bannerHeight
cards:
  - title: Getting started
    url: guide/getting-started/
    description: Install and configure your first instance.
---
Additional Markdown content goes here.
```

Pages support `description` and `eyebrow`. The `hint` shortcode renders callouts:

```text
{{< hint warning >}}
Back up your configuration before upgrading.
{{< /hint >}}
```

Use `info` (the default) or `warning`.

## Customization

Put CSS overrides in your site's `assets/css/custom.css`. Available color variables
are `--bg`, `--panel`, `--panel-2`, `--border`, `--text`, `--muted`, `--dim`,
`--brand`, `--brand-hover`, `--accent`, and `--danger`. Several translucent surfaces
are tuned to the default dark palette; this is a dark theme, not a light-mode system.
Override layouts or partials through your site's `layouts/` directory when needed.

English UI messages are in `i18n/en.toml`. Add translations in your site's `i18n/`
directory. Hugo controls document language, translated content, menus, and URLs;
only English UI translations ship with the initial theme.

Search matches case-insensitive substrings across regular page titles and text,
returns up to six results, and downloads the local index on the first query of
at least two characters. It suits small to medium documentation sites; it does
not provide stemming, ranking, or a remote search service. All indexed text is public.

## Preview and validate

From this repository:

```sh
hugo server --source exampleSite --themesDir ../.. --theme dockleaf
python3 scripts/check.py
```

The preview command assumes this checkout is named `dockleaf`. Validation uses a
temporary theme installation and does not depend on the checkout directory name.
It builds the example at both domain root and a subdirectory, checks links,
assets, search index, nested navigation, and customization, and checks JavaScript
syntax when Node.js is installed. Python 3 and Hugo are required; Node.js is optional.
No packages need installing.

## Publishing on Hugo Themes

Follow the [current submission guidelines](https://github.com/gohugoio/hugoThemesSiteBuilder#adding-a-theme)
for [themes.gohugo.io](https://themes.gohugo.io/).

Before submitting:

- [ ] Publish the repository on a Go Modules-compatible Git host.
- [ ] Complete root `theme.toml`: name, license, license URL, description,
  homepage, tags, features, and author details; add `demosite` for the live example
  and `[original]` attribution for the Searchbase source.
- [x] Declare supported Hugo versions in `hugo.toml` under `[module.hugoVersion]`.
- [x] Include an open-source license and preserve source attribution.
- [x] Provide an English Markdown README covering installation and configuration;
  use absolute URLs for embedded images.
- [ ] Add `images/screenshot.png` or `.jpg`: at least **1500 × 1000** pixels.
- [ ] Add `images/tn.png` or `.jpg`: at least **900 × 600** pixels.
  Both images need a **3:2** aspect ratio, without browser chrome or device mockups.
- [ ] Run `task test` with the latest Hugo before submission.
- [ ] Push all submission files; if using releases, include them in the latest release.
  Preserve published Git references and tags.
- [ ] Fork [hugoThemesSiteBuilder](https://github.com/gohugoio/hugoThemesSiteBuilder),
  add `github.com/coolapso/dockleaf` to `themes.txt` in lexicographical order,
  and open a descriptive pull request. Ensure its Netlify preview succeeds.

Keep the theme free, its README free of paid-product marketing, and maintain Hugo
compatibility; themes without updates for 18 months may be removed. Derivatives
must be notably different; explain their differences.

Dockleaf turns Searchbase's project-specific layouts into configurable branding,
menus, homepage cards, recursive navigation, and portable asset and search URLs.
Its standalone `exampleSite/` demonstrates reuse without Searchbase content.
The checklist records preparation work; it does not indicate acceptance or publication.

## License and origin

GNU AGPLv3; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Extracted from the
[Searchbase](https://github.com/coolapso/searchbase) documentation theme.
Searchbase content, branding, and artwork are not part of Dockleaf.

## Support

If you like this project and want to support / contribute in a different way you can always [:heart: Sponsor Me](https://github.com/sponsors/coolapso) or

<a href="https://www.buymeacoffee.com/coolapso" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" />
</a>
