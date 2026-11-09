"""Generate HTML documentation without executing project programs."""

import ast
import os
import tokenize
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "docs" / "index.html"

sections = []

for path in sorted(ROOT.glob("prog*.py")):
    with tokenize.open(path) as source_file:
        source = source_file.read()

    tree = ast.parse(source)
    description = ast.get_docstring(tree) or "No module description provided."

    sections.append(
        f"<section><h2>{escape(path.name)}</h2>"
        f"<p>{escape(description)}</p>"
    )

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node) or "No description provided."
            sections.append(
                f"<h3>{escape(node.name)}</h3><p>{escape(doc)}</p>"
            )

    sections.append(
        f"<h3>Source code</h3><pre>{escape(source)}</pre></section>"
    )

if not sections:
    raise RuntimeError("No project programs found")

version = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
commit = os.environ.get("GITHUB_SHA", "local build")

page = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    "<title>Project documentation</title>"
    "<style>"
    "body{max-width:960px;margin:40px auto;padding:0 20px;"
    "font:16px/1.6 sans-serif}"
    "pre{background:#f3f4f6;padding:16px;overflow:auto}"
    "section{margin-top:40px}"
    "</style></head><body>"
    "<h1>Project documentation</h1>"
    f"<p>Version: {escape(version)}</p>"
    f"<p>Commit: {escape(commit)}</p>"
    + "".join(sections)
    + "</body></html>"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(page, encoding="utf-8")
print(f"Documentation generated: {OUTPUT}")