#!/usr/bin/env python3
"""
Generate the pipeline architecture figure: pipeline_architecture.png
Requires: matplotlib  (pip3 install matplotlib)
"""

import os
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    from matplotlib.patheffects import withStroke
except ImportError:
    print("ERROR: matplotlib is not installed.")
    print("Install it with:  pip3 install matplotlib")
    sys.exit(1)

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "pipeline_architecture.png")

# ── Colour palette ────────────────────────────────────────────────────────────
MANUAL_BG    = "#C0392B"      # deep red
MANUAL_FG    = "#FFFFFF"
AUTO_BG      = "#2471A3"      # steel blue
AUTO_FG      = "#FFFFFF"
ARTIFACT_BG  = "#ECF0F1"      # light grey
ARTIFACT_FG  = "#2C3E50"
ARROW_COL    = "#566573"
PRIVACY_BG   = "#117A65"      # dark teal
PRIVACY_FG   = "#FFFFFF"
BG_PAGE      = "#FDFEFE"

# ── Figure setup ──────────────────────────────────────────────────────────────
fig_w, fig_h = 18, 13
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.axis("off")
fig.patch.set_facecolor(BG_PAGE)
ax.set_facecolor(BG_PAGE)

# ── Helper functions ──────────────────────────────────────────────────────────
def rounded_box(ax, x, y, w, h, bg, fg, title, body_lines,
                badge=None, badge_bg="#E74C3C", radius=0.35, lw=0):
    """Draw a rounded rectangle with a title and body lines."""
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=bg, edgecolor="white", linewidth=lw)
    ax.add_patch(box)

    # Title strip (slightly darker top bar)
    title_h = 0.55
    title_box = FancyBboxPatch((x, y + h - title_h), w, title_h,
                               boxstyle=f"round,pad=0,rounding_size={radius}",
                               facecolor=bg, edgecolor="white", linewidth=0)
    ax.add_patch(title_box)

    # Title text
    ax.text(x + w/2, y + h - title_h/2, title,
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=fg, zorder=5)

    # Body lines
    n = len(body_lines)
    body_top = y + h - title_h - 0.12
    line_gap = (h - title_h - 0.2) / max(n, 1)
    for i, line in enumerate(body_lines):
        ty = body_top - (i + 0.5) * line_gap
        ax.text(x + 0.18, ty, line, ha="left", va="center",
                fontsize=8.2, color=fg, zorder=5, wrap=False)

    # Optional badge (MANUAL / AUTO)
    if badge:
        bx, by = x + w - 0.1, y + h - 0.1
        ax.text(bx, by, badge, ha="right", va="top",
                fontsize=7.0, fontweight="bold", color=badge_bg,
                fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.18", fc="white",
                          ec=badge_bg, lw=1.2), zorder=6)


def artifact_box(ax, x, y, w, h, label, sublabel=""):
    """Parallelogram-style data artifact box."""
    skew = 0.2
    pts = [(x+skew, y+h), (x+w+skew, y+h), (x+w, y), (x, y)]
    poly = plt.Polygon(pts, closed=True,
                       facecolor=ARTIFACT_BG, edgecolor="#AAB7B8", lw=1.2)
    ax.add_patch(poly)
    ax.text(x + w/2 + skew/2, y + h/2 + 0.05, label,
            ha="center", va="center", fontsize=8, color=ARTIFACT_FG,
            fontweight="bold", zorder=5)
    if sublabel:
        ax.text(x + w/2 + skew/2, y + h/2 - 0.22, sublabel,
                ha="center", va="center", fontsize=7, color="#717D7E",
                style="italic", zorder=5)


def arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COL,
                                lw=1.6, mutation_scale=18))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.05, my, label, ha="left", va="center",
                fontsize=7.5, color=ARROW_COL, style="italic")


# ═══════════════════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════════════════
ax.text(fig_w/2, 12.55,
        "Data Dictionary Pipeline — Privacy-Safe Workflow",
        ha="center", va="center", fontsize=16, fontweight="bold",
        color="#1A252F")
ax.text(fig_w/2, 12.15,
        "How to generate a data dictionary without exposing real patient data to AI tools",
        ha="center", va="center", fontsize=10, color="#566573", style="italic")

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 1  (Stages 1–3)    y = 8.2 – 11.4
# ═══════════════════════════════════════════════════════════════════════════════
BOX_W, BOX_H = 4.6, 2.85
ROW1_Y = 8.45
ROW2_Y = 4.55
GAP    = 0.7
START_X = 0.55

# ── Stage 1 ──────────────────────────────────────────────────────────────────
s1_x = START_X
rounded_box(ax, s1_x, ROW1_Y, BOX_W, BOX_H,
            bg=MANUAL_BG, fg=MANUAL_FG,
            title="STAGE 1  ·  Extract Column Names",
            body_lines=[
                "▸  Open your terminal",
                "▸  cd  to your data folder",
                "▸  Run step1_extract_headers.sh",
                "   with your CSV file path",
                "▸  Output: columns.txt",
                "   (column names only — no data!)",
            ],
            badge="[ MANUAL ]")

# Artifact: columns.txt
art1_x = s1_x + BOX_W + 0.08
art1_y = ROW1_Y + BOX_H/2 - 0.35
artifact_box(ax, art1_x, art1_y, 0.52, 0.72, "[f]", "columns.txt")
arrow(ax, s1_x + BOX_W, ROW1_Y + BOX_H/2,
          art1_x + 0.62, ROW1_Y + BOX_H/2)

# ── Stage 2 ──────────────────────────────────────────────────────────────────
s2_x = s1_x + BOX_W + GAP
rounded_box(ax, s2_x, ROW1_Y, BOX_W, BOX_H,
            bg=MANUAL_BG, fg=MANUAL_FG,
            title="STAGE 2  ·  Create Synthetic Examples",
            body_lines=[
                "▸  Run step2_make_template.py",
                "▸  Open synthetic_template.csv",
                "   in Excel / Numbers / Sheets",
                "▸  Fill Row 2 with FAKE values",
                "   that match the real format",
                "▸  Save as CSV (not xlsx)",
            ],
            badge="[ MANUAL ]")

# Stage 2b sub-box (below Stage 2)
s2b_h = 1.55
s2b_y = ROW1_Y - s2b_h - 0.22
rounded_box(ax, s2_x, s2b_y, BOX_W, s2b_h,
            bg=AUTO_BG, fg=AUTO_FG,
            title="STAGE 2b  ·  Attach Resource Document  (optional)",
            body_lines=[
                "▸  python3 step2b_add_resource_doc.py",
                "   path/to/reference_doc   [ANY FORMAT]",
                "   (.docx  .xlsx  .pdf  .csv  .txt  .md)",
                "▸  Output: resource_doc.txt (auto-included",
                "   in ai_input.txt — informs AI descriptions)",
            ],
            badge="[ AUTO ]", radius=0.25)

# Vertical arrow Stage 2 → Stage 2b
ax.annotate("", xy=(s2_x + BOX_W/2, s2b_y + s2b_h),
            xytext=(s2_x + BOX_W/2, ROW1_Y),
            arrowprops=dict(arrowstyle="-|>", color=ARROW_COL,
                            lw=1.4, mutation_scale=14))

art2_x = s2_x + BOX_W + 0.08
artifact_box(ax, art2_x, art1_y, 0.52, 0.72, "[f]", "template")
arrow(ax, s2_x + BOX_W, ROW1_Y + BOX_H/2,
          art2_x + 0.62, ROW1_Y + BOX_H/2)

# Arrow from art1 to stage 2
arrow(ax, art1_x + 0.62, ROW1_Y + BOX_H/2,
          s2_x, ROW1_Y + BOX_H/2)

# ── Stage 3 ──────────────────────────────────────────────────────────────────
s3_x = s2_x + BOX_W + GAP
rounded_box(ax, s3_x, ROW1_Y, BOX_W, BOX_H,
            bg=AUTO_BG, fg=AUTO_FG,
            title="STAGE 3  ·  Package for AI",
            body_lines=[
                "▸  Run step3_package_for_ai.py",
                "▸  Reads: columns.txt",
                "          synthetic_template.csv",
                "          context_config.txt",
                "▸  Output: ai_input.txt",
                "   (ready to paste into AI tool)",
            ],
            badge="[ AUTO ]")

art3_x = s3_x + BOX_W + 0.08
artifact_box(ax, art3_x, art1_y, 0.52, 0.72, "[f]", "ai_input.txt")
arrow(ax, s3_x + BOX_W, ROW1_Y + BOX_H/2,
          art3_x + 0.62, ROW1_Y + BOX_H/2)

# Arrow from art2 to stage 3
arrow(ax, art2_x + 0.62, ROW1_Y + BOX_H/2,
          s3_x, ROW1_Y + BOX_H/2)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 2  (Stages 4–6)    y = 4.55 – 7.75
# ═══════════════════════════════════════════════════════════════════════════════

# Row-joining arrow: art3 → bends down → Stage 4 right side
art3_mid_x = art3_x + 0.62
bend_x     = art3_mid_x + 0.35
bend_y_top = ROW1_Y + BOX_H/2
bend_y_bot = ROW2_Y + BOX_H/2
s4_x       = START_X
s4_right_x = s4_x + BOX_W

# Draw the L-shaped connector: right → down → left to Stage 4 entry
ax.annotate("", xy=(s4_right_x, bend_y_bot),
            xytext=(art3_mid_x, bend_y_top),
            arrowprops=dict(
                arrowstyle="-|>", color=ARROW_COL, lw=1.6,
                mutation_scale=18,
                connectionstyle=f"arc,angleA=0,angleB=0,armA=60,armB=60,rad=8"
            ))

# ── Stage 4 ──────────────────────────────────────────────────────────────────
rounded_box(ax, s4_x, ROW2_Y, BOX_W, BOX_H,
            bg=MANUAL_BG, fg=MANUAL_FG,
            title="STAGE 4  ·  Run the AI Prompt",
            body_lines=[
                "▸  Open ai_prompt.md — check",
                "   capability requirements",
                "▸  In AI tool: paste ai_prompt.md",
                "   then paste ai_input.txt",
                "▸  AI generates JSON descriptions",
                "▸  Copy response → ai_output.json",
            ],
            badge="[ MANUAL ]")

# ── Stage 5 ──────────────────────────────────────────────────────────────────
s5_x = s4_x + BOX_W + GAP
rounded_box(ax, s5_x, ROW2_Y, BOX_W, BOX_H,
            bg=AUTO_BG, fg=AUTO_FG,
            title="STAGE 5  ·  Format AI Output",
            body_lines=[
                "▸  Run step5_format_output.py",
                "▸  Reads ai_output.json",
                "   + synthetic_template.csv",
                "▸  Output: data_dictionary.xlsx",
                "   (color-coded, 7-column layout,",
                "    styled like template reference)",
            ],
            badge="[ AUTO ]")

arrow(ax, s4_x + BOX_W, ROW2_Y + BOX_H/2,
          s5_x, ROW2_Y + BOX_H/2)

# ── Stage 6 ──────────────────────────────────────────────────────────────────
s6_x = s5_x + BOX_W + GAP
rounded_box(ax, s6_x, ROW2_Y, BOX_W, BOX_H,
            bg=MANUAL_BG, fg=MANUAL_FG,
            title="STAGE 6  ·  Review & Finalize",
            body_lines=[
                "▸  Open data_dictionary.xlsx",
                "▸  Review all AI descriptions",
                "▸  Correct errors, fill gaps",
                "▸  Verify Code/Desc linkages",
                "▸  Save the final dictionary  [DONE]",
                "",
            ],
            badge="[ MANUAL ]")

arrow(ax, s5_x + BOX_W, ROW2_Y + BOX_H/2,
          s6_x, ROW2_Y + BOX_H/2)

# Artifacts for row 2
art4_x = s4_x + BOX_W + 0.08
art4_y = ROW2_Y + BOX_H/2 - 0.35
artifact_box(ax, art4_x, art4_y, 0.52, 0.72, "[f]", "ai_output.json")

art5_x = s5_x + BOX_W + 0.08
artifact_box(ax, art5_x, art4_y, 0.52, 0.72, "[x]", "dict.xlsx")

arrow(ax, s4_x + BOX_W, ROW2_Y + BOX_H/2,
          art4_x + 0.62, ROW2_Y + BOX_H/2)
arrow(ax, art4_x + 0.62, ROW2_Y + BOX_H/2,
          s5_x, ROW2_Y + BOX_H/2)
arrow(ax, s5_x + BOX_W, ROW2_Y + BOX_H/2,
          art5_x + 0.62, ROW2_Y + BOX_H/2)
arrow(ax, art5_x + 0.62, ROW2_Y + BOX_H/2,
          s6_x, ROW2_Y + BOX_H/2)

# ═══════════════════════════════════════════════════════════════════════════════
# PRIVACY CALLOUT BOX (bottom left)
# ═══════════════════════════════════════════════════════════════════════════════
priv_x, priv_y = 0.55, 0.45
priv_w, priv_h = 7.5, 1.8
box_priv = FancyBboxPatch((priv_x, priv_y), priv_w, priv_h,
                          boxstyle="round,pad=0,rounding_size=0.3",
                          facecolor=PRIVACY_BG, edgecolor="white", lw=0)
ax.add_patch(box_priv)
ax.text(priv_x + 0.25, priv_y + priv_h - 0.35,
        "PRIVACY GUARANTEE",
        ha="left", va="center", fontsize=10, fontweight="bold",
        color=PRIVACY_FG)
privacy_lines = [
    "[OK]  Stage 1: Only column NAMES extracted — no row values, no patient data",
    "[OK]  Stage 2: YOU supply fake values using domain knowledge — no AI involvement",
    "[OK]  Stages 3-5: AI tool receives zero real data (column names + synthetic examples only)",
]
for i, line in enumerate(privacy_lines):
    ax.text(priv_x + 0.25, priv_y + priv_h - 0.72 - i*0.38,
            line, ha="left", va="center",
            fontsize=8.5, color=PRIVACY_FG)

# ═══════════════════════════════════════════════════════════════════════════════
# LEGEND (bottom right)
# ═══════════════════════════════════════════════════════════════════════════════
leg_x, leg_y = 9.4, 0.45
leg_w, leg_h = 8.15, 1.8
box_leg = FancyBboxPatch((leg_x, leg_y), leg_w, leg_h,
                         boxstyle="round,pad=0,rounding_size=0.3",
                         facecolor="#F2F3F4", edgecolor="#D5D8DC", lw=1.2)
ax.add_patch(box_leg)
ax.text(leg_x + 0.25, leg_y + leg_h - 0.35,
        "Legend", ha="left", va="center",
        fontsize=10, fontweight="bold", color="#2C3E50")

items = [
    (MANUAL_BG, "  MANUAL stage — requires user action (no AI tool sees your data)"),
    (AUTO_BG,   "  AUTOMATED stage — Python script runs locally on your machine"),
    (ARTIFACT_BG, "  Data file [f]/[x] — produced at this stage"),
]
for i, (col, label) in enumerate(items):
    y_pos = leg_y + leg_h - 0.72 - i*0.38
    swatch = FancyBboxPatch((leg_x + 0.25, y_pos - 0.12), 0.28, 0.26,
                            boxstyle="round,pad=0,rounding_size=0.04",
                            facecolor=col, edgecolor="#AAB7B8", lw=0.8)
    ax.add_patch(swatch)
    ax.text(leg_x + 0.65, y_pos,
            label, ha="left", va="center",
            fontsize=8.5, color="#2C3E50")

# ═══════════════════════════════════════════════════════════════════════════════
# Stage number circles
# ═══════════════════════════════════════════════════════════════════════════════
for idx, (bx, by) in enumerate([
    (s1_x, ROW1_Y), (s2_x, ROW1_Y), (s3_x, ROW1_Y),
    (s4_x, ROW2_Y), (s5_x, ROW2_Y), (s6_x, ROW2_Y),
], 1):
    circ_bg = MANUAL_BG if idx in (1, 2, 4, 6) else AUTO_BG
    circle = plt.Circle((bx + 0.32, by + BOX_H + 0.05), 0.22,
                         color=circ_bg, zorder=7)
    ax.add_patch(circle)
    ax.text(bx + 0.32, by + BOX_H + 0.05, str(idx),
            ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=8)

# ── Save ──────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.1)
plt.savefig(OUTPUT_PATH, dpi=180, bbox_inches="tight",
            facecolor=BG_PAGE, edgecolor="none")
plt.close()
print(f"✅  Saved: {OUTPUT_PATH}")
