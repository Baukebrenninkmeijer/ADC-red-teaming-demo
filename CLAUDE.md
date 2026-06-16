# ADC Demo — Security of AI Agents

Conference demo for **ADC** (Amsterdam Data Conference). Talk theme: red-teaming AI
agents. The deliverable is an HTML slide deck plus a live red-team run against a
deployed orq agent (`clarabelle-cow`).

## What we're working on (current)

The active artifact is the **HTML slide deck in `deck/`**:

- `deck/security-of-ai-agents.html` — the deck. **This is the file we edit.**
- `deck/security-of-ai-agents.bundle.html` — self-contained build (assets inlined via
  `deck/inline_assets.py`) for presenting offline. Regenerate after editing the deck.
- `deck/assets/` — images, video, and baked transcript/result JSON the slides pull from.
- `deck/DEMO_RUNBOOK.md` — how the live demo is run on stage (primary / backup / fallback paths).

Supporting the deck is the live red-team demo:

- `adc_demo_redteam.py` — goal-hijacking red-team run against `agent:clarabelle-cow`
  via evaluatorq. Backup path when the `orq-red-team` skill stalls. (See runbook.)
- `provision.py` — idempotently provisions the `clarabelle-cow` agent + `clarabelle-still-a-cow`
  evaluator on orq (research workspace, ADC project). Safe to re-run.
- `agents/clarabelle_*.txt` — the cow persona prompt, attacker instructions, judge prompt.
- `thoughts.md` — talk narrative / content planning notes.
- `results/03_summary_report.json` — captured output of the validated 2026-06-07 run.

## Conventions

- Edit `deck/security-of-ai-agents.html` directly; rebuild the bundle with
  `uv run python deck/inline_assets.py` (check the script for exact in/out paths).
- `.env` holds the ADC-project `ORQ_API_KEY`. The red-team script force-pops
  `OPENAI_API_KEY` so calls route through the ORQ router.
- Core deps are `evaluatorq[orq,redteam]` + `orq-ai-sdk`.
