#!/usr/bin/env python3
"""Generate SVG keymap diagram for Kometa keyboard."""

SCALE = 0.44
MARGIN_X = 15
MARGIN_Y = 15
KEY_W = 44
KEY_H = 44
KEY_R = 5  # corner radius

COLORS = {
    "default": ("#E8E8E8", "#AAAAAA", "#333333"),   # fill, stroke, text
    "home_mod": ("#C2D9F5", "#7AABDE", "#1A3A5C"),
    "layer": ("#FFD78A", "#C89B30", "#5A3D00"),
    "special": ("#A8DFA8", "#5A9E5A", "#1A4A1A"),
    "empty": ("#F3F3F3", "#DDDDDD", "#AAAAAA"),
    "nav": ("#B8D4F8", "#6699CC", "#1A3A6A"),
    "media": ("#DDD0F0", "#9980CC", "#2D1860"),
    "bt": ("#F5C0C0", "#CC6666", "#500000"),
}


def key_svg(x, y, label1, label2, style):
    fill, stroke, text_color = COLORS.get(style, COLORS["default"])
    parts = []
    parts.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{KEY_W}" height="{KEY_H}" '
        f'rx="{KEY_R}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
    )
    if label1:
        if label2:
            parts.append(
                f'<text x="{x + KEY_W/2:.1f}" y="{y + KEY_H * 0.40:.1f}" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-size="10" fill="{text_color}">{label1}</text>'
            )
            parts.append(
                f'<text x="{x + KEY_W/2:.1f}" y="{y + KEY_H * 0.72:.1f}" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-size="8" fill="{text_color}" opacity="0.7">{label2}</text>'
            )
        else:
            parts.append(
                f'<text x="{x + KEY_W/2:.1f}" y="{y + KEY_H/2:.1f}" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-size="10" fill="{text_color}">{label1}</text>'
            )
    return "\n".join(parts)


def pos(dtsi_x, dtsi_y):
    """Convert dtsi physical layout coordinates to SVG coordinates."""
    sx = (dtsi_x - 100) * SCALE + MARGIN_X
    sy = dtsi_y * SCALE + MARGIN_Y
    return sx, sy


# Physical positions from kometa.dtsi (excluding outer none columns 0 and 11)
# Each entry: (dtsi_x, dtsi_y)
PHYS = [
    # Row 0 – top row
    (100,  38), (200,  12), (300,   0), (400,  12), (500,  25),   # Q W E R T
    (900,  25), (1000, 12), (1100,  0), (1200, 12), (1300, 38),   # Y U I O P
    # Row 1 – home row
    (100, 138), (200, 112), (300, 100), (400, 112), (500, 125),   # A S D F G
    (900, 125), (1000,112), (1100,100), (1200,112), (1300,138),   # H J K L ;
    # Row 2 – bottom row
    (100, 238), (200, 212), (300, 200), (400, 212), (500, 225),   # Z X C V B
    (900, 225), (1000,212), (1100,200), (1200,212), (1300,238),   # N M , . /
    # Thumbs (inner 4; outer 2 are &none and skipped)
    (500, 325), (600, 335),                                        # Sym, Spc
    (800, 335), (900, 325),                                        # Ent, Nav
]

# Layers: each key is (label_line1, label_line2_or_empty, style)
LAYERS = [
    {
        "name": "Base",
        "indicator": "#4A90D9",
        "keys": [
            # Row 0
            ("Q","","default"), ("W","","default"), ("E","","default"), ("R","","default"), ("T","","default"),
            ("Y","","default"), ("U","","default"), ("I","","default"), ("O","","default"), ("P","","default"),
            # Row 1
            ("A","⇧ hold","home_mod"), ("S","⌃ hold","home_mod"), ("D","⌘ hold","home_mod"), ("F","⌥ hold","home_mod"), ("G","","default"),
            ("H","","default"), ("J","⌥ hold","home_mod"), ("K","⌘ hold","home_mod"), ("L","⌃ hold","home_mod"), (";","⇧ hold","home_mod"),
            # Row 2
            ("Z","","default"), ("X","","default"), ("C","","default"), ("V","","default"), ("B","","default"),
            ("N","","default"), ("M","","default"), (",","","default"), (".","","default"), ("/","","default"),
            # Thumbs
            ("▼ Sym","","layer"), ("Space","","default"),
            ("Enter","","default"), ("▼ Nav","","layer"),
        ],
    },
    {
        "name": "Symbols",
        "indicator": "#E67E22",
        "keys": [
            # Row 0
            ("!","","default"), ("@","","default"), ("#","","default"), ("$","","default"), ("%","","default"),
            ("","","empty"),    ("&amp;","","default"), ("*","","default"), ("(","","default"), (")","","default"),
            # Row 1
            ("Esc","⇧ hold","home_mod"), ("⌃","","default"), ("⌘","","default"), ("⌥","","default"), ("^","","default"),
            ("−","","default"), ("=","⌥ hold","home_mod"), ("{","⌘ hold","home_mod"), ("}","⌃ hold","home_mod"), ("'","⇧ hold","home_mod"),
            # Row 2
            ("Tab","","default"), ("","","empty"), ("","","empty"), ("","","empty"), ("Boot","","special"),
            ("","","empty"), ("Bksp","","default"), ("[","","default"), ("]","","default"), ("\\","","default"),
            # Thumbs
            ("","","empty"), ("","","empty"),
            ("","","empty"), ("▼ Adj","","layer"),
        ],
    },
    {
        "name": "Nav",
        "indicator": "#27AE60",
        "keys": [
            # Row 0
            ("1","","default"), ("2","","default"), ("3","","default"), ("4","","default"), ("5","","default"),
            ("6","","default"), ("7","","default"), ("8","","default"), ("9","","default"), ("0","","default"),
            # Row 1
            ("⇧","","default"), ("⌃","","default"), ("⌘","","default"), ("⌥","","default"), ("6","","default"),
            ("←","","nav"), ("↓","⌥ hold","home_mod"), ("↑","⌘ hold","home_mod"), ("→","⌃ hold","home_mod"), ("⇧","","default"),
            # Row 2
            ("`","","default"), ("","","empty"), ("","","empty"), ("Del","","default"), ("","","empty"),
            ("Boot","","special"), ("","","empty"), ("","","empty"), ("","","empty"), ("","","empty"),
            # Thumbs
            ("▼ Adj","","layer"), ("","","empty"),
            ("","","empty"), ("","","empty"),
        ],
    },
    {
        "name": "Adjust",
        "indicator": "#8E44AD",
        "keys": [
            # Row 0
            ("F1","","default"), ("F2","","default"), ("F3","","default"), ("F4","","default"), ("","","empty"),
            ("","","empty"),    ("","","empty"), ("","","empty"), ("","","empty"), ("","","empty"),
            # Row 1
            ("F5","","default"), ("F6","","default"), ("F7","","default"), ("F8","","default"), ("","","empty"),
            ("","","empty"), ("Vol−","","media"), ("Mute","","media"), ("Vol+","","media"), ("","","empty"),
            # Row 2
            ("F9","","default"), ("F10","","default"), ("F11","","default"), ("F12","","default"), ("","","empty"),
            ("BT 0","","bt"), ("⏮","","media"), ("⏯","","media"), ("⏭","","media"), ("BT CLR","","bt"),
            # Thumbs
            ("","","empty"), ("","","empty"),
            ("","","empty"), ("","","empty"),
        ],
    },
]

# Combos to annotate on the Base layer
# Full 42-key matrix positions: RC(r,c) → 12*r + c; thumbs start at 36 (RC(3,3))
# esc:  key-positions <15 20> → RC(1,3)=D, RC(1,8)=K  → PHYS[12], PHYS[17]
# caps: key-positions <13 22> → RC(1,1)=A, RC(1,10)=; → PHYS[10], PHYS[19]
# lang: key-positions < 3  8> → RC(0,3)=E, RC(0,8)=I  → PHYS[2],  PHYS[7]
COMBOS = [
    ("Esc",    12, 17),
    ("CapsLk", 10, 19),
    ("Lang",    2,  7),
]


def render_combo_line(x1, y1, x2, y2, label, color="#888888"):
    cx = (x1 + KEY_W/2 + x2 + KEY_W/2) / 2
    cy = (y1 + KEY_H/2 + y2 + KEY_H/2) / 2 - 14
    return (
        f'<line x1="{x1+KEY_W/2:.1f}" y1="{y1+KEY_H/2:.1f}" '
        f'x2="{x2+KEY_W/2:.1f}" y2="{y2+KEY_H/2:.1f}" '
        f'stroke="{color}" stroke-width="1.5" stroke-dasharray="3,2" opacity="0.6"/>'
        f'\n<rect x="{cx-18:.1f}" y="{cy-7:.1f}" width="36" height="14" rx="3" '
        f'fill="white" stroke="{color}" stroke-width="1" opacity="0.9"/>'
        f'\n<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" dominant-baseline="middle" '
        f'font-size="8" fill="{color}" font-weight="bold">{label}</text>'
    )


def generate_svg():
    TITLE_H = 22   # height for layer name label
    KEY_AREA_H = int((335 + 100) * SCALE + MARGIN_Y)   # bottom of thumbs + margin
    LAYER_BLOCK_H = TITLE_H + KEY_AREA_H
    LAYER_GAP = 14
    SVG_W = int((1300 - 100 + 100) * SCALE + MARGIN_X * 2)   # 602
    SVG_H = len(LAYERS) * LAYER_BLOCK_H + (len(LAYERS) - 1) * LAYER_GAP + MARGIN_Y

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'width="{SVG_W}" height="{SVG_H}">',
        '<style>text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }</style>',
        f'<rect width="{SVG_W}" height="{SVG_H}" fill="white"/>',
    ]

    for li, layer in enumerate(LAYERS):
        y_base = MARGIN_Y + li * (LAYER_BLOCK_H + LAYER_GAP)

        # Layer name pill
        color = layer["indicator"]
        name = layer["name"]
        lines.append(
            f'<rect x="{MARGIN_X}" y="{y_base}" width="80" height="{TITLE_H - 2}" rx="9" fill="{color}"/>'
        )
        lines.append(
            f'<text x="{MARGIN_X + 40}" y="{y_base + (TITLE_H - 2)/2}" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'font-size="11" font-weight="bold" fill="white">{name}</text>'
        )

        # Keys
        keys = layer["keys"]
        for ki, ((dx, dy), (l1, l2, style)) in enumerate(zip(PHYS, keys)):
            sx, sy = pos(dx, dy)
            sy += y_base + TITLE_H
            lines.append(key_svg(sx, sy, l1, l2, style))

        # Combo overlays on base layer only
        if li == 0:
            for combo_label, a_idx, b_idx in COMBOS:
                ax, ay = pos(*PHYS[a_idx])
                bx, by = pos(*PHYS[b_idx])
                ay += y_base + TITLE_H
                by += y_base + TITLE_H
                lines.append(render_combo_line(ax, ay, bx, by, combo_label))

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    import os
    os.makedirs("assets", exist_ok=True)
    svg = generate_svg()
    with open("assets/kometa-layout.svg", "w") as f:
        f.write(svg)
    print("Generated assets/kometa-layout.svg")
    # Print dimensions for verification
    import re
    m = re.search(r'width="(\d+)" height="(\d+)"', svg)
    if m:
        print(f"Dimensions: {m.group(1)} x {m.group(2)}")
