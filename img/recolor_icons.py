"""
Recolorea los iconos pixel-art ROJOS (img/icons-red/*.png) al cian del sitio (#00E5FF).

La luminancia (canal mas brillante) del original pasa a ser la intensidad del
cian, y el canal alpha se conserva. Salida: img/<nombre>.png

Uso:  python img/recolor_icons.py
Requiere: Pillow + numpy.
"""
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "icons-red"
CYAN = np.array([0, 229, 255], dtype=np.float32)


def recolor(path):
    a = np.array(Image.open(path).convert("RGBA")).astype(np.float32)
    lum = a[..., :3].max(axis=2) / 255.0          # intensidad del rojo original
    lum = np.clip(lum * 1.08, 0, 1)               # un pelin mas de brillo
    out = np.zeros_like(a)
    out[..., :3] = CYAN[None, None, :] * lum[..., None]
    out[..., 3] = a[..., 3]
    dst = HERE / path.name
    Image.fromarray(out.astype(np.uint8), "RGBA").save(dst, optimize=True)
    print("OK", dst.name)


if __name__ == "__main__":
    for p in sorted(SRC.glob("icon_*.png")):
        recolor(p)
