import os

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS, exist_ok=True)

fig, ax = plt.subplots(1, 1, figsize=(5.5, 9.0), dpi=600)
ax.set_xlim(0, 14)
ax.set_ylim(0, 21)
ax.axis('off')

# Colors
box_fc='#E8F0FE'; box_ec='#2B579A'
dia_fc='#FFF3E0'; dia_ec='#E65100'
out_fc='#E8F5E9'; out_ec='#2E7D32'
stp_fc='#FFEBEE'; stp_ec='#C62828'
tc='#1A1A1A'; ac='#333333'; lc='#888888'

def box(x, y, w, h, txt, fc=box_fc, ec=box_ec, fs=6.5):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.15", fc=fc, ec=ec, lw=1.0, zorder=2))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            fontfamily='sans-serif', color=tc, weight='medium',
            linespacing=1.3, zorder=3)

def dia(cx, cy, w, h, txt):
    ax.add_patch(plt.Polygon([(cx,cy+h/2),(cx+w/2,cy),(cx,cy-h/2),(cx-w/2,cy)],
        closed=True, fc=dia_fc, ec=dia_ec, lw=1.0, zorder=2))
    ax.text(cx, cy, txt, ha='center', va='center', fontsize=6,
            fontfamily='sans-serif', color=tc, weight='bold',
            linespacing=1.15, zorder=3)

def arrow_down(x, y_from, y_to):
    """Arrow from bottom of one element to top of next"""
    ax.annotate('', xy=(x, y_to), xytext=(x, y_from),
        arrowprops=dict(arrowstyle='->', color=ac, lw=1.0, shrinkA=0, shrinkB=0))

# Layout
cx = 7.0
bw = 5.8
bh = 0.85
sp = 0.45

tx = 2.0
tw = 1.7
th = 0.65

dw = 3.0
dh = 1.0

# Start position - leave room at top
y = 19.8

# 1 Input
y1_center = y
box(cx, y, bw, bh, "Input: q-product parameters\n(sⱼ, mⱼ, bⱼ)")
y1_bot = y - bh/2

y -= bh/2 + sp + bh/2

# 2 Set N
y2_center = y
y2_top = y + bh/2
box(cx, y, bw, bh, "Set truncation order N\n(initial: N = 100)")
y2_bot = y - bh/2
arrow_down(cx, y1_bot, y2_top)

y -= bh/2 + sp + bh/2

# 3 Expand
y3_center = y
y3_top = y + bh/2
ye = y  # save for loop arrow
box(cx, y, bw, bh, "Expand product using SymPy\n(degree-capped at N)")
y3_bot = y - bh/2
arrow_down(cx, y2_bot, y3_top)

y -= bh/2 + sp + bh/2

# 4 Store
y4_center = y
y4_top = y + bh/2
box(cx, y, bw, bh, "Store coefficients\nc(0), c(1), …, c(N) in NumPy array")
y4_bot = y - bh/2
arrow_down(cx, y3_bot, y4_top)

y -= bh/2 + sp + bh/2

# 5 Scan
y5_center = y
y5_top = y + bh/2
box(cx, y, bw, bh, "Scan residue classes\nr (mod m), for m = 2, 3, …, M")
y5_bot = y - bh/2
arrow_down(cx, y4_bot, y5_top)

y -= bh/2 + sp + dh/2

# Diamond 1
yd1 = y
yd1_top = y + dh/2
yd1_bot = y - dh/2
dia(cx, y, dw, dh, "All-zero class\nfound?")
arrow_down(cx, y5_bot, yd1_top)

# No left
ax.plot([cx - dw/2, tx + tw/2 + 0.1], [y, y], color=ac, lw=1.0, zorder=1)
ax.annotate('', xy=(tx + tw/2, y), xytext=(tx + tw/2 + 0.25, y),
    arrowprops=dict(arrowstyle='->', color=ac, lw=1.0))
ax.text(cx - dw/2 - 0.15, y + 0.15, "No", fontsize=6, ha='right',
        va='bottom', color=dia_ec, weight='bold')
box(tx, y, tw, th, "No pattern\nfound", fc=stp_fc, ec=stp_ec, fs=6)

y -= dh/2 + sp + bh/2

# 6 Increase N
y6_center = y
y6_top = y + bh/2
box(cx, y, bw, bh, "Increase N\n(→ 500 → 1000 → 5000) and repeat")
y6_bot = y - bh/2
arrow_down(cx, yd1_bot, y6_top)
ax.text(cx + 0.15, yd1_bot - 0.05, "Yes", fontsize=6, ha='left',
        va='top', color=dia_ec, weight='bold')

# Loop arrow right side back to Expand
lx = cx + bw/2 + 0.55
ax.plot([cx + bw/2, lx], [y, y], color=lc, lw=0.9, zorder=1)
ax.plot([lx, lx], [y, ye], color=lc, lw=0.9, zorder=1)
ax.annotate('', xy=(cx + bw/2, ye), xytext=(lx, ye),
    arrowprops=dict(arrowstyle='->', color=lc, lw=0.9, shrinkA=0, shrinkB=0))

y -= bh/2 + sp + dh/2

# Diamond 2
yd2 = y
yd2_top = y + dh/2
yd2_bot = y - dh/2
dia(cx, y, dw, dh, "Pattern\npersists?")
arrow_down(cx, y6_bot, yd2_top)

# No left aligned
ax.plot([cx - dw/2, tx + tw/2 + 0.1], [y, y], color=ac, lw=1.0, zorder=1)
ax.annotate('', xy=(tx + tw/2, y), xytext=(tx + tw/2 + 0.25, y),
    arrowprops=dict(arrowstyle='->', color=ac, lw=1.0))
ax.text(cx - dw/2 - 0.15, y + 0.15, "No", fontsize=6, ha='right',
        va='bottom', color=dia_ec, weight='bold')
box(tx, y, tw, th, "Discard\ncandidate", fc=stp_fc, ec=stp_ec, fs=6)

y -= dh/2 + sp + bh/2

# 7 Output
y7_center = y
y7_top = y + bh/2
box(cx, y, bw, bh, "Output: structured conjecture\nfor theoretical investigation",
    fc=out_fc, ec=out_ec)
arrow_down(cx, yd2_bot, y7_top)
ax.text(cx + 0.15, yd2_bot - 0.05, "Yes", fontsize=6, ha='left',
        va='top', color=dia_ec, weight='bold')

# Set ylim with proper margins
ax.set_ylim(y - bh/2 - 0.5, 20.5)

plt.savefig(os.path.join(RESULTS, 'Figure1_Flowchart.png'),
            dpi=600, bbox_inches='tight', pad_inches=0.15,
            facecolor='white', edgecolor='none')
plt.close()
print("Done.")
