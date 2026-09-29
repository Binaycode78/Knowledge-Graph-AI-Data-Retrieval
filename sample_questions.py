"""
sample_questions.py
-------------------
Runs 5 predefined Q&A pairs through the full retrieval pipeline
and saves results to results/sample_results.md

Run:
    python sample_questions.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.progress import track

from src.retrieval_system import RetrievalSystem

console = Console()

QUESTIONS = [
    "Which products from TechNova are supplied by FastShip Logistics?",
    "What are all products in the Electronics category and who supplies them?",
    "List all orders placed by Alice and their total value.",
    "Show me all products or nodes that contain the word banana.",
    "Which vendors supply products under ₹1500 in the Fashion category?",
]

RESULTS_DIR = Path("results")
RESULTS_FILE = RESULTS_DIR / "sample_results.md"


def format_result_md(index: int, result: dict) -> str:
    """Format a single Q&A result as markdown."""
    qp = result["query_plan"]
    query_type = qp.get("query_type", "N/A")
    reasoning = qp.get("reasoning", "N/A")
    params = qp.get("params", {})

    params_str = ", ".join(f"`{k}`: {v}" for k, v in params.items() if v)

    retrieved_preview = json.dumps(result["retrieved_data"], indent=2, ensure_ascii=False)
    # Truncate long output for readability
    if len(retrieved_preview) > 2000:
        retrieved_preview = retrieved_preview[:2000] + "\n  ... [truncated for brevity]"

    return f"""
## Question {index}: {result['question']}

### Query Plan (LLM Phase 1)
| Field | Value |
|-------|-------|
| Query Type | `{query_type}` |
| Parameters | {params_str or "none"} |
| Reasoning | {reasoning} |

### Retrieved Graph Data (Phase 2 Input)
```json
{retrieved_preview}
```

### Answer (LLM Phase 2 — grounded on graph data)
{result['answer']}

---
"""


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    console.print("\n[bold cyan]Initialising Knowledge Graph & AI Retrieval System...[/bold cyan]")
    system = RetrievalSystem()
    console.print("[bold green]Graph loaded![/bold green]\n")

    all_results = []

    for i, question in track(enumerate(QUESTIONS, 1), description="Running Q&A...", total=len(QUESTIONS)):
        console.print(f"\n[bold yellow]Q{i}:[/bold yellow] {question}")
        try:
            result = system.ask(question, verbose=False)
            all_results.append((i, result))
            console.print(f"[green]Done[/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            all_results.append((i, {
                "question": question,
                "query_plan": {},
                "retrieved_data": None,
                "answer": f"ERROR: {e}",
            }))

    # Build markdown output
    md_lines = [
        "# Knowledge Graph & AI Retrieval — Sample Q&A Results",
        "",
        f"> Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This document shows 5 sample questions run through the full pipeline:",
        "**User Question → LLM (query planning) → Graph Query → LLM (answer generation) → Final Answer**",
        "",
        "---",
    ]

    for i, result in all_results:
        md_lines.append(format_result_md(i, result))

    md_content = "\n".join(md_lines)
    RESULTS_FILE.write_text(md_content, encoding="utf-8")

    console.print(f"\n[bold green]Results saved to {RESULTS_FILE}[/bold green]")
    console.print("\n[bold]Answers preview:[/bold]")
    for i, result in all_results:
        console.print(f"\n[cyan]Q{i}:[/cyan] {result['question']}")
        console.print(f"[white]{result['answer'][:300]}...[/white]" if len(result['answer']) > 300 else f"[white]{result['answer']}[/white]")


if __name__ == "__main__":
    main()
