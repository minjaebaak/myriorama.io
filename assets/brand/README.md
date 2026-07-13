# MYRIORAMA 브랜드 애셋

> 뮈리오라마(myriorama): 어떤 순서로 이어 붙여도 하나의 풍경이 되는 그림 카드.
> 마크는 그 카드들을 5×2 체커보드 픽셀 그리드로 형상화한 것이다.

## 파일

| 파일 | 용도 |
|---|---|
| `logo.svg` | 가로 로크업 (마크 + 워드마크) — 밝은 배경 기본형 |
| `logo-white.svg` | 가로 로크업 — 어두운 배경용 (전체 화이트) |
| `mark.svg` | 마크 단독 — 잉크 단색 (대표형) |
| `mark-white.svg` | 마크 단독 — 어두운 배경용 |
| `wordmark.svg` | 워드마크 단독 (MYRIORAMA, 자간 0.19em, 완전 벡터 패스) |
| `favicon.svg` | 파비콘 (정사각 캔버스에 마크) |
| `mark-square.svg` | 정사각 마크 — 심볼 폭 기준, 위아래 여백 추가 |
| `png/` | 래스터 파생물 — 투명 배경 (SVG가 원본, 재생성 가능) |
| `jpg/` | **등록용** — 알파 없는 플랫폼 업로드 폼에는 이쪽을 사용 (Paper 배경) |

`png/`: `logo-2048w` `logo-white-2048w` `mark-1024` `mark-white-1024` `mark-square-1024` `favicon-512` `favicon-32` `apple-touch-icon`(180) `og-image`(1200×630)
`jpg/`: `mark-square-1024` `mark-square-512` (프로필·아이콘 칸) · `logo-2048w` (가로 로고 칸)

## 팔레트

| 이름 | HEX | 용도 |
|---|---|---|
| Ink | `#191b1e` | 본문·마크·다크 패널 배경 |
| Paper | `#fbfbfa` | 페이지 배경·다크 배경 위 텍스트 |
| Accent | `#3558c9` | 브랜드 블루 — 액센트 셀·링크·강조 |
| Accent Deep | `#2a47a8` | Accent hover |
| Accent Light | `#8fa8f0` | 다크 배경 위 액센트 |
| Alt Surface | `#f2f2ef` | 섹션 교차 배경 |
| Visual Surface | `#f4f5f3` | 카드 내 일러스트 배경 |

## 타이포그래피

- 본문·워드마크: **Noto Sans KR** (300–800) — 워드마크는 700, letter-spacing 0.19em
- 데이터·라벨: **IBM Plex Mono** (400·500)

## 마크 지오메트리 (SSOT)

- 셀 100 × 100, 간격 25 (= 셀의 1/4), 모서리 반경 16
- 5열 × 2행 체커보드 — 1행: 2·4열, 2행: 1·3·5열 (viewBox `0 0 600 225`)
- **심볼은 단색만** — 밝은 배경 Ink, 어두운 배경 Paper. 액센트 셀 미사용 (2026-07-13 결정. Accent 블루는 UI 요소·링크·강조 전용)
- 로크업: 워드마크 cap-height = 마크 높이의 0.85, 세로 중앙 정렬, 마크-텍스트 간격 = 셀 1.8배

## 재생성

```bash
# 폰트 준비 (저장소 미포함, Google Fonts OFL)
curl -sL -o /tmp/NotoSansKR.ttf "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"
# SVG 생성 (fontTools 필요: pip install fonttools)
python3 assets/brand/build_brand.py   # 스크립트 상단 경로 변수 참조
# PNG는 헤드리스 크롬으로 SVG 렌더 (--default-background-color=00000000 = 투명)
```
