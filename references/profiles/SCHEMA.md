# Profile Schema (신규 도메인 온보딩)

## 필수 필드

| 필드 | 타입 | 값 예시 | 영향 |
|---|---|---|---|
| 업종 | D1~D7 조합 | "D1·D3·D5" | 로딩할 스포크 결정 |
| 유저연령 | 선택지 | "14세미만 허용" / "15세+" / "19세+" | youth-protection·법정대리인 동의 로직 |
| UGC | bool | 있음 / 없음 | D1·D2·D3 cascade + OSP면책 |
| 수익모델 | T1~T8 조합 또는 "없음" | "T2·T4" / "없음(슬롯)" | monetization-triggers 활성화 범위 |
| 글로벌 | 플래그 조합 | "gdpr·pipl" | 오버레이 로딩 |
| 특이사항 | 자유텍스트 | — | 리스크 단문 |

## 파일 위치

`references/profiles/{profile-name}.md`

## Frontmatter 필수

```yaml
---
profile: {name}
schema_version: 1
industry: [D1, D3, D5]
age_min: 15
ugc: true
monetization: []
global_overlays: [gdpr]
last_updated: YYYY-MM-DD
---
```

## 프로파일 추가 절차

1. 이 SCHEMA.md 복사 → 신규 `.md` 생성
2. 필수 필드 전부 채움 (빈칸 = audit.py FAIL)
3. `python scripts/generate.py --profile={name} --all` — 4문서 초안 자동생성
4. `python scripts/audit.py --profile={name}` — Red/Yellow/Green 판정
5. `python scripts/governance_audit.py` — 트리거 정합성 cross-check

## Gotchas

- 14세미만 허용 프로파일 = 법정대리인 동의 로직 탑재 필수 (개보법 **§22-2** 우선, §22 동의 일반론 병행)
- 글로벌 오버레이 3개 초과 = audit 토큰 예산 초과 경고
- 기존 프로파일 수정 시 `last_updated` 갱신 누락 = governance_audit FAIL
