import re, sys, colorsys

HUE_START = 345
HUE_SPAN  = 50
SKIP = set()

def remap(m):
    hx = m.group(0).lower()
    if hx in SKIP:
        return m.group(0)
    h = hx.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    hue, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.08:
        return m.group(0)
    new_h = ((HUE_START + hue * HUE_SPAN) % 360) / 360
    r, g, b = colorsys.hls_to_rgb(new_h, l, min(1, s * 1.1))
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))

svg = open(sys.argv[1]).read()
open(sys.argv[2], "w").write(re.sub(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", remap, svg))
