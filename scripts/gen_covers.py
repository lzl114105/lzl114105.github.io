"""生成占位封面图：纯标准库拼 PNG，不依赖 Pillow。

用法:
    python scripts/gen_covers.py          # 只生成分类卡片图和头像
    python scripts/gen_covers.py --all     # 连三篇示例文章的封面一起重生成
"""
import zlib, struct, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lerp(a, b, t):
    return a + (b - a) * t


def h2(x, y, s=0):
    n = (x * 374761393 + y * 668265263 + s * 1442695040) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0 - 0.5


def make(path, w, h, c1, c2, glow, diag=1.0, grain=2.2, vignette=0.10):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            t = (x / w * diag + y / h * (1 - diag * 0.55))
            t = min(1.0, max(0.0, t))
            t = t * t * (3 - 2 * t)
            gx = (x / w - glow[0]) * 1.7
            gy = (y / h - glow[1]) * 1.7
            d = math.sqrt(gx * gx + gy * gy)
            g = max(0.0, 1.0 - d) ** 2 * glow[2]
            vx = (x / w - 0.5) * 2
            vy = (y / h - 0.5) * 2
            v = 1.0 - (vx * vx + vy * vy) * vignette
            n = h2(x, y) * grain
            for i in range(3):
                c = lerp(c1[i], c2[i], t) + g * 14 + n
                c *= v
                raw.append(0 if c < 0 else (255 if c > 255 else int(c)))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    print("ok", path.replace(ROOT, "."), len(png) // 1024, "KB")


# 分类卡片图:卡片区域是 250x150,源图 800x500 够用
CW, CH = 800, 500

make(f"{ROOT}/content/categories/技术/cover.png", CW, CH,
     (124, 152, 216), (180, 202, 240), (0.72, 0.22, 0.9), 0.7, grain=1.6)

make(f"{ROOT}/content/categories/随笔/cover.png", CW, CH,
     (238, 158, 178), (250, 210, 200), (0.28, 0.24, 1.0), 1.0, grain=1.6)

make(f"{ROOT}/content/categories/备忘/cover.png", CW, CH,
     (150, 206, 188), (240, 224, 192), (0.68, 0.74, 0.9), 0.8, grain=1.6)

if "--all" in sys.argv:
    W, H = 1200, 700
    make(f"{ROOT}/content/post/hello-world/cover.png", W, H,
         (250, 214, 198), (214, 198, 236), (0.22, 0.18, 1.0), 1.0, grain=1.6)
    make(f"{ROOT}/content/post/why-hugo/cover.png", W, H,
         (160, 196, 232), (176, 214, 206), (0.76, 0.24, 0.9), 0.7, grain=1.6)
    make(f"{ROOT}/content/post/markdown-guide/cover.png", W, H,
         (208, 192, 236), (244, 190, 204), (0.32, 0.70, 0.85), 1.0, grain=1.6)
