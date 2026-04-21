# app-and-jang

🇺🇸 [English README](./README.md)

**앱앤장 Engine v2.2 — 앱 정책·법적 고지문서 허브. 7도메인 × 4지식축 + α 7엔진(처분례·판례룰·벤치마크·레이더·심사관·시나리오·각주). 진단·생성·검토·각주 4모드. 한국법 디폴트. "김앤장 10배 증폭기" 포지셔닝.**

## 전제

- **Claude Cowork 또는 Claude Code** 환경
- 한국법 컨텍스트 (개보법 2023 전부개정·AI기본법 2026·플랫폼 공정경쟁촉진법 등)

## 목적

앱 법정의무문서(이용약관·개인정보처리방침·커뮤니티정책 등)의 **진단·초안·각주·검토**를 리스크 스코어·처분례 인용·무효확률 추정과 함께 제공. **법률자문 대체 ✗** — 변호사의 속도·정보밀도 증폭기.

## 발동 조건 · 사용법

P1 트리거(앱앤장/앱정책/앱법무/이용약관/개인정보처리방침 등) + 4모드 동사(만들어줘·검토해줘·진단해줘·각주달아줘) 중 하나로 호출. **디폴트 프로파일=Cre8orClub**. **KISAS**는 `--profile=kisas` — 3대 맹점(학원법·SBT 파기권·IP홀딩스귀속) 경고 자동 삽입.

## 사용 시나리오

| 시나리오 | 프롬프트 | 동작 |
|---|---|---|
| 기존 개인정보처리방침 진단 | `"개인정보처리방침 진단해줘"` | M1 → 리스크스코어 + 처분례 + 무효확률 델타 |
| 이용약관 신규 초안 | `"이용약관 만들어줘"` | M2 → 조항별 [근거]/[벤치마크]/corpus_id 표기 |
| Before/After diff 검토 | `"UGC 라이선스 수정안 검토해줘"` | M3 → 3열 diff + 무효확률 델타 |
| 기존 약관에 각주만 | `"이 약관에 각주달아줘"` | M4 → 오버레이 각주만, 원문 보존 |
| KISAS 맞춤 | `"--profile=kisas SBT 약관 만들어줘"` | 3대 맹점 경고 + `d1-ugc-license-kisas.md` 템플릿 |

## 핵심 기능

- **7도메인** — 콘텐츠·IP / 플랫폼 / 커뮤니티 / 거래 / 개인정보 / 사업자고지 / 앱마켓
- **α 7엔진** — 처분례·판례·벤치마크·레이더·심사관·분쟁·각주 통계 추정
- **2 프로파일** — Cre8orClub (디폴트, closed beta) + KISAS (pre-launch, 교육·소셜·창작·IP·K-pop)
- **KISAS 자동 경고** — 학원법 / SBT 파기권 / IP홀딩스귀속 3건 산출물 서두·체크리스트에 강제 주입
- **self-check** — `scripts/validate.py` 6체크 (크기·네이밍·섹션·evals·구문)
- **8 evals** — 일반 5 + KISAS 3 케이스

## 연동

- **[contract-reviewer](https://github.com/jasonnamii/contract-reviewer)** — B2B 계약 (본 스킬은 앱 대면 법정의무문서 전담)
- **[policy-planning](https://github.com/jasonnamii/policy-planning)** — 정책기획
- **[bp-guide](https://github.com/jasonnamii/bp-guide)** — 사업계획서

## 설치

```bash
git clone https://github.com/jasonnamii/app-and-jang.git ~/.claude/skills/app-and-jang
```

## 업데이트

```bash
cd ~/.claude/skills/app-and-jang && git pull
```

`~/.claude/skills/` 하위 스킬은 Claude Code·Cowork 세션에서 자동 사용 가능합니다.

## 마이그레이션

이전 이름: [`app-policy`](https://github.com/jasonnamii/app-policy) (archived). v2.2에서 "김앤장 10배 증폭기" 포지셔닝 + 2-프로파일(Cre8orClub+KISAS) 체제로 재편하면서 `app-and-jang`으로 rename.

## Cowork 스킬 제품군

25+ 커스텀 스킬 중 하나. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

개인·내부용. 법률 서비스 ✗.
