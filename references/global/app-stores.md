# Apple App Store · Google Play Policy — v2.3 (2026-05-25 신규)

## 트리거
앱 스토어 제출·리젝 대응·정책 변경 점검

---

## Apple App Store Review Guidelines — 2025-2026 핵심 변경

### 개인정보·AI 데이터
- **2025-11 신설** — 앱이 **제3자 AI**와 개인정보 공유 시 **공시 + 사용자 명시 동의** 필수
- App Privacy Label 강화 — 수집 데이터·목적·사용자 연결 여부 상세 공개
- Privacy Manifest (3rd-party SDK) — 2025 점진 강제

### 연령제한 콘텐츠 (Creator Apps)
- 크리에이터 앱 — 앱 연령 등급 초과 콘텐츠 **식별 수단** + **검증·선언 연령 기반 제한 메커니즘** 필수
- Cre8orClub·KISAS 직격 — 연령 게이트 + 콘텐츠 모더레이션 결합 SOP

### 브랜드·상표
- 타 개발사 아이콘·브랜드·제품명을 자신의 앱 아이콘·이름에 사용 ✗ (승인 없으면)

### 금융앱
- 대출앱 **최대 APR 36% 상한** (비용·수수료 포함)
- 60일 이내 일시상환 강제 ✗

### 외부결제 (US 한정)
- **US App Store** — 인앱 디지털 상품의 외부 결제·체크아웃 페이지로 안내 버튼·링크·CTA 허용 (Epic v. Apple 판결 후속)

### SDK 요건
- **2026-04-28부터** App Store Connect 업로드 = iOS 26 & iPadOS 26 SDK 이상 빌드 필수

### AI 생성 콘텐츠
- 앱이 AI/자동화 사용 시 작동방식 설명 + 자동생성 시점 사용자 인지

---

## Google Play Developer Program Policy — 2025-2026 핵심 변경

### AI 생성 콘텐츠 (2025 신규)
- 별도 규제 영역으로 분리
- **유해 콘텐츠 생성 방지 사전 의무** (사후 신고 대응 ✗)
- 2025-01 추가 — AI 출력 라벨링 명확화·모더레이션 강화·아동 대상 추가 안전조치
- 아동 대상 시 미성년 대상 음란·조작 콘텐츠 생성 ✗

### Data Safety 강화
- Data Safety 섹션 엄격 집행 — 미준수 = 앱 제거
- 수집·저장·공유 명확 설명 의무
- 오해 소지·불완전 정보 = 벌칙·제거

### 권한 정책 (2026-04-15)
- **Contacts Permissions** 강화 — 광범위 접근 거버넌스
- 광범위 접근 미필요 시 **Android Contact Picker** 사용 의무 (데이터 최소화)
- 정책 통지 = **2026-04-15** → **30일+ 정합화 기간**

### Family·Children
- 13세 미만 또는 Mixed Audience 대상 시 추가 안전조치 의무
- COPPA·Designed for Families 프로그램 준수

---

## Cre8orClub / KISAS 매핑

### 공통
- **연령 게이트** (15+ Cre8orClub / KISAS 연령 정책) — Apple Creator 연령 메커니즘 + Play Family 정책 동시 충족
- **다크패턴 금지 4중 가드** — 한국 전상법 §21-2 + EU DSA + Apple/Google 정책 = 단일 UX 설계로 통합 충족
- **AI 생성 콘텐츠 라벨** — 한국 AI기본법 §27 + Apple/Google 정책 = 동시 준수
- **개인정보 공유 동의** — Apple 제3자 AI 공시 = 한국 §17 제3자 제공 별도동의로 1차 충족

### 차이
- Apple **iOS 26 SDK 강제** = 2026-04-28 일정 별도 관리 (개발팀 캘린더)
- Play **Contact Picker** = 친구초대·매칭 기능 재설계 필요 시 사전 분리
- **외부결제** = 한국 인앱결제법(전기통신사업법 §50-2) + US 외부결제 허용 = 결제 플로우 지역별 분기

## 레퍼런스
- Apple Developer App Review Guidelines (developer.apple.com/app-store/review/guidelines/)
- Apple Developer News (developer.apple.com/news/)
- Google Play Developer Policy Center (play.google/developer-content-policy/)
- Google Play Console Help — 정책 발표 2025-07-10, 2026-04-15
