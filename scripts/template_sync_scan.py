#!/usr/bin/env python3
"""
template_sync_scan.py — 템플릿↔실문서 동기화 스캐너 (governance-runbook §5-4)

7쌍 1:1 매핑을 semantic diff로 검사한다.
- 템플릿 존재 여부 · 실문서 존재 여부
- 핵심 조문 커버리지 (실문서 count ≥ 템플릿 count)
- 시행일·법률번호 키워드 누락

Usage:
  python3 scripts/template_sync_scan.py --weekly
  python3 scripts/template_sync_scan.py --report _audit/template_sync_202617.md
  python3 scripts/template_sync_scan.py --fail-on-drift
"""
from __future__ import annotations
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "references" / "templates"
DOCS_DIR = ROOT / "documents"
AUDIT_DIR = ROOT / "documents" / "_audit"

# §5-4 1:1 매핑 7쌍 (governance-runbook_v1 §5-4 표 기반)
MAPPING = [
    ("d5-privacy-policy.md",       "privacy-policy_v1.md"),
    ("d6-terms-of-service.md",     "terms-of-service_v1.md"),
    ("d3-community-guideline.md",  "community-guideline_v1.md"),
    ("d5-cookie-policy.md",        "cookie-policy_v1.md"),
    ("d5-location-terms.md",       "location-terms_v1.md"),
    ("d3-youth-protection.md",     "youth-protection_v1.md"),
    ("d3-ugc-operation.md",        "ugc-operation_v1.md"),
]

# 핵심 조문 (governance-runbook §5-4 분기 점검 대상)
# 실문서 count ≥ 템플릿 count 이어야 한다.
CORE_ARTICLES = [
    r"§14-2",
    r"§22-2",
    r"§28-8",
    r"§37-2",
    r"§44-2",
    r"§44-3",
    r"§25조의2",
    r"§17",
]

# 시행일·법률번호 앵커
ANCHORS = [
    r"2024-10-16",
    r"법률\s*제\s*20494호",
]


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text))


def scan_pair(template_name: str, doc_name: str) -> dict:
    tpl_path = TEMPLATES_DIR / template_name
    doc_path = DOCS_DIR / doc_name
    result = {
        "template": template_name,
        "document": doc_name,
        "template_exists": tpl_path.exists(),
        "document_exists": doc_path.exists(),
        "drift": [],
        "article_diff": {},
        "anchor_diff": {},
    }

    if not tpl_path.exists():
        result["drift"].append(f"템플릿 부재: {template_name}")
    if not doc_path.exists():
        result["drift"].append(f"실문서 부재: {doc_name}")
    if not (tpl_path.exists() and doc_path.exists()):
        return result

    tpl_text = tpl_path.read_text(encoding="utf-8", errors="ignore")
    doc_text = doc_path.read_text(encoding="utf-8", errors="ignore")

    for art in CORE_ARTICLES:
        tpl_n = count_pattern(tpl_text, art)
        doc_n = count_pattern(doc_text, art)
        result["article_diff"][art] = {"tpl": tpl_n, "doc": doc_n}
        if tpl_n > 0 and doc_n < tpl_n:
            result["drift"].append(
                f"{art} 커버리지 부족: 템플릿 {tpl_n}회 vs 실문서 {doc_n}회"
            )

    for anchor in ANCHORS:
        tpl_n = count_pattern(tpl_text, anchor)
        doc_n = count_pattern(doc_text, anchor)
        result["anchor_diff"][anchor] = {"tpl": tpl_n, "doc": doc_n}
        if tpl_n > 0 and doc_n == 0:
            result["drift"].append(
                f"앵커 누락: `{anchor}` 템플릿 있음 · 실문서 0회"
            )

    return result


def iso_yearweek(d: dt.date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}{w:02d}"


def render_report(results: list[dict], mode: str) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    total_drift = sum(len(r["drift"]) for r in results)
    pair_drift = sum(1 for r in results if r["drift"])
    status = "drift 0건" if total_drift == 0 else f"drift {total_drift}건 / {pair_drift}쌍"

    lines = [
        f"# 템플릿↔실문서 동기화 리포트 ({mode})",
        f"",
        f"- 생성: {now}",
        f"- 대상: {len(results)}쌍 (§5-4)",
        f"- 상태: **{status}**",
        f"",
        f"## 쌍별 결과",
        f"",
        f"| 템플릿 | 실문서 | 상태 | 비고 |",
        f"|---|---|---|---|",
    ]
    for r in results:
        st = "✅ ok" if not r["drift"] else f"⚠️ {len(r['drift'])}건"
        note = ""
        if not r["template_exists"]:
            note = "템플릿 부재"
        elif not r["document_exists"]:
            note = "실문서 부재"
        elif r["drift"]:
            note = r["drift"][0][:40]
        lines.append(f"| `{r['template']}` | `{r['document']}` | {st} | {note} |")


    if total_drift > 0:
        lines += ["", "## Drift 상세", ""]
        for r in results:
            if not r["drift"]:
                continue
            lines.append(f"### `{r['document']}` ← `{r['template']}`")
            for d in r["drift"]:
                lines.append(f"- {d}")
            lines.append("")

    lines += [
        "## 조문 커버리지 매트릭스",
        "",
        "| 실문서 | " + " | ".join(CORE_ARTICLES) + " |",
        "|---" * (len(CORE_ARTICLES) + 1) + "|",
    ]
    for r in results:
        if not (r["template_exists"] and r["document_exists"]):
            continue
        row = [f"`{r['document']}`"]
        for art in CORE_ARTICLES:
            d = r["article_diff"].get(art, {"tpl": 0, "doc": 0})
            cell = f"{d['doc']}/{d['tpl']}"
            if d["tpl"] > 0 and d["doc"] < d["tpl"]:
                cell = f"**⚠️{cell}**"
            row.append(cell)
        lines.append("| " + " | ".join(row) + " |")


    lines += [
        "",
        "*(셀 값 = 실문서 / 템플릿 count · ⚠️ = 커버리지 부족)*",
        "",
        "## 액션",
        "- drift 0건: 유지 · 다음 주간 스캔 대기",
        "- drift 감지: governance-runbook §7 에스컬레이션 · 같은 PR에서 동기화",
        "- 템플릿·실문서 경로 불일치: §5-4 매핑표 업데이트",
    ]
    return "\n".join(lines)


def main() -> int:
    global DOCS_DIR, AUDIT_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--weekly", action="store_true", help="주간 모드 (리포트 경로 자동)")
    ap.add_argument("--report", type=str, help="리포트 저장 경로 (상대=ROOT 기준)")
    ap.add_argument("--fail-on-drift", action="store_true", help="drift 감지 시 exit 1")
    ap.add_argument("--docs-dir", type=str, default=None,
                    help="운영 문서 디렉토리 경로 (예: ~/VAULT/projects/cre8orclub/_policy-docs). 미지정 시 스킬 루트 하위 documents/ 사용")
    args = ap.parse_args()
    if args.docs_dir:
        DOCS_DIR = Path(args.docs_dir).expanduser().resolve()
        AUDIT_DIR = DOCS_DIR / "_audit"

    mode = "weekly" if args.weekly else "ondemand"
    results = [scan_pair(t, d) for t, d in MAPPING]
    report = render_report(results, mode)
    print(report)


    out_path = None
    if args.report:
        out_path = Path(args.report)
        if not out_path.is_absolute():
            out_path = ROOT / args.report
    elif args.weekly:
        yw = iso_yearweek(dt.date.today())
        out_path = AUDIT_DIR / f"template_sync_{yw}.md"

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"\n[저장] {out_path.relative_to(ROOT)}")

    total_drift = sum(len(r["drift"]) for r in results)
    if args.fail_on_drift and total_drift > 0:
        print(f"\n[FAIL] drift {total_drift}건 감지", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
