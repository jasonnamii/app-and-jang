# app-and-jang

🇰🇷 [한국어 README](./README.ko.md)

**App & Jang (앱앤장) Engine v2.2 — Korean app legal/policy doc hub. 7 domains × 4 knowledge axes + α 7 engines (enforcement corpus · precedent rules · benchmark · regulatory radar · examiner heuristics · dispute scenarios · footnote). 4 modes: audit · draft · review · footnote. Korean law default. Positioned as a 10× amplifier on top of top-tier legal counsel.**

## Prerequisites

- **Claude Cowork or Claude Code** environment
- Korean legal context (Personal Info Protection Act 2023, AI Framework Act 2026, Platform Fair Competition Act, etc.)

## Goal

Draft, audit, and annotate Korean app legal documents (Terms of Service, Privacy Policy, Community Policy, etc.) with built-in risk scoring, enforcement corpus citations, and invalidity probability estimates. Not a replacement for legal counsel — it's a speed + density amplifier for your lawyer.

## When & How to Use

Trigger by explicitly invoking one of: 앱앤장, 앱정책, 앱법무, 이용약관, 개인정보처리방침, or one of the 4 mode verbs (만들어줘/검토해줘/진단해줘/각주달아줘). Default profile: **Cre8orClub**. For **KISAS**, add `--profile=kisas` — this auto-injects the 3 critical warnings (Academy Law / SBT right-to-erasure conflict / IP holdings assignment).

## Use Cases

| Scenario | Prompt | What Happens |
|---|---|---|
| Audit existing Privacy Policy | `"개인정보처리방침 진단해줘"` | M1 mode → risk score + enforcement precedents + invalidity delta |
| Draft ToS from scratch | `"이용약관 만들어줘"` | M2 mode → clause-by-clause with [근거]/[벤치마크]/corpus_id |
| Review Before/After diff | `"UGC 라이선스 수정안 검토해줘"` | M3 mode → 3-column diff with invalidity probability delta |
| Footnote existing document | `"이 약관에 각주달아줘"` | M4 mode → overlay annotations only, original text preserved |
| KISAS-specific review | `"--profile=kisas SBT 약관 만들어줘"` | Auto-injects 3 warnings + uses `d1-ugc-license-kisas.md` template |

## Key Features

- **7 Domains** — Content/IP, Platform, Community, Commerce, Privacy, Disclosure, Store compliance
- **α 7 Engines** — Statistical risk via enforcement corpus, precedent rules, benchmarks, regulatory radar, examiner heuristics, dispute scenarios, footnote synthesis
- **2 Profiles** — Cre8orClub (default, closed beta) + KISAS (pre-launch edu/social/IP/K-pop platform)
- **KISAS Auto-Warnings** — 3 critical blind spots auto-injected into every output (Hakwon Act, SBT erasure, IP holdings)
- **Self-Check** — `scripts/validate.py` enforces SKILL.md size, domain naming, required sections, evals, script syntax
- **8 Evals** — 5 general + 3 KISAS-specific test cases in `evals/cases.json`

## Works With

- **[contract-reviewer](https://github.com/jasonnamii/contract-reviewer)** — B2B contracts (this skill handles app-facing legal docs only)
- **[policy-planning](https://github.com/jasonnamii/policy-planning)** — Public policy proposals
- **[bp-guide](https://github.com/jasonnamii/bp-guide)** — Business plans

## Installation

```bash
git clone https://github.com/jasonnamii/app-and-jang.git ~/.claude/skills/app-and-jang
```

## Update

```bash
cd ~/.claude/skills/app-and-jang && git pull
```

Skills placed in `~/.claude/skills/` are automatically available in Claude Code and Cowork sessions.

## Migration Note

This skill was previously published as [`app-policy`](https://github.com/jasonnamii/app-policy) (archived). v2.2 renamed to `app-and-jang` to reflect the "10× 김앤장" positioning and dual-profile (Cre8orClub + KISAS) support.

## Part of Cowork Skills

This is one of 25+ custom skills. See the full catalog: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

Personal/internal use. Not a legal service.
