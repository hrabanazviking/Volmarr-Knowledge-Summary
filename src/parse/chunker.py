"""Structural Chunking Module.
Splits normalized Markdown into heading-aware semantic chunks preserving heading paths, context, and metadata.
"""

import re
import json
from pathlib import Path
from rich.console import Console

console = Console()

class SemanticChunker:
    def __init__(self, normalized_dir: str = "data/normalized", chunks_dir: str = "data/chunks"):
        self.normalized_dir = Path(normalized_dir)
        self.chunks_dir = Path(chunks_dir)
        self.chunks_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def parse_frontmatter(md_text: str) -> tuple[dict, str]:
        """Extract YAML frontmatter and body."""
        if not md_text.startswith("---"):
            return {}, md_text
        parts = md_text.split("---", 2)
        if len(parts) < 3:
            return {}, md_text
        front_yaml = parts[1]
        body = parts[2].strip()
        
        meta = {}
        for line in front_yaml.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip().strip('"')
                if val.startswith("[") and val.endswith("]"):
                    try:
                        val = json.loads(val)
                    except Exception:
                        pass
                meta[key] = val
        return meta, body

    def chunk_document(self, md_path: Path) -> list[dict]:
        with open(md_path, "r", encoding="utf-8") as f:
            full_text = f.read()
            
        meta, body = self.parse_frontmatter(full_text)
        cid = meta.get("content_id", md_path.stem)
        article_title = meta.get("title", md_path.stem)
        source_url = meta.get("url", "")
        
        lines = body.split("\n")
        chunks = []
        
        current_heading_path = [article_title]
        current_paragraphs = []
        chunk_idx = 1
        
        def commit_chunk():
            nonlocal chunk_idx, current_paragraphs
            text = "\n".join(current_paragraphs).strip()
            if not text:
                return
            chunk_id = f"{cid}_{chunk_idx:03d}"
            chunks.append({
                "chunk_id": chunk_id,
                "content_id": cid,
                "source_url": source_url,
                "article_title": article_title,
                "heading_path": list(current_heading_path),
                "author": meta.get("author", "Volmarr"),
                "author_type": meta.get("author_type", "site_owner"),
                "categories": meta.get("categories", []),
                "tags": meta.get("tags", []),
                "published": meta.get("published", ""),
                "text": text,
                "position": chunk_idx
            })
            chunk_idx += 1
            current_paragraphs = []

        for line in lines:
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                h_text = header_match.group(2).strip()
                
                # If we already have content, commit previous chunk
                if current_paragraphs:
                    commit_chunk()
                    
                # Update heading path based on depth
                # Depth 1 -> [Title, H1] (or replace Title if H1 is title)
                # Depth 2 -> [Title, H2]
                # Depth 3 -> [Title, H2, H3]
                if level == 1:
                    current_heading_path = [article_title, h_text] if h_text != article_title else [article_title]
                elif level == 2:
                    current_heading_path = [article_title, h_text]
                elif level >= 3:
                    if len(current_heading_path) >= 2:
                        current_heading_path = current_heading_path[:2] + [h_text]
                    else:
                        current_heading_path = [article_title, h_text]
            else:
                current_paragraphs.append(line)
                # If section becomes too long (> 2000 chars and double newline), split conservatively
                if len("\n".join(current_paragraphs)) > 3000 and line.strip() == "":
                    commit_chunk()
                    
        # Commit trailing chunk
        if current_paragraphs:
            commit_chunk()
            
        return chunks

    def process_all(self, content_ids: list[str] = None) -> list[dict]:
        target_files = list(self.normalized_dir.glob("*.md"))
        if content_ids:
            target_files = [f for f in target_files if f.stem in content_ids]
            
        console.print(f"[bold cyan]Chunking {len(target_files)} normalized Markdown documents...[/bold cyan]")
        
        for f in target_files:
            chunks = self.chunk_document(f)
            if not chunks:
                continue
            out_file = self.chunks_dir / f"{f.stem}.json"
            with open(out_file, "w", encoding="utf-8") as out_f:
                json.dump(chunks, out_f, indent=2, ensure_ascii=False)
                
        # Compile master all_chunks.jsonl across ALL chunk files
        all_chunks = []
        for json_file in sorted(self.chunks_dir.glob("*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as jf:
                    file_chunks = json.load(jf)
                    all_chunks.extend(file_chunks)
            except Exception as e:
                console.print(f"[yellow]Skipping corrupt chunk file {json_file}: {e}[/yellow]")

        index_file = self.chunks_dir / "all_chunks.jsonl"
        with open(index_file, "w", encoding="utf-8") as out_idx:
            for ch in all_chunks:
                out_idx.write(json.dumps(ch, ensure_ascii=False) + "\n")
                
        console.print(f"[bold green]Chunking complete.[/bold green] Compiled {len(all_chunks)} total semantic chunks in {index_file}.")
        return all_chunks

if __name__ == "__main__":
    chunker = SemanticChunker()
    chunker.process_all()
