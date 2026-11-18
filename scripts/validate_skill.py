#!/usr/bin/env python3
"""Validate EarthRISE skills against standards/SKILL_STANDARD.md and VERIFICATION.md.

Usage:
    python scripts/validate_skill.py                 # validate every skill in the library
    python scripts/validate_skill.py Science/my-skill  # validate one or more skill folders
Exit code 1 if any MUST rule fails.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ("GIT", "Science", "Solution_Management")
STATUSES = ("draft", "peer-reviewed", "verified", "certified", "deprecated")
LEVEL = {s: i for i, s in enumerate(STATUSES[:-1])}
SENSITIVITY = ("public", "internal", "partner-restricted")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET_PATTERNS = [
    re.compile(p)
    for p in (
        r"AKIA[0-9A-Z]{16}",                        # AWS key id
        r"ghp_[A-Za-z0-9]{36}",                     # GitHub PAT
        r"github_pat_[A-Za-z0-9_]{40,}",
        r"sk-[A-Za-z0-9_-]{20,}",                   # generic API key
        r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
        r"\"private_key\"\s*:\s*\"-----BEGIN",      # GCP service account json
        r"(?i)(password|passwd|secret|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]",
    )
]
MAX_SKILL_LINES = 500


def load_artifact_types() -> set[str]:
    data = yaml.safe_load((ROOT / "standards" / "artifact_types.yaml").read_text())
    return set(data["types"])


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body


def discover() -> list[Path]:
    return sorted(p.parent for d in DOMAINS for p in (ROOT / d).glob("*/SKILL.md"))


def validate(skill_dir: Path, types: set[str], all_ids: set[str]) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    rel = skill_dir.relative_to(ROOT)
    folder = skill_dir.name
    domain = skill_dir.parent.name

    if domain not in DOMAINS:
        errs.append(f"parent folder '{domain}' is not one of {DOMAINS}")

    for req in ("SKILL.md", "skill.yaml", "README.md"):
        if not (skill_dir / req).exists():
            errs.append(f"missing required file {req}")
    if errs:
        return errs, warns

    # ---- SKILL.md ----
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except Exception as e:  # noqa: BLE001
        return [f"SKILL.md frontmatter: {e}"], warns
    extra = set(fm) - {"name", "description"}
    if extra:
        errs.append(f"SKILL.md frontmatter has extra keys {sorted(extra)} (only name, description)")
    name = fm.get("name", "")
    desc = fm.get("description", "") or ""
    if name != folder:
        errs.append(f"SKILL.md name '{name}' != folder '{folder}'")
    if not NAME_RE.match(folder) or len(folder) > 64:
        errs.append("skill name must be kebab-case and <= 64 chars")
    if re.search(r"claude|anthropic", folder):
        errs.append("skill name must not contain 'claude' or 'anthropic'")
    if not desc or len(desc) > 1024:
        errs.append("description must be 1..1024 chars")
    if "<" in desc or ">" in desc:
        errs.append("description must not contain angle brackets")
    if not re.search(r"(?i)\buse (this )?(skill )?when\b", desc):
        warns.append("description should say WHEN to use it ('Use when …')")
    n_lines = text.count("\n") + 1
    if n_lines > MAX_SKILL_LINES:
        errs.append(f"SKILL.md is {n_lines} lines (max {MAX_SKILL_LINES}); move detail to references/")
    for section in ("## Purpose", "## Inputs", "## Outputs", "## Guardrails"):
        if section not in body:
            errs.append(f"SKILL.md missing section '{section}'")
    for section in ("## Steps", "## Example"):
        if section not in body:
            warns.append(f"SKILL.md should have section '{section}'")

    # ---- skill.yaml ----
    try:
        man = yaml.safe_load((skill_dir / "skill.yaml").read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return errs + [f"skill.yaml parse error: {e}"], warns
    required = ("id", "title", "domain", "version", "owner", "maintainers", "status",
                "summary", "tags", "inputs", "outputs", "data_sensitivity", "verification")
    for k in required:
        if k not in man:
            errs.append(f"skill.yaml missing '{k}'")
    if man.get("id") != folder:
        errs.append(f"skill.yaml id '{man.get('id')}' != folder '{folder}'")
    if man.get("domain") != domain:
        errs.append(f"skill.yaml domain '{man.get('domain')}' != parent folder '{domain}'")
    if not re.match(r"^\d+\.\d+\.\d+$", str(man.get("version", ""))):
        errs.append("version must be SemVer X.Y.Z")
    status = man.get("status")
    if status not in STATUSES:
        errs.append(f"status '{status}' not in {STATUSES}")
    if man.get("data_sensitivity") not in SENSITIVITY:
        errs.append(f"data_sensitivity must be one of {SENSITIVITY}")
    for direction in ("inputs", "outputs"):
        for item in man.get(direction) or []:
            t = (item or {}).get("type")
            if t not in types:
                errs.append(f"{direction} type '{t}' not in standards/artifact_types.yaml")
    if not man.get("outputs"):
        errs.append("skill must declare at least one output")
    comp = man.get("composes_with") or {}
    for d in ("upstream", "downstream"):
        for sid in comp.get(d) or []:
            if sid not in all_ids:
                warns.append(f"composes_with.{d} references unknown skill '{sid}'")
    if status == "deprecated" and not man.get("deprecated_by"):
        warns.append("deprecated skill should set deprecated_by")

    # ---- badge prerequisites ----
    ver = man.get("verification") or {}
    reviewers = ver.get("reviewers") or []
    lvl = LEVEL.get(status, -1)
    evals_path = skill_dir / "evals" / "evals.json"
    if lvl >= LEVEL["peer-reviewed"]:
        if not evals_path.exists():
            errs.append("peer-reviewed+ requires evals/evals.json")
        else:
            ev = json.loads(evals_path.read_text()).get("evals", [])
            pos = [e for e in ev if e.get("type") == "positive"]
            neg = [e for e in ev if e.get("type") == "negative"]
            if len(pos) < 3 or len(neg) < 1:
                errs.append("evals need >= 3 positive and >= 1 negative cases")
        in_domain = [r for r in reviewers if r.get("domain") == domain]
        if not any((r.get("rubric") or 0) >= 70 and (r.get("eval_pass") or 0) >= 0.8 for r in in_domain):
            errs.append("peer-reviewed+ requires an in-domain reviewer with rubric>=70 and eval_pass>=0.8")
        if not ver.get("review_due"):
            errs.append("peer-reviewed+ requires verification.review_due")
    if lvl >= LEVEL["verified"]:
        cross = [r for r in reviewers if r.get("domain") not in (domain, None)]
        if not any((r.get("rubric") or 0) >= 85 and (r.get("eval_pass") or 0) >= 0.9 for r in cross):
            errs.append("verified+ requires a cross-domain reviewer with rubric>=85 and eval_pass>=0.9")
        accounts = {r.get("account") for r in reviewers if r.get("account")}
        if len(accounts) < 2:
            errs.append("verified+ requires evals run on >= 2 distinct Claude accounts")
        if len(man.get("maintainers") or []) < 2:
            errs.append("verified+ requires >= 2 maintainers")
    if lvl >= LEVEL["certified"]:
        wf_hits = [w for w in (ROOT / "workflows").glob("*.md") if f"`{folder}`" in w.read_text()]
        if not wf_hits:
            warns.append("certified skill is not used in any workflows/*.md (recommended)")
        so = ver.get("expert_signoff") or {}
        experts = (yaml.safe_load((ROOT / "standards" / "experts.yaml").read_text()) or {}).get("experts", {})
        handle = so.get("handle")
        if not (handle and so.get("issue") and so.get("date")):
            errs.append("certified requires verification.expert_signoff {handle, issue, date}")
        else:
            if handle not in (experts.get(domain) or []):
                errs.append(f"expert_signoff.handle {handle} is not a listed {domain} expert in standards/experts.yaml")
            if handle == man.get("owner") or handle in (man.get("maintainers") or []):
                errs.append("expert_signoff.handle must not be the skill's owner or a maintainer")
            if not re.match(r"^https://github\.com/[^/]+/[^/]+/issues/\d+$", str(so["issue"])):
                errs.append("expert_signoff.issue must be a GitHub issue URL")
    due = ver.get("review_due")
    if due and isinstance(due, (dt.date, str)):
        d = due if isinstance(due, dt.date) else dt.date.fromisoformat(str(due))
        if d < dt.date.today():
            warns.append(f"review_due {d} has passed -> shown as STALE")

    # ---- secret scan ----
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.stat().st_size < 2_000_000:
            try:
                content = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pat in SECRET_PATTERNS:
                if pat.search(content):
                    errs.append(f"possible secret in {f.relative_to(skill_dir)} ({pat.pattern[:24]}…)")
                    break

    return [f"{rel}: {e}" for e in errs], [f"{rel}: {w}" for w in warns]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="skill folders (default: all)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    a = ap.parse_args()
    types = load_artifact_types()
    all_dirs = discover()
    all_ids = {d.name for d in all_dirs}
    targets = [(ROOT / p).resolve() for p in a.paths] if a.paths else all_dirs
    n_err = n_warn = 0
    for d in targets:
        errs, warns = validate(d, types, all_ids)
        for w in warns:
            print(f"WARN  {w}")
        for e in errs:
            print(f"ERROR {e}")
        n_err += len(errs)
        n_warn += len(warns)
        if not errs:
            print(f"OK    {d.relative_to(ROOT)}")
    print(f"\n{len(targets)} skill(s): {n_err} error(s), {n_warn} warning(s)")
    return 1 if n_err or (a.strict and n_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
