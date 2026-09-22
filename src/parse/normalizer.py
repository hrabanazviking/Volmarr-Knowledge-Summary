"""Normalizer module for stripping WordPress boilerplate and converting articles to clean Markdown.
Preserves Unicode (Old Norse, runes), extracts metadata (dates, authors, tags), and formats YAML frontmatter.
"""

import re
import json
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md
from rich.console import Console

console = Console()

class CorpusNormalizer:
    def __init__(self, raw_dir: str = "data/raw", normalized_dir: str = "data/normalized", manifest_path: str = "data/corpus_manifest.jsonl"):
        self.raw_dir = Path(raw_dir)
        self.normalized_dir = Path(normalized_dir)
        self.manifest_path = Path(manifest_path)
        self.normalized_dir.mkdir(parents=True, exist_ok=True)

    def load_manifest(self) -> list[dict]:
        records = []
        if self.manifest_path.exists():
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

    @staticmethod
    def classify_author(author_name: str) -> str:
        """Classify author as site_owner, guest, persona, or ai_collaborator."""
        name_lower = author_name.lower()
        if "volmarr" in name_lower:
            return "site_owner"
        ai_collaborators = ["astrid", "eirynth", "caducea", "liv vaelen", "véyrúnn", "veyrunn", "chatgpt", "claude"]
        for ai in ai_collaborators:
            if ai in name_lower:
                return "ai_collaborator"
        return "guest"

    def clean_html(self, html_content: bytes) -> tuple[dict, str]:
        soup = BeautifulSoup(html_content, "lxml")
        
        # 1. Extract metadata from head
        meta_title = ""
        published = ""
        modified = ""
        
        for m in soup.find_all("meta"):
            prop = m.get("property") or m.get("name") or ""
            content = m.get("content") or ""
            if prop == "og:title" and not meta_title:
                meta_title = content.strip()
            elif prop == "article:published_time" and not published:
                published = content.strip()
            elif prop == "article:modified_time" and not modified:
                modified = content.strip()
                
        # 2. Locate main content
        post_div = soup.find("div", class_=lambda c: c and "post" in c.split())
        title = ""
        if post_div:
            h_tag = post_div.find(["h1", "h2", "h3"])
            if h_tag:
                title = h_tag.get_text(strip=True)
                
        if not title:
            title = meta_title or (soup.title.string.split("•")[0].split("–")[0].split("|")[0].strip() if soup.title else "Untitled")

        # Extract categories & tags from post-meta
        categories = []
        tags = []
        author = "Volmarr"
        
        # Check title / content for collaborator signatures
        title_lower = title.lower()
        if "caducea" in title_lower:
            author = "Caducea"
        elif "astrid" in title_lower:
            author = "Astrid Freyjasdottir"
        elif "eirynth" in title_lower:
            author = "Eirynth Vinterdóttir"
        elif "dr. liv vaelen" in title_lower or "liv vaelen" in title_lower:
            author = "Dr. Liv Vaelen"

        meta_div = soup.find(class_=lambda c: c and ("post-meta" in c or "entry-meta" in c))
        if meta_div:
            links = meta_div.find_all("a")
            for link in links:
                rel = link.get("rel") or []
                href = link.get("href") or ""
                text = link.get_text(strip=True)
                if not text or text.lower() in ["leave a comment", "edit"]:
                    continue
                if "category" in rel or "/category/" in href:
                    categories.append(text)
                elif "tag" in rel or "/tag/" in href:
                    tags.append(text)
                elif "author" in rel or "/author/" in href:
                    author = text

        # Extract entry content container
        entry = None
        if post_div:
            entry = post_div.find("div", class_="entry") or post_div.find("div", class_="entry-content")
        if not entry:
            entry = soup.find("div", class_="entry") or soup.find("div", class_="entry-content") or soup.find("div", id="content") or soup.body

        # 3. Strip unwanted elements
        # Remove comments, scripts, styles, forms, jetpack widgets, sharedaddy
        for comment in entry.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        unwanted_selectors = [
            "script", "style", "noscript", "iframe", "form",
            ".sharedaddy", ".jp-relatedposts", ".sd-like",
            ".jetpack-likes-widget-wrapper", ".likes-widget-placeholder",
            ".post-likes-widget-placeholder", "#comments", "#respond",
            ".navigation", ".wpcnt", ".robots-nocontent"
        ]
        for sel in unwanted_selectors:
            for el in entry.select(sel):
                el.decompose()

        # Remove "Share this:" and "Like this:" paragraphs
        for p in entry.find_all(["p", "div", "h3"]):
            text = p.get_text(strip=True)
            if text in ["Share this:", "Like this:", "Related", "Leave a Reply", "Leave a comment"]:
                p.decompose()

        # 4. Convert entry to Markdown
        raw_html_clean = str(entry)
        markdown_body = md(raw_html_clean, heading_style="ATX", strip=["img"] if False else [])
        
        # Clean excessive blank lines and whitespace
        markdown_body = re.sub(r"\n{3,}", "\n\n", markdown_body).strip()
        
        meta = {
            "title": title,
            "published": published,
            "modified": modified,
            "author": author,
            "author_type": self.classify_author(author),
            "categories": sorted(list(set(categories))),
            "tags": sorted(list(set(tags)))
        }
        return meta, markdown_body

    def normalize_record(self, record: dict) -> bool:
        cid = record["content_id"]
        raw_file = self.raw_dir / f"{cid}.html"
        if not raw_file.exists():
            return False
            
        with open(raw_file, "rb") as f:
            raw_bytes = f.read()
            
        meta, markdown_body = self.clean_html(raw_bytes)
        
        # Update manifest record fields if discovered
        if meta["title"]:
            record["title"] = meta["title"]
        if meta["published"] and not record.get("published"):
            record["published"] = meta["published"]
        if meta["modified"]:
            record["modified"] = meta["modified"]
        if meta["author"]:
            record["author"] = meta["author"]
        if meta["categories"]:
            record["categories"] = meta["categories"]
        if meta["tags"]:
            record["tags"] = meta["tags"]
            
        normalized_hash = "sha256:" + hashlib.sha256(markdown_body.encode("utf-8")).hexdigest()
        record["normalized_hash"] = normalized_hash
        
        # Build YAML frontmatter
        frontmatter = [
            "---",
            f"content_id: {cid}",
            f"url: {record['url']}",
            f"title: \"{meta['title'].replace('\"', '\\\"')}\"",
            f"published: \"{meta['published']}\"",
            f"modified: \"{meta['modified']}\"",
            f"author: \"{meta['author']}\"",
            f"author_type: \"{meta['author_type']}\"",
            f"categories: {json.dumps(meta['categories'], ensure_ascii=False)}",
            f"tags: {json.dumps(meta['tags'], ensure_ascii=False)}",
            f"normalized_hash: \"{normalized_hash}\"",
            "---",
            "",
            markdown_body
        ]
        
        out_file = self.normalized_dir / f"{cid}.md"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(frontmatter) + "\n")
            
        return True

    def normalize_all(self, content_ids: list[str] = None):
        records = self.load_manifest()
        record_map = {r["content_id"]: r for r in records}
        
        targets = [record_map[cid] for cid in content_ids if cid in record_map] if content_ids else records
        console.print(f"[bold cyan]Normalizing {len(targets)} records...[/bold cyan]")
        
        normalized_count = 0
        for r in targets:
            if self.normalize_record(r):
                normalized_count += 1
                
        self.save_manifest(records)
        console.print(f"[bold green]Normalization complete.[/bold green] {normalized_count} files written to {self.normalized_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Normalize raw HTML articles to clean Markdown")
    parser.add_argument("--ids", type=str, default=None, help="Comma-separated content IDs to normalize")
    args = parser.parse_args()
    
    cids = [x.strip() for x in args.ids.split(",")] if args.ids else None
    normalizer = CorpusNormalizer()
    normalizer.normalize_all(content_ids=cids)
