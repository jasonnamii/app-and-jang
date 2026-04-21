#!/usr/bin/env python3
"""
app-policy audit 엔진
사용: python audit.py --profile=cre8orclub --domains=all
출력: 누락문서·Red/Yellow/Green 판정표 (Markdown)
"""
import argparse
import json
import sys
from pathlib import Path

DOMAINS = {
    "D1": "콘텐츠·IP",
    "D2": "플랫폼 사업자",
    "D3": "관계·커뮤니티",
    "D4": "수익·거래",
    "D5": "개인정보",
    "D6": "사업자 고지",
    "D7": "플랫폼 준수",
}

PROFILES = {
    "cre8orclub": {
        "active_domains": ["D1", "D2", "D3", "D5", "D6", "D7"],
        "slot_domains": ["D4"],
        "global": ["gdpr", "dmca", "jasrac", "pipl"],
        "age": "15+",
        "ugc": True,
    },
}

REQUIRED_DOCS = {
    "D1": ["UGC 저작권 조항", "퍼블리시티 고지"],
    "D2": ["청소년보호정책", "Notice&Takedown 정책", "커뮤니티 운영정책"],
    "D3": ["커뮤니티 가이드라인", "제재 기준"],
    "D4": ["결제·환불·청약철회", "정산 약관"],
    "D5": ["개인정보처리방침(12항목)", "수집·이용 동의서", "마케팅 수신동의", "해외이전 동의", "CPO 지정"],
    "D6": ["이용약관", "사업자정보 표시", "통신판매업 신고"],
    "D7": ["앱스토어 처리방침 URL", "구글플레이 데이터 안전", "앱 권한 고지", "연령등급"],
}


def audit(profile_name, domains_arg, existing_docs=None):
    profile = PROFILES.get(profile_name)
    if not profile:
        print(f"❌ 알 수 없는 프로파일: {profile_name}")
        sys.exit(1)

    targets = profile["active_domains"] if domains_arg == "all" else domains_arg.split(",")
    existing = set(existing_docs or [])

    rows = []
    for dom in targets:
        docs = REQUIRED_DOCS.get(dom, [])
        for doc in docs:
            status = "✅ Green" if doc in existing else "🔴 Red (누락)"
            rows.append((dom, DOMAINS[dom], doc, status))

    # 슬롯 경고
    slot_rows = []
    for dom in profile.get("slot_domains", []):
        docs = REQUIRED_DOCS.get(dom, [])
        for doc in docs:
            slot_rows.append((dom, DOMAINS[dom], doc, "⚪ Slot (수익화시 활성)"))

    return rows, slot_rows, profile


def render_md(rows, slot_rows, profile):
    out = ["# App Policy Audit Report\n"]
    out.append(f"**프로파일:** Cre8orClub | **연령:** {profile['age']} | **UGC:** {profile['ugc']}\n")
    out.append(f"**글로벌 오버레이 권장:** {', '.join(profile['global'])}\n")
    out.append("\n## 활성 도메인\n")
    out.append("| 도메인 | 영역 | 문서 | 상태 |")
    out.append("|------|------|------|------|")
    for r in rows:
        out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    if slot_rows:
        out.append("\n## 슬롯 도메인 (수익화시 활성)\n")
        out.append("| 도메인 | 영역 | 문서 | 상태 |")
        out.append("|------|------|------|------|")
        for r in slot_rows:
            out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    red_count = sum(1 for r in rows if "Red" in r[3])
    out.append(f"\n## 요약\n- 🔴 Red(누락): {red_count}건\n- ✅ Green(완비): {len(rows) - red_count}건")
    out.append("\n---\n⚠️ 법률자문 대체 ✗ — 참고용. 변호사 최종검토 필수.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="cre8orclub")
    ap.add_argument("--domains", default="all")
    ap.add_argument("--existing", default="")
    ap.add_argument("--format", default="md", choices=["md", "json"])
    args = ap.parse_args()

    existing = [s.strip() for s in args.existing.split("|") if s.strip()]
    rows, slot_rows, profile = audit(args.profile, args.domains, existing)

    if args.format == "json":
        print(json.dumps({"rows": rows, "slot_rows": slot_rows, "profile": profile}, ensure_ascii=False, indent=2))
    else:
        print(render_md(rows, slot_rows, profile))


if __name__ == "__main__":
    main()
