# d7-permissions 템플릿 (앱 권한 요청 사유 — Purpose String) — v1.0

## 법적 근거
- **개인정보보호법 §15·§17** (수집·이용·제공)
- **위치정보법 §15·§16** (위치정보 별도 동의)
- **Apple Info.plist** — NSxxxUsageDescription 필수
- **Google Play Manifest** — 권한 사용 사유 정책 (2025·2026 강화)

## 필수 권한별 사유 문구 (v2.3 — Apple Info.plist 키 기준)

### 카메라 (NSCameraUsageDescription)
```
Cre8orClub은(는) 아티스트와 팬이 공유할 사진·영상을 촬영하는 데
카메라를 사용합니다.
```

### 사진 보관함 (NSPhotoLibraryUsageDescription)
```
프로필·게시물에 첨부할 사진을 선택하기 위해 사진 보관함에
접근합니다. 회사는 선택한 사진만 업로드합니다.
```

### 마이크 (NSMicrophoneUsageDescription)
```
음성 메시지·라이브 댓글 녹음에 마이크를 사용합니다.
```

### 위치 — 사용 중 (NSLocationWhenInUseUsageDescription)
```
주변 팬 모임·오프라인 이벤트를 추천하기 위해 앱 사용 중에만
위치를 확인합니다. 위치정보법 §15에 따른 별도 동의가 추가로
필요합니다.
```

### 위치 — 항상 (NSLocationAlwaysAndWhenInUseUsageDescription)
```
백그라운드 위치 사용 사유 명시 필수 — Cre8orClub 미사용 권장.
사용 시: "팬 모임 알림 정확도 향상을 위해 백그라운드 위치를
사용합니다. 언제든지 설정에서 변경할 수 있습니다."
```

### 연락처 (NSContactsUsageDescription)
```
친구 초대 시 연락처를 회사가 직접 저장·전송하지 않으며,
사용자의 기기에서만 매칭합니다. (실 매칭 방식에 따라 수정)
```
※ **2026-04-15 Google Play Contacts Permissions 정책** — 광범위 접근 미필요 시 Android Contact Picker 사용 의무

### 알림 (NSUserNotificationsUsageDescription / Android POST_NOTIFICATIONS)
```
새 게시물·메시지·이벤트 알림을 위해 사용합니다.
설정에서 언제든 끌 수 있습니다.
```

### Face ID·Touch ID (NSFaceIDUsageDescription)
```
빠른 로그인·결제 본인확인에 Face ID를 사용합니다. 회사는
생체정보 자체를 저장하지 않으며 기기에만 보관됩니다.
```

### 추적 (NSUserTrackingUsageDescription — App Tracking Transparency)
```
사용자 맞춤 광고를 위해 다른 앱·웹사이트의 활동을 추적할 수
있도록 허용해 주세요. 거부해도 서비스 이용에 제한이 없습니다.
```

## Android 위험 권한 정책 매핑

| Android 권한 | iOS 대응 | v2.3 주의 |
|---|---|---|
| READ_CONTACTS | NSContacts | **2026-04-15 Contact Picker 의무** (광범위 접근 시) |
| ACCESS_FINE_LOCATION | NSLocation | 위치정보법 §15 별도 동의 + 백그라운드 정당 사유 |
| CAMERA | NSCamera | 사용 사유 명시 + 일회성 우선 |
| RECORD_AUDIO | NSMicrophone | 라이브·녹화 명시 |
| READ_MEDIA_IMAGES/VIDEO | NSPhotoLibrary | Android 13+ 분리 |
| POST_NOTIFICATIONS | NSUserNotifications | Android 13+ 런타임 요청 |
| BLUETOOTH_CONNECT | NSBluetooth | 사용 사유 명시 |

## 적용 조건 (서비스별 분기)
- **Cre8orClub** — 카메라·사진·마이크·알림·ATT 디폴트 (Always Location ✗)
- **KISAS** — 카메라·사진·알림 + 미성년 ATT 거부 디폴트 (COPPA 회피)
- **글로벌** — ATT는 iOS 14.5+ 디폴트 + EU는 ePrivacy + 한국은 정통망법 §50

## v2.3 신규 주의
- **Apple 2025-11 강화** — 제3자 AI와 공유 시 권한 요청 사유에 명시 의무
- **Google Play 2026-04-15** — Contacts Permissions 정책 + 30일+ 정합화 기간
- **Privacy Manifest** — 3rd-party SDK 권한 사용 사유 PrivacyInfo.xcprivacy 명시
- **권한 거부 시 우회 사용 ✗** — IDFA·MAC 주소 추가 수집으로 우회 = 정책 위반

---
⚠️ 법률자문 대체 ✗ — 참고용. 변호사 최종검토 필수. · 📅 2026-05-25 (v2.3)
