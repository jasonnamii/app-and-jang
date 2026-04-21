#!/usr/bin/env python3
"""
α L4 Defense — 각주 무결성 검증기
- corpus_id whitelist 검증 (hallucination 차단)
- 신뢰도 등급 누락 탐지
- 법령·판례 인용 형식 검증
- FAIL 시 exit 1 (CI/PR 차단)
"""
import re
import sys
import json
import argparse
from pathlib import Path

CORPUS_DIR = Path(__file__).parent.parent.parent / "references" / "alpha" / "_corpus"
CORPUS_ID_PATTERN = re.compile(r"corpus_id:\s*([A-Z0-9_]+)")
CASE_ID_PATTERN = re.compile(r"case_id:\s*([A-Z0-9_]+)")
RELIABILITY_PATTERN = re.compile(r"\[신뢰도:\s*(상|중|하)\]")
CITATION_PATTERN = re.compile(r"\[(처분례|판례|벤치마크|근거)\]")


def load_whitelist():
    """코퍼스 디렉터리에서 허용 ID 목록 수집."""
    ids = set()
    if not CORPUS_DIR.exists():
        return ids
    for f in CORPUS_DIR.glob("**/*.json"):
        try:
            data = json.loads(f.read_text())
            if isinstance(data, list):
                for item in data:
                    if "corpus_id" in item:
                        ids.add(item["corpus_id"])
                    if "case_id" in item:
                        ids.add(item["case_id"])
            elif isinstance(data, dict):
                if "corpus_id" in data:
                    ids.add(data["corpus_id"])
                if "case_id" in data:
                    ids.add(data["case_id"])
        except Exception:
            continue
    return ids


def validate(input_path: Path, whitelist: set, strict: bool = True) -> list:
    """입력 문서 스캔 → 오류 리스트 반환."""
    errors = []
    text = input_path.read_text()

    # 1. corpus_id whitelist 검증
    for m in CORPUS_ID_PATTERN.finditer(text):
        cid = m.group(1)
        if whitelist and cid not in whitelist:
            errors.append(f"UNKNOWN_CORPUS_ID: {cid}")

    for m in CASE_ID_PATTERN.finditer(text):
        cid = m.group(1)
        if whitelist and cid not in whitelist:
            errors.append(f"UNKNOWN_CASE_ID: {cid}")

    # 2. 인용에 신뢰도 등급 누락 탐지
    citations = CITATION_PATTERN.findall(text)
    reliabilities = RELIABILITY_PATTERN.findall(text)
    if strict and len(citations) > 0 and len(reliabilities) == 0:
        errors.append("MISSING_RELIABILITY_TAG: 인용 블록에 [신뢰도: 상/중/하] 필수")

    # 3. 확정 단언 탐지 (디스클레이머 라인 제외)
    forbidden_phrases = [
        (r"확실히\s*무효", "확실히 무효"),
        (r"법적으로\s*(유효|무효)", "법적으로 유효/무효"),
        (r"확정적", "확정적"),
        (r"변호사가\s*보장", "변호사가 보장"),
    ]
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("⚠️") or stripped.startswith("🔍") or "대체 ✗" in line:
            continue
        for pattern, label in forbidden_phrases:
            if re.search(pattern, line):
                errors.append(f"FORBIDDEN_PHRASE: {label}")

    # 4. 디스클레이머 존재 여부
    if "법률자문 대체 ✗" not in text and "변호사 최종검토" not in text:
        errors.append("MISSING_DISCLAIMER: 산출물 하단 디스클레이머 필수")

    return errors


def main():
    parser = argparse.ArgumentParser(description="α L4 Footnote Validator")
    parser.add_argument("--input", required=True, help="검증 대상 .md 파일")
    parser.add_argument("--strict", action="store_true", help="엄격 모드")
    parser.add_argument("--dry-run", action="store_true", help="whitelist 없이 실행 (초기 MVP)")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(2)

    whitelist = set() if args.dry_run else load_whitelist()
    errors = validate(path, whitelist, strict=args.strict)

    if errors:
        print(f"FAIL — {len(errors)} 오류", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK — {path.name} 검증 통과")


if __name__ == "__main__":
    main()
