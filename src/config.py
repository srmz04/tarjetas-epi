from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
LOCAL_ASSETS_DIR = ROOT_DIR / "assets_local"
ENTRADA_DIR = ROOT_DIR / "entrada"
SALIDA_DIR = ROOT_DIR / "salida"

CSS_PATH = ASSETS_DIR / "tarjeta.css"
FONDO_LOCAL_PATH = LOCAL_ASSETS_DIR / "fondo_institucional.png"
FONDO_REPO_PATH = ASSETS_DIR / "fondo_neutro.png"
FONDO_PATH = FONDO_LOCAL_PATH if FONDO_LOCAL_PATH.exists() else FONDO_REPO_PATH
HEADER_LOCAL_PATH = LOCAL_ASSETS_DIR / "header_institucional.png"
FOOTER_LOCAL_PATH = LOCAL_ASSETS_DIR / "footer_institucional.png"
HEADER_PATH = HEADER_LOCAL_PATH if HEADER_LOCAL_PATH.exists() else FONDO_PATH
FOOTER_PATH = FOOTER_LOCAL_PATH if FOOTER_LOCAL_PATH.exists() else FONDO_PATH

REQUIRED_FIELDS = (
    "fecha",
    "destinatario",
    "titulo",
    "firmante",
)

DEFAULTS = {
    "cargo_destinatario": "",
    "folio": "",
    "cargo_firmante": "",
    "iniciales": "",
    "salida": "Tarjeta_Informativa",
}
