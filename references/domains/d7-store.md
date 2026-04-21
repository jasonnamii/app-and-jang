# D7. 플랫폼 준수 (앱마켓) 도메인 (DEEP v1.0)

> **스코프**: Apple App Review·Google Play Policy·데이터안전·권한고지·연령등급. **배포 시 필수**. a1·a2·a3·a4 교차색인.

---

## 1. 핵심 가이드라인 (a1 매핑)

| 플랫폼 | 정책 문서 | 핵심 |
|---|---|---|
| Apple | App Store Review Guidelines | 5.1.1(개인정보), 5.1.2(데이터 수집), 1.2(UGC) |
| Apple | App Privacy | **Nutrition Label** 14 카테고리 자진 고지 |
| Google | Play Policy | Data Safety 섹션 **2022-07 의무화** |
| Google | Target API Level | 매년 상향 강제 (2026년 API 35+) |
| ATT (Apple) | AppTrackingTransparency | 트래킹 동의 팝업 **iOS 14.5+** |

> 한국법 교차: 개보법 §22-2(14세 미만 법정대리인 동의 우선) + §22(동의 일반) **이중 적용** (플랫폼 정책 + 국내법)

---

## 2. 리딩 이슈 (a2 매핑)

### D7-1. 인앱결제 강제 금지 (한국 vs Apple·Google)
- 전기통신사업법 §50-1 (2021 개정)
- 방통위 과징금 **630억** (2023-10) — **미집행 상태 2026-04 현재**
- **앱 함의**: 외부결제 링크 허용 여부 주기적 모니터링 필요

### D7-2. 앱 리뷰 거부 사유 — UGC·DRM
- Apple 5.1.2: 사용자 데이터 제3자 공유 시 명시 동의 필수
- Apple 1.2: UGC 앱은 신고 기능·모더레이션·사용자 차단 필수
- **앱 함의**: 크리에이터·팬 플랫폼은 **사용자 차단·신고·모더레이션 3종** 필수

### D7-3. ATT (AppTrackingTransparency)
- 2021-04 iOS 14.5부터 트래킹 사전 동의 팝업 의무
- 광고 SDK의 IDFA 수집 거부율 70%+ (2022~)
- **앱 함의**: 광고·분석 SDK 통합 시 ATT 팝업 구현 + 거부 시 대체 플로우

### D7-4. Data Safety (Google Play)
- 2022-07 의무화: 수집·공유·암호화 14 항목 자진 고지
- 허위 신고 시 앱 제거
- **앱 함의**: 처리방침과 **1:1 매칭** 필수 (불일치 = 심사 거부)

---

## 3. 행정·심사 동향 (a3 매핑)

| 기관 | 사안 | 규모 |
|---|---|---|
| 방통위 | 애플·구글 등 188사 일괄 제재 | 과징금·과태료 각 **8.56억** (2024-06-12) |
| 방통위 | 인앱결제 강제 | **630억 미집행** |
| Apple | App Review 심사 거부 | 평균 거부율 30%+ |
| Google | 정책 위반 앱 제거 | 연간 수만 건 |

> → a3-sanctions.md §2 방통위

---

## 4. 템플릿 (a4 매핑)

| 문서 | 1차 벤치 | 2차 벤치 | 공공 템플릿 |
|---|---|---|---|
| App Privacy URL | 네이버 | 카카오 | Apple 가이드 |
| Data Safety 시트 | 배민 | 당근 | Google Play 템플릿 |
| 권한 고지 문구 | 쿠팡 | 토스 | KISA 가이드 |
| 연령등급 심사 신청서 | — | — | 게임위 / GRAC |

> → templates/d7-data-safety.md · d7-permissions.md · d7-app-privacy-url.md
> → a4-templates.md §3.2·§3.3

---

## 5. Cre8orClub 특화 이슈

- **UGC 플랫폼 표시**: Apple 1.2 요구사항 5종 필수
  1. UGC 필터링 방법
  2. 게시물 신고 메커니즘
  3. 공격적 사용자 차단 기능
  4. 저작권 침해 신고 절차
  5. 모더레이션 정책 공개
- **권한 최소화**: 카메라·마이크·위치·연락처 — **사용 시점 요청** (pre-permission 금지)
- **연령등급**: 15세 이상 정책 → Apple 12+·Google Teen 해당 여부 확인
- **ATT 팝업**: 광고·분석 SDK 있으면 필수 구현
- **Data Safety ↔ 처리방침**: 100% 매칭 — D5와 버전 동기화

---

## 6. 도메인 체크리스트

### Apple
- [ ] App Privacy **Nutrition Label** 14개 카테고리 모두 기재
- [ ] App Privacy URL = 처리방침 URL (D5 동기화)
- [ ] ATT 팝업 (광고·분석 SDK 있을 시)
- [ ] Apple 1.2 UGC 5종 (필터·신고·차단·저작권·모더레이션)
- [ ] Sign in with Apple (다른 소셜로그인 있으면 의무)
- [ ] 연령등급 12+ 이상 설정

### Google Play
- [ ] Data Safety 14 카테고리
- [ ] Data Safety ↔ 처리방침 **1:1 매칭**
- [ ] Target API Level 최신 (2026년 35+)
- [ ] Permissions Declaration Form (위치·SMS·통화기록 등)
- [ ] 가족용 앱이면 Designed for Families 정책

### 공통
- [ ] 권한 요청 사유 **명시 문구** (한국어 최소, 다국어 배포 시 각 언어)
- [ ] 인앱결제 정책 (Apple·Google 각 30%·15% 수수료)
- [ ] 크래시·버그 리포트 SDK 개인정보 수집 여부 점검

---

## 7. 글로벌 오버레이 포인터

- **GDPR**: 쿠키·트래킹 SDK 동의 (EU 내 배포)
- **COPPA**: 13세 미만 대상 앱 → Designed for Families
- **LGPD** (브라질): 처리방침 포르투갈어 번역 권장
- **중국 앱스토어**: ICP 신고·PIPL 오버레이 (R5)

---

⚠️ 법률자문 대체 ✗ | 📅 2026-04-21 | ⚖️ 대한민국 + Apple·Google 정책 | 📚 a1 L1·L12 · a2 D7-1~4 · a3 §2 · a4 §3
