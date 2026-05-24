# d7-data-safety 템플릿 (Google Play Data Safety + Apple App Privacy Label) — v1.0

## 법적 근거
- **Google Play Data Safety Section** (2022 도입, 2025 강화)
- **Apple App Privacy Label** (iOS 14.5+, 2025-11 강화)
- **개인정보보호법 §30** (처리방침과 일치 의무)

## 필수 공시 항목 (양 스토어 공통)
1. **수집 데이터 카테고리** (이름·이메일·위치·금융정보·건강 등)
2. **수집 목적** (서비스 운영·맞춤·광고·분석 등)
3. **사용자 데이터 연결 여부** (식별 가능 vs 익명)
4. **제3자 공유 여부** + 상대방·목적
5. **보안 처리** (전송 암호화·저장 암호화)
6. **사용자 삭제 권리** (앱 내 삭제 기능 제공 여부)

## Google Play Data Safety 구성 (v2.3 강화)

```
[Data collected]
✓ Personal info: Name, Email, User ID
  - Collected: Yes
  - Shared: No
  - Optional: No
  - Purpose: Account management, Analytics
  - Linked to user: Yes

✓ Photos and videos: Photos
  - Collected: Yes  
  - Shared: No
  - Optional: Yes
  - Purpose: App functionality
  - Linked to user: Yes

[Data security]
✓ Data is encrypted in transit
✓ You can request that data be deleted
✓ Committed to follow Play Families Policy (해당 시)

[Data deletion]
URL: https://cre8or.club/delete-account
또는 앱 내: 설정 > 계정 > 계정 삭제
```

## Apple App Privacy Label 구성 (v2.3)

```
Privacy
"Data Used to Track You"
- 없음 (또는 Analytics 등 명시)

"Data Linked to You"
- Contact Info: Email, Name, Phone
- User Content: Photos, Videos
- Identifiers: User ID
- Usage Data: Product Interaction

"Data Not Linked to You"
- Diagnostics: Crash Data, Performance Data

[Privacy Manifest — 2024+]
NSPrivacyAccessedAPITypes 명시
3rd-party SDK 별 PrivacyInfo.xcprivacy 포함
```

## 적용 조건 (서비스별 분기)
- **Cre8orClub** — UGC + 음악 + 추천 → Photos·Videos·Usage Data 다수 수집 → 정확한 라벨링 필수
- **KISAS** — 학생·미성년 → "Data of Minors" 별도 카테고리 + Children's Privacy Policy 추가
- **글로벌** — COPPA Mixed Audience·GDPR Privacy by Design·CPRA Sensitive PI 별도 매핑

## v2.3 신규 주의
- **Apple 2025-11 강화** — 제3자 AI와 개인정보 공유 시 별도 공시 + 명시 동의 (App Privacy Label에도 반영)
- **Google Play 2025-2026 Data Safety 엄격 집행** — 미준수 = 앱 제거
- **Privacy Manifest (Apple)** — 2024-05+ 모든 SDK 필수. NSPrivacyAccessedAPITypes 명시 ✗ = 빌드 차단
- **AI 생성 콘텐츠** — Apple/Google 양 정책 = AI 사용 사실·작동방식 공시 + AI 출력 라벨링

---
⚠️ 법률자문 대체 ✗ — 참고용. 변호사 최종검토 필수. · 📅 2026-05-25 (v2.3)
