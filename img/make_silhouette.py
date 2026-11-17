"""
Genera img/kaiju-silhouette.png a partir de img/kaiju-source.webp.

Pasos:
 1. Quita el "tablero de ajedrez" falso del fondo con un flood-fill desde los
    bordes (pixeles claros y poco saturados). Los contornos negros del personaje
    frenan el relleno, asi que el craneo (gris claro) no se pierde.
 2. Se queda con el componente conectado mas grande (elimina marcas de agua).
 3. Aplana el personaje a un color unico (cian #00E5FF) con alpha moderado; las
    venas cian brillantes y el craneo tienen alpha distinto para dar algo de forma.

Uso:  python img/make_silhouette.py
Requiere: Pillow + numpy.
"""
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
SRC = HERE / "kaiju-source.webp"
OUT = HERE / "kaiju-silhouette.png"

ACCENT = (0, 229, 255)
OUT_WIDTH = 1100
BRIGHT_MIN = 175      # canal minimo para considerar "claro"
SAT_MAX = 22          # max(rgb)-min(rgb) para considerar "poco saturado"


def flood(cand, seeds):
    """Flood-fill 4-conectado sobre `cand` desde `seeds` (ambos bool HxW)."""
    h, w = cand.shape
    reach = np.zeros_like(cand)
    c = cand.ravel()
    r = reach.ravel()
    dq = deque(np.flatnonzero(seeds & cand).tolist())
    for i in dq:
        r[i] = True
    while dq:
        i = dq.popleft()
        x = i % w
        for j in (i - w, i + w, i - 1 if x > 0 else -1, i + 1 if x < w - 1 else -1):
            if 0 <= j < c.size and c[j] and not r[j]:
                r[j] = True
                dq.append(j)
    return reach


def largest_component(mask):
    h, w = mask.shape
    m = mask.ravel()
    seen = np.zeros(m.size, dtype=bool)
    best = []
    for start in np.flatnonzero(m):
        if seen[start]:
            continue
        comp = [start]
        seen[start] = True
        k = 0
        while k < len(comp):
            i = comp[k]; k += 1
            x = i % w
            for j in (i - w, i + w, i - 1 if x > 0 else -1, i + 1 if x < w - 1 else -1):
                if 0 <= j < m.size and m[j] and not seen[j]:
                    seen[j] = True
                    comp.append(j)
        if len(comp) > len(best):
            best = comp
    out = np.zeros(m.size, dtype=bool)
    out[np.array(best, dtype=np.int64)] = True
    return out.reshape(h, w)


def main():
    rgb = np.array(Image.open(SRC).convert("RGB")).astype(np.int16)
    h, w, _ = rgb.shape
    mx, mn = rgb.max(2), rgb.min(2)
    bg_like = (mn >= BRIGHT_MIN) & ((mx - mn) <= SAT_MAX)

    border = np.zeros((h, w), dtype=bool)
    border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
    bg = flood(bg_like, border)
    # engrosa 1px el fondo para comerse el halo claro del antialiasing
    bg_img = Image.fromarray((bg * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    fg = ~(np.array(bg_img) > 0)
    fg = largest_component(fg)

    # tapa huecos pequenos dentro del personaje (cierra con dilate+erode)
    m = Image.fromarray((fg * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    fg = np.array(m) > 127

    # clasificacion de zonas dentro del personaje
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    vein = (g > 150) & (b > 150) & (r < 140) & ((g - r) > 70)
    skull = (mn > 150) & ((mx - mn) < 40)

    alpha = np.zeros((h, w), dtype=np.float32)
    alpha[fg] = 0.55
    alpha[fg & skull] = 0.38
    alpha[fg & vein] = 1.0

    a_img = Image.fromarray((alpha * 255).astype(np.uint8))
    # suaviza venas/bordes para que no haya ruido de detalle fino
    a_img = a_img.filter(ImageFilter.GaussianBlur(2.2))
    # recorta al contorno exacto (mascara suavizada) para bordes limpios
    mask = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    a = (np.array(a_img).astype(np.float32) * (np.array(mask).astype(np.float32) / 255.0))

    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = ACCENT
    out[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    img = img.resize((OUT_WIDTH, round(h * OUT_WIDTH / w)), Image.LANCZOS)
    img.save(OUT, optimize=True)
    print("OK", OUT, OUT.stat().st_size // 1024, "KB", img.size)


if __name__ == "__main__":
    main()
