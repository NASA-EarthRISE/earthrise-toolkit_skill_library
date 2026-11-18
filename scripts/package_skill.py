#!/usr/bin/env python3
"""Zip a skill folder for upload to the Claude app (or sharing with another account).

Only the files Claude needs are included (SKILL.md, scripts/, references/, assets/).
Library-only files (skill.yaml, evals/) are left out.

Usage:
    python scripts/package_skill.py Science/classification-accuracy-assessment [--out dist/]
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDE_DIRS = ("scripts", "references", "assets")
EXCLUDE_SUFFIX = (".pyc",)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill", help="path like Science/my-skill")
    ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    src = (ROOT / a.skill).resolve()
    if not (src / "SKILL.md").exists():
        sys.exit(f"No SKILL.md in {src}")
    out = ROOT / a.out
    out.mkdir(exist_ok=True)
    zpath = out / f"{src.name}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(src / "SKILL.md", f"{src.name}/SKILL.md")
        for d in INCLUDE_DIRS:
            for f in (src / d).rglob("*") if (src / d).exists() else []:
                if f.is_file() and not f.name.startswith(".") and f.suffix not in EXCLUDE_SUFFIX and "__pycache__" not in f.parts:
                    z.write(f, f"{src.name}/{f.relative_to(src)}")
    print(f"Packaged -> {zpath.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
