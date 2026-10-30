# Paper automation

The first working stage is intentionally conservative:

1. `discover.py` reads recent `cs.CL`, `cs.AI`, and `cs.LG` entries from arXiv.
2. It applies deterministic interest weights for LLMs, agents, RL, evaluation, benchmarks, multimodality, and data safety.
3. It writes the top candidates to `data/candidates.json`.
4. The scheduled GitHub Action refreshes this queue every weekday.

It does **not** publish a full interpretation from the abstract alone. The next stage will:

- download and parse the PDF or LaTeX source;
- extract and verify method figures and result tables;
- generate a structured evidence file with page-level citations;
- render a Markdown draft;
- create a Pull Request for review;
- publish automatically only after quality gates pass.

This separation prevents a short abstract from being mistaken for a verified paper review.
