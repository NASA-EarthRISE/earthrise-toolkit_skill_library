#!/usr/bin/env python3
"""CI check: every `certified` skill's expert_signoff issue really has an /approve
comment from that expert, posted on GitHub.

Needs a GitHub token (GITHUB_TOKEN or GH_TOKEN). In GitHub Actions the default token works.
Without a token it exits 0 with a notice, so local runs don't fail.

Usage:
    python scripts/verify_signoffs.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ("GIT", "Science", "Solution_Management")


def gh_get(url: str, token: str):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def comments(api_issue: str, token: str) -> list[dict]:
    out, page = [], 1
    while True:
        batch = gh_get(f"{api_issue}/comments?per_page=100&page={page}", token)
        out += batch
        if len(batch) < 100:
            return out
        page += 1


def check(skill_yaml: Path, experts: dict, cmd: str, token: str, fetch=comments) -> list[str]:
    m = yaml.safe_load(skill_yaml.read_text())
    if m.get("status") != "certified":
        return []
    so = (m.get("verification") or {}).get("expert_signoff") or {}
    handle, issue = so.get("handle", ""), so.get("issue", "")
    mt = re.match(r"^https://github\.com/([^/]+)/([^/]+)/issues/(\d+)$", str(issue))
    if not mt:
        return [f"{m['id']}: expert_signoff.issue is not a GitHub issue URL"]
    if handle not in experts.get(m["domain"], []):
        return [f"{m['id']}: {handle} is not a listed {m['domain']} expert"]
    api = f"https://api.github.com/repos/{mt[1]}/{mt[2]}/issues/{mt[3]}"
    login = handle.lstrip("@").lower()
    try:
        cs = fetch(api, token)
    except Exception as e:  # noqa: BLE001
        return [f"{m['id']}: could not read {issue}: {e}"]
    ok = any(c.get("user", {}).get("login", "").lower() == login
             and any(line.strip().lower().startswith(cmd) for line in (c.get("body") or "").splitlines())
             for c in cs)
    return [] if ok else [f"{m['id']}: no '{cmd}' comment from {handle} on {issue}"]


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    cfg = yaml.safe_load((ROOT / "standards" / "experts.yaml").read_text()) or {}
    experts, cmd = cfg.get("experts", {}), cfg.get("approve_command", "/approve").lower()
    files = [y for d in DOMAINS for y in sorted((ROOT / d).glob("*/skill.yaml"))]
    certified = [y for y in files if (yaml.safe_load(y.read_text()) or {}).get("status") == "certified"]
    if not certified:
        print("No certified skills to verify.")
        return 0
    if not token:
        print("NOTICE: no GITHUB_TOKEN; skipping sign-off verification (CI will run it).")
        return 0
    errs = [e for y in certified for e in check(y, experts, cmd, token)]
    for e in errs:
        print(f"ERROR {e}")
    print(f"{len(certified)} certified skill(s), {len(errs)} sign-off error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
