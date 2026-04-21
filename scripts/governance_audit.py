#!/usr/bin/env python3
"""
governance_audit.py — 3중 방어선 자체 감사 스크립트

Layer 1: _launches/ 런칭 템플릿 기입·서명 검증
Layer 3: scripts/trigger_scan.py 패턴 커버리지
Cross: 4문서 T1~T8 언급 일치성

Usage:
  python3 scripts/governance_audit.py --weekly
  python3 scripts/governance_audit.py --quarterly --report _audit/q.md
  python3 scripts/governance_audit.py --full --fail-on-violations
"""
from __future__ import annotations
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 기본값: 스킬 루트 하위. --docs-dir / --launches-dir 로 외부 경로(볼트·프로젝트 레포) 지정 가능.
LAUNCHES_DIR = ROOT / "_launches"
DOCS_DIR = ROOT / "documents"

LAUNCH_REQUIRED = [rf"T{i}\." for i in range(1, 9)]
UNFILLED = re.compile(r"\[\s*\]\s*(YES|NO)", re.I)
SIGN_DATE = re.compile(r"(승인일|서명일)\s*[:：]\s*\d{4}-\d{2}-\d{2}")


def scan_launches():
    if not LAUNCHES_DIR.exists():
        return {"status": "no_dir", "files": 0, "violations": []}
    files = sorted(LAUNCHES_DIR.rglob("*.md"))
    violations = []
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        missing = [s for s in LAUNCH_REQUIRED if not re.search(s, content)]
        if missing:
            violations.append({"file": str(f.relative_to(ROOT)), "issue": f"섹션 누락: {missing}"})
        unfilled = UNFILLED.findall(content)
        if unfilled:
            violations.append({"file": str(f.relative_to(ROOT)), "issue": f"미기입 YES/NO {len(unfilled)}건"})
        if "법무" in content and not SIGN_DATE.search(content):
            violations.append({"file": str(f.relative_to(ROOT)), "issue": "서명일 누락"})
    return {"status": "ok" if not violations else "fail", "files": len(files), "violations": violations}


def scan_trigger_patterns():
    script = ROOT / "scripts" / "trigger_scan.py"
    if not script.exists():
        return {"status": "missing"}
    content = script.read_text(encoding="utf-8", errors="ignore")
    covered = [f"T{i}" for i in range(1, 9) if re.search(rf"T{i}\b", content)]
    missing = [f"T{i}" for i in range(1, 9) if f"T{i}" not in covered]
    return {"status": "ok" if not missing else "incomplete", "covered": covered, "missing": missing}


def cross_check_docs():
    # SKILL.md §10: T1~T8 신설·변경 시 4문서 동시개정 (terms·privacy·community·cookie-policy)
    # 거버넌스 인프라(launch-template·pr-checklist·trigger_scan) + 정책 4문서 도메인별 필수 매핑
    REQUIRED = {
        "launch-template_v1.md": {"path": DOCS_DIR / "launch-template_v1.md", "required": "all"},
        "pr-checklist_v1.md": {"path": DOCS_DIR / "pr-checklist_v1.md", "required": "all"},
        "monetization-triggers_v1.md": {"path": DOCS_DIR / "monetization-triggers_v1.md", "required": "all"},
        "trigger_scan.py": {"path": ROOT / "scripts" / "trigger_scan.py", "required": "all"},
        "terms-of-service_v1.md": {"path": DOCS_DIR / "terms-of-service_v1.md", "required": ["T1", "T2", "T6", "T7"]},
        "privacy-policy_v1.md": {"path": DOCS_DIR / "privacy-policy_v1.md", "required": ["T3", "T4", "T5", "T8"]},
        "community-guideline_v1.md": {"path": DOCS_DIR / "community-guideline_v1.md", "required": ["T6", "T8"]},
        "cookie-policy_v1.md": {"path": DOCS_DIR / "cookie-policy_v1.md", "required": ["T3", "T4", "T5"]},
    }
    results = {}
    drift = []
    for name, meta in REQUIRED.items():
        path = meta["path"]
        required = meta["required"]
        if not path.exists():
            results[name] = {"exists": False}
            drift.append(f"{name}: 파일 부재")
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        counts = {f"T{i}": len(re.findall(rf"T{i}\b", content)) for i in range(1, 9)}
        req_list = [f"T{i}" for i in range(1, 9)] if required == "all" else required
        missing = [tn for tn in req_list if counts.get(tn, 0) == 0]
        results[name] = {"exists": True, "counts": counts, "required": req_list, "missing": missing}
        for tn in missing:
            drift.append(f"{name}: {tn} 미언급 (필수)")
    return {"status": "ok" if not drift else "drift", "files": results, "drift": drift}


def generate_report(mode):
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    l1 = scan_launches()
    l3 = scan_trigger_patterns()
    cx = cross_check_docs()
    lines = [
        f"# 거버넌스 감사 리포트 ({mode})",
        f"",
        f"- 생성: {now}",
        f"",
        f"## Layer 1 — 런칭 템플릿",
        f"- 상태: **{l1['status']}** · 파일 {l1.get('files', 0)} · 위반 {len(l1.get('violations', []))}",
    ]
    for v in l1.get("violations", [])[:20]:
        lines.append(f"  - `{v['file']}`: {v['issue']}")
    lines += [
        f"",
        f"## Layer 3 — CI 스캐너 커버리지",
        f"- 상태: **{l3['status']}** · 커버 {l3.get('covered', [])} · 누락 {l3.get('missing', [])}",
        f"",
        f"## 교차 문서 정합성",
        f"- 상태: **{cx['status']}**",
    ]
    for d in cx.get("drift", []):
        lines.append(f"  - {d}")
    lines += ["", "## 액션", "- 위반·편차 0건: 유지", "- 위반 시: governance-runbook §7 에스컬레이션"]
    return "\n".join(lines)


def main():
    global DOCS_DIR, LAUNCHES_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--weekly", action="store_true")
    ap.add_argument("--monthly", action="store_true")
    ap.add_argument("--quarterly", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--report", type=str)
    ap.add_argument("--fail-on-violations", action="store_true")
    ap.add_argument("--docs-dir", type=str, default=None,
                    help="운영 문서 디렉토리 경로 (예: ~/VAULT/projects/cre8orclub/_policy-docs). 미지정 시 스킬 루트 하위 documents/ 사용")
    ap.add_argument("--launches-dir", type=str, default=None,
                    help="런칭 템플릿 디렉토리 경로. 미지정 시 스킬 루트 하위 _launches/ 사용")
    args = ap.parse_args()
    if args.docs_dir:
        DOCS_DIR = Path(args.docs_dir).expanduser().resolve()
    if args.launches_dir:
        LAUNCHES_DIR = Path(args.launches_dir).expanduser().resolve()
    mode = "weekly" if args.weekly else "monthly" if args.monthly else "quarterly" if args.quarterly else "full"
    report = generate_report(mode)
    print(report)
    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = ROOT / args.report
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"\n[저장] {out}")
    if args.fail_on_violations:
        l1 = scan_launches()
        cx = cross_check_docs()
        if l1.get("violations") or cx.get("drift"):
            print("\n[FAIL] 위반·편차 감지", file=sys.stderr)
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
