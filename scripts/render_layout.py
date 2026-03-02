#!/usr/bin/env python3
"""Render Finerty XKB layout as SVG for use in README."""

import re
import sys

# --- Layout definition ---
# Each entry: keycode, (col, row), width (in key units)
# Standard ISO 104-key physical layout
ISO_LAYOUT = [
    # Function row
    ("ESC",   0.0,  0, 1.0),
    ("FK01",  1.5,  0, 1.0), ("FK02",  2.5,  0, 1.0), ("FK03",  3.5,  0, 1.0), ("FK04",  4.5,  0, 1.0),
    ("FK05",  6.0,  0, 1.0), ("FK06",  7.0,  0, 1.0), ("FK07",  8.0,  0, 1.0), ("FK08",  9.0,  0, 1.0),
    ("FK09", 10.5,  0, 1.0), ("FK10", 11.5,  0, 1.0), ("FK11", 12.5,  0, 1.0), ("FK12", 13.5,  0, 1.0),
    ("PRSC", 15.0,  0, 1.0), ("SCLK", 16.0,  0, 1.0), ("PAUS", 17.0,  0, 1.0),
    # Number row
    ("TLDE",  0.0,  1, 1.0),
    ("AE01",  1.0,  1, 1.0), ("AE02",  2.0,  1, 1.0), ("AE03",  3.0,  1, 1.0), ("AE04",  4.0,  1, 1.0),
    ("AE05",  5.0,  1, 1.0), ("AE06",  6.0,  1, 1.0), ("AE07",  7.0,  1, 1.0), ("AE08",  8.0,  1, 1.0),
    ("AE09",  9.0,  1, 1.0), ("AE10", 10.0,  1, 1.0), ("AE11", 11.0,  1, 1.0), ("AE12", 12.0,  1, 1.0),
    ("BKSP", 13.0,  1, 2.0),
    ("INS",  15.0,  1, 1.0), ("HOME", 16.0,  1, 1.0), ("PGUP", 17.0,  1, 1.0),
    # Top alpha row
    ("TAB",   0.0,  2, 1.5),
    ("AD01",  1.5,  2, 1.0), ("AD02",  2.5,  2, 1.0), ("AD03",  3.5,  2, 1.0), ("AD04",  4.5,  2, 1.0),
    ("AD05",  5.5,  2, 1.0), ("AD06",  6.5,  2, 1.0), ("AD07",  7.5,  2, 1.0), ("AD08",  8.5,  2, 1.0),
    ("AD09",  9.5,  2, 1.0), ("AD10", 10.5,  2, 1.0), ("AD11", 11.5,  2, 1.0), ("AD12", 12.5,  2, 1.0),
    ("RTRN", 13.5,  2, 1.5),
    ("DEL",  15.0,  2, 1.0), ("END",  16.0,  2, 1.0), ("PGDN", 17.0,  2, 1.0),
    # Middle alpha row
    ("CAPS",  0.0,  3, 1.75),
    ("AC01",  1.75, 3, 1.0), ("AC02",  2.75, 3, 1.0), ("AC03",  3.75, 3, 1.0), ("AC04",  4.75, 3, 1.0),
    ("AC05",  5.75, 3, 1.0), ("AC06",  6.75, 3, 1.0), ("AC07",  7.75, 3, 1.0), ("AC08",  8.75, 3, 1.0),
    ("AC09",  9.75, 3, 1.0), ("AC10", 10.75, 3, 1.0), ("AC11", 11.75, 3, 1.0), ("BKSL", 12.75, 3, 2.25),
    # Bottom alpha row
    ("LFSH",  0.0,  4, 2.25),
    ("AB01",  2.25, 4, 1.0), ("AB02",  3.25, 4, 1.0), ("AB03",  4.25, 4, 1.0), ("AB04",  5.25, 4, 1.0),
    ("AB05",  6.25, 4, 1.0), ("AB06",  7.25, 4, 1.0), ("AB07",  8.25, 4, 1.0), ("AB08",  9.25, 4, 1.0),
    ("AB09", 10.25, 4, 1.0), ("AB10", 11.25, 4, 1.0),
    ("RTSH", 12.25, 4, 2.75),
    ("UP",   16.0,  4, 1.0),
    # Space row
    ("LCTL",  0.0,  5, 1.5),
    ("LWIN",  1.5,  5, 1.25),
    ("LALT",  2.75, 5, 1.25),
    ("SPCE",  4.0,  5, 6.25),
    ("RALT", 10.25, 5, 1.25),
    ("RWIN", 11.5,  5, 1.25),
    ("MENU", 12.75, 5, 1.25),
    ("RCTL", 14.0,  5, 1.5),
    ("LEFT", 15.0,  5, 1.0), ("DOWN", 16.0,  5, 1.0), ("RGHT", 17.0,  5, 1.0),
]

# Symbol display overrides (XKB name → display string)
SYMBOL_MAP = {
    "grave": "`", "asciitilde": "~", "section": "§", "onehalf": "½",
    "exclam": "!", "quotedbl": '"', "at": "@", "numbersign": "#",
    "sterling": "£", "dollar": "$", "currency": "¤", "percent": "%",
    "EuroSign": "€", "asciicircum": "^", "dead_circumflex": "^̈",
    "ampersand": "&", "asterisk": "*", "braceleft": "{", "braceright": "}",
    "bracketleft": "[", "bracketright": "]", "parenleft": "(", "parenright": ")",
    "minus": "-", "underscore": "_", "dead_diaeresis": "¨", "equal": "=",
    "plus": "+", "dead_tilde": "~̈", "dead_acute": "´", "dead_grave": "`̈",
    "aring": "å", "Aring": "Å", "odiaeresis": "ö", "Odiaeresis": "Ö",
    "adiaeresis": "ä", "Adiaeresis": "Ä", "apostrophe": "'", "bar": "|",
    "backslash": "\\", "comma": ",", "semicolon": ";", "less": "<",
    "period": ".", "colon": ":", "greater": ">", "slash": "/",
    "question": "?", "space": "Space", "mu": "µ", "NoSymbol": "",
    "Return": "↵", "Tab": "⇥", "BackSpace": "⌫", "Escape": "Esc",
    "Caps_Lock": "Caps", "Shift_L": "Shift", "Shift_R": "Shift",
    "Control_L": "Ctrl", "Control_R": "Ctrl", "Alt_L": "Alt", "Alt_R": "AltGr",
    "ISO_Level3_Shift": "AltGr", "Super_L": "Super", "Super_R": "Super",
    "Menu": "Menu", "Insert": "Ins", "Delete": "Del", "Home": "Home",
    "End": "End", "Prior": "PgUp", "Next": "PgDn",
    "Up": "↑", "Down": "↓", "Left": "←", "Right": "→",
    "Print": "PrtSc", "Scroll_Lock": "ScrLk", "Pause": "Pause",
    "F1":"F1","F2":"F2","F3":"F3","F4":"F4","F5":"F5","F6":"F6",
    "F7":"F7","F8":"F8","F9":"F9","F10":"F10","F11":"F11","F12":"F12",
}

# Labels for keys not in the symbols file
FALLBACK_LABELS = {
    "ESC": "Esc", "BKSP": "⌫", "TAB": "⇥", "RTRN": "↵", "CAPS": "Caps",
    "LFSH": "Shift", "RTSH": "Shift", "LCTL": "Ctrl", "RCTL": "Ctrl",
    "LALT": "Alt", "RALT": "AltGr", "LWIN": "⊞", "RWIN": "⊞", "MENU": "☰",
    "SPCE": "", "INS": "Ins", "DEL": "Del", "HOME": "Home", "END": "End",
    "PGUP": "PgUp", "PGDN": "PgDn", "UP": "↑", "DOWN": "↓", "LEFT": "←", "RGHT": "→",
    "PRSC": "PrtSc", "SCLK": "ScrLk", "PAUS": "Pause",
    "FK01":"F1","FK02":"F2","FK03":"F3","FK04":"F4","FK05":"F5","FK06":"F6",
    "FK07":"F7","FK08":"F8","FK09":"F9","FK10":"F10","FK11":"F11","FK12":"F12",
}


def sym(name):
    name = name.strip()
    if name in SYMBOL_MAP:
        return SYMBOL_MAP[name]
    if len(name) == 1:
        return name
    return name


def parse_symbols(path):
    keys = {}
    with open(path) as f:
        content = f.read()
    pattern = r'key\s+<(\w+)>\s*\{[^[]*\[([^\]]+)\]'
    for m in re.finditer(pattern, content):
        keycode = m.group(1)
        syms = [s.strip() for s in m.group(2).split(',')]
        keys[keycode] = syms
    return keys


def render_svg(keys, output_path):
    U = 54        # key unit in px
    GAP = 4       # gap between keys
    PAD = 20      # padding around board
    CORNER = 6

    # Colors — dark "hacker" theme
    BG = "#1a1b26"
    KEY_BG = "#24283b"
    KEY_BORDER = "#414868"
    KEY_HIGHLIGHT = "#2a2e47"  # keys that have AltGr chars
    TEXT_NORMAL = "#c0caf5"
    TEXT_SHIFT = "#7aa2f7"
    TEXT_ALTGR = "#9ece6a"
    TEXT_ALTSH = "#e0af68"
    TEXT_LABEL = "#565f89"
    ACCENT = "#7aa2f7"

    # Compute canvas size
    max_x = max(x + w for _, x, _, w in ISO_LAYOUT)
    max_y = max(r for _, _, r, _ in ISO_LAYOUT) + 1
    W = int(max_x * U + PAD * 2 + (max_x) * GAP)
    H = int(max_y * U + PAD * 2 + (max_y + 1) * GAP)

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    lines.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')

    # Fonts
    lines.append('''<defs>
  <style>
    .sym { font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace; }
    .label { font-family: "Segoe UI", system-ui, sans-serif; }
  </style>
</defs>''')

    # Title
    lines.append(f'<text x="{W//2}" y="14" text-anchor="middle" font-size="11" fill="{TEXT_LABEL}" class="label" font-weight="600" letter-spacing="2">FINERTY LAYOUT</text>')

    for keycode, col, row, width in ISO_LAYOUT:
        kx = PAD + col * (U + GAP)
        ky = PAD + row * (U + GAP) + 20
        kw = width * U + (width - 1) * GAP
        kh = U

        syms = keys.get(keycode, [])
        has_altgr = len(syms) >= 3 and syms[2].strip() not in ("", "NoSymbol")
        fill = KEY_HIGHLIGHT if has_altgr else KEY_BG

        # Key body
        lines.append(f'<rect x="{kx:.1f}" y="{ky:.1f}" width="{kw:.1f}" height="{kh}" rx="{CORNER}" fill="{fill}" stroke="{KEY_BORDER}" stroke-width="1.5"/>')
        # Inner highlight line
        lines.append(f'<rect x="{kx+2:.1f}" y="{ky+2:.1f}" width="{kw-4:.1f}" height="{kh-4}" rx="{CORNER-2}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>')

        margin = 6
        fs_main = 13
        fs_small = 10

        if keycode in FALLBACK_LABELS and not syms:
            label = FALLBACK_LABELS[keycode]
            lines.append(f'<text x="{kx + kw/2:.1f}" y="{ky + kh/2 + 4:.1f}" text-anchor="middle" font-size="{fs_small}" fill="{TEXT_LABEL}" class="label">{label}</text>')
        elif syms:
            s0 = sym(syms[0]) if len(syms) > 0 else ""
            s1 = sym(syms[1]) if len(syms) > 1 else ""
            s2 = sym(syms[2]) if len(syms) > 2 else ""
            s3 = sym(syms[3]) if len(syms) > 3 else ""

            def esc(s):
                return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

            # Bottom-left: normal
            if s0:
                lines.append(f'<text x="{kx+margin:.1f}" y="{ky+kh-margin:.1f}" font-size="{fs_main}" fill="{TEXT_NORMAL}" class="sym">{esc(s0)}</text>')
            # Top-left: shift
            if s1 and s1 != s0.upper():
                lines.append(f'<text x="{kx+margin:.1f}" y="{ky+margin+fs_small:.1f}" font-size="{fs_small}" fill="{TEXT_SHIFT}" class="sym">{esc(s1)}</text>')
            # Bottom-right: altgr
            if s2 and s2 not in ("", "NoSymbol"):
                lines.append(f'<text x="{kx+kw-margin:.1f}" y="{ky+kh-margin:.1f}" text-anchor="end" font-size="{fs_small}" fill="{TEXT_ALTGR}" class="sym">{esc(s2)}</text>')
            # Top-right: shift+altgr
            if s3 and s3 not in ("", "NoSymbol"):
                lines.append(f'<text x="{kx+kw-margin:.1f}" y="{ky+margin+fs_small:.1f}" text-anchor="end" font-size="{fs_small}" fill="{TEXT_ALTSH}" class="sym">{esc(s3)}</text>')
        else:
            label = FALLBACK_LABELS.get(keycode, keycode)
            lines.append(f'<text x="{kx + kw/2:.1f}" y="{ky + kh/2 + 4:.1f}" text-anchor="middle" font-size="{fs_small}" fill="{TEXT_LABEL}" class="label">{label}</text>')

    # Legend
    legend_y = H - 10
    legend_x = PAD
    items = [
        (TEXT_NORMAL, "Normal"),
        (TEXT_SHIFT,  "Shift"),
        (TEXT_ALTGR,  "AltGr"),
        (TEXT_ALTSH,  "Shift+AltGr"),
    ]
    for color, label in items:
        lines.append(f'<rect x="{legend_x}" y="{legend_y - 10}" width="10" height="10" rx="2" fill="{color}"/>')
        lines.append(f'<text x="{legend_x + 14}" y="{legend_y}" font-size="10" fill="{TEXT_LABEL}" class="label">{label}</text>')
        legend_x += 100

    lines.append('</svg>')

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    symbols_path = sys.argv[1] if len(sys.argv) > 1 else "symbols/fi"
    output_path  = sys.argv[2] if len(sys.argv) > 2 else "layout.svg"
    keys = parse_symbols(symbols_path)
    render_svg(keys, output_path)
