# d7-app-privacy-url 템플릿 (앱스토어 개인정보처리방침 URL 등록) — v1.0

## 법적 근거
- **개인정보보호법 §30** (개인정보처리방침 수립·공개 의무)
- **Apple App Store Connect**: Privacy Policy URL 필수
- **Google Play Console**: Privacy Policy URL 필수 (앱 정보 + Data Safety)

## 필수 요건
1. **HTTPS URL** (HTTP 거부)
2. **공개 접근 가능** (로그인 ✗)
3. **앱별 별도 URL 가능** (Cre8orClub·KISAS 분리)
4. **표시 언어 = 스토어 배포 언어 1+ 일치**
5. **24/7 가용성** (스토어 심사 시 다운 = 리젝 사유)

## URL 구성 권장 (v2.3)

```
[디폴트 — 한국어]
https://cre8or.club/privacy

[다국어 분기 — 권장]
https://cre8or.club/privacy?lang=ko
https://cre8or.club/privacy?lang=en
https://cre8or.club/privacy?lang=ja
https://cre8or.club/privacy?lang=zh

[KISAS 별도]
https://kisas.kr/privacy

[버전 관리]
https://cre8or.club/privacy?v=1.3 (이력 보존)
https://cre8or.club/privacy/archive/v1.2 (구버전 보관)
```

## 등록 위치
- **Apple App Store Connect**: 앱 정보 > 개인정보 처리방침 URL
- **Google Play Console**: 앱 콘텐츠 > 개인정보처리방침 (+ Data Safety 별도)
- **앱 내**: 설정 > 개인정보처리방침 (스토어 URL과 일치)
- **웹**: 모든 페이지 푸터

## 적용 조건 (서비스별 분기)
- **Cre8orClub** — iOS·Android 동시 배포 → URL 1개 (다국어 ?lang= 분기)
- **KISAS** — 별도 URL (kisas.kr) — 서비스 도메인 일치
- **글로벌** — 지역별 처리방침 분기 시 URL 분리 가능 (예: /privacy/eu·/privacy/us)

## v2.3 신규 주의
- **Apple 2025-11 강화** — App Privacy Label과 본문 일치 의무 (상충 시 리젝)
- **Google Play 2026-04-15 Contacts Permissions 정책** — 처리방침에 Contacts 광범위 접근 사용 사유 명시 필수
- **개정 시 사용자 공지** — 개보법 §30 ③ — 30일 전 공지 + 중요사항 강조 (앱 내 팝업 권장)

---
⚠️ 법률자문 대체 ✗ — 참고용. 변호사 최종검토 필수. · 📅 2026-05-25 (v2.3)
