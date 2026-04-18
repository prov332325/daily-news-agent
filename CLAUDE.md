# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A daily IT news agent that fetches articles from an RSS feed (yozm.wishket.com), summarizes them using Gemini 2.5 Flash, and delivers the Korean-language report to a Discord channel via webhook. The workflow runs automatically every day at 09:00 KST via GitHub Actions.

## Setup

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # then fill in GEMINI_API_KEY
```

## Running

```bash
python trend_agent.py
```

Set these environment variables (or in `.env`):
- `GEMINI_API_KEY` — from Google AI Studio
- `DISCORD_WEBHOOK_URL` — Discord channel webhook (optional; skipped if absent)

## Architecture

`trend_agent.py` is the single entry point and contains all logic:

1. **`fetch_news(count)`** — fetches RSS feed via `requests` + `feedparser`, returns a plain-text list of `title + link` pairs.
2. **`analyze_with_gemini(news, count)`** — sends the news list to `gemini-2.5-flash` with a strict "facts only" Korean-language prompt. The prompt is addressed to "은실님" (the intended recipient).
3. **`send_to_discord(report)`** — splits the report into ≤1900-char chunks (Discord's 2000-char limit) and POSTs each chunk to the webhook.

The number of articles fetched is controlled by `NEWS_COUNT = 10` at the top of the file.

## GitHub Actions

`.github/workflows/news.yml` runs `trend_agent.py` daily at UTC 00:00 (KST 09:00). Secrets required in the repo: `GEMINI_API_KEY`, `DISCORD_WEBHOOK_URL`. The workflow can also be triggered manually via `workflow_dispatch`.

## Notes

- `check_available_llm_list.py` is a dev utility to list available Gemini models — it contains a hardcoded API key that should be replaced before use.
- The RSS source URL is currently `yozm.wishket.com/magazine/feed/`; the original GeekNews URL (`news.hada.io/rss/news`) is commented out.
