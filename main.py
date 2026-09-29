"""
main.py
-------
Interactive CLI for the Knowledge Graph & AI Retrieval System.

Run:
    python main.py
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.retrieval_system import RetrievalSystem

console = Console()

BANNER = """
+----------------------------------------------------------+
|    Knowledge Graph & AI Data Retrieval System            |
|         Powered by NetworkX + Groq LLM (Llama 3.3)       |
+----------------------------------------------------------+
"""

SAMPLE_QUESTIONS = [
    "Which products from TechNova are supplied by FastShip Logistics?",
    "What are all products in the Electronics category and who supplies them?",
    "List all orders placed by Alice and their total value.",
    "Show me all products that contain the word banana.",
    "Which vendors supply products under ₹1500 in the Fashion category?",
]


def print_banner():
    console.print(BANNER, style="bold cyan")


def print_graph_summary(system: RetrievalSystem):
    summary = system.get_summary()
    table = Table(title="Knowledge Graph Summary", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Nodes", str(summary["total_nodes"]))
    table.add_row("Total Edges", str(summary["total_edges"]))
    for nt, cnt in summary["node_types"].items():
        table.add_row(f"  {nt} nodes", str(cnt))
    console.print(table)
    console.print()


def print_answer(result: dict, verbose: bool = False):
    console.print()
    console.print(Panel(
        Text(result["question"], style="bold yellow"),
        title="Question",
        border_style="yellow",
    ))

    if verbose:
        console.print(Panel(
            Text(str(result["query_plan"]), style="dim"),
            title="Query Plan (LLM Phase 1)",
            border_style="dim",
        ))

    console.print(Panel(
        Text(result["answer"], style="white"),
        title="Answer (grounded on graph data)",
        border_style="green",
    ))
    console.print()


def run_interactive(system: RetrievalSystem, verbose: bool = False):
    console.print("[bold green]Type your question (or 'quit' to exit, 'demo' for sample questions):[/bold green]\n")

    while True:
        try:
            question = console.input("[bold cyan]>> [/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Exiting...[/yellow]")
            break

        if not question:
            continue

        if question.lower() in ("quit", "exit", "q"):
            console.print("[yellow]Goodbye![/yellow]")
            break

        if question.lower() == "demo":
            console.print("\n[bold magenta]Running 5 demo questions...[/bold magenta]\n")
            for i, q in enumerate(SAMPLE_QUESTIONS, 1):
                console.print(f"[bold blue]Question {i}:[/bold blue] {q}")
                try:
                    result = system.ask(q, verbose=verbose)
                    print_answer(result, verbose=verbose)
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
            continue

        if question.lower() == "schema":
            console.print(Panel(system.schema_info, title="Graph Schema", border_style="blue"))
            continue

        try:
            with console.status("[bold green]Querying Knowledge Graph...[/bold green]"):
                result = system.ask(question, verbose=verbose)
            print_answer(result, verbose=verbose)
        except Exception as e:
            console.print(f"[red]Error processing question: {e}[/red]")


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print_banner()

    console.print("[bold]Initialising Knowledge Graph...[/bold]")
    system = RetrievalSystem()
    console.print("[bold green]Graph loaded successfully![/bold green]\n")

    print_graph_summary(system)

    console.print("[dim]Commands: 'demo' (run 5 sample Q&As) | 'schema' (view graph schema) | 'quit' (exit)[/dim]")
    console.print("[dim]Use --verbose / -v flag for detailed pipeline output[/dim]\n")

    run_interactive(system, verbose=verbose)


if __name__ == "__main__":
    main()
