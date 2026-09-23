"""Search and Retrieval CLI for Volmarr Knowledge Base.
Allows querying across canonical concepts, extracted atomic claims, and source provenance.
"""

import sys
import re
import json
import argparse
from pathlib import Path

# Force UTF-8 encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class KnowledgeSearch:
    def __init__(self, db_dir: str = "data/database", knowledge_dir: str = "knowledge"):
        self.db_dir = Path(db_dir)
        self.knowledge_dir = Path(knowledge_dir)
        self.registry_path = self.db_dir / "concept_registry.jsonl"
        self.claims_path = self.db_dir / "source_claims.jsonl"
        self.graph_path = self.db_dir / "prerequisite_graph.json"

        self.concepts = self._load_concepts()
        self.graph_order = self._load_graph_order()

    def _load_concepts(self) -> list[dict]:
        if not self.registry_path.exists():
            return []
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def _load_graph_order(self) -> dict[str, dict]:
        if not self.graph_path.exists():
            return {}
        with open(self.graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {item["slug"]: item for item in data.get("topological_reading_order", [])}

    def search(self, query: str, limit: int = 5):
        q = query.lower()
        q_tokens = set(re.findall(r"\w+", q))
        if not q_tokens:
            console.print("[yellow]Empty search query.[/yellow]")
            return

        console.print(f"\n[bold yellow]=====================================================[/bold yellow]")
        console.print(f"[bold yellow]   KNOWLEDGE SEARCH RESULTS: '{query}'[/bold yellow]")
        console.print(f"[bold yellow]=====================================================[/bold yellow]\n")

        # 1. Search Concepts
        matched_concepts = []
        for c in self.concepts:
            name_lower = c["canonical_name"].lower()
            def_lower = c["definition_short"].lower()
            score = 0
            if q in name_lower:
                score += 10
            if q in def_lower:
                score += 5
            for kw in c.get("prerequisites", []):
                if q in kw:
                    score += 3
            if score > 0:
                matched_concepts.append((score, c))

        matched_concepts.sort(key=lambda x: x[0], reverse=True)

        if matched_concepts:
            console.print("[bold cyan]>>> Canonical Concepts Found:[/bold cyan]")
            for _, c in matched_concepts[:limit]:
                g_info = self.graph_order.get(c["slug"], {})
                rank = g_info.get("rank", "?")
                prereqs = ", ".join(c.get("prerequisites", [])) or "None (Axiomatic)"
                panel_text = (
                    f"[bold white]{c['canonical_name']}[/bold white] [dim]({c['taxonomy_level']})[/dim] | Reading Order Rank: [bold green]#{rank}[/bold green]\n"
                    f"[italic]{c['definition_short']}[/italic]\n\n"
                    f"[dim]Prerequisites:[/dim] {prereqs}\n"
                    f"[dim]Total Sourced Claims:[/dim] {c.get('total_claims', 0)} across {c.get('source_articles_count', 0)} articles\n"
                    f"[dim]Canonical File:[/dim] [cyan]knowledge/{c['taxonomy_level']}/...[/cyan]"
                )
                console.print(Panel(panel_text, border_style="cyan"))

        # 2. Search Atomic Claims
        matched_claims = []
        if self.claims_path.exists():
            with open(self.claims_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        cl = json.loads(line)
                        stmt = cl.get("statement", "")
                        stmt_lower = stmt.lower()
                        c_name = cl.get("canonical_name", "").lower()
                        score = 0
                        if q in stmt_lower:
                            score += 5
                        if q in c_name:
                            score += 2
                        overlap = len(q_tokens & set(re.findall(r"\w+", stmt_lower)))
                        score += overlap
                        if score >= 3:
                            matched_claims.append((score, cl))

        matched_claims.sort(key=lambda x: x[0], reverse=True)

        if matched_claims:
            console.print("\n[bold cyan]>>> Extracted Sourced Claims:[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Concept", style="cyan", width=22)
            table.add_column("Statement", style="white")
            table.add_column("Epistemic Type", style="dim", width=18)
            table.add_column("Source", style="blue", width=30)

            for _, cl in matched_claims[:limit]:
                types_str = ", ".join(cl.get("knowledge_type", [])[:2])
                src_title = cl.get("article_title", "Source Article")
                table.add_row(
                    cl.get("canonical_name", "Unknown"),
                    cl.get("statement", "")[:140] + ("..." if len(cl.get("statement", "")) > 140 else ""),
                    types_str,
                    src_title[:28]
                )
            console.print(table)
        else:
            if not matched_concepts:
                console.print(f"[yellow]No exact matches found for '{query}'.[/yellow]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Volmarr Knowledge Base")
    parser.add_argument("query", type=str, nargs="?", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Max results to display")
    args = parser.parse_args()

    searcher = KnowledgeSearch()
    if args.query:
        searcher.search(args.query, limit=args.limit)
    else:
        console.print("[bold cyan]Interactive Knowledge Search Mode (type 'exit' or Ctrl+C to quit)[/bold cyan]")
        try:
            while True:
                q = console.input("\n[bold green]Enter search query:[/bold green] ").strip()
                if not q or q.lower() in ["exit", "quit", "q"]:
                    break
                searcher.search(q, limit=args.limit)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Search closed.[/dim]")
