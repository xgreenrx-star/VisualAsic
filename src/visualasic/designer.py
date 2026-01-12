"""Prototype Form Designer placeholders for VisualAsic.

This module will contain the core classes for the WYSIWYG form designer (canvas, controls, serializer, codegen helpers).
"""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict

@dataclass
class Form:
    id: str
    title: str
    width: int = 320
    height: int = 240
    controls: list = None


def load_form(path: str) -> Dict[str, Any]:
    """Load a `.form` JSON file and return the parsed dict.

    Simple loader used by tests and the initial prototype. Raises ValueError if schema is missing.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Form file not found: {path}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if "schema_version" not in data:
        raise ValueError("Invalid .form file: schema_version missing")
    return data


def save_form(form_dict: Dict[str, Any], path: str):
    """Save a form dictionary to path as JSON."""
    p = Path(path)
    p.write_text(json.dumps(form_dict, indent=2), encoding="utf-8")
