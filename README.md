# Yanjie's Paper Radar

A minimal research blog for daily paper discovery and long-form technical interpretation, built with [AstroPaper](https://github.com/satnaing/astro-paper) and deployed to GitHub Pages.

Planned site: <https://momomoxiaobai.github.io/paper-radar/>

## What is included

- Clean AstroPaper-based blog with light/dark mode, search, RSS, tags and archives.
- A detailed PresentAgent paper review with source figures and the main result table.
- GitHub Pages deployment workflow.
- A weekday arXiv discovery workflow and deterministic candidate scoring script.
- State and candidate files for the future verified paper-research pipeline.

## Local development

Requirements: Node.js 24 and pnpm 11.

```bash
pnpm install
pnpm dev
```

Production build:

```bash
pnpm build
```

## Daily paper discovery

Run the deterministic first stage manually:

```bash
python automation/discover.py
```

It fetches recent arXiv entries from `cs.CL`, `cs.AI`, and `cs.LG`, scores them against the configured interests, and writes the top candidates to `data/candidates.json`.

The discovery script deliberately does not publish an article from the abstract alone. Full paper parsing, figure/table extraction, evidence verification, LLM generation and Pull Request review will be added as a separate quality-gated stage.

## GitHub Pages setup

After pushing this repository to `momomoxiaobai/paper-radar`:

1. Open **Settings -> Pages**.
2. Set **Source** to **GitHub Actions**.
3. Run the `Deploy blog to GitHub Pages` workflow, or push to `main`.

## Content policy

Automatically generated reviews should distinguish:

- facts and numbers stated in the paper;
- findings reproduced by a local experiment;
- interpretation or opinion from this blog.

Figures and tables must preserve their source labels, and key experimental claims should be checked against the PDF before publication.

## Theme attribution

This project is based on AstroPaper, released under the MIT License. The original license is preserved in this repository.
