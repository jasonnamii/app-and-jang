#!/usr/bin/env python3
"""
validate.py — app-policy 스킬 self-check (v2.1 신규)

검증 항목:
  1. SKILL.md 크기 (<10KB 권장, <15KB 하드리밋)
  2. 도메인 네이밍: SKILL.md 포인터 ↔ 실파일 정합
  3. α 엔진: SKILL.md 포인터 ↔ 실파일 정합
  4. 필수 섹션 존재 (절대 규칙·7도메인·모드·Gotchas·디스클레이머)
  5. evals/cases.json 존재 + 유효 JSON + 최소 3케이스
  6. 스크립트 실행 가능 여부 (문법 체크)

Usage:
  python scripts/validate.py --skill-dir=./
  python scripts/validate.py  # 현재 디렉토리 기준 (스크립트 상대경로)
"""
from __future__ import annotations
import argparse
import ast
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_SECTIONS = ["절대 규칙", "7도메인", "모드", "Gotchas", "디스클레이머"]
SKILL_SIZE_WARN = 10 * 1024    # 10KB
SKILL_SIZE_HARD = 15 * 1024    # 15KB
MIN_EVAL_CASES = 3


def check_skill_md_size(root: Path) -> dict:
    f = root / "SKILL.md"
    if not f.exists():
        return {"check": "skill_md_size", "status": "FAIL", "evidence": "SKILL.md 없음"}
    size = f.stat().st_size
    if size >= SKILL_SIZE_HARD:
        return {"check": "skill_md_size", "status": "FAIL", "evidence": f"{size}B >= {SKILL_SIZE_HARD}B (하드리밋)"}
    if size >= SKILL_SIZE_WARN:
        return {"check": "skill_md_size", "status": "WARN", "evidence": f"{size}B >= {SKILL_SIZE_WARN}B (권장)"}
    return {"check": "skill_md_size", "status": "PASS", "evidence": f"{size}B"}


def check_domain_naming(root: Path) -> dict:
    """SKILL.md에서 참조한 domains/d*.md 파일명 ↔ 실파일 정합."""
    skill_md = (root / "SKILL.md").read_text(encoding="utf-8")
    # SKILL.md에서 references/domains/ 하위 파일명 추출
    referenced = set(re.findall(r"domains/(d\d+-[a-z-]+\.md)", skill_md))
    actual = set(p.name for p in (root / "references" / "domains").glob("d*.md"))
    missing = referenced - actual
    orphan = actual - referenced
    if missing:
        return {"check": "domain_naming", "status": "FAIL",
                "evidence": f"SKILL.md 참조인데 실파일 없음: {sorted(missing)}"}
    # 단수 파일 패턴 사용 여부 체크 (d{1..7}-*.md 같은 glob 패턴은 허용)
    has_glob = "d{1..7}-*.md" in skill_md or "d{1..7}" in skill_md
    if not referenced and not has_glob:
        return {"check": "domain_naming", "status": "WARN",
                "evidence": "SKILL.md에 구체 도메인 파일 참조도 glob 패턴도 없음"}
    return {"check": "domain_naming", "status": "PASS",
            "evidence": f"referenced={len(referenced)}, actual={len(actual)}, orphan={len(orphan)}"}


def check_alpha_naming(root: Path) -> dict:
    skill_md = (root / "SKILL.md").read_text(encoding="utf-8")
    referenced = set(re.findall(r"alpha/(a\d+-[a-z-]+\.md)", skill_md))
    actual = set(p.name for p in (root / "references" / "alpha").glob("a*.md"))
    missing = referenced - actual
    if missing:
        return {"check": "alpha_naming", "status": "FAIL",
                "evidence": f"SKILL.md 참조인데 실파일 없음: {sorted(missing)}"}
    return {"check": "alpha_naming", "status": "PASS",
            "evidence": f"referenced={len(referenced)}, actual={len(actual)}"}


def check_required_sections(root: Path) -> dict:
    skill_md = (root / "SKILL.md").read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SECTIONS if s not in skill_md]
    if missing:
        return {"check": "required_sections", "status": "FAIL",
                "evidence": f"누락: {missing}"}
    return {"check": "required_sections", "status": "PASS",
            "evidence": f"전 {len(REQUIRED_SECTIONS)}개 섹션 존재"}


def check_evals(root: Path) -> dict:
    f = root / "evals" / "cases.json"
    if not f.exists():
        return {"check": "evals", "status": "FAIL", "evidence": "evals/cases.json 없음"}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"check": "evals", "status": "FAIL", "evidence": f"JSON invalid: {e}"}
    cases = data.get("cases", [])
    if len(cases) < MIN_EVAL_CASES:
        return {"check": "evals", "status": "FAIL",
                "evidence": f"{len(cases)} < {MIN_EVAL_CASES}"}
    # 필수 필드
    missing_fields = []
    for c in cases:
        if "id" not in c or "mode" not in c:
            missing_fields.append(c.get("id", "?"))
    if missing_fields:
        return {"check": "evals", "status": "WARN",
                "evidence": f"id/mode 누락 케이스: {missing_fields}"}
    return {"check": "evals", "status": "PASS", "evidence": f"cases={len(cases)}"}


def check_scripts_syntax(root: Path) -> dict:
    errors = []
    for py in (root / "scripts").rglob("*.py"):
        try:
            ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError as e:
            errors.append(f"{py.relative_to(root)}: {e}")
    if errors:
        return {"check": "scripts_syntax", "status": "FAIL", "evidence": errors}
    return {"check": "scripts_syntax", "status": "PASS", "evidence": "all scripts parse OK"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-dir", type=str, default=None,
                    help="스킬 루트 경로. 미지정 시 스크립트 상위 디렉토리.")
    ap.add_argument("--json", action="store_true", help="JSON 출력")
    args = ap.parse_args()

    root = Path(args.skill_dir).resolve() if args.skill_dir else SKILL_ROOT

    checks = [
        check_skill_md_size(root),
        check_domain_naming(root),
        check_alpha_naming(root),
        check_required_sections(root),
        check_evals(root),
        check_scripts_syntax(root),
    ]

    fail = sum(1 for c in checks if c["status"] == "FAIL")
    warn = sum(1 for c in checks if c["status"] == "WARN")
    passed = sum(1 for c in checks if c["status"] == "PASS")

    result = {
        "skill": "app-policy",
        "skill_dir": str(root),
        "summary": {"PASS": passed, "WARN": warn, "FAIL": fail},
        "checks": checks,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== app-and-jang self-check ({root}) ===")
        for c in checks:
            sym = {"PASS": "🟢", "WARN": "🟠", "FAIL": "🔴"}[c["status"]]
            print(f"  {sym} {c['check']}: {c['evidence']}")
        print(f"\nSummary: PASS={passed} · WARN={warn} · FAIL={fail}")

    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
