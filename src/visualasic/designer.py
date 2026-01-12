"""Prototype Form Designer placeholders for VisualAsic.

This module will contain the core classes for the WYSIWYG form designer (canvas, controls, serializer, codegen helpers).
"""

from dataclasses import dataclass

@dataclass
class Form:
    id: str
    title: str
    width: int = 320
    height: int = 240
    controls: list = None


def load_form(path):
    # placeholder: load .form JSON
    raise NotImplementedError


def save_form(form, path):
    # placeholder: save .form JSON
    raise NotImplementedError
