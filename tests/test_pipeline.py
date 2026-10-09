import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_tarjeta_demo_genera_html_y_pdf():
    demo = ROOT / "plantillas" / "tarjeta_base.md"

    result = subprocess.run(
        [str(ROOT / "tarjeta"), str(demo)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    html = ROOT / "salida" / "Tarjeta_Informativa_Demo_2026-10-09.html"
    pdf = ROOT / "salida" / "Tarjeta_Informativa_Demo_2026-10-09.pdf"

    assert html.exists()
    assert pdf.exists()
    assert pdf.stat().st_size > 20_000


def test_gitignore_no_versiona_entradas_ni_salidas():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "entrada/" in gitignore
    assert "salida/" in gitignore
    assert "assets_local/" in gitignore
    assert "*.pdf" in gitignore
    assert "*.docx" in gitignore


def test_pdf_es_media_carta_horizontal():
    pdf = ROOT / "salida" / "Tarjeta_Informativa_Demo_2026-10-09.pdf"
    if not pdf.exists():
        subprocess.run([str(ROOT / "tarjeta"), str(ROOT / "plantillas" / "tarjeta_base.md")], check=True)

    result = subprocess.run(
        ["pdfinfo", str(pdf)],
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Page size:       612 x 396 pts" in result.stdout
