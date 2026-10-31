---
title: Configuration
weight: 20
---
## Site identity

Set `params.brand`, `params.description`, and optional `params.logo` and
`params.favicon` in `hugo.toml`. Store images under your site's `static/` directory.

## Navigation

Main and footer links use Hugo menus. Sidebar navigation follows content sections,
page weights, and titles. Add `_index.md` to each section, including nested sections.
Use `navTitle` for a shorter label and `hideFromNav: true` to hide a page or subtree
from the sidebar. Hidden navigation pages remain searchable.

## Homepage

The homepage supports `heading`, `description`, `eyebrow`, `banner`, `bannerAlt`,
`bannerWidth`, `bannerHeight`, and a `cards` list in its front matter. Each card has
`title`, `url`, and `description`. All are optional; Markdown content follows the cards.

## Colors and fonts

Create `assets/css/custom.css` in your site to override theme variables and styles:

```css
:root {
  --brand: #34d399;
  --brand-hover: #6ee7b7;
}
```

Dockleaf uses system fonts and makes no external font or search requests.
