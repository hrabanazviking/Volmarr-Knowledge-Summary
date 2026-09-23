import re
import json
from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge")
DB_DIR = Path("data/database")

def test_concept_registry_uniqueness():
    registry_file = DB_DIR / "concept_registry.jsonl"
    assert registry_file.exists()
    
    concepts = [json.loads(line) for line in open(registry_file, encoding="utf-8") if line.strip()]
    assert len(concepts) == 25, f"Expected 25 canonical concepts, found {len(concepts)}"
    
    ids = [c["concept_id"] for c in concepts]
    assert len(ids) == len(set(ids)), "Duplicate concept IDs found in registry"
    
    names = [c["canonical_name"].lower() for c in concepts]
    assert len(names) == len(set(names)), "Duplicate canonical concept names found"

def test_pairwise_semantic_redundancy():
    md_files = [f for f in KNOWLEDGE_DIR.rglob("*.md") if f.name not in ["00_INDEX.md", "00_GLOSSARY.md", "00_CONCEPT_MAP.md", "build_report.md", "unresolved_conflicts.md", "redundancy_report.md"]]
    assert len(md_files) == 25, f"Expected 25 concept markdown docs, found {len(md_files)}"
    
    words = {}
    for f in md_files:
        text = f.read_text(encoding="utf-8").lower()
        words[f.name] = set(re.findall(r"\w+", text))
        
    max_sim = 0.0
    violators = []
    
    for i in range(len(md_files)):
        for j in range(i + 1, len(md_files)):
            f1 = md_files[i].name
            f2 = md_files[j].name
            w1 = words[f1]
            w2 = words[f2]
            sim = len(w1 & w2) / len(w1 | w2) if (w1 or w2) else 0.0
            if sim > max_sim:
                max_sim = sim
            if sim >= 0.45:
                violators.append((f1, f2, sim))
                
    assert not violators, f"Redundancy threshold (0.45) violated: {violators}"
    assert max_sim < 0.45, f"Max similarity {max_sim:.3f} exceeded 0.45"

def test_duplicate_clusters_recorded():
    clusters_file = DB_DIR / "duplicate_clusters.jsonl"
    assert clusters_file.exists()
    clusters = [json.loads(line) for line in open(clusters_file, encoding="utf-8") if line.strip()]
    assert len(clusters) > 0, "Expected non-empty duplicate clusters log"
