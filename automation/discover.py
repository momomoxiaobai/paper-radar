#!/usr/bin/env python3
"""Fetch recent arXiv papers and create a scored candidate queue.

This is intentionally the small, deterministic first stage of the pipeline.
It does not publish an article. A later research skill can consume the queue,
read the PDF, verify figures/tables, and create a reviewable Markdown draft.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CANDIDATES_PATH = DATA_DIR / "candidates.json"
STATE_PATH = DATA_DIR / "state.json"

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}

KEYWORDS = {
    "large language model": 14,
    "language model": 8,
    "post-training": 16,
    "reinforcement learning": 14,
    "reward model": 12,
    "agent": 10,
    "benchmark": 9,
    "evaluation": 8,
    "multimodal": 8,
    "code generation": 10,
    "data safety": 12,
    "privacy": 8,
}


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def arxiv_id(url: str) -> str:
    return url.rstrip("/").split("/")[-1].split("v")[0]


def score_paper(title: str, abstract: str, categories: list[str]) -> tuple[int, list[str]]:
    title_l = title.lower()
    body_l = f"{title} {abstract}".lower()
    score = 20
    reasons: list[str] = []

    for keyword, weight in KEYWORDS.items():
        if keyword in title_l:
            score += weight
            reasons.append(f"标题命中：{keyword}")
        elif keyword in body_l:
            score += max(3, weight // 2)
            reasons.append(f"摘要命中：{keyword}")

    if "cs.CL" in categories:
        score += 8
        reasons.append("cs.CL")
    if "cs.AI" in categories or "cs.LG" in categories:
        score += 5

    return min(score, 100), reasons[:6]


def fetch_entries() -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search_query": "(cat:cs.CL OR cat:cs.AI OR cat:cs.LG)",
            "start": 0,
            "max_results": 50,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    request = urllib.request.Request(
        f"{ARXIV_API}?{params}",
        headers={"User-Agent": "paper-radar/0.1 (https://github.com/momomoxiaobai/paper-radar)"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        root = ET.fromstring(response.read())

    entries = []
    for entry in root.findall("atom:entry", ATOM):
        paper_url = clean(entry.findtext("atom:id", namespaces=ATOM))
        title = clean(entry.findtext("atom:title", namespaces=ATOM))
        abstract = clean(entry.findtext("atom:summary", namespaces=ATOM))
        categories = [node.attrib["term"] for node in entry.findall("atom:category", ATOM)]
        authors = [clean(node.findtext("atom:name", namespaces=ATOM)) for node in entry.findall("atom:author", ATOM)]
        score, reasons = score_paper(title, abstract, categories)
        entries.append(
            {
                "arxiv_id": arxiv_id(paper_url),
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "categories": categories,
                "published": clean(entry.findtext("atom:published", namespaces=ATOM)),
                "paper_url": paper_url,
                "pdf_url": paper_url.replace("/abs/", "/pdf/") + ".pdf",
                "score": score,
                "score_reasons": reasons,
            }
        )
    return entries


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state = load_json(STATE_PATH, {"processed": [], "last_discovery_at": None})
    processed = set(state.get("processed", []))

    candidates = [item for item in fetch_entries() if item["arxiv_id"] not in processed]
    candidates.sort(key=lambda item: (item["score"], item["published"]), reverse=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Heuristic candidate queue. PDF research and article publication require a later verified generation stage.",
        "candidates": candidates[:20],
    }
    CANDIDATES_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    state["last_discovery_at"] = payload["generated_at"]
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
