from pathlib import Path

class HandlerManager:
    """Simple manager to create/open handler stubs for VisualAsic.

    It writes simple VB-like subroutine stubs to a handlers/ directory.
    """
    def __init__(self, root: Path):
        self.root = Path(root)
        self.handlers_dir = self.root / "handlers"
        self.handlers_dir.mkdir(parents=True, exist_ok=True)

    def handler_path(self, name: str) -> Path:
        # sanitize name slightly
        return self.handlers_dir / f"{name}.vb"

    def create_handler(self, name: str) -> Path:
        p = self.handler_path(name)
        if not p.exists():
            content = f"Sub {name}()\n    ' TODO: implement {name}\nEnd Sub\n"
            p.write_text(content, encoding="utf-8")
        return p
