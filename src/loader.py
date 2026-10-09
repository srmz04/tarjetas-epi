import re
from pathlib import Path

import yaml

from config import DEFAULTS, REQUIRED_FIELDS

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")
RAW_INSTRUCTION_RE = re.compile(
    r"(agrega un cierre|pendiente redactar|texto por definir|reemplaza lo correspondiente|quita asteriscos|no mames|TODO|FIXME)",
    re.IGNORECASE,
)


def cargar_tarjeta(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)

    if not match:
        raise ValueError("El archivo debe iniciar con front matter YAML entre lineas ---.")

    yaml_text = match.group(1)
    body = match.group(2).strip()

    meta = yaml.safe_load(yaml_text) or {}
    if not isinstance(meta, dict):
        raise ValueError("El front matter YAML debe ser un diccionario de campos.")

    meta = {**DEFAULTS, **meta}

    missing = [field for field in REQUIRED_FIELDS if not str(meta.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")

    if not body:
        raise ValueError("El cuerpo de la tarjeta esta vacio.")

    if PLACEHOLDER_RE.search(text):
        raise ValueError("La tarjeta contiene placeholders sin resolver tipo {{...}}.")

    if RAW_INSTRUCTION_RE.search(body):
        raise ValueError("El cuerpo contiene instrucciones crudas. Redacta el texto final antes de generar PDF.")

    return meta, body
