"""Rebuild all derived assets using ReleasePackager."""

import sys
sys.path.insert(0, ".")

from src.export.packager import ReleasePackager

packager = ReleasePackager()
manifest = packager.build_release()
print("Release packaging completed successfully!")
print(f"Total assets: {len(manifest.get('assets', {}))}")
