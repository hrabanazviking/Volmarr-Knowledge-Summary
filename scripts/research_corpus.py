"""Corpus Research Engine for Volmarr Knowledge Synthesis.
Enables deep querying of normalized articles, chunk text, publication dates, and provenance.
"""

import os
import re
import json
import glob
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "data" / "corpus_manifest.jsonl"
NORMALIZED_DIR = PROJECT_ROOT / "data" / "normalized"

def load_manifest() -> dict[str, dict]:
    manifest = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    manifest[item["content_id"]] = item
    return manifest

def search_corpus(patterns: list[str], max_results: int = 15) -> list[dict]:
    manifest = load_manifest()
    results = []
    
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
    
    for file_path in glob.glob(str(NORMALIZED_DIR / "*.md")):
        cid = Path(file_path).stem
        meta = manifest.get(cid, {})
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Score by how many patterns match and total occurrences
        matches = {}
        total_hits = 0
        for pat, regex in zip(patterns, compiled_patterns):
            finds = list(regex.finditer(content))
            if finds:
                matches[pat] = len(finds)
                total_hits += len(finds)
                
        if len(matches) == len(patterns): # all patterns match
            # Extract key excerpt around first match
            first_match = compiled_patterns[0].search(content)
            start = max(0, first_match.start() - 250)
            end = min(len(content), first_match.end() + 350)
            snippet = content[start:end].replace("\n", " ").strip()
            
            results.append({
                "content_id": cid,
                "title": meta.get("title", ""),
                "url": meta.get("url", ""),
                "published": meta.get("published", ""),
                "score": total_hits,
                "snippet": snippet,
                "full_length": len(content)
            })
            
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]

if __name__ == "__main__":
    import sys
    query = sys.argv[1:] if len(sys.argv) > 1 else ["troth", "reciprocity"]
    res = search_corpus(query)
    print(f"Query: {query} (Found {len(res)} matches)")
    for r in res[:5]:
        print(f"\n--- {r['title']} ({r['published']}) ---")
        print(f"URL: {r['url']}")
        print(f"Snippet: ...{r['snippet']}...")
