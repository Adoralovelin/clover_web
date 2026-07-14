"""Accurate cactus sprite crop: flood-fill BG, keep interiors, align frames."""
from pathlib import Path
import numpy as np
from PIL import Image
from collections import deque
from scipy import ndimage

SRC = Path(
    r"c:\Users\Adora L\Downloads\stitch_little_artist_gallery\assets\magic_show"
    r"\ChatGPT Image Jul 13, 2026, 08_00_38 PM.png"
)
OUT_DIR = Path(r"c:\Users\Adora L\Downloads\stitch_little_artist_gallery\website\images")
OUT_SHEET = OUT_DIR / "cactus-sprite.png"
OUT_FRAMES = OUT_DIR / "cactus-frames"
OUT_DEBUG = OUT_DIR / "cactus-crop-debug.png"

COLS, ROWS = 4, 2


def looks_like_bg(r, g, b) -> bool:
    """Checker / near-white guide pixels (not boot highlights inside character)."""
    chroma = max(abs(int(r) - int(g)), abs(int(g) - int(b)), abs(int(r) - int(b)))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    if r >= 250 and g >= 250 and b >= 250:
        return True
    # checkerboard greys
    if chroma <= 20 and 165 <= lum <= 248:
        return True
    return False


def flood_transparent(arr: np.ndarray) -> np.ndarray:
    """Make background transparent by flooding from image borders only.

    Interior whites (boot shine, flower center) stay because they are not
    connected to the border through background-colored pixels.
    """
    h, w = arr.shape[:2]
    rgba = arr.copy()
    vis = np.zeros((h, w), dtype=bool)
    q = deque()

    def try_push(y, x):
        if y < 0 or x < 0 or y >= h or x >= w or vis[y, x]:
            return
        r, g, b, a = rgba[y, x]
        if a == 0 or looks_like_bg(r, g, b):
            vis[y, x] = True
            q.append((y, x))

    for x in range(w):
        try_push(0, x)
        try_push(h - 1, x)
    for y in range(h):
        try_push(y, 0)
        try_push(y, w - 1)

    while q:
        y, x = q.popleft()
        rgba[y, x, 3] = 0
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            try_push(y + dy, x + dx)

    # Soft fringe: bg-looking pixels adjacent to already-cleared, only 1px
    # and only if low-chroma (avoid eating red flower / green body)
    alpha = rgba[:, :, 3] > 0
    cleared = ~alpha
    near = ndimage.binary_dilation(cleared, iterations=1) & alpha
    r = rgba[:, :, 0].astype(np.int16)
    g = rgba[:, :, 1].astype(np.int16)
    b = rgba[:, :, 2].astype(np.int16)
    chroma = np.maximum(np.maximum(np.abs(r - g), np.abs(g - b)), np.abs(r - b))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    fringe = near & (chroma <= 25) & (lum >= 175)
    rgba[fringe, 3] = 0
    return rgba


def character_mask(arr: np.ndarray) -> np.ndarray:
    return arr[:, :, 3] > 0


def isolate_cell(cell: np.ndarray) -> np.ndarray:
    """Keep the main cactus blob; drop tiny neighbor bleed chips."""
    mask = character_mask(cell)
    if not mask.any():
        out = cell.copy()
        out[:, :, 3] = 0
        return out

    labeled, n = ndimage.label(mask)
    h, w = mask.shape
    cx, cy = w / 2.0, h * 0.55  # bias toward body center

    best, best_score = 0, -1e18
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        area = len(xs)
        if area < 80:
            continue
        mx, my = xs.mean(), ys.mean()
        touches = (xs.min() <= 0) or (xs.max() >= w - 1)
        # small edge-touching chips = bleed
        if touches and area < 2500:
            continue
        score = area - np.hypot(mx - cx, my - cy) * 12
        if score > best_score:
            best_score, best = score, i

    if best == 0:
        sizes = ndimage.sum(mask, labeled, range(1, n + 1))
        best = int(np.argmax(sizes)) + 1

    keep = labeled == best
    # Include tiny nearby fragments that are part of outline (1px gaps)
    keep = ndimage.binary_dilation(keep, iterations=2) & mask

    out = cell.copy()
    out[~keep, 3] = 0
    return out


def tight_bbox(alpha: np.ndarray, pad: int = 2):
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0:
        return None
    h, w = alpha.shape
    return (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w - 1, int(xs.max()) + pad),
        min(h - 1, int(ys.max()) + pad),
    )


def density_splits(mask: np.ndarray, axis: int, parts: int) -> list[int]:
    """Split along axis using low-density valleys near equal divisions."""
    proj = mask.astype(np.float32).sum(axis=axis)
    k = 31
    smooth = np.convolve(proj, np.ones(k) / k, mode="same")
    n = len(smooth)
    splits = [0]
    for i in range(1, parts):
        ideal = int(n * i / parts)
        lo = max(8, int(ideal - n * 0.07))
        hi = min(n - 8, int(ideal + n * 0.07))
        splits.append(int(np.argmin(smooth[lo:hi])) + lo)
    splits.append(n)
    return splits


def body_center_x(alpha: np.ndarray) -> float:
    """Center from lower body / boots for stable run alignment."""
    h, w = alpha.shape
    band = alpha[int(h * 0.55) :, :]
    if band.any():
        _, xs = np.where(band)
        return float(xs.mean())
    _, xs = np.where(alpha)
    return float(xs.mean()) if len(xs) else w / 2


def feet_y(alpha: np.ndarray) -> int:
    rows = np.where(alpha.any(axis=1))[0]
    return int(rows[-1]) if len(rows) else alpha.shape[0] - 1


def main():
    raw = np.array(Image.open(SRC).convert("RGBA"))
    h, w = raw.shape[:2]
    print(f"source: {w}x{h}")

    rgba = flood_transparent(raw)
    mask = character_mask(rgba)
    x_splits = density_splits(mask, axis=0, parts=COLS)
    y_splits = density_splits(mask, axis=1, parts=ROWS)
    print("x_splits", x_splits)
    print("y_splits", y_splits)

    OUT_FRAMES.mkdir(parents=True, exist_ok=True)
    crops, metas = [], []

    for row in range(ROWS):
        for col in range(COLS):
            x0, x1 = x_splits[col], x_splits[col + 1]
            y0, y1 = y_splits[row], y_splits[row + 1]
            cell = rgba[y0:y1, x0:x1].copy()
            # gentle side inset to discourage bleed, then re-isolate
            inset = 3
            if cell.shape[1] > inset * 2:
                cell[:, :inset, 3] = 0
                cell[:, -inset:, 3] = 0
            isolated = isolate_cell(cell)
            bb = tight_bbox(isolated[:, :, 3], pad=2)
            idx = row * COLS + col
            if bb is None:
                print(f"frame {idx}: EMPTY")
                crops.append(Image.new("RGBA", (64, 64), (0, 0, 0, 0)))
                metas.append(None)
                continue
            bx0, by0, bx1, by1 = bb
            cropped = isolated[by0 : by1 + 1, bx0 : bx1 + 1]
            alpha = cropped[:, :, 3] > 0
            fw, fh = cropped.shape[1], cropped.shape[0]
            meta = {
                "idx": idx,
                "size": (fw, fh),
                "feet_y": feet_y(alpha),
                "body_cx": body_center_x(alpha),
            }
            metas.append(meta)
            crops.append(Image.fromarray(cropped))
            print(
                f"frame {idx}: {fw}x{fh} feet={meta['feet_y']} "
                f"body_cx={meta['body_cx']:.1f}"
            )

    max_left = max_right = max_above = max_below = 0
    for meta in metas:
        if not meta:
            continue
        fw, fh = meta["size"]
        cx, feet = meta["body_cx"], meta["feet_y"]
        max_left = max(max_left, int(np.ceil(cx)))
        max_right = max(max_right, int(np.ceil(fw - cx)))
        max_above = max(max_above, feet)
        max_below = max(max_below, fh - 1 - feet)

    pad = 4
    canvas_w = max_left + max_right + pad * 2
    canvas_h = max_above + max_below + pad * 2
    canvas_w += canvas_w % 2
    canvas_h += canvas_h % 2
    ox, oy = pad + max_left, pad + max_above
    print(f"aligned canvas: {canvas_w}x{canvas_h}")

    aligned = []
    for fr, meta in zip(crops, metas):
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        if meta:
            x = int(round(ox - meta["body_cx"]))
            y = int(round(oy - meta["feet_y"]))
            canvas.paste(fr, (x, y), fr)
        aligned.append(canvas)
        canvas.save(OUT_FRAMES / f"frame_{meta['idx'] if meta else len(aligned)-1:02d}.png")

    sheet = Image.new("RGBA", (canvas_w * COLS, canvas_h * ROWS), (0, 0, 0, 0))
    for i, fr in enumerate(aligned):
        sheet.paste(fr, ((i % COLS) * canvas_w, (i // COLS) * canvas_h), fr)
    sheet.save(OUT_SHEET)

    # checker debug
    dbg = Image.new("RGB", sheet.size)
    px = dbg.load()
    sp = sheet.load()
    for y in range(sheet.size[1]):
        for x in range(sheet.size[0]):
            base = (220, 220, 220) if ((x // 12) + (y // 12)) % 2 == 0 else (245, 245, 245)
            r, g, b, a = sp[x, y]
            if a == 0:
                px[x, y] = base
            else:
                t = a / 255.0
                px[x, y] = (
                    int(base[0] * (1 - t) + r * t),
                    int(base[1] * (1 - t) + g * t),
                    int(base[2] * (1 - t) + b * t),
                )
    dbg.save(OUT_DEBUG)

    (OUT_DIR / "cactus-sprite-meta.txt").write_text(
        f"FW={canvas_w}\nFH={canvas_h}\nCOLS={COLS}\nROWS={ROWS}\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_SHEET} ({sheet.size[0]}x{sheet.size[1]})")


if __name__ == "__main__":
    main()
