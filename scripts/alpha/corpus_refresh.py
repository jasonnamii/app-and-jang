#!/usr/bin/env python3
"""
α L5 — 코퍼스 자동갱신 스케줄러 (MVP 스캐폴딩)
- PIPC·FTC·KCA 공개 RSS/페이지 폴링
- diff 감지 → 새 항목 JSON 저장
- v2.0: --dry-run (수동 갱신 보조)
- v2.1: cron 자동화

공공누리 4유형 준수 — 메타데이터만 저장, 원문 ✗
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

SOURCES = {
    "pipc": "https://pipc.go.kr",  # 개인정보위 처분공개
    "ftc":  "https://ftc.go.kr",   # 공정위 의결
    "kcc":  "https://kcc.go.kr",   # 방통위
    "kca":  "https://kca.go.kr",   # 소비자원
    "kopico": "https://kopico.go.kr",  # 분쟁조정위
}

CORPUS_DIR = Path(__file__).parent.parent.parent / "references" / "alpha" / "_corpus"


def scan_source(key: str, url: str, dry_run: bool = True) -> dict:
    """단일 소스 스캔. v2.0은 scaffold, 실제 구현은 v2.1."""
    # TODO v2.1: requests·bs4 구현
    return {
        "source": key,
        "url": url,
        "scanned_at": datetime.utcnow().isoformat() + "Z",
        "new_items": 0,
        "status": "DRY_RUN" if dry_run else "TODO_IMPLEMENTATION",
    }


def main():
    parser = argparse.ArgumentParser(description="α L5 Corpus Refresh")
    parser.add_argument("--source", default="pipc,ftc,kca",
                        help="쉼표 구분 소스 (pipc,ftc,kcc,kca,kopico)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default=str(CORPUS_DIR), help="코퍼스 디렉터리")
    args = parser.parse_args()

    sources = [s.strip() for s in args.source.split(",") if s.strip()]
    unknown = [s for s in sources if s not in SOURCES]
    if unknown:
        print(f"ERROR: Unknown sources: {unknown}", file=sys.stderr)
        print(f"Available: {list(SOURCES.keys())}", file=sys.stderr)
        sys.exit(2)

    Path(args.output).mkdir(parents=True, exist_ok=True)

    total_new = 0
    for key in sources:
        result = scan_source(key, SOURCES[key], dry_run=args.dry_run)
        print(f"[{result['source']}] {result['status']} — new: {result['new_items']}")
        total_new += result["new_items"]

    print(f"\nTOTAL: {total_new} 신규 항목")
    if args.dry_run:
        print("(dry-run: 실제 폴링 미수행. v2.1에서 requests/bs4 구현)")


if __name__ == "__main__":
    main()
