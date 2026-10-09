import argparse
import re
import sys
import unicodedata
from pathlib import Path

from config import SALIDA_DIR
from loader import cargar_tarjeta
from reporte_html import generar_html
from reporte_pdf import generar_pdf


def nombre_seguro(raw):
    text = str(raw or "Tarjeta_Informativa")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    text = text.strip("._")
    return text or "Tarjeta_Informativa"


def main():
    parser = argparse.ArgumentParser(description="Generador local de tarjetas informativas de salud.")
    parser.add_argument("entrada", help="Archivo Markdown con front matter YAML.")
    args = parser.parse_args()

    entrada = Path(args.entrada).resolve()
    if not entrada.exists():
        print(f"[ERROR] No existe el archivo: {entrada}")
        sys.exit(1)

    try:
        SALIDA_DIR.mkdir(exist_ok=True)

        meta, body = cargar_tarjeta(entrada)
        html = generar_html(meta, body)

        nombre = nombre_seguro(meta.get("salida") or entrada.stem)
        html_path = SALIDA_DIR / f"{nombre}.html"
        pdf_path = SALIDA_DIR / f"{nombre}.pdf"

        generar_pdf(html, html_path, pdf_path)

    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    print(f"[OK] HTML: {html_path}")
    print(f"[OK] PDF:  {pdf_path}")


if __name__ == "__main__":
    main()
