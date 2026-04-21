# app-policy — REFERENCES 인덱스

SKILL.md에서 분리된 상세 참조표. on-demand 로드 전용.

---

## 7도메인 상세 매핑 (실파일 정합)

| # | 도메인 | 파일 | 필수도 | Cre8orClub | 핵심 법령 |
|---|-------|------|------|-----------|---------|
| D1 | **콘텐츠·IP** | `domains/d1-content-ip.md` | ✓ | ✓ | 저작권법·상표법·부정경쟁방지법·퍼블리시티 |
| D2 | **플랫폼 사업자** | `domains/d2-platform.md` | ✓ | ✓ | 정통망법 §44-7·N번방법·OSP 면책·DMCA |
| D3 | **관계·커뮤니티** | `domains/d3-community.md` | ✓ | ✓ | 정통망법·N번방법·딥페이크법·성폭력처벌법 |
| D4 | **수익·거래** | `domains/d4-commerce.md` | 수익화시 | △ (슬롯) | 전상법·전금법·약관규제법·콘진법 |
| D5 | **개인정보** | `domains/d5-privacy.md` | ✓ | ✓ | 개보법(2023 전부개정)·정통망법·위치법 |
| D6 | **사업자 고지** | `domains/d6-disclosure.md` | ✓ | ✓ | 약관규제법·전상법·정통망법 |
| D7 | **플랫폼 준수(앱마켓)** | `domains/d7-store.md` | 배포시 | ✓ | Apple App Review·Google Play Policy |

---

## α 7엔진 전체 스포크

| 엔진 | 역할 | 파일 |
|------|------|------|
| α1 처분례 코퍼스 | 개인정보위·공정위·방통위 처분례 300+건 DB. 빈도·평균 과징금·조항 매핑 | `alpha/a1-enforcement-corpus.md` |
| α2 판례 룰엔진 | 무효 판결 룰 → Base 60% + 가감. 무효확률 출력 | `alpha/a2-precedent-rules.md` |
| α3 벤치마크 DB | 토스·카카오·네이버·당근·배민·쿠팡 Top 20 앱 TOS·PP 자동폴링 | `alpha/a3-benchmark-db.md` |
| α4 규제 레이더 | PIPC·FTC·방통위·국회 월간 스캔. 6개월 선행지표 | `alpha/a4-regulatory-radar.md` |
| α5 심사관 휴리스틱 | 공식 가이드 외 실무 휴리스틱 30개. **BETA** | `alpha/a5-examiner-heuristics.md` |
| α6 분쟁 시나리오 | 26+ 분쟁 패턴 → 5대 카테고리. 가드레일 20문구 + 7-Phase 프리모템 | `alpha/a6-dispute-scenarios.md` |
| α7 각주 자동화 | α1~α6 통합 인덱싱. 인라인 각주·리스크·과징금·무효확률 자동 삽입 | `alpha/a7-footnote-engine.md` |

---

## 4지식축

| 축 | 내용 | 파일 |
|----|------|------|
| a1 | 법령 | `axes/a1-laws.md` |
| a2 | 판례 | `axes/a2-cases.md` |
| a3 | 행정처분 | `axes/a3-sanctions.md` |
| a4 | 템플릿 | `axes/a4-templates.md` |
| a5 | 글로벌 오버레이 | `axes/a5-global.md` |

---

## 글로벌 오버레이 (`--global=` 시만 로드)

`global/` 하위: `gdpr.md` · `dmca.md` · `jasrac.md` · `pipl.md` · `coppa.md` · `ccpa.md`

---

## 템플릿·체크리스트

- `templates/d{1..7}-*.md` — 도메인별 약관·정책 템플릿
- `checklist/d{1..7}-*.md` — 도메인별 출시 체크리스트
- `checklist/cre8orclub-launch.md` — 프로젝트별 런칭 체크리스트 샘플

---

## 프로파일

- `profiles/SCHEMA.md` — 프로파일 스키마 정의
- `profiles/cre8orclub.md` — 디폴트 프로파일

---

## 방어선 (6레이어)

| L | 이름 | 담당 |
|---|------|------|
| L0 | Governance | `references/governance/*` (PM·PR·CI) |
| L1 | PM | PREFLIGHT 4체크·프로파일 스키마·런북 §3 |
| L2 | PR | `pr-governance_v1.md` 체크리스트·트리거 동기화 |
| L3 | CI | `trigger_scan.py` · `governance_audit.py` · `audit.py` |
| L4 | α 코퍼스 무결성 | `alpha/footnote_validator.py` (FAIL=차단) |
| L5 | α 자동갱신 | `alpha/corpus_refresh.py` (월 1회 PIPC·FTC·법원) |

---

## CI 명령 전수

```bash
# 스킬 self-check (v2.1 신규)
python scripts/validate.py --skill-dir=./

# 프로젝트 감사 (경로 인자 명시, 규칙 15)
python scripts/audit.py --profile=cre8orclub --domains=all
python scripts/governance_audit.py --docs-dir=/path/to/project/docs --launches-dir=/path/to/project/launches
python scripts/trigger_scan.py

# α
python scripts/alpha/footnote_validator.py --input=draft.md
python scripts/alpha/corpus_refresh.py --source=pipc,ftc,kca --dry-run

# 템플릿 동기 (v1.x)
python scripts/template_sync_scan.py
```

**긴급 우회:** `documents/emergency-bypass-log_v1.md`에 사유·복구일자 기록. **연 3회 초과=재설계 트리거.**

---

## α 점수 모델 상세 공식

### 리스크스코어 구간
- **저(0~25)**: 처분례 0건 + 무효확률 <50% + 분쟁 시나리오 ✗
- **중(26~50)**: 처분례 1~5건 OR 무효확률 50~70% OR 시나리오 1건
- **고(51~75)**: 처분례 5~20건 OR 무효확률 70~85% OR 시나리오 2~3건
- **극高(76~100)**: 처분례 20+건 OR 무효확률 85%+ OR 시나리오 4+건

### 무효확률 (α2 룰엔진)
```
Base = 60% (한국 법원 약관 무효판결 평균)
가산: +15% (명백 불공정), +10% (최근 5년 유사 무효판례), +5% (조항 범위 광범위)
감산: -15% (명시동의), -10% (30일 사전공지), -5% (구체 근거법령)
```

### 과징금 기대값
```
E[X] = Σ (해당 처분례 발생빈도 × 평균 과징금액 × 사례적합도)
```

---

## 호출 예시

- "이용약관 만들어줘" → M2·D6·α7 On
- "개인정보처리방침 진단해줘" → M1·D5·α1+α2+α6
- "이 약관에 각주만 달아줘" → M4·α7 only
- "김앤장 의견서 형식" → M2 + `--format=opinion-letter`
- "런칭 법정의무문서 점검" → M1 + `governance_audit.py --docs-dir=` + α 전체
- "최근 6개월 규제 레이더" → α4 단독

---

## Migration

- **v1.x → v2.0:** Breaking ✗. α 디폴트 On (M1/M2). M3 옵션·M4 신규.
- **v2.0 → v2.1:** Breaking ✗. 도메인 네이밍 실파일 정합·`validate.py` 추가·`governance_audit` 경로 인자화(`--docs-dir` / `--launches-dir`)·SKILL.md 슬림(15→10KB)·evals/cases.json 신규.
