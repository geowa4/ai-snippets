"""Summarizes each incident report."""

import logging
from os import getenv
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROMPT_PATH = Path("prompt")
REPORTS_DIR = Path("incident-reports")
SUMMARY_DIR = Path("incident-summaries")


agent = Agent(
    OpenAIModel(
        getenv("MODEL_NAME", "gemma-3-27b-it"),
    ),
    system_prompt=PROMPT_PATH.read_text(),
)


def summarize_reports(report_dir: Path, summary_dir: Path) -> None:
    """Summarizes all incident-reports."""
    if not report_dir.exists() or not report_dir.is_dir():
        logger.critical(
            "Directory %s does not exist or is not a directory.", report_dir
        )
        return
    summary_dir.mkdir(exist_ok=True)

    for file_path in report_dir.glob("*.md"):
        logger.info(f"Summarizing {file_path}")
        content = file_path.read_text()

        summary = agent.run_sync(content)

        summary_path = summary_dir / file_path.name
        summary_path.write_text(summary.output)


if __name__ == "__main__":
    summarize_reports(REPORTS_DIR, SUMMARY_DIR)
