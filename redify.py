import re, sys, colorsys

SKIP = {"#3178c6", "#3572a5", "#563d7c", "#da5b0b", "#f1e05a", "#444444"}  # pie langs
L_SPLIT = 0.40   # below → blue, above → red
RED, BLUE = 355, 222

def to_hex(r, g, b):
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))

def recolor(r, g, b, orig):
    if to_hex(r, g, b) in SKIP:
        return orig
    hue, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.08:
        return orig
    h = (BLUE if l < L_SPLIT else RED) / 360
    return to_hex(*colorsys.hls_to_rgb(h, l, min(1, max(s, 0.6))))

def sub(m):
    t = m.group(0)
    if t.startswith("#"):
        h = t[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    else:
        n = [float(x) for x in re.findall(r"[\d.]+", t)[:3]]
        if t.startswith("rgb"):
            r, g, b = (x / 255 for x in n)
        else:
            r, g, b = colorsys.hls_to_rgb(n[0] / 360, n[2] / 100, n[1] / 100)
    return recolor(r, g, b, t)

svg = open(sys.argv[1]).read()
pat = r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgb\([^)]*\)|hsl\([^)]*\)"
open(sys.argv[2], "w").write(re.sub(pat, sub, svg))
