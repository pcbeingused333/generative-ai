import ast
import pathlib
import re

PAGES = pathlib.Path(__file__).resolve().parent.parent / "pages"
# Vertex AI no longer serves these model families.
RETIRED = re.compile(r"^gemini-(1\.5|2\.0|2\.5)-")


def _model_literals(path: pathlib.Path) -> list[str]:
    tree = ast.parse(path.read_text())
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and node.value.startswith("gemini-")
    ]


def test_pages_do_not_offer_retired_gemini_models():
    offending = {
        page.name: [m for m in _model_literals(page) if RETIRED.match(m)]
        for page in sorted(PAGES.glob("*.py"))
    }
    offending = {name: models for name, models in offending.items() if models}
    assert not offending, f"retired Gemini models still referenced: {offending}"
