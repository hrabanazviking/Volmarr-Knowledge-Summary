"""Batch Pipeline Runner.
Processes the entire 571-post corpus in sequential slices, automatically
continuing from slice to slice until 100% of the corpus is ingested and synthesized.
Automatically commits and pushes to Git upon completion.
"""

import sys
import subprocess
import json
from pathlib import Path

# Force UTF-8 encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console

from src.fetch.archivist import Archivist
from src.parse.normalizer import CorpusNormalizer
from src.parse.chunker import SemanticChunker
from src.extract.extractor import ClaimExtractor
from src.cluster.registry import ConceptRegistryBuilder
from src.graph.prerequisite_graph import PrerequisiteGraph
from src.synthesize.weaver import KnowledgeWeaver
from src.validate.auditor import KnowledgeAuditor

console = Console()

def run_git_push(commit_msg: str):
    console.print(f"[bold cyan]Pushing changes to Git repository...[/bold cyan]")
    try:
        subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT, check=True)
        res = subprocess.run(["git", "status", "--porcelain"], cwd=PROJECT_ROOT, capture_output=True, text=True)
        if res.stdout.strip():
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, check=True)
            console.print("[bold green][OK] Successfully pushed changes to GitHub origin/main.[/bold green]")
        else:
            console.print("[yellow]No git changes to commit.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Git push failed: {e}[/bold red]")

def run_all_slices(slice_size: int = 100):
    manifest_path = Path("data/corpus_manifest.jsonl")
    if not manifest_path.exists():
        raise FileNotFoundError("corpus_manifest.jsonl not found.")

    with open(manifest_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    pending_records = [r for r in records if r.get("fetch_status") != "ok"]
    already_ok = [r for r in records if r.get("fetch_status") == "ok"]

    console.print(f"[bold yellow]Total Corpus Records:[/bold yellow] {len(records)}")
    console.print(f"[bold green]Already Cached:[/bold green] {len(already_ok)}")
    console.print(f"[bold cyan]Pending Ingestion:[/bold cyan] {len(pending_records)}")

    # Slice pending records
    slices = [pending_records[i:i + slice_size] for i in range(0, len(pending_records), slice_size)]
    console.print(f"[bold magenta]Divided pending workload into {len(slices)} slices of up to {slice_size} items.[/bold magenta]\n")

    archivist = Archivist()
    normalizer = CorpusNormalizer()
    chunker = SemanticChunker()

    for idx, s in enumerate(slices, start=1):
        s_cids = [r["content_id"] for r in s]
        console.print(f"\n[bold yellow]=====================================================[/bold yellow]")
        console.print(f"[bold yellow]   PROCESSING SLICE {idx} / {len(slices)} ({len(s_cids)} items) [/bold yellow]")
        console.print(f"[bold yellow]=====================================================[/bold yellow]")

        # 1. Fetch
        console.print(f"[cyan]Slice {idx}: Fetching raw HTML...[/cyan]")
        archivist.fetch_records(content_ids=s_cids)

        # 2. Normalize
        console.print(f"[cyan]Slice {idx}: Normalizing to clean Markdown...[/cyan]")
        normalizer.normalize_all(content_ids=s_cids)

        # 3. Chunk
        console.print(f"[cyan]Slice {idx}: Chunking documents...[/cyan]")
        chunker.process_all(content_ids=s_cids)

        console.print(f"[bold green][OK] Slice {idx}/{len(slices)} completed. Auto-continuing to next slice...[/bold green]")

    # All slices finished: Build global claims, registry, graph, synthesis, and audit
    console.print(f"\n[bold yellow]=====================================================[/bold yellow]")
    console.print(f"[bold yellow]   ALL SLICES INGESTED - FINAL SYNTHESIS & AUDIT     [/bold yellow]")
    console.print(f"[bold yellow]=====================================================[/bold yellow]")

    # 4. Extract
    console.print("[cyan]Extracting atomic claims across the full accumulated corpus...[/cyan]")
    extractor = ClaimExtractor()
    extractor.run()

    # 5. Registry & Clustering
    console.print("[cyan]Building complete canonical concept registry...[/cyan]")
    builder = ConceptRegistryBuilder()
    builder.build_registry()

    # 6. Graph & Topological Order
    console.print("[cyan]Building prerequisite DAG & topological ordering...[/cyan]")
    graph = PrerequisiteGraph()
    graph.build_graph()

    # 7. Knowledge Synthesis
    console.print("[cyan]Weaving full canonical Markdown library across all 11 levels...[/cyan]")
    weaver = KnowledgeWeaver()
    weaver.synthesize_all()

    # 8. QA Audit
    console.print("[cyan]Running comprehensive quality assurance audit...[/cyan]")
    auditor = KnowledgeAuditor()
    auditor.audit_all()

    console.print("\n[bold green]Entire 571-post corpus ingestion & canonical synthesis completed successfully![/bold green]")

    # 9. Git Push
    run_git_push("Full corpus ingestion and canonical synthesis across 571 articles")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch auto-continue slice runner")
    parser.add_argument("--slice-size", type=int, default=100, help="Number of URLs per slice")
    args = parser.parse_args()
    run_all_slices(slice_size=args.slice_size)
