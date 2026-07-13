#!/usr/bin/env python3
"""MYRIORAMA 브랜드 벡터 애셋 생성.

마크 지오메트리(SSOT): cell=100, gap=25, rx=16, 5x2 체커보드
  row1(y=0):   col2(x=125), col4(x=375)
  row2(y=125): col1(x=0), col3(x=250, accent), col5(x=500)
  viewBox 0 0 600 225
워드마크: Noto Sans KR wght700 글리프 패스 추출, tracking 0.19em
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

SP = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/minjaebaak/Desktop/MYRIORAMA/homepage/assets/brand"
os.makedirs(OUT, exist_ok=True)

INK = "#191b1e"
PAPER = "#fbfbfa"
ACCENT = "#3558c9"

# ---------- 마크 지오메트리 ----------
CELL, GAP, RX = 100, 25, 16
MARK_W, MARK_H = 5 * CELL + 4 * GAP, 2 * CELL + GAP  # 600 x 225
ROW1 = [1, 3]        # 0-based col index
ROW2 = [0, 2, 4]
ACCENT_CELL = (1, 2)  # (row=1(하단), col=2(중앙))

def mark_rects(ink, accent=None):
    rects = []
    for r, cols in enumerate([ROW1, ROW2]):
        for c in cols:
            x, y = c * (CELL + GAP), r * (CELL + GAP)
            color = accent if (accent and (r, c) == ACCENT_CELL) else ink
            rects.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" fill="{color}"/>')
    return "\n  ".join(rects)

def svg(w, h, body, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">\n  {body}\n</svg>\n'

def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print("wrote", name)

write("mark.svg", svg(MARK_W, MARK_H, mark_rects(INK)))
write("mark-accent.svg", svg(MARK_W, MARK_H, mark_rects(INK, ACCENT)))
write("mark-white.svg", svg(MARK_W, MARK_H, mark_rects(PAPER)))

# 파비콘: 정사각 660, 마크 중앙 배치 (accent)
fav_body = f'<g transform="translate(30,{(660 - MARK_H) / 2})">\n  {mark_rects(INK, ACCENT)}\n  </g>'
write("favicon.svg", svg(660, 660, fav_body))

# ---------- 워드마크 (글리프 패스 추출) ----------
font = TTFont(os.path.join(SP, "NotoSansKR.ttf"))
instantiateVariableFont(font, {"wght": 700}, inplace=True)
upem = font["head"].unitsPerEm
cap = font["OS/2"].sCapHeight
cmap = font.getBestCmap()
glyphset = font.getGlyphSet()
hmtx = font["hmtx"]

TEXT = "MYRIORAMA"
TRACK = 0.19 * upem  # letter-spacing 0.19em

paths, xoff = [], 0.0
for i, ch in enumerate(TEXT):
    gname = cmap[ord(ch)]
    pen = SVGPathPen(glyphset)
    glyphset[gname].draw(pen)
    d = pen.getCommands()
    paths.append((xoff, d))
    adv = hmtx[gname][0]
    xoff += adv + (TRACK if i < len(TEXT) - 1 else 0)

# 마지막 글자의 잉크 우측 경계로 폭 트림
last_pen = BoundsPen(glyphset)
glyphset[cmap[ord(TEXT[-1])]].draw(last_pen)
last_adv = hmtx[cmap[ord(TEXT[-1])]][0]
word_units_w = xoff - last_adv + last_pen.bounds[2]

# 워드마크 단독 SVG: cap-height를 225(마크 높이)로 스케일
S_word = MARK_H / cap
WW = word_units_w * S_word
word_paths = "\n  ".join(
    f'<path transform="translate({x:.1f},0)" d="{d}"/>' for x, d in paths
)
word_group = (
    f'<g fill="{INK}" transform="translate(0,{MARK_H}) scale({S_word:.6f},{-S_word:.6f})">\n'
    f"  {word_paths}\n  </g>"
)
write("wordmark.svg", svg(round(WW), MARK_H, word_group))

# ---------- 가로 로크업 (마크 + 워드마크) ----------
# 네비 비율 근사: 워드마크 cap-height ≈ 마크 높이의 0.85, 세로 중앙 정렬, 간격 = 1.8*CELL
def lockup(mark_ink, text_ink, accent=None, name="logo.svg"):
    s = 0.85 * MARK_H / cap
    ww = word_units_w * s
    gap = 1.8 * CELL
    total_w = MARK_W + gap + ww
    cap_px = cap * s
    baseline = (MARK_H + cap_px) / 2
    wp = "\n    ".join(
        f'<path transform="translate({x:.1f},0)" d="{d}"/>' for x, d in paths
    )
    body = (
        f"{mark_rects(mark_ink, accent)}\n"
        f'  <g fill="{text_ink}" transform="translate({MARK_W + gap:.1f},{baseline:.2f}) scale({s:.6f},{-s:.6f})">\n'
        f"    {wp}\n  </g>"
    )
    write(name, svg(round(total_w), MARK_H, body, vb=f"0 0 {total_w:.0f} {MARK_H}"))
    return total_w

logo_w = lockup(INK, INK, ACCENT, "logo.svg")
lockup(PAPER, PAPER, None, "logo-white.svg")

print(f"cap={cap} upem={upem} wordmark_units={word_units_w:.0f} logo_w={logo_w:.0f}")
