---
title: Deployment
weight: 10
---
## Static hosting

Run `hugo --minify` and publish the generated `public/` directory.

## Subdirectory hosting

Set `baseURL` to your full public URL, including its path, such as
`https://example.org/project/`. Theme assets and search follow that path.
Use relative links or Hugo page references in your own content.
