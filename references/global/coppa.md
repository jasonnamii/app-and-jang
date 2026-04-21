# COPPA (Children's Online Privacy Protection Act, US)

## 트리거
`--global=coppa` · 13세 미만 미국 유저 대상 · Directed-to-Children 서비스

## 최신 규제 동향 — 2026-04-22 전면 시행
FTC가 2025-04-22 관보 게재한 **COPPA Rule Final Amendments** (16 CFR Part 312)가 **2026-04-22 full compliance** 기준으로 발효. 기존 스몰 비즈니스 유예 종료.

### 이번 개정 핵심 5건
1. **Separate Opt-in for 3rd-party Disclosure** — 타깃광고·외부 공유에 별도 동의 필수 (수집 동의와 분리)
2. **Data Retention Written Policy** — 보유기간·삭제 기준 문서화 및 공개 의무 (목적 초과 보관 ✗)
3. **Security Program Mandatory** — 관리적·기술적·물리적 보호조치 프로그램 구축·유지·문서화
4. **Expanded PII Definition** — 생체인식 데이터(음성·영상·얼굴)·정부 발급 식별자 추가
5. **VPC(Verifiable Parental Consent) 방법 확대** — Knowledge-based auth · Text-plus · Government ID matching 명시

## 핵심 의무 (상시)
- **Notice** — 정책 최상단에 수집·이용·공유 항목 고지
- **VPC** — 수집 前 검증가능한 부모 동의 확보
- **Access & Deletion** — 부모 열람·삭제 요청 응답
- **Safe Harbor Programs** — FTC 승인 프로그램(kidSAFE·iKeepSafe·PRIVO·ESRB) 가입 시 면책 추정
- **집행** — FTC + 주 법무장관 · 위반당 최대 **$53,088** (2025 조정치)

## Cre8orClub 매핑
- **15세 이상 정책** → 13세 미만 가입 차단 (연령 게이트 의무)
- **미국 스토어 제출 시** → "Children Under 13: No" 체크 필수
- **글로벌 오버레이 적용 시** (미국 서비스 확장 시나리오)
  - 별도 동의 UI 설계 (타깃광고 분리 opt-in)
  - Data Retention Policy 별도 조항 삽입
  - VPC 플로우 구현 (credit card $0.50 차지 · Government ID 매칭 등)
  - Security Program 문서화 (a5-security 연동)

## 레퍼런스
- 16 CFR Part 312 (Children's Online Privacy Protection Rule)
- FTC Final Rule (2025-04-22 관보 게재 · 2026-04-22 전면 시행)
- FTC Six-Step Compliance Plan
