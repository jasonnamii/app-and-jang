#!/usr/bin/env python3
"""
app-policy review 엔진 (스텁)
사용: python review.py --file=existing_policy.md --domain=D5
출력: Before/After 3열 + 법적근거 태깅
"""
import argparse
import re
import sys
from pathlib import Path

# 개인정보처리방침 12항목 필수 키워드 (D5)
D5_REQUIRED_KEYWORDS = [
    "수집", "목적", "보유", "파기", "제3자", "위탁",
    "권리", "책임자", "변경", "안전", "쿠키", "고충",
]

RISK_PATTERNS = [
    (r"일방적.*변경", "약관법 §10 위반 가능 — 7일/30일 사전고지 필요", "Red"),
    (r"모든.*책임.*면제", "약관법 §7 면책조항 과도 — 무효 가능", "Red"),
    (r"영구히.*이용", "UGC 영구 이용권 과도 — 서비스 운영 목적 한정 권장", "Yellow"),
]


def review_d5(text):
    missing = [kw for kw in D5_REQUIRED_KEYWORDS if kw not in text]
    risks = []
    for pat, msg, level in RISK_PATTERNS:
        if re.search(pat, text):
            risks.append((level, msg, pat))
    return missing, risks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--domain", default="D5")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"❌ 파일 없음: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")

    if args.domain == "D5":
        missing, risks = review_d5(text)
        print("# Review Report\n")
        print(f"**파일:** {path.name}")
        print(f"**도메인:** {args.domain} 개인정보\n")
        print("## 누락 키워드 (12항목 기준)")
        if missing:
            for m in missing:
                print(f"- 🔴 {m}")
        else:
            print("- ✅ 12항목 모두 언급")
        print("\n## 리스크 패턴")
        if risks:
            for level, msg, pat in risks:
                icon = "🔴" if level == "Red" else "🟡"
                print(f"- {icon} {level}: {msg} (패턴: `{pat}`)")
        else:
            print("- ✅ 주요 리스크 패턴 미검출")
        print("\n---\n⚠️ 참고용 자동검토. 변호사 최종검토 필수.")
    else:
        print(f"TBD: {args.domain} 검토 로직 확장 필요")


if __name__ == "__main__":
    main()
