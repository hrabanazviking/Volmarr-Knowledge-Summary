import json
from pathlib import Path

DATA_DIR = Path("data")

def test_manifest_completeness():
    manifest_file = DATA_DIR / "corpus_manifest.jsonl"
    assert manifest_file.exists(), "Manifest file missing"
    
    entries = []
    with open(manifest_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
                
    assert len(entries) >= 570, f"Expected at least 570 entries, found {len(entries)}"
    
    # Verify core static pages are present
    urls = {e["url"] for e in entries}
    assert "https://volmarrsheathenism.com/about-volmarr/" in urls
    assert "https://volmarrsheathenism.com/heathen-third-path/" in urls
    assert "https://volmarrsheathenism.com/modern-norse-paganism/" in urls

def test_raw_and_normalized_coverage():
    manifest_file = DATA_DIR / "corpus_manifest.jsonl"
    entries = [json.loads(line) for line in open(manifest_file, encoding="utf-8") if line.strip()]
    
    raw_dir = DATA_DIR / "raw"
    normalized_dir = DATA_DIR / "normalized"
    
    assert raw_dir.exists()
    assert normalized_dir.exists()
    
    for e in entries:
        cid = e["content_id"]
        raw_path = raw_dir / f"{cid}.html"
        norm_path = normalized_dir / f"{cid}.md"
        
        assert raw_path.exists(), f"Raw HTML missing for {cid}"
        assert norm_path.exists(), f"Normalized markdown missing for {cid}"
        assert raw_path.stat().st_size > 0, f"Raw file {cid} is empty"
        assert norm_path.stat().st_size > 0, f"Normalized file {cid} is empty"
