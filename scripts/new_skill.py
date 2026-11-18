#!/usr/bin/env python3
"""Scaffold a new skill from templates/skill-template.

Usage:
    python scripts/new_skill.py Science my-new-skill --owner @handle
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ("GIT", "Science", "Solution_Management")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain", choices=DOMAINS)
    ap.add_argument("name", help="kebab-case skill id")
    ap.add_argument("--owner", required=True, help="GitHub handle, e.g. @jdoe")
    a = ap.parse_args()
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", a.name):
        sys.exit("name must be kebab-case")
    dest = ROOT / a.domain / a.name
    if dest.exists():
        sys.exit(f"{dest} already exists")
    shutil.copytree(ROOT / "templates" / "skill-template", dest)
    owner = a.owner if a.owner.startswith("@") else f"@{a.owner}"
    for f in dest.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".yaml", ".json"}:
            t = f.read_text(encoding="utf-8")
            t = t.replace("your-skill-name", a.name).replace("@your-github-handle", owner)
            t = t.replace("domain: Science", f"domain: {a.domain}").replace("domain-Science", f"domain-{a.domain}")
            f.write_text(t, encoding="utf-8")
    print(f"Created {dest.relative_to(ROOT)}\nNext: edit SKILL.md + skill.yaml, then run python scripts/validate_skill.py {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
