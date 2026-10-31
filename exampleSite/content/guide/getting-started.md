---
title: Getting started
description: Install Dockleaf in an existing Hugo site.
weight: 10
---
## Installation

Copy the Dockleaf theme into `themes/dockleaf` and set `theme = 'dockleaf'`
in your site's `hugo.toml`. See the repository README for Git installation.

## Your first page

```sh
hugo new content guide/introduction.md
hugo server -D
```

{{< hint info >}}
Publish pages by removing `draft: true` from their front matter.
{{< /hint >}}

## Features

| Feature | Implementation |
| --- | --- |
| Search | Local JSON index and JavaScript |
| Navigation | Weighted content sections |
| Styling | Plain CSS |

{{< hint warning >}}
A JavaScript-capable browser is required for search and the mobile menu.
{{< /hint >}}
