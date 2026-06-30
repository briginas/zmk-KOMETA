#!/usr/bin/env python3
"""Generate an editable diagrams.net keymap diagram for the Kometa keyboard."""

import os
from html import escape

from gen_svg import (
    KEY_H,
    KEY_W,
    LAYER_STRIDE,
    LAYERS,
    PANEL_H,
    PANEL_W,
    PANEL_X,
    PANEL_Y,
    SVG_HEIGHT,
    SVG_WIDTH,
    THUMB_ROTATIONS,
    key_position,
)


DRAWIO_VERSION = "24.7.17"
DRAWIO_MODIFIED = "2026-06-30T00:00:00.000Z"

KEY_STYLES = {
    "normal": {
        "fill": "#383e47",
        "stroke": "#05070a",
        "font": "#edf2f7",
    },
    "layer-red": {
        "fill": "#a20025",
        "stroke": "#6f0000",
        "font": "#edf2f7",
    },
    "layer-gold": {
        "fill": "#d9a725",
        "stroke": "#b08312",
        "font": "#111820",
    },
    "layer-blue": {
        "fill": "#5c8cca",
        "stroke": "#456893",
        "font": "#111820",
    },
    "special": {
        "fill": "#495566",
        "stroke": "#121820",
        "font": "#edf2f7",
    },
    "empty": {
        "fill": "#202833",
        "stroke": "#596170",
        "font": "#edf2f7",
    },
}

BAR_STYLES = {
    "bar-base": ("#3f4a59", "#556173"),
    "bar-sym": ("#a20025", "#6f0000"),
    "bar-nav": ("#d9a725", "#b08312"),
    "bar-adj": ("#5c8cca", "#456893"),
}


def attr(value):
    return escape(str(value), quote=True)


def cell(cell_id, value, style, x, y, width, height):
    return (
        f'    <mxCell id="{attr(cell_id)}" value="{attr(value)}" '
        f'style="{attr(style)}" vertex="1" parent="1">\n'
        f'      <mxGeometry x="{x:.0f}" y="{y:.0f}" width="{width:.0f}" '
        f'height="{height:.0f}" as="geometry"/>\n'
        "    </mxCell>"
    )


def rect_style(fill, stroke, rounded=True, extra=""):
    rounded_flag = "1" if rounded else "0"
    style = (
        f"rounded={rounded_flag};whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};"
        "arcSize=12;align=center;verticalAlign=middle;"
    )
    if extra:
        style += extra
    return style


def text_style(font_color, font_size, bold=False, extra=""):
    font_style = "1" if bold else "0"
    style = (
        "text;html=1;strokeColor=none;fillColor=none;"
        f"fontColor={font_color};fontSize={font_size};fontStyle={font_style};"
        "align=center;verticalAlign=middle;resizable=0;points=[];"
    )
    if extra:
        style += extra
    return style


def key_label(key):
    label = key["label"]
    sub = key["sub"]

    if label and sub:
        return (
            f"{escape(label)}<br>"
            f'<font style="font-size: 8px; color: #9fb0c3">{escape(sub)}</font>'
        )
    if label:
        return escape(label)
    return ""


def key_font_size(key):
    return 10 if len(key["label"]) > 3 or key["sub"] else 15


def render_key(layer_id, layer_offset_y, index, key):
    x, y = key_position(index)
    style = KEY_STYLES[key["style"]]
    extra = (
        f"fontColor={style['font']};fontStyle=1;fontSize={key_font_size(key)};"
        "spacing=2;connectable=0;"
    )
    if key["style"] == "empty":
        extra += "dashed=1;dashPattern=4 4;"

    rotation = THUMB_ROTATIONS.get(index)
    if rotation:
        extra += f"rotation={rotation};"

    return cell(
        f"{layer_id}-key-{index}",
        key_label(key),
        rect_style(style["fill"], style["stroke"], extra=extra),
        x,
        layer_offset_y + y,
        KEY_W,
        KEY_H,
    )


def render_layer(index, layer):
    layer_offset_y = index * LAYER_STRIDE
    layer_id = layer["id"]
    bar_fill, bar_stroke = BAR_STYLES[layer["bar"]]
    cells = [
        cell(
            f"{layer_id}-panel",
            "",
            rect_style("#151b24", "#293241", extra="connectable=0;"),
            PANEL_X,
            layer_offset_y + PANEL_Y,
            PANEL_W,
            PANEL_H,
        ),
        cell(
            f"{layer_id}-bar",
            "",
            rect_style(bar_fill, bar_stroke, extra="connectable=0;"),
            305,
            layer_offset_y + 28,
            210,
            30,
        ),
        cell(
            f"{layer_id}-title",
            escape(layer["name"]),
            text_style("#ffffff", 16, bold=True),
            305,
            layer_offset_y + 28,
            210,
            30,
        ),
        cell(
            f"{layer_id}-note",
            escape(layer["note"]),
            text_style("#aeb9c8", 12),
            230,
            layer_offset_y + 58,
            360,
            28,
        ),
    ]

    cells.extend(
        render_key(layer_id, layer_offset_y, key_index, key)
        for key_index, key in enumerate(layer["keys"])
    )

    if layer.get("combo"):
        cells.append(
            cell(
                f"{layer_id}-combo",
                escape(layer["combo"]),
                text_style("#7ea6e0", 12),
                165,
                layer_offset_y + 300,
                490,
                28,
            )
        )

    return "\n".join(cells)


def generate_drawio():
    layers = "\n".join(render_layer(index, layer) for index, layer in enumerate(LAYERS))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="{DRAWIO_MODIFIED}" agent="Cursor" version="{DRAWIO_VERSION}" type="device">
  <diagram id="kometa-layout" name="Kometa layout">
    <mxGraphModel dx="1060" dy="760" grid="1" gridSize="10" guides="1" tooltips="1" connect="0" arrows="0" fold="1" page="1" pageScale="1" pageWidth="{SVG_WIDTH}" pageHeight="{SVG_HEIGHT}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{cell("sheet", "", rect_style("#10141b", "none", rounded=False, extra="connectable=0;"), 0, 0, SVG_WIDTH, SVG_HEIGHT)}
{layers}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    with open("assets/kometa-layout.drawio", "w", encoding="utf-8") as f:
        f.write(generate_drawio())
    print("Generated assets/kometa-layout.drawio")
