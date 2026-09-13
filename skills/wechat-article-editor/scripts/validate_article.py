#!/usr/bin/env python3
"""Mechanical checks for a final Markdown article."""

import re
import sys
from pathlib import Path


def main(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    errors, warnings = [], []
    lines = text.splitlines()
    titles = [x for x in lines if x.startswith("# ")]
    if len(titles) != 1:
        errors.append(f"expected exactly one H1 title, found {len(titles)}")
    placeholders = re.findall(r"TODO|TBD|\[待[^]]*\]|<!--\s*(?:IMAGE|NOTE):", text, re.I)
    if placeholders:
        errors.append(f"unresolved editorial placeholders: {len(placeholders)}")
    if re.search(r"https?://[^\s)>]+\)(?!\s*$)", text):
        warnings.append("inspect link formatting")
    body = re.sub(r"[#>*_`\-\[\]()!]", "", text)
    chinese = len(re.findall(r"[\u4e00-\u9fff]", body))
    if chinese < 500:
        warnings.append(f"article is short: about {chinese} Chinese characters")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.startswith("#")]
    long_paragraphs = [p for p in paragraphs if len(p) > 500]
    if long_paragraphs:
        warnings.append(f"{len(long_paragraphs)} paragraph(s) exceed 500 characters")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    if errors:
        return 1
    print(f"VALID: about {chinese} Chinese characters")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_article.py article.md")
    raise SystemExit(main(sys.argv[1]))
