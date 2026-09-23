from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge")

REQUIRED_SECTIONS = [
    "## In Brief",
    "## Core Idea",
    "## Key Principles",
    "## Distinctions",
    "## Source Provenance"
]

def test_canonical_documents_schema_compliance():
    concept_docs = [
        f for f in KNOWLEDGE_DIR.rglob("*.md")
        if "_meta" not in f.parts and f.name not in ["00_INDEX.md", "00_GLOSSARY.md", "00_CONCEPT_MAP.md"]
    ]
    assert len(concept_docs) == 25, f"Expected 25 concept documents, got {len(concept_docs)}"
    
    missing_sections = []
    for doc in concept_docs:
        text = doc.read_text(encoding="utf-8")
        assert text.startswith("# "), f"{doc.name} missing h1 title"
        for sec in REQUIRED_SECTIONS:
            if sec not in text:
                missing_sections.append((doc.name, sec))
                
    assert not missing_sections, f"Schema compliance failures: {missing_sections}"
