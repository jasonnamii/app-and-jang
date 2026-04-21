---
name: app-and-jang
description: |
  앱 정책·법적 고지문서 v2.2 "앱앤장". 7도메인×4축 + α 7엔진(처분례·판례룰·벤치마크·레이더·심사관·시나리오·각주). 진단·생성·검토·각주 4모드. 한국법 디폴트. 김앤장 10배 증폭기. 디폴트 프로파일=Cre8orClub, KISAS 프로파일 별도.
  P1: 앱앤장, appandjang, 앱정책, 앱법무, 앱컴플라이언스, 이용약관, 개인정보처리방침, 위치정보약관, 청소년보호정책, 커뮤니티정책, 쿠키정책, OSS고지, UGC저작권, 퍼블리시티, OSP면책, 앱스토어정책, 크리에이터약관, 팬플랫폼, 처분례, 판례룰, 벤치마크, 규제레이더, 심사관휴리스틱, 분쟁시나리오, 각주엔진, 과징금기대값, 무효확률, 김앤장, KISAS, Cre8orClub, SBT, 학원법, IP귀속, 홀딩스.
  P2: 만들어줘, 검토해줘, 진단해줘, 각주달아줘, draft, review, audit.
  P3: app compliance, app legal, privacy policy, enforcement corpus, footnote engine.
  P4: 런칭 전 법정의무문서 점검시, 약관 초안 작성시, 개보법 개정 반영시, 앱스토어 리젝 대응시, SBT·IP귀속·학원법 검토시.
  P5: 마크다운 출력, 각주인라인, 리포트 산출, 체크리스트 형식.
  NOT: B2B계약(→contract-reviewer), 정책기획(→policy-planning), BP(→bp-guide).
---

# App & Jang (앱앤장) Engine v2.2 "Regulatory Alpha"

앱 운영 **법적 고지문서**를 다루는 허브. **7도메인 × 4지식축 + α 7엔진**(처분례·판례·벤치마크·레이더·심사관·분쟁·각주)로 진단·생성·검토·각주합성. **법률자문 대체 ✗** — 참고용 초안·체크리스트·리스크 스코어링(과징금 기대값·무효확률)까지. 변호사 최종검토 필수. 포지셔닝: **김앤장 10배 증폭기**.

---

## 절대 규칙

| # | 규칙 | 이유 |
|---|------|------|
| 1 | **법률자문 경계** — 산출물 하단 디스클레이머 자동. 유효/무효 확정판단 ✗. α는 "통계적 추정" | 변호사법 §22 |
| 2 | **한국법 디폴트** — 개보법·정통망법·위치법·전금법·전상법(§21-2 다크패턴 2025-02-14)·청보법·저작권법·콘진법 On | 다수 사용자 한국 |
| 3 | **글로벌 플래그** — `--global=gdpr,dmca,jasrac,pipl,coppa,ccpa` 호출 시만 로드 | 토큰 예산 |
| 4 | **7도메인 독립 호출** — D1~D7 단일 호출 시 해당 스포크만 로드 | 강제 cascade 비효율 |
| 5 | **PREFLIGHT 4체크** — 모드·도메인·앱프로파일·기존문서유무 | 산출물 형태 결정 |
| 6 | **프로파일 디폴트** — 미지정 시 **Cre8orClub** 적용. KISAS는 `--profile=kisas`. 신규=`profiles/SCHEMA.md` 준수 | 2개 앱 동시 운영 |
| 7 | **최신 법령 주의** — 개보법 2023 전부개정(시행령 2025-03-13)·AI기본법 2026-01-22·플랫폼 공정경쟁촉진법 2025~2026. 검토시점·출처 명시 | 법령 변동 |
| 8 | **산출물 하단 고정** — 디스클레이머 + 업데이트 날짜 + 준거법 + 참조 법령/판례 출처 | 법적 추적성 |
| 9 | **트리거 4문서 동시개정** — T1~Tn 변경=SKILL.md·RELEASE_CRITERIA.md·pr-governance_v1.md·ci-governance_v1.md 동시. `trigger_scan.py` FAIL=차단 | 방어선 동기화 |
| 10 | **1회 핑퐁 최대** — 프로파일·도메인 확정 1회. 이후 강제실행 | 속도 |
| 11 | **α 코퍼스 무결성** — 인용은 corpus_id 필수. LLM 생성 사건번호 ✗. `footnote_validator.py` FAIL=차단 | Hallucination 방어 |
| 12 | **신뢰도 등급** — α 근거에 [신뢰도: 상/중/하]. 공식=상, 실무=중, 커뮤니티=하 | 사용자 검증권 |
| 13 | **BETA 라벨 강제** — α5 "중/하" 및 실험기능은 BETA + `--include-experimental` 필수 | 신뢰 경계 |
| 14 | **On-demand 로드** — references/ 60+ 파일 상시 로드 ✗. 도메인·α엔진은 필요시만 | 토큰 예산 |
| 15 | **governance_audit 대상 경로** — 감사 대상은 **프로젝트별 운영문서** (예: Cre8orClub 산출물). 스킬 내부 경로 ✗. `--docs-dir=<path>` / `--launches-dir=<path>` 명시 필수 | 스킬-프로젝트 분리 |
| 16 | **KISAS 특수 맹점 3건 자동 발동** — KISAS 프로파일 로드 시 ①학원법(오프라인 캠프 유상) ②SBT 파기권(온체인 개인식별) ③IP홀딩스귀속(표준 UGC 템플릿 불가) 세 맹점을 산출물 서두·체크리스트·리스크탭에 **무조건** 경고로 삽입. 누락=FAIL | 치명 리스크 보호 |

---

## 구조

```
app-policy/
├── SKILL.md                          ← 허브 (본 파일)
├── CHANGELOG.md
├── references/                       ← on-demand 로드 (규칙 14)
│   ├── domains/d{1..7}-*.md          ← 7 도메인 스포크 (상세: REFERENCES.md)
│   ├── axes/a{1..5}-*.md             ← 4지식축 + 글로벌
│   ├── alpha/a{1..7}-*.md            ← α 7엔진 스포크
│   ├── templates/                    ← 문서 템플릿
│   ├── checklist/                    ← 도메인별 체크리스트
│   ├── profiles/                     ← 프로젝트 프로파일 (SCHEMA+샘플)
│   └── global/                       ← GDPR·DMCA·JASRAC·PIPL·COPPA·CCPA
├── scripts/
│   ├── audit.py · trigger_scan.py · governance_audit.py
│   ├── review.py · generate.py · template_sync_scan.py
│   ├── validate.py                   ← self-check (v2.1 신규)
│   └── alpha/footnote_validator.py · corpus_refresh.py
├── documents/                        ← 스킬 운영 문서 (emergency-bypass 등)
└── evals/cases.json                  ← 4모드 샘플 (v2.1 신규)
```

**상세 파일 인덱스:** `→ references/REFERENCES.md`

---

## 7도메인 (실파일 정합)

| # | 도메인 | 파일 | 필수도 |
|---|-------|------|------|
| D1 | 콘텐츠·IP | `domains/d1-content-ip.md` | ✓ |
| D2 | 플랫폼 사업자 | `domains/d2-platform.md` | ✓ |
| D3 | 관계·커뮤니티 | `domains/d3-community.md` | ✓ |
| D4 | 수익·거래 | `domains/d4-commerce.md` | 수익화시 |
| D5 | 개인정보 | `domains/d5-privacy.md` | ✓ |
| D6 | 사업자 고지 | `domains/d6-disclosure.md` | ✓ |
| D7 | 플랫폼 준수(앱마켓) | `domains/d7-store.md` | 배포시 |

**도메인별 법령·스코프·Cre8orClub 관련 상세:** `→ references/REFERENCES.md`

---

## 4지식축 × α 7엔진

**4축:** 법령·판례·행정처분·템플릿 → `→ references/axes/a{1..5}-*.md`
**α 7엔진:** 처분례·판례룰·벤치마크·레이더·심사관·분쟁·각주 → `→ references/alpha/a{1..7}-*.md`
**α 상세표:** `→ references/REFERENCES.md §α`

**α 포지셔닝:** 김앤장 의견서를 문구 단위로 분해해 약관에 직조. **속도 30초 + 정보밀도 1.5~2x + 월간 자동갱신** 3축. 법적 면책(서명) = 인간 변호사 경로 존치.

---

## 모드 (M1~M4)

| 모드 | 역할 | 트리거 | 동원 엔진 |
|------|------|--------|---------|
| **M1 진단** | 기존문서 → 리스크 스캔 → 보완 | "진단해줘/검토해줘" | α1·α2·α6 |
| **M2 생성** | 프로파일·도메인 → 초안 | "만들어줘/draft" | α3·α6·α7(기본 On) |
| **M3 검토** | Before/After 3열 diff | "바꿔줘/review" | α2 (무효확률 델타) |
| **M4 α 각주** | 기존약관 → 각주 오버레이(문구수정 ✗) | "각주달아줘" | α7 only |

**출력 포맷 (M2/M4):**
```markdown
{약관 문구}
> [근거] {법조문}
> [리스크] {低/中/高/극高} · 과징금 기대값 ~{금액}
> [처분례] {기관 사건번호} [신뢰도: 상] (corpus_id: {ID})
> [판례] {법원 사건번호} [신뢰도: 상] (case_id: {ID})
> [벤치마크] {서비스 PP §X} (updated: {YYYY-MM-DD})
> [무효확률] {%} · [가드레일] "{권장 수정}"
```

---

## α 점수 모델 (요약)

**리스크스코어** 0~100 · **과징금 기대값** `E[X]=Σ(빈도×평균액×적합도)` · **무효확률** Base 60%±가감
**상세 공식·구간:** `→ references/REFERENCES.md §α 점수 모델`

---

## 방어선·CI

6레이어(L0 Governance → L5 α 자동갱신)·CI 명령·긴급 우회 규정: `→ references/REFERENCES.md §방어선·CI`

**핵심 CI 2줄:**
```bash
python scripts/validate.py              # 스킬 self-check (v2.1)
python scripts/audit.py --profile=cre8orclub --domains=all  # 프로젝트 감사
```

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 유효·무효 확정판단 요청 | 거부 + 변호사 권고 |
| 글로벌 오버레이 디폴트 로드 | 미지정=한국법. `--global=` 명시 |
| 판례·처분례 전수 요청 | 리딩 5~10건 + 링크목록 |
| 단일 문서 요청 시 타 도메인 생성 | 요청 도메인만. D6은 1줄 포인터 |
| 법령 개정 미반영 | 검토시점·출처 주석 |
| M3 원본 변형 | diff·3열·원본 보존 |
| α 사건번호 LLM 생성 | whitelist·미등록=차단 |
| α 무효확률 확정 단언 | "통계적 추정" 고정 |
| α5 BETA를 공식처럼 출력 | 플래그 없으면 "중/하" 숨김 |
| α 코퍼스 구버전 | `updated_at` 6개월+ 경고 |
| 변호사법 §22 경계 | "초안·탐지" 고수 |
| 긴급우회 남용 | 연 3회 초과=재설계 |
| 피드백 | 재발동 개선안은 thumbs-down으로 Anthropic |

---

## 디스클레이머 (산출물 하단 자동)

```
⚠️ 법률자문 대체 ✗ · 📅 {YYYY-MM-DD} · ⚖️ 대한민국(+오버레이 해당국) · 📚 {참조}
🔍 α 출력은 통계적 추정 · corpus_id 검증가능 · 변호사 최종검토 필수
```

---

## 호출 예시·Migration

호출 예시·Migration 노트·옵션 플래그: `→ references/REFERENCES.md §호출 예시·Migration`

**디폴트 비활성:** `--no-footnote` · `--no-alpha` · `--include-experimental`
