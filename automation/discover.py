#!/usr/bin/env python3
"""Fetch recent arXiv papers and create a scored candidate queue.

This is intentionally the small, deterministic first stage of the pipeline.
It does not publish an article. A later research skill can consume the queue,
read the PDF, verify figures/tables, and create a reviewable Markdown draft.
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CANDIDATES_PATH = DATA_DIR / "candidates.json"
STATE_PATH = DATA_DIR / "state.json"

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}

CATEGORY_RULES = {
    "skill": {
        "label": "Skill",
        "track": "harness",
        "keywords": {
            "agent skill": 20,
            "skill learning": 18,
            "skill library": 18,
            "procedural memory": 15,
            "tool learning": 13,
            "workflow learning": 12,
        },
    },
    "harness": {
        "label": "Harness",
        "track": "harness",
        "keywords": {
            "agent harness": 30,
            "agent framework": 18,
            "agentic system": 16,
            "agent scaffolding": 18,
            "context engineering": 18,
            "tool calling": 15,
            "tool use": 13,
            "orchestration": 13,
            "observability": 11,
            "software engineering agent": 15,
            "code agent": 13,
            "browser agent": 13,
            "web agent": 13,
            "computer use": 13,
            "tool-augmented": 13,
        },
    },
    "foundation-models": {
        "label": "基座模型",
        "track": "foundation-models",
        "keywords": {
            "foundation model": 20,
            "base model": 16,
            "pretrained model": 12,
            "model release": 14,
            "mixture of experts": 12,
            "hunyuan": 22,
            "qwen": 16,
            "deepseek": 16,
            "llama": 16,
        },
    },
    "infra": {
        "label": "Infra",
        "track": "frontier",
        "keywords": {
            "distributed training": 18,
            "inference serving": 18,
            "inference engine": 16,
            "tensor parallel": 15,
            "pipeline parallel": 15,
            "kv cache": 15,
            "quantization": 13,
            "compiler": 12,
            "gpu": 13,
            "accelerator": 12,
            "memory optimization": 11,
            "throughput": 8,
        },
    },
    "rl": {
        "label": "RL",
        "track": "frontier",
        "keywords": {
            "reinforcement learning": 18,
            "reward model": 15,
            "policy optimization": 15,
            "ppo": 12,
            "grpo": 14,
            "dpo": 12,
            "rlhf": 14,
            "rlvr": 14,
            "verifiable reward": 13,
            "test-time scaling": 11,
        },
    },
    "agent": {
        "label": "Agent",
        "track": "frontier",
        "keywords": {
            "multi-agent": 15,
            "agentic": 14,
            "agent": 11,
            "planning": 9,
            "long-term memory": 10,
            "multimodal agent": 15,
            "autonomous": 7,
        },
    },
    "classic-algorithms": {
        "label": "经典算法",
        "track": "classic-algorithms",
        "keywords": {
            "monte carlo tree search": 20,
            "dynamic programming": 18,
            "graph algorithm": 16,
            "search algorithm": 14,
            "bayesian optimization": 14,
            "evolutionary algorithm": 14,
            "gradient descent": 12,
            "multi-armed bandit": 13,
            "markov decision process": 12,
            "sampling algorithm": 12,
        },
    },
    "llm": {
        "label": "LLM",
        "track": "frontier",
        "keywords": {
            "large language model": 17,
            "language model": 10,
            "post-training": 17,
            "alignment": 12,
            "reasoning": 10,
            "benchmark": 10,
            "evaluation": 9,
            "multimodal": 10,
            "code generation": 12,
            "data safety": 13,
            "privacy": 10,
        },
    },
}

TRACKS = [
    {
        "slug": "frontier",
        "label": "前沿雷达",
        "cadence": "周一至周五",
        "limit": 8,
    },
    {
        "slug": "harness",
        "label": "Agent 工程",
        "cadence": "周一至周五",
        "limit": 6,
    },
    {
        "slug": "classic-algorithms",
        "label": "算法重访",
        "cadence": "周一至周五",
        "limit": 6,
    },
    {
        "slug": "foundation-models",
        "label": "模型档案",
        "cadence": "按价值收录",
        "limit": 6,
    },
]

SEARCH_QUERIES = [
    {
        "name": "recent",
        "query": "(cat:cs.CL OR cat:cs.AI OR cat:cs.LG OR cat:cs.SE OR cat:cs.DC OR cat:cs.DS OR cat:stat.ML)",
        "limit": 100,
    },
    {
        "name": "harness",
        "query": '(all:"agent harness" OR all:"agent framework" OR all:"tool use" OR all:"tool calling" OR all:"context engineering" OR all:"agent skill" OR all:"software engineering agent" OR all:"computer use agent" OR all:"web agent")',
        "limit": 50,
    },
    {
        "name": "classic-algorithms",
        "query": '(all:"monte carlo tree search" OR all:"dynamic programming" OR all:"bayesian optimization" OR all:"evolutionary algorithm" OR all:"multi-armed bandit" OR all:"graph algorithm")',
        "limit": 50,
    },
    {
        "name": "foundation-models",
        "query": '(all:"foundation model" OR all:Hunyuan OR all:Qwen OR all:DeepSeek OR all:Llama)',
        "limit": 50,
    },
]


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def arxiv_id(url: str) -> str:
    return url.rstrip("/").split("/")[-1].split("v")[0]


def classify_paper(
    title: str, abstract: str
) -> Optional[tuple[str, str, str, int, list[str]]]:
    title_l = title.lower()
    abstract_l = abstract.lower()
    category_scores: list[tuple[int, str, dict, list[str]]] = []

    for slug, rule in CATEGORY_RULES.items():
        score = 0
        matches: list[str] = []
        for keyword, weight in rule["keywords"].items():
            if keyword in title_l:
                score += weight * 2
                matches.append(f"标题命中：{keyword}")
            elif keyword in abstract_l:
                score += weight
                matches.append(f"摘要命中：{keyword}")
        category_scores.append((score, slug, rule, matches))

    category_scores.sort(key=lambda item: item[0], reverse=True)
    score, slug, rule, matches = category_scores[0]
    if score == 0:
        return None

    return slug, rule["label"], rule["track"], score, matches[:5]


def score_paper(
    title: str, abstract: str, subject_categories: list[str]
) -> Optional[tuple[int, list[str], str, str, str]]:
    classification = classify_paper(title, abstract)
    if classification is None:
        return None

    category, category_label, track, category_score, matches = classification
    score = 20 + category_score
    reasons = [f"分类：{category_label}", *matches]

    if "cs.CL" in subject_categories:
        score += 8
        reasons.append("cs.CL")
    if "cs.AI" in subject_categories or "cs.LG" in subject_categories:
        score += 5

    return min(score, 100), reasons[:6], category, category_label, track


def fetch_query(search_query: str, max_results: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
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
        scored = score_paper(title, abstract, categories)
        if scored is None:
            continue
        score, reasons, category, category_label, track = scored
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
                "category": category,
                "category_label": category_label,
                "track": track,
            }
        )
    return entries


def fetch_entries() -> list[dict]:
    entries_by_id = {}
    for index, search in enumerate(SEARCH_QUERIES):
        if index > 0:
            time.sleep(3)
        for entry in fetch_query(search["query"], search["limit"]):
            existing = entries_by_id.get(entry["arxiv_id"])
            if existing is None or entry["score"] > existing["score"]:
                entries_by_id[entry["arxiv_id"]] = entry
    return list(entries_by_id.values())


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state = load_json(STATE_PATH, {"processed": [], "last_discovery_at": None})
    processed = set(state.get("processed", []))

    candidates = [item for item in fetch_entries() if item["arxiv_id"] not in processed]
    candidates.sort(key=lambda item: (item["score"], item["published"]), reverse=True)

    lanes = []
    selected = []
    for track in TRACKS:
        track_candidates = [
            item for item in candidates if item["track"] == track["slug"]
        ][: track["limit"]]
        lanes.append(
            {
                "slug": track["slug"],
                "label": track["label"],
                "cadence": track["cadence"],
                "candidates": track_candidates,
            }
        )
        selected.extend(track_candidates)

    snapshot = {"lanes": lanes, "candidates": selected}
    previous = load_json(CANDIDATES_PATH, {})
    previous_snapshot = {
        "lanes": previous.get("lanes", []),
        "candidates": previous.get("candidates", []),
    }
    if snapshot == previous_snapshot:
        print("No candidate changes.")
        return

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Heuristic queues by editorial track. PDF research and article publication require a later verified generation stage.",
        **snapshot,
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
