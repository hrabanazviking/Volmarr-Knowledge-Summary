from pathlib import Path
from src.export.packager import ReleasePackager

def test_release_packager():
    packager = ReleasePackager()
    release_data = packager.build_release()
    
    assert "release_title" in release_data
    assert "version" in release_data
    assert "distributed_assets" in release_data
    assert len(release_data["distributed_assets"]) >= 10
    
    manifest_path = Path("dist/release_manifest.json")
    assert manifest_path.exists()
    assert manifest_path.stat().st_size > 1000
    
    # Check that each asset has valid hash and non-zero size
    for asset in release_data["distributed_assets"]:
        assert asset["size_bytes"] > 0
        assert len(asset["sha256"]) == 64
