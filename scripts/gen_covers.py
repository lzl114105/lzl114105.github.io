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
     (52, 62, 72), (108, 122, 134), (0.72, 0.22, 0.8), 0.6)

make(f"{ROOT}/content/categories/随笔/cover.png", CW, CH,
     (236, 230, 220), (206, 214, 205), (0.30, 0.26, 0.9), 1.0)

make(f"{ROOT}/content/categories/备忘/cover.png", CW, CH,
     (226, 220, 236), (212, 206, 196), (0.66, 0.74, 0.75), 0.8)

# 头像放 assets/ 而不是 static/:主题的图片 helper 只从 assets/ 取
make(f"{ROOT}/assets/img/avatar.png", 420, 420,
     (226, 220, 208), (108, 132, 120), (0.38, 0.32, 1.05), 0.9, grain=2.6)

if "--all" in sys.argv:
    W, H = 1200, 700
    make(f"{ROOT}/content/post/hello-world/cover.png", W, H,
         (242, 236, 226), (198, 208, 210), (0.24, 0.18, 0.85), 1.0)
    make(f"{ROOT}/content/post/why-hugo/cover.png", W, H,
         (44, 54, 49), (86, 90, 92), (0.78, 0.24, 0.75), 0.6)
    make(f"{ROOT}/content/post/markdown-guide/cover.png", W, H,
         (232, 228, 237), (214, 199, 184), (0.34, 0.72, 0.7), 1.0)
