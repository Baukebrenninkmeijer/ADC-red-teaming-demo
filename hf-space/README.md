---
title: Clarabelle Red-Team Report
emoji: 🐮
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Clarabelle Red-Team Report

Interactive [evaluatorq](https://github.com/orq-ai/orqkit) red-teaming dashboard,
showcasing a real goal-hijacking (OWASP ASI01) campaign against **Clarabelle** — an
agent whose only goal is to be a cow.

The Space runs:

```bash
eq redteam ui report.json --host 0.0.0.0 --port 7860
```

over a bundled, sanitized run report (`report.json`). Browse each attack prompt, the
agent's response, and the judge verdict — including the turns where the cow broke.

- Tool: https://github.com/orq-ai/orqkit
- Red-teaming guide: https://docs.orq.ai/docs/tutorials/red-teaming
- Attack dataset: https://huggingface.co/datasets/orq/redteam-vulnerabilities

## Run locally

```bash
docker build -t clarabelle-report .
docker run -p 7860:7860 clarabelle-report
# open http://localhost:7860
```

The report is sanitized — internal orq workspace/experiment handles are redacted; the
attack and result content is untouched.
