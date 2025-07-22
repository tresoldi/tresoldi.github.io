# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based academic website hosted on GitHub Pages for Tiago Tresoldi, featuring sections for research, software, and blog content. The site uses a data-driven page generation system with dynamic content created from structured data files.

## Site Architecture

- **Jekyll Static Site**: Uses the minima theme with GitHub Pages deployment
- **Data-Driven Content**: Pages are generated from structured data files using `generate_pages.py`
- **Content Sources**:
  - `_data/software.json`: Software project information organized by categories
  - `_data/publications.bib`: Research publications in BibTeX format
- **Generated Pages**: 
  - `software.md`: Generated from JSON data with project categories and descriptions
  - `research.md`: Generated from BibTeX data with formatted publication lists

## Development Commands

### Local Development

Activate the "env\_general" virtual environment with pyenv:

```bash
pyenv activate env_general
```

For other things:

```bash
# Install dependencies (requires Ruby and Bundler)
bundle install

# Serve site locally with live reload
bundle exec jekyll serve

# Build site for production
bundle exec jekyll build
```

### Content Generation
```bash
# Regenerate data-driven pages from source files
python3 generate_pages.py
```

## Key Files and Structure

- `_config.yml`: Jekyll configuration with site metadata and page ordering
- `generate_pages.py`: Python script that parses BibTeX and JSON data to generate markdown pages
- `_data/`: Contains structured data files (publications.bib, software.json)
- `_includes/`: Custom header template
- `_posts/`: Blog posts in markdown format
- Main pages: `index.md`, `about.md`, `blog.md`, `llm.md` (static content)

## Content Management

The site uses a hybrid approach:
- Static pages (about, index, blog, llm) are manually maintained
- Dynamic pages (research, software) are generated from data files
- Always run `python3 generate_pages.py` after updating `_data/` files
- The Python script handles BibTeX parsing with proper field extraction and author formatting

## Deployment

Site is configured for GitHub Pages deployment with the `github-pages` gem. Changes pushed to the main branch are automatically deployed.
