"""Incremental Update Engine and Auto-Continue Daemon Loop.
Continuously or periodically polls volmarrsheathenism.com for newly published posts or updates,
processes delta changes, updates the canonical knowledge base, runs audits, and pushes to Git.
"""

import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

# Windows UTF-8 safety
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
from src.discover.crawler import SiteCrawler
from src.fetch.archivist import Archivist
from src.parse.normalizer import CorpusNormalizer
from src.parse.chunker import SemanticChunker
from src.extract.extractor import ClaimExtractor
from src.cluster.registry import ConceptRegistryBuilder
from src.graph.prerequisite_graph import PrerequisiteGraph
from src.synthesize.weaver import KnowledgeWeaver
from src.validate.auditor import KnowledgeAuditor

console = Console()

class IncrementalLoopEngine:
    def __init__(self, interval_seconds: int = 300):
        self.interval = interval_seconds
        self.manifest_path = Path("data/corpus_manifest.jsonl")

    def git_commit_and_push(self, message: str) -> bool:
        console.print("[bold cyan]Checking Git working tree for changes...[/bold cyan]")
        try:
            subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT, check=True)
            res = subprocess.run(["git", "status", "--porcelain"], cwd=PROJECT_ROOT, capture_output=True, text=True)
            if res.stdout.strip():
                subprocess.run(["git", "commit", "-m", message], cwd=PROJECT_ROOT, check=True)
                subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, check=True)
                console.print(f"[bold green][OK] Committed & pushed: '{message}'[/bold green]")
                return True
            else:
                console.print("[dim]No file changes to commit.[/dim]")
                return False
        except Exception as e:
            console.print(f"[bold red]Git push failed: {e}[/bold red]")
            return False

    def load_existing_sitemap_lastmods(self) -> dict[str, str]:
        if not self.manifest_path.exists():
            return {}
        sitemap_mods = {}
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    sitemap_mods[r["url"]] = r.get("sitemap_lastmod") or r.get("modified", "")
        return sitemap_mods

    def check_for_updates(self) -> list[str]:
        """Check sitemap against stored manifest to identify new or modified URLs."""
        console.print(f"\n[cyan][{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] Checking site for updates...[/cyan]")
        old_mods = self.load_existing_sitemap_lastmods()
        
        crawler = SiteCrawler()
        discovered = crawler.discover()

        changed_cids = []
        for r in discovered:
            url = r["url"]
            lastmod = r.get("sitemap_lastmod") or r.get("modified", "")
            if url not in old_mods:
                console.print(f"[green]New URL detected:[/green] {url}")
                changed_cids.append(r["content_id"])
            elif lastmod and lastmod != old_mods[url]:
                console.print(f"[yellow]Modified content detected:[/yellow] {url} (new: {lastmod} vs old: {old_mods[url]})")
                changed_cids.append(r["content_id"])

        return changed_cids

    def process_delta(self, changed_cids: list[str]):
        console.print(f"[bold yellow]Processing delta update for {len(changed_cids)} changed/new items...[/bold yellow]")
        
        # 1. Fetch changed items
        Archivist().fetch_records(content_ids=changed_cids)

        # 2. Normalize changed items
        CorpusNormalizer().normalize_all(content_ids=changed_cids)

        # 3. Chunk changed items
        SemanticChunker().process_all(content_ids=changed_cids)

        # 4. Extract claims across accumulated corpus
        ClaimExtractor().run()

        # 5. Registry & Clustering
        ConceptRegistryBuilder().build_registry()

        # 6. Graph & Order
        PrerequisiteGraph().build_graph()

        # 7. Synthesize Canonical Markdown
        KnowledgeWeaver().synthesize_all()

        # 8. QA Audit
        KnowledgeAuditor().audit_all()

        # 9. Commit & Push
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self.git_commit_and_push(f"Incremental update: {len(changed_cids)} posts updated ({now_str} UTC)")

    def run_once(self) -> bool:
        changed_cids = self.check_for_updates()
        if changed_cids:
            self.process_delta(changed_cids)
            return True
        else:
            console.print("[dim green]Site is fully up to date. No new posts detected.[/dim green]")
            return False

    def run_forever(self):
        console.print(f"[bold green]Starting continuous auto-continue loop (poll interval: {self.interval}s)...[/bold green]")
        console.print("[dim]Press Ctrl+C to terminate.[/dim]\n")
        try:
            while True:
                self.run_once()
                console.print(f"[dim]Sleeping for {self.interval} seconds until next check...[/dim]")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            console.print("\n[yellow]Continuous loop stopped by user.[/yellow]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Incremental Update Engine and Auto-Continue Loop")
    parser.add_argument("--once", action="store_true", help="Run a single incremental check and exit")
    parser.add_argument("--interval", type=int, default=300, help="Loop interval in seconds (default: 300)")
    args = parser.parse_args()

    engine = IncrementalLoopEngine(interval_seconds=args.interval)
    if args.once:
        engine.run_once()
    else:
        engine.run_forever()
