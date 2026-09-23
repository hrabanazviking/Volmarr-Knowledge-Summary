"""Crawler and site discovery module.
Discovers all canonical URLs from sitemap.xml and feeds, outputs corpus_manifest.jsonl and discovery_report.md.
"""

import json
import re
import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import httpx
import yaml
from rich.console import Console

console = Console()

class SiteCrawler:
    def __init__(self, config_path: str = "config/site.yaml", exclusions_path: str = "config/exclusions.txt"):
        self.config_path = Path(config_path)
        self.exclusions_path = Path(exclusions_path)
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
            
        self.exclusions = []
        if self.exclusions_path.exists():
            with open(self.exclusions_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.exclusions.append(line)

    @staticmethod
    def generate_content_id(url: str) -> str:
        """Generate a clean, stable content ID based on the URL path."""
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.strip("/")
        if not path:
            return "page_home"
        
        # If standard date pattern: 2026/09/22/slug
        date_match = re.match(r"^(\d{4})/(\d{2})/(\d{2})/(.+)$", path)
        if date_match:
            year, month, day, slug = date_match.groups()
            clean_slug = re.sub(r"[^a-zA-Z0-9_\-]+", "_", slug).strip("_")
            return f"post_{year}_{month}_{day}_{clean_slug}"
        
        # Static page
        clean_page = re.sub(r"[^a-zA-Z0-9_\-]+", "_", path).strip("_")
        return f"page_{clean_page}"

    def is_excluded(self, url: str) -> bool:
        """Check if URL matches any exclusion pattern."""
        for pattern in self.exclusions:
            if pattern in url:
                return True
        return False

    def discover(self, output_manifest: str = "data/corpus_manifest.jsonl", report_path: str = "reports/discovery_report.md") -> list[dict]:
        sitemap_url = self.config["site"]["sitemap_url"]
        console.print(f"[bold blue]Fetching sitemap from:[/bold blue] {sitemap_url}")
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VolmarrKnowledgeSynth/1.0"}
        resp = httpx.get(sitemap_url, headers=headers, timeout=30.0, follow_redirects=True)
        resp.raise_for_status()
        
        root = ET.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        
        raw_entries = root.findall("sm:url", ns)
        console.print(f"Found [green]{len(raw_entries)}[/green] raw sitemap URL elements.")
        
        # Load existing manifest if present to preserve metadata and status
        existing_records = {}
        out_file = Path(output_manifest)
        if out_file.exists():
            try:
                with open(out_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            rec = json.loads(line)
                            existing_records[rec["url"]] = rec
            except Exception as e:
                console.print(f"[yellow]Could not read existing manifest: {e}[/yellow]")

        canonical_records = {}
        excluded_urls = []
        
        for elem in raw_entries:
            loc = elem.find("sm:loc", ns)
            if loc is None or not loc.text:
                continue
            url = loc.text.strip()
            
            # Skip if excluded
            if self.is_excluded(url):
                excluded_urls.append(url)
                continue
                
            lastmod = elem.find("sm:lastmod", ns)
            lastmod_str = lastmod.text.strip() if (lastmod is not None and lastmod.text) else ""
            
            parsed = urllib.parse.urlparse(url)
            path = parsed.path.strip("/")
            
            # Determine content type
            if not path:
                content_type = "home"
            elif re.match(r"^\d{4}/\d{2}/\d{2}/.+", path):
                content_type = "post"
            else:
                content_type = "page"
                
            content_id = self.generate_content_id(url)
            
            if url in existing_records:
                record = existing_records[url]
                record["sitemap_lastmod"] = lastmod_str
            else:
                record = {
                    "content_id": content_id,
                    "url": url,
                    "canonical_url": url,
                    "content_type": content_type,
                    "modified": lastmod_str,
                    "sitemap_lastmod": lastmod_str,
                    "published": lastmod_str,  # Will be refined during fetch/parse from HTML
                    "author": "Volmarr",       # Default, will be extracted during parsing
                    "title": "",               # Extracted during parsing
                    "categories": [],
                    "tags": [],
                    "content_hash": "",
                    "normalized_hash": "",
                    "discovered_from": ["sitemap.xml"],
                    "fetch_status": "pending",
                    "extracted_at": None
                }
            canonical_records[url] = record

        records_list = list(canonical_records.values())
        
        # Sort by date/url
        records_list.sort(key=lambda r: (r.get("modified") or "", r["url"]), reverse=True)
        
        # Save to JSONL
        out_file = Path(output_manifest)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            for rec in records_list:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                
        console.print(f"[bold green]Saved {len(records_list)} canonical records to {output_manifest}[/bold green]")
        
        # Generate Discovery Report
        posts = [r for r in records_list if r["content_type"] == "post"]
        pages = [r for r in records_list if r["content_type"] == "page"]
        home = [r for r in records_list if r["content_type"] == "home"]
        
        dates = [r["modified"] for r in records_list if r["modified"]]
        dates.sort()
        oldest_pub = dates[0] if dates else "Unknown"
        newest_pub = dates[-1] if dates else "Unknown"
        
        rep_file = Path(report_path)
        rep_file.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_file, "w", encoding="utf-8") as f:
            f.write("# Corpus Discovery Report\n\n")
            f.write(f"Generated on: {datetime.utcnow().isoformat()}Z\n\n")
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Total Canonical URLs:** {len(records_list)}\n")
            f.write(f"- **Total Canonical Posts:** {len(posts)}\n")
            f.write(f"- **Total Static Pages:** {len(pages)}\n")
            f.write(f"- **Home / Root Page:** {len(home)}\n")
            f.write(f"- **Total Excluded Entries:** {len(excluded_urls)}\n")
            f.write(f"- **Oldest Recorded Date:** `{oldest_pub}`\n")
            f.write(f"- **Newest Recorded Date:** `{newest_pub}`\n\n")
            f.write("## Static Pages Discovered\n\n")
            for p in pages:
                f.write(f"- [`{p['content_id']}`]({p['url']}) (modified: {p['modified']})\n")
                
        console.print(f"[bold green]Discovery report written to {report_path}[/bold green]")
        return records_list

if __name__ == "__main__":
    crawler = SiteCrawler()
    crawler.discover()
