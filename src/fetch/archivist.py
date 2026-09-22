"""Archivist module for fetching and storing raw HTML sources.
Implements concurrent async fetching with semaphore throttling, retries, incremental caching,
and real-time manifest updates.
"""

import json
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import httpx
import yaml
from rich.console import Console

console = Console()

class Archivist:
    def __init__(self, config_path: str = "config/site.yaml", manifest_path: str = "data/corpus_manifest.jsonl", raw_dir: str = "data/raw"):
        self.config_path = Path(config_path)
        self.manifest_path = Path(manifest_path)
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
            
        self.rate_limit = self.config.get("crawl", {}).get("rate_limit_seconds", 0.2)
        self.timeout = self.config.get("crawl", {}).get("timeout_seconds", 20.0)
        self.max_concurrency = 5
        self.client_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VolmarrKnowledgeArchivist/1.0"
        }

    def load_manifest(self) -> list[dict]:
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found at {self.manifest_path}. Run discovery crawler first.")
        records = []
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def save_manifest(self, records: list[dict]):
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    async def _fetch_single(self, client: httpx.AsyncClient, semaphore: asyncio.Semaphore, record: dict, stats: dict):
        cid = record["content_id"]
        url = record["url"]
        raw_file = self.raw_dir / f"{cid}.html"

        # Check if already downloaded
        if raw_file.exists() and record.get("content_hash") and record.get("fetch_status") == "ok":
            stats["skipped"] += 1
            return

        async with semaphore:
            for attempt in range(1, 3):
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    html_bytes = resp.content
                    content_hash = "sha256:" + hashlib.sha256(html_bytes).hexdigest()

                    with open(raw_file, "wb") as f:
                        f.write(html_bytes)

                    record["content_hash"] = content_hash
                    record["fetch_status"] = "ok"
                    record["fetched_at"] = datetime.now(timezone.utc).isoformat()
                    stats["updated"] += 1
                    
                    if stats["updated"] % 25 == 0:
                        console.print(f"[cyan]Fetched {stats['updated']} / {stats['total']} items...[/cyan]")
                    
                    await asyncio.sleep(self.rate_limit)
                    return
                except Exception as e:
                    if attempt == 2:
                        console.print(f"[bold red]Failed fetching {url} after 2 attempts: {e}[/bold red]")
                        record["fetch_status"] = f"error: {str(e)}"
                        stats["failed"] += 1
                    else:
                        await asyncio.sleep(1.0)

    async def fetch_async(self, target_records: list[dict]) -> list[dict]:
        semaphore = asyncio.Semaphore(self.max_concurrency)
        stats = {"updated": 0, "skipped": 0, "failed": 0, "total": len(target_records)}

        limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
        async with httpx.AsyncClient(headers=self.client_headers, timeout=self.timeout, follow_redirects=True, limits=limits) as client:
            tasks = [self._fetch_single(client, semaphore, r, stats) for r in target_records]
            await asyncio.gather(*tasks)

        console.print(f"[bold green]Fetch completed.[/bold green] Updated: {stats['updated']}, Skipped: {stats['skipped']}, Failed: {stats['failed']}")
        return target_records

    def fetch_records(self, content_ids: list[str] = None, limit: int = None, content_types: list[str] = None) -> list[dict]:
        records = self.load_manifest()
        record_map = {r["content_id"]: r for r in records}

        target_records = []
        for r in records:
            if content_ids and r["content_id"] not in content_ids:
                continue
            if content_types and r["content_type"] not in content_types:
                continue
            target_records.append(r)
            if limit and len(target_records) >= limit:
                break

        console.print(f"[bold cyan]Archivist starting concurrent fetch for {len(target_records)} target items...[/bold cyan]")
        asyncio.run(self.fetch_async(target_records))

        # Update manifest
        for tr in target_records:
            record_map[tr["content_id"]] = tr
        self.save_manifest(list(record_map.values()))
        return target_records

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and store raw HTML from manifest")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of items to fetch")
    parser.add_argument("--ids", type=str, default=None, help="Comma-separated list of content_ids to fetch")
    parser.add_argument("--type", type=str, default=None, help="Comma-separated content types (post,page)")
    args = parser.parse_args()

    cids = [x.strip() for x in args.ids.split(",")] if args.ids else None
    ctypes = [x.strip() for x in args.type.split(",")] if args.type else None

    archivist = Archivist()
    archivist.fetch_records(content_ids=cids, limit=args.limit, content_types=ctypes)
