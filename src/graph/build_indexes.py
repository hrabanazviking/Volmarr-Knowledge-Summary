"""Bi-directional Knowledge Layer Indexer.
Generates source_to_concepts.json and concept_to_sources.json from source_claims.jsonl and concept_registry.jsonl.
"""

import json
from pathlib import Path
from collections import defaultdict
from rich.console import Console

console = Console()

def build_bidirectional_indexes():
    db_dir = Path("data/database")
    claims_path = db_dir / "source_claims.jsonl"
    registry_path = db_dir / "concept_registry.jsonl"

    if not claims_path.exists() or not registry_path.exists():
        console.print("[red]Missing claims or registry file.[/red]")
        return

    # Load registry
    concepts = {}
    with open(registry_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                concepts[item["slug"]] = item

    source_to_concepts = defaultdict(lambda: {"title": "", "url": "", "author": "", "concepts": defaultdict(int), "claims_count": 0})
    concept_to_sources = defaultdict(lambda: {"canonical_name": "", "taxonomy_level": "", "sources": {}})

    for slug, c_data in concepts.items():
        concept_to_sources[slug]["canonical_name"] = c_data["canonical_name"]
        concept_to_sources[slug]["taxonomy_level"] = c_data["taxonomy_level"]

    with open(claims_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                c = json.loads(line)
                slug = c["concept_name"]
                c_id = c.get("source_ids", ["unknown"])[0]
                url = c.get("source_url", "")
                title = c.get("article_title", "")
                author = c.get("author", "Volmarr")

                # Update source_to_concepts
                source_to_concepts[c_id]["title"] = title
                source_to_concepts[c_id]["url"] = url
                source_to_concepts[c_id]["author"] = author
                source_to_concepts[c_id]["concepts"][slug] += 1
                source_to_concepts[c_id]["claims_count"] += 1

                # Update concept_to_sources
                if url:
                    if url not in concept_to_sources[slug]["sources"]:
                        concept_to_sources[slug]["sources"][url] = {
                            "content_id": c_id,
                            "title": title,
                            "claims_count": 0
                        }
                    concept_to_sources[slug]["sources"][url]["claims_count"] += 1

    # Convert defaultdicts to regular dicts for JSON serialization
    s2c_clean = {}
    for cid, data in source_to_concepts.items():
        s2c_clean[cid] = {
            "title": data["title"],
            "url": data["url"],
            "author": data["author"],
            "claims_count": data["claims_count"],
            "concepts": dict(data["concepts"])
        }

    c2s_clean = dict(concept_to_sources)

    s2c_file = db_dir / "source_to_concepts.json"
    c2s_file = db_dir / "concept_to_sources.json"

    with open(s2c_file, "w", encoding="utf-8") as f:
        json.dump(s2c_clean, f, indent=2, ensure_ascii=False)

    with open(c2s_file, "w", encoding="utf-8") as f:
        json.dump(c2s_clean, f, indent=2, ensure_ascii=False)

    console.print(f"[bold green]Bi-directional indexes built successfully:[/bold green]")
    console.print(f"  - {s2c_file} ({len(s2c_clean)} source documents mapped)")
    console.print(f"  - {c2s_file} ({len(c2s_clean)} canonical concepts indexed)")

if __name__ == "__main__":
    build_bidirectional_indexes()
