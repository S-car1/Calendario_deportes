"""Utilidades compartidas por los scripts de ingesta."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
}


def write_raw(source_name: str, data) -> Path:
    """Guarda la respuesta cruda de una fuente en data/raw/<source_name>.json"""
    path = RAW_DIR / f"{source_name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[{source_name}] guardado en {path} ({len(json.dumps(data))} bytes)")
    return path


def env(name: str, required: bool = True) -> str:
    val = os.environ.get(name)
    if required and not val:
        raise SystemExit(f"Falta la variable de entorno {name}")
    return val
