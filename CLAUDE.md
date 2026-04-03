# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A personal cybersecurity blog and knowledge base built on the [Jekyll Chirpy theme](https://github.com/cotes2020/jekyll-theme-chirpy), deployed to GitHub Pages at `https://ocholuo.github.io/`. Content covers security certifications, CTFs, cloud security, network security, and general IT learning paths.

## Common Commands

### Local Development

```bash
# Serve site locally with live reload
bundle exec jekyll s -H 0.0.0.0 -l
# or use the helper script:
bash tools/run
```

### Build & Test

```bash
# Production build + HTML link validation
bash tools/test

# Build JS assets (needed after changing _javascript/)
npm install
npm run build        # production bundle
npm run watch        # watch mode during development
```

### CSS Linting

```bash
npm test             # lint _sass/**/*.scss with stylelint
npm run fixlint      # auto-fix stylelint issues
```

## Architecture

### Content Structure

- `_posts/` — all blog posts, organized into topic subdirectories (e.g. `02Security/`, `01Cloud/`, `30System/`). Posts that don't have a date in their filename won't be published.
- `_tabs/` — top-level navigation pages (`about.md`, `archives.md`, `categories.md`, `tags.md`).
- `_data/` — site data files: `authors.yml`, `contact.yml`, `share.yml`, and `locales/` for i18n.

### Post Front Matter

Every post requires this YAML front matter:

```yaml
---
title: Post Title
date: YYYY-MM-DD HH:MM:SS -0400
categories: [TopLevelCategory, SubCategory]
tags: [tag1, tag2]
---
```

Optional fields: `math: true` (enables MathJax), `image:` (post cover image), `toc: false` (disable table of contents).

Post URLs are generated as `/posts/:title/` (the title slug from the filename, not the front matter title).

### Theme Customization

- `_sass/addon/` — custom SCSS overrides on top of the Chirpy theme
- `_sass/colors/` — light/dark color scheme variables
- `_javascript/` — source JS files bundled via Rollup into `assets/js/dist/`; edit source files here, not the dist output
- `_layouts/` and `_includes/` — Liquid template overrides for the Chirpy theme

### Deployment

Pushing to `main` triggers the GitHub Actions workflow (`.github/workflows/pages-deploy.yml`), which builds with `JEKYLL_ENV=production` and deploys to GitHub Pages. The `updatepost` branch is for drafting/editing posts before merging to `main`.
