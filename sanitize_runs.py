"""Publish sanitized red-team run data.

`.evaluatorq/runs/` is gitignored and carries internal orq handles
(experiment_url on my.orq.ai, evaluator/deployment/workspace IDs). This copies
the public Clarabelle-cow runs into a tracked `data/redteam-runs/` with those
handles redacted. Attack prompts, agent responses, verdicts, and token counts
are kept — that's the data people come to see.
"""

from __future__ import annotations

import json
from pathlib import Path

SRC = Path(__file__).parent / ".evaluatorq" / "runs"
OUT = Path(__file__).parent / "data" / "redteam-runs"

# Only the public cow demo; skip the unrelated HAL/JARVIS workshop runs.
INCLUDE_AGENT = "clarabelle-cow"
REDACT_KEYS = {
    "experiment_url", "evaluator_id", "deployment_id", "deployment_version_id",
    "workspace", "workspace_id", "project_id", "dataset_id", "trace_id", "span_id",
}
REDACT = "[redacted]"


def scrub(o):
    if isinstance(o, dict):
        return {k: (REDACT if k in REDACT_KEYS else scrub(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub(v) for v in o]
    if isinstance(o, str) and "my.orq.ai" in o:
        return REDACT
    return o


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    kept = 0
    for f in sorted(SRC.glob("*.json")):
        d = json.load(f.open())
        if INCLUDE_AGENT not in (d.get("tested_agents") or []):
            continue
        (OUT / f.name).write_text(json.dumps(scrub(d), indent=2))
        kept += 1
    # fail loud if a handle slipped through
    blob = "\n".join(p.read_text() for p in OUT.glob("*.json"))
    bad = [s for s in ("my.orq.ai", "orq-research", "01KFTGH3A3ZEQBY4JH0RHTAQYN") if s in blob]
    assert not bad, f"leak survived sanitization: {bad}"
    print(f"-> {OUT}: {kept} cow runs sanitized, 0 internal handles remain")


if __name__ == "__main__":
    main()
