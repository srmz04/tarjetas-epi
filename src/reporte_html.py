from html import escape

import markdown as markdown_lib


def _p(text, class_name=""):
    text = str(text or "").strip()
    if not text:
        return ""
    cls = f' class="{class_name}"' if class_name else ""
    return f"<p{cls}>{escape(text)}</p>"


def generar_html(meta, body_md):
    body_html = markdown_lib.markdown(body_md, extensions=["tables"])

    destinatario = "\n".join(
        [
            _p(meta["destinatario"]),
            _p(meta.get("cargo_destinatario")),
        ]
    )

    fecha_folio = "\n".join(
        [
            _p(meta["fecha"]),
            _p(meta.get("folio")),
        ]
    )

    cierre = "\n".join(
        [
            _p("Atentamente,"),
            _p(meta.get("cargo_firmante"), "cargo-firmante"),
            _p(meta["firmante"], "firmante"),
            _p(meta.get("iniciales"), "iniciales"),
        ]
    )

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{escape(meta["titulo"])}</title>
</head>
<body>
  <div class="header-bg"></div>
  <div class="footer-bg"></div>
  <main class="page">
    <section class="encabezado">
      <div class="destinatario">
        {destinatario}
      </div>
      <div class="fecha-folio">
        {fecha_folio}
      </div>
    </section>

    <h1>{escape(meta["titulo"])}</h1>

    <section class="contenido">
      {body_html}
    </section>

    <section class="cierre">
      {cierre}
    </section>
  </main>
</body>
</html>"""
