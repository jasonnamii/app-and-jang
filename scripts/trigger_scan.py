#!/usr/bin/env python3
"""
trigger_scan.py — Cre8orClub 수익화·광고·프로파일링 트리거 감지기

CI/로컬/프리커밋에서 코드베이스(또는 diff)를 스캔하여 T1~T8 트리거 해당 여부를
탐지한다. 하나라도 히트하면 exit 1 + monetization-triggers_v1 체크리스트 안내를
출력한다.

사용:
  python trigger_scan.py <코드 루트>               # 전체 스캔
  python trigger_scan.py --diff                    # git diff HEAD 스캔
  python trigger_scan.py --staged                  # git 스테이징 영역 스캔
  python trigger_scan.py --fail-on-match <루트>    # 히트 시 exit 1 (CI용)

통합 제안:
  - GitHub Actions: .github/workflows/policy.yml 에 pre-merge job
  - pre-commit: .pre-commit-config.yaml hook
  - Makefile: `make policy-check`
"""
from __future__ import annotations
import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Trigger:
    code: str
    title: str
    patterns: list[str]
    hits: list[tuple[str, int, str]] = field(default_factory=list)  # (path, lineno, line)


# 정규식은 대소문자 무시. 과탐을 허용하고 사람이 YES/NO로 확인.
TRIGGERS: list[Trigger] = [
    Trigger("T1", "결제·인앱결제·PG", [
        r"\bpurchase\b", r"\bpayment\b", r"\bbilling\b", r"\bcheckout\b",
        r"StoreKit", r"BillingClient", r"inapp", r"in-app",
        r"toss.?payments", r"iamport", r"kakao.?pay", r"naver.?pay",
    ]),
    Trigger("T2", "구독·자동갱신", [
        r"\bsubscription\b", r"\bsubscribe\b", r"auto.?renew", r"recurring",
        r"membership", r"premium.?tier",
    ]),
    Trigger("T3", "광고 송출", [
        r"\bAdMob\b", r"GoogleMobileAds", r"MobileAds",
        r"AudienceNetwork", r"FBAudienceNetwork", r"Meta.?Ads",
        r"\badsense\b", r"ad.?unit", r"sponsored", r"InterstitialAd",
        r"RewardedAd", r"BannerAd",
    ]),
    Trigger("T4", "개인화·프로파일링", [
        r"personalization", r"personalize", r"profiling",
        r"recommend(er|ation)", r"feed.?ranking",
        r"user.?embedding", r"interest.?vector", r"behavioral",
        r"targeting",
    ]),
    Trigger("T5", "광고 귀속·MMP", [
        r"AppsFlyer", r"\bAdjust\b", r"\bBranch\b(?!\s*\()",
        r"\bkochava\b", r"\bSingular\b",
        r"\battribution\b", r"\butm_source\b", r"\butm_campaign\b",
    ]),
    Trigger("T6", "크리에이터 수익·정산", [
        r"creator.?payout", r"settle(ment)?", r"disburse",
        r"revenue.?share", r"tip(ping)?", r"donation", r"fan.?funding",
        r"sponsor(ship)?",
    ]),
    Trigger("T7", "가상자산·토큰·NFT", [
        r"\bNFT\b", r"\btoken\b", r"ERC.?(20|721|1155)",
        r"web3", r"wallet.?connect", r"blockchain",
        r"crypto(currency)?", r"virtual.?asset",
    ]),
    Trigger("T8", "미성년자 데이터 경로", [
        r"under.?14", r"under.?19", r"minor.?user",
        r"청소년", r"미성년", r"age.?gate",
    ]),
]

# 스캔 대상 확장자 (텍스트성). 바이너리·미디어·로그는 제외.
INCLUDE_EXT = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".swift", ".m", ".mm", ".kt", ".kts", ".java",
    ".go", ".rs", ".rb", ".php", ".cs",
    ".json", ".yaml", ".yml", ".toml", ".gradle",
    ".plist", ".xml", ".html", ".vue", ".svelte",
}

# 스캔 제외 디렉토리
EXCLUDE_DIRS = {
    "node_modules", ".git", ".next", "build", "dist", "out",
    "Pods", "DerivedData", "vendor", "venv", ".venv",
    "__pycache__", ".mypy_cache", ".pytest_cache",
    ".claude", "_archive",
}


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in INCLUDE_EXT:
                yield p


def git_changed_files(mode: str) -> list[Path]:
    if mode == "diff":
        cmd = ["git", "diff", "--name-only", "HEAD"]
    elif mode == "staged":
        cmd = ["git", "diff", "--name-only", "--cached"]
    else:
        return []
    try:
        out = subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError:
        return []
    paths = []
    for line in out.splitlines():
        p = Path(line)
        if p.exists() and p.suffix.lower() in INCLUDE_EXT:
            paths.append(p)
    return paths


def scan_file(path: Path, triggers: list[Trigger]) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    for lineno, line in enumerate(text.splitlines(), 1):
        for t in triggers:
            for pat in t.patterns:
                if re.search(pat, line, re.IGNORECASE):
                    t.hits.append((str(path), lineno, line.strip()[:200]))
                    break  # 같은 트리거 중복 방지


def render_report(triggers: list[Trigger]) -> tuple[str, int]:
    total = sum(len(t.hits) for t in triggers)
    if total == 0:
        return "✅ 수익화·광고·프로파일링 트리거 미검출.\n", 0

    lines = ["⚠️ 트리거 감지됨 — monetization-triggers_v1 체크리스트 발동 필요", ""]
    for t in triggers:
        if not t.hits:
            continue
        lines.append(f"## {t.code}. {t.title}  (hits: {len(t.hits)})")
        for path, lineno, snippet in t.hits[:10]:
            lines.append(f"  {path}:{lineno}  {snippet}")
        if len(t.hits) > 10:
            lines.append(f"  ... +{len(t.hits) - 10} more")
        lines.append("")
    lines.append("다음 단계:")
    lines.append("  1) PM: documents/launch-template_v1.md 작성 (T 체크)")
    lines.append("  2) 법무: documents/monetization-triggers_v1.md D-30 착수")
    lines.append("  3) 정책 개정: ToS/Privacy/Cookie/UGCOP 해당 조항")
    return "\n".join(lines) + "\n", total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".", help="스캔 루트 (기본 현재 디렉토리)")
    ap.add_argument("--diff", action="store_true", help="git diff HEAD 만 스캔")
    ap.add_argument("--staged", action="store_true", help="git 스테이징 영역만 스캔")
    ap.add_argument("--fail-on-match", action="store_true", help="히트 시 exit 1 (CI용)")
    args = ap.parse_args()

    if args.diff:
        paths = git_changed_files("diff")
    elif args.staged:
        paths = git_changed_files("staged")
    else:
        paths = list(iter_files(Path(args.root)))

    for p in paths:
        scan_file(p, TRIGGERS)

    report, total = render_report(TRIGGERS)
    print(report)

    if total > 0 and args.fail_on_match:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
