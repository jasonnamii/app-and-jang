# α3. 벤치마크 DB

## 역할
한국 Top 20 앱 TOS·PP 자동 폴링 + diff 추적. 약관 작성 시 "유사 서비스가 어떻게 쓰는지" 즉시 비교.

## Top 20 (Tier 1·2)

### Tier 1 (Top 5 우선)
1. 토스 (toss.im)
2. 카카오톡 (kakao.com)
3. 네이버 (naver.com)
4. 당근 (daangn.com)
5. 배달의민족 (baemin.com)

### Tier 2 (확장)
6. 쿠팡 (coupang.com)
7. 11번가 (11st.co.kr)
8. 무신사 (musinsa.com)
9. 마켓컬리 (kurly.com)
10. 야놀자 (yanolja.com)
11. 멜론 (melon.com)
12. 지니뮤직 (genie.co.kr)
13. 왓챠 (watcha.com)
14. 티빙 (tving.com)
15. 웨이브 (wavve.com)
16. 라인 (line.me)
17. 인스타그램 (instagram.com)
18. 유튜브 (youtube.com)
19. 디스코드 (discord.com)
20. 트위치 (twitch.tv)

## 폴링 메타데이터

```json
{
  "service_id": "toss",
  "doc_type": "privacy_policy",
  "url": "https://www.toss.im/.../privacy",
  "last_check": "2026-04-22",
  "last_change": "2026-02-14",
  "version": "v3.7",
  "doc_hash": "sha256:abc...",
  "key_clauses": {
    "보유기간": "탈퇴 후 30일 이내 파기",
    "3자제공": "별도 동의 시에만",
    "자동갱신": "해지 1-click",
    "분쟁관할": "서울중앙지법"
  },
  "domain": ["D2", "D6"]
}
```

## v2.0 MVP
- Top 5 수동 인덱싱 (월 1회)
- 핵심 조항 4~6개 추출
- diff 발생 시 알림

## v2.1
- Top 20 자동폴링 (주 1회)
- 조항 50+ 추출
- 연도별 변천사
