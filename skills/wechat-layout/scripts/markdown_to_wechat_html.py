#!/usr/bin/env python3
"""Render Markdown to a conservative inline-styled WeChat HTML fragment."""

import argparse
import re
from pathlib import Path

try:
    import markdown
except ImportError as exc:
    raise SystemExit("Install dependency: python -m pip install 'markdown>=3.5,<4'") from exc


STYLES = {
    "wrapper": "max-width:100%;margin:0 auto;color:#252525;font-size:16px;line-height:1.82;letter-spacing:.02em;word-break:break-word;",
    "h1": "font-size:26px;line-height:1.35;margin:0 0 1.1em;font-weight:700;color:#111;",
    "h2": "font-size:21px;line-height:1.45;margin:2em 0 .8em;padding-left:.65em;border-left:4px solid #2563eb;font-weight:700;color:#111;",
    "h3": "font-size:18px;line-height:1.5;margin:1.6em 0 .65em;font-weight:700;color:#222;",
    "p": "margin:0 0 1em;",
    "blockquote": "margin:1.3em 0;padding:.9em 1em;border-left:4px solid #93c5fd;background:#f6f8fb;color:#4b5563;",
    "img": "display:block;max-width:100%;height:auto;margin:1.2em auto .5em;border-radius:6px;",
    "a": "color:#2563eb;text-decoration:none;border-bottom:1px solid #bfdbfe;",
    "ul": "margin:.6em 0 1.1em;padding-left:1.4em;",
    "ol": "margin:.6em 0 1.1em;padding-left:1.4em;",
    "li": "margin:.35em 0;",
    "code": "padding:.12em .35em;border-radius:3px;background:#f1f5f9;font-family:Menlo,Consolas,monospace;font-size:.9em;",
    "pre": "overflow-x:auto;margin:1.2em 0;padding:1em;border-radius:6px;background:#0f172a;color:#e2e8f0;font-size:13px;line-height:1.6;",
}


def inject_style(html: str, tag: str, style: str) -> str:
    pattern = rf"<{tag}(\s[^>]*)?>"
    def replace(match):
        attrs = match.group(1) or ""
        if re.search(r"\sstyle=", attrs, re.I):
            return match.group(0)
        return f'<{tag}{attrs} style="{style}">'
    return re.sub(pattern, replace, html, flags=re.I)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    source = Path(args.input).read_text(encoding="utf-8")
    if re.search(r"TODO|TBD|<!--\s*(?:IMAGE|NOTE):", source, re.I):
        raise SystemExit("Refusing to render unresolved placeholders or editorial markers")
    body = markdown.markdown(source, extensions=["extra", "sane_lists"])
    for tag, style in STYLES.items():
        if tag != "wrapper":
            body = inject_style(body, tag, style)
    output = f'<section style="{STYLES["wrapper"]}">\n{body}\n</section>\n'
    Path(args.output).write_text(output, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
