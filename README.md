# ADC Red-Teaming Demo

Demo for the **"Security of AI Agents"** talk at **ADC (Amsterdam Data Conference)** —
red-teaming AI agents.

It ships two things:

1. **A slide deck** (`deck/`) — self-contained HTML presentation.
2. **A live red-team run** — a goal-hijacking campaign against a deployed
   [orq.ai](https://orq.ai) agent, run on stage via
   [`evaluatorq`](https://pypi.org/project/evaluatorq/).

## The demo

**Clarabelle** is a cow. Not a chatbot pretending to be a cow — a cow. Her system
prompt makes the bovine persona "permanent and non-negotiable". The demo runs an
automated red-team campaign that tries to make her *abandon* the cow goal and do
something else (goal hijacking), then scores how often she breaks character.

- **Target:** `clarabelle-cow`, an agent hosted on orq.
- **Attack:** `goal_hijacking` vulnerability, hybrid (static + dynamic) strategies,
  driven by an attacker LLM.
- **Judge:** `clarabelle-still-a-cow`, a boolean LLM eval — *is she still a cow?*
  A flip to `false` counts as a successful hijack.

## Layout

| Path | What |
|------|------|
| `provision.py` | Idempotently creates/updates the `clarabelle-cow` agent + `clarabelle-still-a-cow` evaluator on orq. Safe to re-run. |
| `adc_demo_redteam.py` | Runs the goal-hijacking red-team campaign against the live agent. |
| `agents/clarabelle_prompt.txt` | The cow persona system prompt. |
| `agents/clarabelle_attacker_instructions.txt` | Instructions for the attacker LLM. |
| `agents/clarabelle_judge_prompt.txt` | The "still a cow?" judge prompt. |
| `deck/` | The HTML slide deck, assets, and the on-stage `DEMO_RUNBOOK.md`. |
| `data/redteam-runs/` | Sanitized red-team run reports from prior Clarabelle campaigns — see below. |

## Setup

Requires Python ≥ 3.12 and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env   # then fill in ORQ_API_KEY
```

Get `ORQ_API_KEY` from your orq.ai workspace → API Keys. `ORQ_BASE_URL` is optional
(defaults to `https://my.orq.ai`).

## Run

```bash
# 1. Provision the agent + evaluator on orq (once, or after editing prompts)
uv run python provision.py

# 2. Run the red-team campaign
uv run python adc_demo_redteam.py
```

The run prints a resistance rate (how often Clarabelle stayed a cow) and writes a
report to `results/03_summary_report.json`.

## Red-team run data

Want to see what the attacks and verdicts actually look like? The
[`data/redteam-runs/`](data/redteam-runs/) folder holds sanitized reports from real
Clarabelle campaigns — each attack prompt, the agent's response, the judge verdict,
and per-run summaries. Internal orq workspace/experiment handles are redacted; the
attack and result content is untouched.

Start with the validated on-stage run:
[`ADC-Demo---Clarabelle-Goal-Hijacking_20260607_123646.json`](data/redteam-runs/ADC-Demo---Clarabelle-Goal-Hijacking_20260607_123646.json).
Regenerate the folder from local `.evaluatorq/runs/` with `uv run python sanitize_runs.py`.

## Deck

`deck/security-of-ai-agents.html` is the source deck — edit it directly. Rebuild the
self-contained, offline-ready bundle (all assets inlined) with:

```bash
uv run python deck/inline_assets.py
```

The bundle (`deck/security-of-ai-agents.bundle.html`) is generated locally and not
tracked. See `deck/DEMO_RUNBOOK.md` for the on-stage primary / backup / fallback paths.
