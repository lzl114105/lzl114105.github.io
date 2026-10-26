"""生成插画风封面：纯标准库逐像素绘制，不依赖 Pillow。

画的是极简动画场景：渐变天空 + 太阳/月亮 + 多层起伏山峦 + 星点 + 颗粒。
不涉及任何第三方素材，输出可直接商用。

用法:
    python scripts/gen_scene_covers.py           # 分类卡片 + 文章封面
    python scripts/gen_scene_covers.py --only post
"""
import zlib, struct, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = 0.0 if t < 0 else (1.0 if t > 1 else t)
    return t * t * (3 - 2 * t)


def noise(x, y, s=0):
    n = (x * 374761393 + y * 668265263 + s * 1442695040) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def ridge(xf, base, waves):
    y = base
    for amp, freq, phase in waves:
        y += amp * math.sin(2 * math.pi * freq * xf + phase)
    return y


def scene(path, w, h, sky_top, sky_bot, hills, sun=None, stars=False, grain=2.4):
    """hills: [(color, base, waves), ...] 由远及近"""
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        yf = y / h
        for x in range(w):
            xf = x / w

            # 天空：由暗到亮的竖向渐变
            t = smooth(yf * 1.12)
            c = [lerp(sky_top[i], sky_bot[i], t) for i in range(3)]

            # 星点（只在上半部，越靠上越亮）
            if stars and yf < 0.62:
                n = noise(x, y, 7)
                if n > 0.9985 - (0.62 - yf) * 0.0012:
                    c = [min(255, v + 150) for v in c]

            # 日/月 + 光晕
            if sun:
                sx, sy, sr, scol, sglow = sun
                dx = (xf - sx) * (w / h) * 1.0
                dy = yf - sy
                d = math.sqrt(dx * dx + dy * dy)
                g = math.exp(-(d / (sr * 3.4)) ** 2) * sglow
                for i in range(3):
                    c[i] = lerp(c[i], scol[i], min(0.95, g))
                if d < sr:
                    c = [lerp(scol[i], 255, 0.35) for i in range(3)]

            # 山峦：由远及近覆盖
            for color, base, waves in hills:
                if yf > ridge(xf, base, waves):
                    c = list(color)
                    break

            # 颗粒
            nz = (noise(x, y, 3) - 0.5) * grain
            raw.extend(int(max(0, min(255, v + nz))) for v in c)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    print("ok", path.replace(ROOT, "."), len(png) // 1024, "KB")


# ── 三篇文章封面 ─────────────────────────────────────────────────────────
PW, PH = 1200, 800

# 暮色：紫→杏的天空，青黛山影
scene(f"{ROOT}/content/post/hello-world/cover.png", PW, PH,
      (56, 42, 84), (252, 190, 152),
      [((126, 116, 156), 0.56, [(0.012, 1.3, 0.4), (0.008, 3.1, 1.9)]),
       ((84, 92, 126), 0.66, [(0.016, 1.7, 2.2), (0.007, 4.3, 0.6)]),
       ((44, 50, 72), 0.79, [(0.014, 2.1, 4.1), (0.006, 5.7, 2.7)])],
      sun=(0.71, 0.42, 0.075, (255, 236, 202), 0.95))

# 夜：深靛天空 + 月 + 星
scene(f"{ROOT}/content/post/why-hugo/cover.png", PW, PH,
      (14, 16, 38), (74, 68, 116),
      [((54, 56, 92), 0.58, [(0.012, 1.1, 1.1), (0.008, 2.9, 3.4)]),
       ((32, 34, 58), 0.70, [(0.016, 1.9, 2.8), (0.007, 4.1, 1.2)]),
       ((14, 15, 28), 0.83, [(0.013, 2.3, 4.6), (0.006, 5.3, 0.2)])],
      sun=(0.67, 0.30, 0.055, (232, 236, 255), 0.55), stars=True, grain=3.0)

# 晨：粉→奶油，叠一层浅绛
scene(f"{ROOT}/content/post/markdown-guide/cover.png", PW, PH,
      (255, 214, 226), (255, 246, 230),
      [((232, 182, 196), 0.60, [(0.012, 1.2, 2.0), (0.008, 3.3, 0.9)]),
       ((204, 156, 176), 0.71, [(0.016, 1.6, 3.6), (0.007, 4.7, 2.1)]),
       ((132, 104, 128), 0.84, [(0.014, 2.0, 5.0), (0.006, 5.1, 1.5)])],
      sun=(0.29, 0.31, 0.085, (255, 252, 244), 1.0))

# ── 三个分类卡片 ─────────────────────────────────────────────────────────
CW, CH = 900, 600

scene(f"{ROOT}/assets/img/cat-tech.png", CW, CH,
      (36, 58, 108), (168, 198, 238),
      [((106, 138, 190), 0.60, [(0.012, 1.4, 0.8), (0.008, 3.2, 2.6)]),
       ((66, 92, 146), 0.71, [(0.016, 1.8, 3.3), (0.007, 4.6, 1.1)]),
       ((34, 50, 88), 0.84, [(0.014, 2.2, 5.2), (0.006, 5.5, 0.4)])],
      sun=(0.74, 0.34, 0.06, (226, 238, 255), 0.7), stars=True, grain=2.8)

scene(f"{ROOT}/assets/img/cat-life.png", CW, CH,
      (72, 44, 74), (252, 178, 178),
      [((186, 118, 138), 0.60, [(0.012, 1.3, 1.6), (0.008, 3.0, 4.0)]),
       ((138, 84, 106), 0.71, [(0.016, 1.7, 2.4), (0.007, 4.2, 0.9)]),
       ((66, 42, 58), 0.84, [(0.014, 2.1, 5.6), (0.006, 5.2, 3.1)])],
      sun=(0.30, 0.38, 0.072, (255, 226, 214), 0.9))

scene(f"{ROOT}/assets/img/cat-note.png", CW, CH,
      (28, 66, 74), (198, 232, 216),
      [((126, 186, 172), 0.60, [(0.012, 1.5, 0.2), (0.008, 3.4, 2.9)]),
       ((80, 136, 130), 0.71, [(0.016, 1.9, 3.9), (0.007, 4.4, 1.4)]),
       ((36, 70, 76), 0.84, [(0.014, 2.3, 5.9), (0.006, 5.6, 0.7)])],
      sun=(0.66, 0.30, 0.058, (236, 250, 244), 0.6), stars=True, grain=2.8)
