from datetime import datetime
from pathlib import Path

import ollama, os

EVIDENCE_DIR = Path("evidence")
RUNBOOK_PATH = Path("ir_runbook.md")
REPORTS_DIR = Path("reports")
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """You are a senior SOC analyst conducting ransomware incident triage.
Analyze the provided evidence logs and incident-response runbook.
Respond ONLY with a Markdown incident report."""

USER_PROMPT_TEMPLATE = """Review the evidence logs and IR runbook below, then produce a Markdown incident report with these sections:

1. **Summary** — executive overview of the incident
2. **Timeline** — chronological key events derived from the logs
3. **Root Cause** — likely entry vector and patient zero
4. **MITRE ATT&CK Mapping** — for each finding, list tactic, technique name, and technique ID (e.g., T1110)
5. **Runbook Steps: Completed vs. Missed** — compare observed evidence against the runbook checklist
6. **Recommended Next Actions** — prioritized follow-up steps

--- EVIDENCE LOGS ---
{evidence}

--- IR RUNBOOK ---
{runbook}
"""


def read_evidence_logs(evidence_dir: Path) -> str:
    """Step 1: Read every log file in the evidence/ folder."""
    sections = []
    for path in sorted(evidence_dir.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        sections.append(f"### {path.name}\n{path.read_text(encoding='utf-8').strip()}")
    return "\n\n".join(sections)


def read_runbook(runbook_path: Path) -> str:
    """Step 2: Read the incident-response runbook."""
    return runbook_path.read_text(encoding="utf-8")


def generate_report(evidence: str, runbook: str) -> str:
    """Step 3: Send evidence and runbook to the local Llama 3.2 model via Ollama."""
    user_prompt = USER_PROMPT_TEMPLATE.format(evidence=evidence, runbook=runbook)
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response["message"]["content"]


def write_report(report: str, reports_dir: Path) -> Path:
    """Step 4: Ensure reports/ exists and write a timestamped Markdown file."""
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_path = reports_dir / f"report_{timestamp}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> None:
    evidence = read_evidence_logs(EVIDENCE_DIR)
    runbook = read_runbook(RUNBOOK_PATH)
    report = generate_report(evidence, runbook)
    output_path = write_report(report, REPORTS_DIR)
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
