"""Create/update the orq Hugging Face Space that hosts the Clarabelle report UI.

Uses the cached HF token (`huggingface-cli login` already done). Run:
    uv run python hf-space/deploy_space.py
"""

from __future__ import annotations

from pathlib import Path

from huggingface_hub import HfApi, create_repo

REPO_ID = "orq/clarabelle-redteam"
HERE = Path(__file__).parent


def main() -> None:
    create_repo(REPO_ID, repo_type="space", space_sdk="docker", exist_ok=True)
    api = HfApi()
    api.upload_folder(
        folder_path=str(HERE),
        repo_id=REPO_ID,
        repo_type="space",
        ignore_patterns=["deploy_space.py", "__pycache__/*", "*.pyc"],
        commit_message="Deploy Clarabelle red-team report dashboard",
    )
    print(f"-> https://huggingface.co/spaces/{REPO_ID}")


if __name__ == "__main__":
    main()
