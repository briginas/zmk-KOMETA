#!/usr/bin/env python3
"""Generate a Sweep-style SVG keymap diagram for the Kometa keyboard."""

from html import escape


SVG_WIDTH = 820
SVG_HEIGHT = 1370
KEY_W = 48
KEY_H = 42
KEY_CENTER_X = KEY_W / 2
KEY_CENTER_Y = KEY_H / 2

PANEL_X = 32
PANEL_Y = 12
PANEL_W = 756
PANEL_H = 320
LAYER_STRIDE = 340

POS_X_OFFSET = 40
POS_X_SCALE = 0.48
POS_Y_OFFSET = 70
POS_Y_SCALE = 0.59

THUMB_ROTATIONS = {
    36: 0,
    37: 15,
    38: 30,
    39: -30,
    40: -15,
    41: 0,
}


def k(label="", sub="", style="normal"):
    return {"label": label, "sub": sub, "style": style}


def empty(label="", sub=""):
    return k(label, sub, "empty")


# Full 42-key physical layout from boards/shields/kometa/kometa.dtsi:
# three 12-key rows plus six thumb keys. Positions mapped from RC order.
PHYS = [
    # Row 0
    (0, 48), (100, 38), (200, 12), (300, 0), (400, 12), (500, 25),
    (900, 25), (1000, 12), (1100, 0), (1200, 12), (1300, 38), (1400, 48),
    # Row 1
    (0, 148), (100, 138), (200, 112), (300, 100), (400, 112), (500, 125),
    (900, 125), (1000, 112), (1100, 100), (1200, 112), (1300, 138), (1400, 148),
    # Row 2
    (0, 248), (100, 238), (200, 212), (300, 200), (400, 212), (500, 225),
    (900, 225), (1000, 212), (1100, 200), (1200, 212), (1300, 238), (1400, 248),
    # Thumbs
    (400, 312), (500, 325), (600, 335), (800, 335), (900, 325), (1000, 312),
]


LAYERS = [
    {
        "id": "base-layer",
        "name": "Base",
        "bar": "bar-base",
        "note": "QWERTY with balanced home row mods",
        "combo": "Combos: D+K = Esc | A+; = Caps | E+I = Lang",
        "keys": [
            empty(), k("Q"), k("W"), k("E"), k("R"), k("T"),
            k("Y"), k("U"), k("I"), k("O"), k("P"), empty(),
            empty(), k("A", "Sft"), k("S", "Ctl"), k("D", "Gui"), k("F", "Alt"), k("G"),
            k("H"), k("J", "Alt"), k("K", "Gui"), k("L", "Ctl"), k(";", "Sft"), empty(),
            empty(), k("Z"), k("X"), k("C"), k("V"), k("B"),
            k("N"), k("M"), k(","), k("."), k("/"), empty(),
            empty(), k("Sym", style="layer-red"), k("Space", style="special"),
            k("Enter", style="special"), k("Nav", style="layer-gold"), empty(),
        ],
    },
    {
        "id": "symbols-layer",
        "name": "Symbols",
        "bar": "bar-sym",
        "note": "Hold left thumb from Base",
        "keys": [
            empty(), k("!"), k("@"), k("#"), k("$"), k("%"),
            empty(), k("&"), k("*"), k("("), k(")"), empty(),
            empty(), k("Esc", "Sft", "special"), k("LCtl"), k("LGui"), k("LAlt"), k("^"),
            k("-"), k("=", "Alt"), k("{", "Gui"), k("}", "Ctl"), k("'", "Sft"), empty(),
            empty(), k("Tab", style="special"), empty(), empty(), empty(), k("Boot", style="layer-blue"),
            empty(), k("Bspc", style="special"), k("["), k("]"), k("\\"), empty(),
            empty(), empty(), empty(), empty(), k("Adjust", style="layer-blue"), empty(),
        ],
    },
    {
        "id": "nav-layer",
        "name": "Nav",
        "bar": "bar-nav",
        "note": "Hold right thumb from Base",
        "keys": [
            empty(), k("1"), k("2"), k("3"), k("4"), k("5"),
            k("6"), k("7"), k("8"), k("9"), k("0"), empty(),
            empty(), k("LSft"), k("LCtl"), k("LGui"), k("LAlt"), k("6"),
            k("Left", style="special"), k("Down", "Alt", "special"), k("Up", "Gui", "special"),
            k("Right", "Ctl", "special"), k("RSft"), empty(),
            empty(), k("`"), empty("TRNS"), empty("TRNS"), k("Del", style="special"), empty("TRNS"),
            k("Boot", style="layer-blue"), empty(), empty(), empty(), empty(), empty(),
            empty(), k("Adjust", style="layer-blue"), empty(), empty(), empty(), empty(),
        ],
    },
    {
        "id": "adjust-layer",
        "name": "Adjust",
        "bar": "bar-adj",
        "note": "From Symbols right thumb or Nav left thumb",
        "keys": [
            empty(), k("F1"), k("F2"), k("F3"), k("F4"), empty(),
            empty(), empty(), empty(), empty(), empty(), empty(),
            empty(), k("F5"), k("F6"), k("F7"), k("F8"), empty(),
            empty(), k("Vol-", style="special"), k("Mute", style="special"), k("Vol+", style="special"), empty(), empty(),
            empty(), k("F9"), k("F10"), k("F11"), k("F12"), empty(),
            k("BT", "0", "layer-blue"), k("Prev", style="special"), k("Play", style="special"),
            k("Next", style="special"), k("BT", "CLR", "layer-blue"), empty(),
            empty(), empty(), empty(), empty(), empty(), empty(),
        ],
    },
]


def key_position(index):
    dtsi_x, dtsi_y = PHYS[index]
    return (
        POS_X_OFFSET + dtsi_x * POS_X_SCALE,
        POS_Y_OFFSET + dtsi_y * POS_Y_SCALE,
    )


def key_id(style):
    return f"key-{style}"


def text_class(key):
    style = key["style"]
    small = len(key["label"]) > 3 or bool(key["sub"])

    if style in {"layer-gold", "layer-blue"}:
        return "key-text-dark-small" if small else "key-text-dark"

    return "key-text-small" if small else "key-text"


def render_key(index, key):
    x, y = key_position(index)
    rotation = THUMB_ROTATIONS.get(index)
    transform = f"translate({x:.0f} {y:.0f})"
    if rotation:
        transform += f" rotate({rotation} {KEY_CENTER_X:.0f} {KEY_CENTER_Y:.0f})"

    lines = [f'    <g transform="{transform}"><use href="#{key_id(key["style"])}"/>']

    label = escape(key["label"])
    sub = escape(key["sub"])
    cls = text_class(key)

    if label and sub:
        lines.append(f'<text class="{cls}" x="24" y="17">{label}</text>')
        lines.append(f'<text class="key-sub" x="24" y="30">{sub}</text>')
    elif label:
        lines.append(f'<text class="{cls}" x="24" y="21">{label}</text>')

    lines.append("</g>")
    return "".join(lines)


def render_layer(layer, offset_y):
    lines = [
        f'  <g id="{layer["id"]}" transform="translate(0 {offset_y})">',
        f'    <rect class="layer-panel" x="{PANEL_X}" y="{PANEL_Y}" '
        f'width="{PANEL_W}" height="{PANEL_H}" rx="8" ry="8"/>',
        f'    <rect class="{layer["bar"]}" x="305" y="28" width="210" height="30" rx="4" ry="4"/>',
        f'    <text class="title-text" x="410" y="43">{escape(layer["name"])}</text>',
        f'    <text class="note-text" x="410" y="72">{escape(layer["note"])}</text>',
        "",
    ]

    if len(layer["keys"]) != len(PHYS):
        raise ValueError(f'{layer["name"]} has {len(layer["keys"])} keys, expected {len(PHYS)}')

    row_breaks = {12, 24, 36}
    for index, key in enumerate(layer["keys"]):
        if index in row_breaks:
            lines.append("")
        lines.append(render_key(index, key))

    if layer.get("combo"):
        lines.extend([
            "",
            f'    <text class="combo-text" x="410" y="314">{escape(layer["combo"])}</text>',
        ])

    lines.append("  </g>")
    return "\n".join(lines)


def generate_svg():
    layers_svg = "\n\n".join(
        render_layer(layer, index * LAYER_STRIDE)
        for index, layer in enumerate(LAYERS)
    )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">Kometa keymap layout</title>
  <desc id="desc">Four-layer layout diagram for the Kometa ZMK keymap.</desc>
  <defs>
    <g id="key-normal">
      <rect class="key-normal" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-layer-red">
      <rect class="key-layer-red" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-layer-gold">
      <rect class="key-layer-gold" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-layer-blue">
      <rect class="key-layer-blue" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-special">
      <rect class="key-special" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-empty">
      <rect class="key-empty" width="48" height="42" rx="6" ry="6"/>
    </g>
    <style>
      .sheet {{ fill: #10141b; }}
      .layer-panel {{ fill: #151b24; stroke: #293241; stroke-width: 1; }}
      .bar-base {{ fill: #3f4a59; stroke: #556173; }}
      .bar-sym {{ fill: #a20025; stroke: #6f0000; }}
      .bar-nav {{ fill: #d9a725; stroke: #b08312; }}
      .bar-adj {{ fill: #5c8cca; stroke: #456893; }}
      .key-normal {{ fill: #383e47; stroke: #05070a; stroke-width: 1; }}
      .key-layer-red {{ fill: #a20025; stroke: #6f0000; stroke-width: 1; }}
      .key-layer-gold {{ fill: #d9a725; stroke: #b08312; stroke-width: 1; }}
      .key-layer-blue {{ fill: #5c8cca; stroke: #456893; stroke-width: 1; }}
      .key-special {{ fill: #495566; stroke: #121820; stroke-width: 1; }}
      .key-empty {{ fill: #202833; stroke: #596170; stroke-width: 1; stroke-dasharray: 4 4; }}
      .title-text {{ fill: #ffffff; font: 700 16px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .note-text {{ fill: #aeb9c8; font: 12px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text {{ fill: #edf2f7; font: 700 15px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text-dark {{ fill: #111820; font: 700 14px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text-small {{ fill: #edf2f7; font: 700 10px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text-dark-small {{ fill: #111820; font: 700 10px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-sub {{ fill: #9fb0c3; font: 700 8.5px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .combo-text {{ fill: #7ea6e0; font: 12px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
    </style>
  </defs>

  <rect class="sheet" width="{SVG_WIDTH}" height="{SVG_HEIGHT}"/>

{layers_svg}
</svg>
'''


if __name__ == "__main__":
    import os

    os.makedirs("assets", exist_ok=True)
    with open("assets/kometa-layout.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg())
    print("Generated assets/kometa-layout.svg")
