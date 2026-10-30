# Paper automation

The first working stage is intentionally conservative:

1. `discover.py` reads recent arXiv entries across language, AI, ML, software engineering, distributed systems and algorithms.
2. It assigns one primary category: `RL`, `Agent`, `LLM`, `Infra`, `Harness`, `Skill`, `经典算法`, or `基座模型`.
3. It builds three weekday queues—`一线资讯`, `Harness`, and `经典算法`—plus a separate `基座收藏夹` that is not treated as a fourth daily lane.
4. It writes the balanced queues and their category metadata to `data/candidates.json`.
5. The scheduled GitHub Action refreshes this queue every weekday and stays quiet when the queue has not materially changed.

It does **not** publish a full interpretation from the abstract alone. The next stage will:

- download and parse the PDF or LaTeX source;
- extract and verify method figures and result tables;
- generate a structured evidence file with page-level citations;
- render a Markdown draft;
- create a Pull Request for review;
- publish automatically only after quality gates pass.

This separation prevents a short abstract from being mistaken for a verified paper review.
