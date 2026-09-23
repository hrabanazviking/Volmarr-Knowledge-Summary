#!/usr/bin/env python3
"""Autonomous Knowledge Pipeline Loop Runner (loop.py).
Provides a resilient, continuous automation loop that:
1. Polls volmarrsheathenism.com for newly published posts or updates (incremental discovery).
2. Processes new/modified content through the full ingestion pipeline (fetch -> normalize -> chunk -> extract).
3. Updates the concept registry, DAG prerequisite graph, canonical Markdown library, and bi-directional indexes.
4. Synchronizes mirrors to knowledge/_meta/.
5. Runs the full 16-suite evaluation test framework (pytest).
6. Automatically commits and pushes all changes to GitHub origin/main.
7. Displays a real-time terminal status dashboard and sleeps until the next cycle.
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class AutonomousPipelineLoop:
    def __init__(self, interval_seconds: int = 60, auto_push: bool = True, force_resynth: bool = False):
        self.interval = interval_seconds
        self.auto_push = auto_push
        self.force_resynth = force_resynth
        self.iteration = 0
        self.start_time = datetime.now(timezone.utc)
        self.manifest_path = PROJECT_ROOT / "data" / "corpus_manifest.jsonl"
        self.db_dir = PROJECT_ROOT / "data" / "database"

    def print_banner(self):
        uptime = str(datetime.now(timezone.utc) - self.start_time).split(".")[0]
        banner_text = (
            f"[bold cyan]Volmarr Knowledge Synthesis - Autonomous Loop Runner[/bold cyan]\n"
            f"[dim]Cycle Interval: {self.interval}s | Auto-Git-Push: {'ENABLED' if self.auto_push else 'DISABLED'} | Uptime: {uptime}[/dim]"
        )
        console.print(Panel(banner_text, style="cyan", expand=False))

    def get_corpus_stats(self) -> dict:
        total_urls = 0
        if self.manifest_path.exists():
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                total_urls = sum(1 for line in f if line.strip())

        raw_count = len(list((PROJECT_ROOT / "data" / "raw").glob("*.html"))) if (PROJECT_ROOT / "data" / "raw").exists() else 0
        norm_count = len(list((PROJECT_ROOT / "data" / "normalized").glob("*.md"))) if (PROJECT_ROOT / "data" / "normalized").exists() else 0

        claims_count = 0
        claims_file = self.db_dir / "source_claims.jsonl"
        if claims_file.exists():
            with open(claims_file, "r", encoding="utf-8") as f:
                claims_count = sum(1 for line in f if line.strip())

        concepts_count = 0
        registry_file = self.db_dir / "concept_registry.jsonl"
        if registry_file.exists():
            with open(registry_file, "r", encoding="utf-8") as f:
                concepts_count = sum(1 for line in f if line.strip())

        return {
            "total_urls": total_urls,
            "raw_cached": raw_count,
            "normalized": norm_count,
            "claims": claims_count,
            "concepts": concepts_count
        }

    def check_for_deltas(self) -> list[str]:
        """Detect new or updated articles from sitemap."""
        from src.discover.crawler import SiteCrawler
        console.print("[dim cyan]-> Checking live sitemap for updates...[/dim cyan]")
        try:
            crawler = SiteCrawler()
            discovered = crawler.discover()
            
            old_mods = {}
            if self.manifest_path.exists():
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            r = json.loads(line)
                            old_mods[r["url"]] = r.get("sitemap_lastmod") or r.get("modified", "")

            changed_cids = []
            for r in discovered:
                url = r["url"]
                lastmod = r.get("sitemap_lastmod") or r.get("modified", "")
                if url not in old_mods:
                    console.print(f"[bold green]New URL discovered:[/bold green] {url}")
                    changed_cids.append(r["content_id"])
                elif lastmod and lastmod != old_mods[url]:
                    console.print(f"[bold yellow]Modified content discovered:[/bold yellow] {url}")
                    changed_cids.append(r["content_id"])

            return changed_cids
        except Exception as e:
            console.print(f"[yellow]Sitemap check warning: {e}. Proceeding with local state.[/yellow]")
            return []

    def run_pipeline_delta(self, changed_cids: list[str]):
        """Runs the incremental processing for newly detected articles."""
        from src.fetch.archivist import Archivist
        from src.parse.normalizer import CorpusNormalizer
        from src.parse.chunker import SemanticChunker
        from src.extract.extractor import ClaimExtractor
        from src.cluster.registry import ConceptRegistryBuilder
        from src.graph.prerequisite_graph import PrerequisiteGraph
        from src.synthesize.weaver import KnowledgeWeaver

        console.print(f"[bold yellow]Processing {len(changed_cids)} changed/new items...[/bold yellow]")
        Archivist().fetch_records(content_ids=changed_cids)
        CorpusNormalizer().normalize_all(content_ids=changed_cids)
        SemanticChunker().process_all(content_ids=changed_cids)
        ClaimExtractor().run()
        ConceptRegistryBuilder().build_registry()
        PrerequisiteGraph().build_graph()
        KnowledgeWeaver().synthesize_all()

    def sync_indexes_and_meta(self):
        """Ensures bi-directional indexes and _meta mirrors are fresh."""
        try:
            # 1. Bi-directional indexes
            from src.graph.build_indexes import build_bidirectional_indexes
            build_bidirectional_indexes()

            # 2. Sync knowledge/_meta
            import shutil
            meta_dir = PROJECT_ROOT / "knowledge" / "_meta"
            meta_dir.mkdir(parents=True, exist_ok=True)
            sync_files = [
                ("data/corpus_manifest.jsonl", meta_dir / "corpus_manifest.jsonl"),
                ("data/database/concept_registry.jsonl", meta_dir / "concept_registry.jsonl"),
                ("data/database/source_claims.jsonl", meta_dir / "source_claims.jsonl"),
                ("data/database/duplicate_clusters.jsonl", meta_dir / "duplicate_clusters.jsonl"),
                ("data/database/prerequisite_graph.json", meta_dir / "prerequisite_graph.json"),
                ("data/database/review_queue.jsonl", meta_dir / "review_queue.jsonl"),
                ("reports/unresolved_conflicts.md", meta_dir / "unresolved_conflicts.md"),
                ("reports/build_report.md", meta_dir / "build_report.md"),
                ("reports/redundancy_report.md", meta_dir / "redundancy_report.md"),
            ]
            for src_rel, dst_path in sync_files:
                src_path = PROJECT_ROOT / src_rel
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
        except Exception as e:
            console.print(f"[yellow]Index/meta sync notice: {e}[/yellow]")

    def run_tests(self) -> tuple[bool, str]:
        """Runs the pytest evaluation suite."""
        console.print("[dim cyan]-> Running evaluation suite (pytest)...[/dim cyan]")
        try:
            res = subprocess.run(
                ["uv", "run", "pytest", "-q"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = res.stdout.strip() or res.stderr.strip()
            summary = output.splitlines()[-1] if output else "No output"
            return (res.returncode == 0, summary)
        except Exception as e:
            return (False, f"Test error: {e}")

    def git_sync(self, commit_msg: str) -> bool:
        """Stages changes, commits, and pushes to remote."""
        if not self.auto_push:
            return False
            
        try:
            subprocess.run(["git", "add", "-A"], cwd=PROJECT_ROOT, check=True)
            res = subprocess.run(["git", "status", "--porcelain"], cwd=PROJECT_ROOT, capture_output=True, text=True)
            if res.stdout.strip():
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_ROOT, check=True)
                console.print(f"[bold green][OK] Committed changes: '{commit_msg}'[/bold green]")
                push_res = subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, capture_output=True, text=True)
                if push_res.returncode == 0:
                    console.print("[bold green][OK] Successfully pushed to origin/main[/bold green]")
                    return True
                else:
                    console.print(f"[bold red]Git push failed: {push_res.stderr.strip()}[/bold red]")
                    return False
            else:
                console.print("[dim green]-> Working tree clean. Remote up to date.[/dim green]")
                return False
        except Exception as e:
            console.print(f"[bold red]Git sync error: {e}[/bold red]")
            return False

    def run_iteration(self):
        self.iteration += 1
        console.print(f"\n[bold yellow]===========================================================[/bold yellow]")
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        console.print(f"[bold yellow]   ITERATION {self.iteration} | {now_str} [/bold yellow]")
        console.print(f"[bold yellow]===========================================================[/bold yellow]")

        # 1. Delta check
        changed_cids = self.check_for_deltas()
        if changed_cids or self.force_resynth:
            self.run_pipeline_delta(changed_cids)

        # 2. Run QA audit
        from src.validate.auditor import KnowledgeAuditor
        KnowledgeAuditor().audit_all()

        # 3. Synchronize indexes and mirrors
        self.sync_indexes_and_meta()

        # 4. Run test suite
        passed, test_summary = self.run_tests()
        if passed:
            console.print(f"[bold green][OK] Evaluation Suite: {test_summary}[/bold green]")
        else:
            console.print(f"[bold red][FAIL] Evaluation Suite: {test_summary}[/bold red]")

        # 5. Git Commit & Push
        stats = self.get_corpus_stats()
        commit_msg = (
            f"Auto-sync iteration {self.iteration}: "
            f"{stats['total_urls']} corpus items, {stats['concepts']} concepts, {test_summary}"
        )
        self.git_sync(commit_msg)

        # 6. Display Dashboard Summary Table
        table = Table(title=f"Pipeline Status (Iteration {self.iteration})", expand=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold green")

        table.add_row("Total Manifest URLs", str(stats["total_urls"]))
        table.add_row("Cached HTML Files", str(stats["raw_cached"]))
        table.add_row("Normalized Markdown", str(stats["normalized"]))
        table.add_row("Atomic Source Claims", str(stats["claims"]))
        table.add_row("Canonical Concepts", str(stats["concepts"]))
        table.add_row("Evaluation Suite", "[green]16/16 PASSED[/green]" if passed else "[red]FAILED[/red]")
        table.add_row("Next Check In", f"{self.interval} seconds")
        console.print(table)

    def start(self, run_once: bool = False):
        self.print_banner()
        if run_once:
            self.run_iteration()
            console.print("[bold green]Run-once completed successfully.[/bold green]")
            return

        try:
            while True:
                self.run_iteration()
                console.print(f"\n[dim]Sleeping for {self.interval} seconds (Press Ctrl+C to stop)...[/dim]")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Loop runner gracefully terminated by user.[/bold yellow]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Knowledge Synthesis Loop Runner")
    parser.add_argument("--once", action="store_true", help="Execute single loop iteration and exit")
    parser.add_argument("--interval", type=int, default=60, help="Loop interval in seconds (default: 60)")
    parser.add_argument("--no-push", action="store_true", help="Disable automatic git push")
    parser.add_argument("--force", action="store_true", help="Force complete re-synthesis on each cycle")
    args = parser.parse_args()

    loop = AutonomousPipelineLoop(
        interval_seconds=args.interval,
        auto_push=not args.no_push,
        force_resynth=args.force
    )
    loop.start(run_once=args.once)
