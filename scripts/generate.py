#!/usr/bin/env python3
"""
app-policy generate 엔진 (스텁)
사용: python generate.py --doc=privacy-policy --profile=cre8orclub
출력: 템플릿 기반 초안 (references/templates/ 활용)
"""
import argparse
import sys
from pathlib import Path

TEMPLATE_MAP = {
    # D1 콘텐츠·IP
    "ugc-license": "d1-ugc-license.md",
    "publicity": "d1-publicity-consent.md",
    # D2 플랫폼
    "takedown": "d2-takedown-policy.md",
    # D3 커뮤니티 (youth-protection은 D3 정본 사용)
    "community": "d3-community-guideline.md",
    "sanction": "d3-sanction-policy.md",
    "ugc-operation": "d3-ugc-operation.md",
    "youth": "d3-youth-protection.md",  # 정본
    # D5 개인정보
    "privacy-policy": "d5-privacy-policy.md",
    "cookie": "d5-cookie-policy.md",
    "location": "d5-location-terms.md",
    "marketing-consent": "d5-marketing-consent.md",
    "consent-form": "d5-consent-form.md",
    # D6 사업자 고지
    "terms": "d6-terms-of-service.md",
    "business-info": "d6-business-info.md",
    # D7 스토어
    "app-privacy-url": "d7-app-privacy-url.md",
    "data-safety": "d7-data-safety.md",
    "permissions": "d7-permissions.md",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True, choices=list(TEMPLATE_MAP.keys()))
    ap.add_argument("--profile", default="cre8orclub")
    args = ap.parse_args()

    tmpl_name = TEMPLATE_MAP[args.doc]
    tmpl_path = Path(__file__).parent.parent / "references" / "templates" / tmpl_name
    if not tmpl_path.exists():
        print(f"❌ 템플릿 없음: {tmpl_path}")
        sys.exit(1)

    content = tmpl_path.read_text(encoding="utf-8")
    # 프로파일 변수 치환은 추후 확장
    print(content)


if __name__ == "__main__":
    main()
