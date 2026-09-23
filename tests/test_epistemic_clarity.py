import json
from pathlib import Path

DB_DIR = Path("data/database")

VALID_EPISTEMIC_TAGS = {
    "historical",
    "reconstruction",
    "modern_heathen_practice",
    "personal_practice",
    "theology",
    "devotional",
    "philosophical",
    "mystical",
    "experiential",
    "speculative",
    "metaphorical",
    "technological",
    "political_or_social_commentary",
    "creative_mythmaking",
    "ritual_instruction"
}

def test_claims_epistemic_tagging():
    claims_file = DB_DIR / "source_claims.jsonl"
    assert claims_file.exists()
    
    unlabeled_count = 0
    total_claims = 0
    invalid_tags = set()
    
    with open(claims_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total_claims += 1
            claim = json.loads(line)
            tags = claim.get("knowledge_type", [])
            if not tags:
                unlabeled_count += 1
            for t in tags:
                if t not in VALID_EPISTEMIC_TAGS:
                    invalid_tags.add(t)
                    
    assert total_claims > 1000, f"Expected > 1000 claims, found {total_claims}"
    assert unlabeled_count == 0, f"Found {unlabeled_count} unlabeled claims"
    assert not invalid_tags, f"Found unrecognized epistemic tags: {invalid_tags}"

def test_concepts_epistemic_categories():
    registry_file = DB_DIR / "concept_registry.jsonl"
    assert registry_file.exists()
    
    concepts = [json.loads(line) for line in open(registry_file, encoding="utf-8") if line.strip()]
    for c in concepts:
        ktypes = c.get("knowledge_types", [])
        assert len(ktypes) > 0, f"Concept {c['concept_id']} missing knowledge_types"
        for kt in ktypes:
            assert kt in VALID_EPISTEMIC_TAGS, f"Invalid knowledge_type '{kt}' in concept {c['concept_id']}"
