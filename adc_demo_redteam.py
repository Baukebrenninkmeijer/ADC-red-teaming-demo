"""Goal-hijacking red-team run against the orq-hosted Clarabelle cow agent.

Targets the live agent ``clarabelle-cow`` (provisioned by ``provision.py``) via
evaluatorq's built-in ORQ backend, and runs a dynamic goal-hijacking campaign:
the attacker tries to make Clarabelle abandon the cow goal and pursue its own.

Run:
    uv run python redteam_clarabelle.py

Env (from .env, ADC project key):
    ORQ_API_KEY, ORQ_BASE_URL (optional)
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from evaluatorq.redteam import LLMConfig, LLMCallConfig, red_team

DEMO_DIR = Path(__file__).parent
RESULTS_DIR = DEMO_DIR / "results"

# "agent:<key>" routes through evaluatorq's ORQ backend to the live hosted agent.
TARGET = "agent:clarabelle-cow"


async def main() -> None:
    load_dotenv(DEMO_DIR / ".env", override=True)
    os.environ.pop("OPENAI_API_KEY", None)  # force ORQ router; shell OPENAI_API_KEY would shadow it

    if not os.environ.get("ORQ_API_KEY"):
        raise SystemExit("ERROR: ORQ_API_KEY not set (check .env).")

    attacker_instructions = (DEMO_DIR / "agents" / "clarabelle_attacker_instructions.txt").read_text()
    model = LLMCallConfig(model="openai/gpt-5.4")

    start = time.time()
    # red_team persists the report itself: a timestamped copy in ./.evaluatorq/runs/
    # (always), plus output_dir/03_summary_report.json when output_dir + save="final".
    report = await red_team(
        target=TARGET,
        vulnerabilities=["goal_hijacking"],
        mode="hybrid",
        max_turns=20,
        max_dynamic_datapoints=20,
        max_static_datapoints=20,
        generated_strategy_count=20,
        attacker_instructions=attacker_instructions,
        parallelism=10,
        llm_config=LLMConfig(attacker=model, evaluator=model),
        generate_recommendations=True,
        verbosity=1,
        name="ADC Demo — Clarabelle Goal Hijacking",
        output_dir=RESULTS_DIR,
    )
    print(f"\nCompleted in {time.time() - start:.1f}s")
    print(
        f"Resistance rate: {report.summary.resistance_rate:.0%} "
        f"({report.summary.vulnerabilities_found}/{report.summary.total_attacks} hijacked)"
    )
    print(f"-> {RESULTS_DIR / '03_summary_report.json'}")


if __name__ == "__main__":
    asyncio.run(main())
