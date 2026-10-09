#!/usr/bin/env python3
"""Genera header y footer locales desde assets_local/fondo_institucional.png."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS_LOCAL = ROOT / "assets_local"
SOURCE = ASSETS_LOCAL / "fondo_institucional.png"
HEADER = ASSETS_LOCAL / "header_institucional.png"
FOOTER = ASSETS_LOCAL / "footer_institucional.png"


def trim_bg(image: Image.Image, tolerance: int = 18) -> Image.Image:
    rgba = image.convert("RGBA")
    bg = rgba.getpixel((0, 0))[:3]
    bg_image = Image.new("RGBA", rgba.size, bg + (255,))
    diff = ImageChops.difference(rgba, bg_image).convert("L")
    mask = diff.point(lambda value: 255 if value > tolerance else 0)
    box = mask.getbbox()
    return rgba.crop(box) if box else rgba


def paste_fit(base: Image.Image, image: Image.Image, box: tuple[int, int, int, int], anchor: str) -> None:
    x, y, width, height = box
    scale = min(width / image.width, height / image.height)
    new_width = max(1, round(image.width * scale))
    new_height = max(1, round(image.height * scale))
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    if anchor == "left-bottom":
        position = (x, y + height - new_height)
    elif anchor == "right-bottom":
        position = (x + width - new_width, y + height - new_height)
    elif anchor == "center":
        position = (x + (width - new_width) // 2, y + (height - new_height) // 2)
    else:
        raise ValueError(f"Anchor no soportado: {anchor}")

    base.alpha_composite(resized, position)


def generar_header(source: Image.Image) -> None:
    header_width = 1275
    header_height = 190
    header = Image.new("RGBA", (header_width, header_height), (255, 255, 255, 0))

    # Curva gris superior completa, reducida para media carta.
    top_curve = source.crop((0, 0, 1275, 74))
    header.alpha_composite(top_curve, (0, 0))

    # Logotipo central sin ampliar de mas; debe quedar arriba del bloque de texto.
    logo = trim_bg(source.crop((515, 72, 760, 312)), tolerance=20)
    paste_fit(header, logo, ((header_width - 168) // 2, 48, 168, 124), "center")

    header.save(HEADER)


def generar_footer(source: Image.Image) -> None:
    footer_width = 1275
    footer_height = 150
    footer = Image.new("RGBA", (footer_width, footer_height), (255, 255, 255, 0))

    # Laterales tomados antes de la banda gruesa original para evitar un bloque inferior pesado.
    left = trim_bg(source.crop((0, 1150, 365, 1546)), tolerance=18)
    right = trim_bg(source.crop((910, 1150, source.width, 1546)), tolerance=18)
    paste_fit(footer, left, (0, 0, 300, 132), "left-bottom")
    paste_fit(footer, right, (footer_width - 300, 0, 300, 132), "right-bottom")

    draw = ImageDraw.Draw(footer, "RGBA")
    band_y = 132
    segments = [
        (0.00, 0.22, (126, 14, 83, 255)),
        (0.22, 0.43, (158, 17, 95, 255)),
        (0.43, 0.58, (232, 0, 52, 255)),
        (0.58, 0.75, (246, 0, 51, 255)),
        (0.75, 1.00, (87, 34, 41, 255)),
    ]
    for start, end, color in segments:
        draw.rectangle((round(start * footer_width), band_y, round(end * footer_width), footer_height), fill=color)
    draw.rectangle((0, footer_height - 3, footer_width, footer_height), fill=(146, 0, 76, 255))

    # Logos centrales sobre blanco, separados de la franja inferior.
    center = trim_bg(source.crop((455, 1360, 820, 1537)), tolerance=20)
    logo_width = 325
    logo_height = round(center.height * (logo_width / center.width))
    logo = center.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    logo_x = (footer_width - logo_width) // 2
    logo_y = band_y - logo_height - 7
    draw.rounded_rectangle(
        (logo_x - 18, logo_y - 7, logo_x + logo_width + 18, logo_y + logo_height + 6),
        radius=20,
        fill=(255, 255, 255, 232),
    )
    footer.alpha_composite(logo, (logo_x, logo_y))

    footer.save(FOOTER)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"No existe {SOURCE}. Copia ahi la imagen institucional local.")

    ASSETS_LOCAL.mkdir(exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    generar_header(source)
    generar_footer(source)
    print(f"[OK] Header: {HEADER}")
    print(f"[OK] Footer: {FOOTER}")


if __name__ == "__main__":
    main()
