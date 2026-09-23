from pathlib import Path
import re
import json

knowledge_dir = Path("knowledge")
files = sorted([
    f for f in knowledge_dir.rglob("*.md")
    if "_meta" not in f.parts and not f.name.startswith("00_")
])

print(f"Total concept files found: {len(files)}")
by_tier = {}
all_data = []

for f in files:
    content = f.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "UNKNOWN"
    
    # Brief
    brief_match = re.search(r"## In Brief\s*\n\s*([^\n]+)", content)
    brief = brief_match.group(1).strip() if brief_match else ""
    
    # Prerequisites
    prereq_match = re.search(r"Prerequisites:?\s*([^\n]+)", content)
    prereqs = prereq_match.group(1).strip() if prereq_match else ""
    
    tier = f.parent.name
    by_tier.setdefault(tier, []).append((f.name, title, brief, prereqs))
    all_data.append({
        "tier": tier,
        "filename": f.name,
        "path": f.as_posix(),
        "rel_path": f.relative_to(knowledge_dir).as_posix(),
        "title": title,
        "brief": brief,
        "prereqs_raw": prereqs
    })

print("\nBreakdown by Tier:")
for tier, doc_list in by_tier.items():
    print(f"  {tier}: {len(doc_list)} files")

with open("data/database/canon_inspection.json", "w", encoding="utf-8") as out:
    json.dump(all_data, out, indent=2, ensure_ascii=False)
