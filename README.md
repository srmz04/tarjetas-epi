# tarjetas-epi

Generador local de tarjetas informativas de salud en PDF a partir de Markdown.

## Qué resuelve

Convierte una entrada estructurada en un documento de media carta listo para revisión o impresión. Separa el contenido, la validación y la presentación para que el formato sea repetible y fácil de mantener.

## Privacidad

El procesamiento ocurre en el equipo local. `entrada/`, `salida/`, documentos y recursos institucionales están excluidos de Git. El repositorio contiene una plantilla con datos ficticios y no incluye tarjetas operativas ni datos personales.

## Instalación

```bash
git clone https://github.com/srmz04/tarjetas-epi.git
cd tarjetas-epi
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
chmod +x tarjeta
```

## Uso

```bash
mkdir -p entrada
cp plantillas/tarjeta_base.md entrada/caso.md
./tarjeta entrada/caso.md
```

El HTML intermedio y el PDF se guardan en `salida/`. La página mide 8.5 × 5.5 pulgadas para colocar dos tarjetas en una hoja carta.

## Identidad visual local

Si cuenta con autorización para usar recursos institucionales, coloque el fondo en `assets_local/fondo_institucional.png` y ejecute:

```bash
.venv/bin/python scripts/preparar_assets_locales.py
```

La carpeta `assets_local/` no se publica. Sin recursos locales, el generador usa un fondo neutro incluido en el proyecto.

## Arquitectura

```text
plantillas/tarjeta_base.md   entrada de ejemplo
src/loader.py                lectura y validación
src/reporte_html.py          composición del contenido
src/reporte_pdf.py           exportación a PDF
assets/tarjeta.css           presentación
```

## Pruebas

```bash
.venv/bin/pytest
```
