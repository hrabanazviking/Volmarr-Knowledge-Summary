"""Unified CLI for the Volmarr Website Knowledge Synthesis Pipeline.
Allows running the entire end-to-end pipeline or any individual stage.
"""

import sys
import argparse
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

def run_pipeline(fetch_limit: int = None, fetch_ids: str = None):
    console.print("[bold yellow]=====================================================[/bold yellow]")
    console.print("[bold yellow]   VOLMARR WEBSITE KNOWLEDGE SYNTHESIS PIPELINE     [/bold yellow]")
    console.print("[bold yellow]=====================================================[/bold yellow]\n")

    # 1. Discover
    console.print("[bold cyan]>>> Stage 1: Site Discovery[/bold cyan]")
    crawler = SiteCrawler()
    crawler.discover()

    # 2. Fetch
    console.print("\n[bold cyan]>>> Stage 2: Raw Archive Fetch[/bold cyan]")
    archivist = Archivist()
    cids = [x.strip() for x in fetch_ids.split(",")] if fetch_ids else None
    archivist.fetch_records(content_ids=cids, limit=fetch_limit)

    # 3. Normalize
    console.print("\n[bold cyan]>>> Stage 3: HTML Boilerplate Stripping & Markdown Normalization[/bold cyan]")
    normalizer = CorpusNormalizer()
    normalizer.normalize_all(content_ids=cids)

    # 4. Chunk
    console.print("\n[bold cyan]>>> Stage 4: Structural Semantic Chunking[/bold cyan]")
    chunker = SemanticChunker()
    chunker.process_all(content_ids=cids)

    # 5. Extract
    console.print("\n[bold cyan]>>> Stage 5: Atomic Knowledge Claim Extraction[/bold cyan]")
    extractor = ClaimExtractor()
    extractor.run()

    # 6. Cluster & Registry
    console.print("\n[bold cyan]>>> Stage 6: Concept Registry & Deduplication[/bold cyan]")
    builder = ConceptRegistryBuilder()
    builder.build_registry()

    # 7. Graph & Ordering
    console.print("\n[bold cyan]>>> Stage 7: Prerequisite Dependency Graph & Topological Sort[/bold cyan]")
    graph = PrerequisiteGraph()
    graph.build_graph()

    # 8. Weave
    console.print("\n[bold cyan]>>> Stage 8: Canonical Knowledge Synthesis (Markdown)[/bold cyan]")
    weaver = KnowledgeWeaver()
    weaver.synthesize_all()

    # 9. Audit
    console.print("\n[bold cyan]>>> Stage 9: QA & Redundancy Audit[/bold cyan]")
    auditor = KnowledgeAuditor()
    auditor.audit_all()

    console.print("\n[bold green]Pipeline execution completed successfully![/bold green]")

def main():
    parser = argparse.ArgumentParser(description="Volmarr Knowledge Synthesis Pipeline")
    parser.add_argument("--all", action="store_true", help="Run the full pipeline end-to-end")
    parser.add_argument("--discover", action="store_true", help="Run site discovery")
    parser.add_argument("--fetch", action="store_true", help="Fetch raw HTML")
    parser.add_argument("--normalize", action="store_true", help="Normalize raw HTML to Markdown")
    parser.add_argument("--chunk", action="store_true", help="Run semantic chunking")
    parser.add_argument("--extract", action="store_true", help="Extract atomic claims")
    parser.add_argument("--registry", action="store_true", help="Build concept registry")
    parser.add_argument("--graph", action="store_true", help="Generate prerequisite graph")
    parser.add_argument("--weave", action="store_true", help="Synthesize canonical Markdown")
    parser.add_argument("--audit", action="store_true", help="Run quality assurance audit")
    parser.add_argument("--review", action="store_true", help="Display human review queue")
    parser.add_argument("--test", action="store_true", help="Run Phase 27 pytest evaluation suite")
    parser.add_argument("--build", action="store_true", help="Execute complete release packaging and build all assets")
    parser.add_argument("--export", action="store_true", help="Export AI companion memory pack for RAG")
    parser.add_argument("--loop", action="store_true", help="Run in continuous auto-continue watcher loop")
    parser.add_argument("--interval", type=int, default=300, help="Loop interval in seconds (default: 300)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of items to fetch/process")
    parser.add_argument("--ids", type=str, default=None, help="Comma-separated content IDs to process")

    args = parser.parse_args()

    if args.loop:
        from src.incremental_loop import IncrementalLoopEngine
        IncrementalLoopEngine(interval_seconds=args.interval).run_forever()
        return

    if len(sys.argv) == 1 or args.all:
        run_pipeline(fetch_limit=args.limit, fetch_ids=args.ids)
        return

    if args.discover:
        SiteCrawler().discover()
    if args.fetch:
        cids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        Archivist().fetch_records(content_ids=cids, limit=args.limit)
    if args.normalize:
        cids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        CorpusNormalizer().normalize_all(content_ids=cids)
    if args.chunk:
        cids = [x.strip() for x in args.ids.split(",")] if args.ids else None
        SemanticChunker().process_all(content_ids=cids)
    if args.extract:
        ClaimExtractor().run()
    if args.registry:
        ConceptRegistryBuilder().build_registry()
    if args.graph:
        PrerequisiteGraph().build_graph()
    if args.weave:
        KnowledgeWeaver().synthesize_all()
    if args.audit:
        KnowledgeAuditor().audit_all()
    if args.review:
        from src.validate.review_queue import ReviewQueueManager
        manager = ReviewQueueManager()
        manager.populate_initial_queue()
        manager.display_queue()
    if args.test:
        import pytest
        sys.exit(pytest.main(["-v", "tests"]))

if __name__ == "__main__":
    main()
