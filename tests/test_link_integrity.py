import re
from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge")

def test_markdown_internal_link_integrity():
    md_files = list(KNOWLEDGE_DIR.rglob("*.md"))
    assert len(md_files) >= 28, f"Expected at least 28 markdown files, found {len(md_files)}"
    
    broken_links = []
    total_links = 0
    
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
        for label, target in links:
            if target.startswith("http://") or target.startswith("https://"):
                continue
            total_links += 1
            target_clean = target.split("#")[0]
            resolved_path = (f.parent / target_clean).resolve()
            if not resolved_path.exists():
                broken_links.append((str(f.relative_to(KNOWLEDGE_DIR)), label, target))
                
    assert not broken_links, f"Found {len(broken_links)} broken relative links: {broken_links}"
    assert total_links > 150, f"Expected > 150 internal links, found {total_links}"

def test_index_and_glossary_exist():
    assert (KNOWLEDGE_DIR / "00_INDEX.md").exists()
    assert (KNOWLEDGE_DIR / "00_GLOSSARY.md").exists()
    assert (KNOWLEDGE_DIR / "00_CONCEPT_MAP.md").exists()
