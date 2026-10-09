from weasyprint import CSS, HTML

from config import ASSETS_DIR, CSS_PATH, FONDO_PATH, FOOTER_PATH, HEADER_PATH, ROOT_DIR


def generar_pdf(html_text, html_path, pdf_path):
    if not CSS_PATH.exists():
        raise FileNotFoundError(f"No existe CSS: {CSS_PATH}")

    if not FONDO_PATH.exists():
        raise FileNotFoundError(f"No existe el fondo configurado: {FONDO_PATH}")

    if not HEADER_PATH.exists():
        raise FileNotFoundError(f"No existe el encabezado configurado: {HEADER_PATH}")

    if not FOOTER_PATH.exists():
        raise FileNotFoundError(f"No existe el pie configurado: {FOOTER_PATH}")

    html_path.write_text(html_text, encoding="utf-8")

    css_text = CSS_PATH.read_text(encoding="utf-8")
    css_text = css_text.replace("__BACKGROUND_IMAGE__", FONDO_PATH.as_uri())
    css_text = css_text.replace("__HEADER_IMAGE__", HEADER_PATH.as_uri())
    css_text = css_text.replace("__FOOTER_IMAGE__", FOOTER_PATH.as_uri())

    HTML(
        string=html_text,
        base_url=str(ROOT_DIR),
    ).write_pdf(
        target=str(pdf_path),
        stylesheets=[CSS(string=css_text, base_url=str(ASSETS_DIR))],
    )

    if not pdf_path.exists():
        raise RuntimeError("No se genero el PDF.")

    if pdf_path.stat().st_size < 20_000:
        raise RuntimeError("El PDF generado parece demasiado pequeno. Revisa fondo, CSS o WeasyPrint.")
