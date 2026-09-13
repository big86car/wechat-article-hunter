#!/usr/bin/env python3
"""Validate the originality gate report and enforce pass conditions."""

import json
import sys
from pathlib import Path


DIMENSIONS = {
    "provenance_completeness", "attribution_integrity", "expression_independence",
    "structural_independence", "original_value",
}


def main(path: str) -> int:
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    verdict = report.get("verdict")
    if verdict not in {"pass", "revise", "block"}:
        errors.append("verdict must be pass, revise, or block")
    scores = report.get("scores", {})
    if set(scores) != DIMENSIONS:
        errors.append("scores must contain exactly the five rubric dimensions")
    elif any(not isinstance(v, (int, float)) or not 1 <= v <= 5 for v in scores.values()):
        errors.append("every score must be between 1 and 5")
    findings = report.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be an array")
        findings = []
    contributions = report.get("original_contributions")
    if not isinstance(contributions, list):
        errors.append("original_contributions must be an array")
        contributions = []
    blocking = [x for x in findings if x.get("severity") == "blocking"]
    if verdict == "pass":
        if any(v < 4 for v in scores.values()) if set(scores) == DIMENSIONS else True:
            errors.append("pass requires every rubric score to be at least 4")
        if blocking:
            errors.append("pass cannot contain blocking findings")
        if not contributions:
            errors.append("pass requires at least one original contribution")
        if report.get("manual_review_required"):
            errors.append("pass cannot require unresolved manual review")
    if verdict == "block" and not blocking:
        errors.append("block requires at least one blocking finding")
    for index, finding in enumerate(findings):
        if finding.get("route_to") not in {"research", "outline", "writing"}:
            errors.append(f"findings[{index}].route_to is invalid")
    if errors:
        print("INVALID\n" + "\n".join(f"- {item}" for item in errors))
        return 1
    print(f"VALID: verdict={verdict}, findings={len(findings)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_originality_report.py originality-report.json")
    raise SystemExit(main(sys.argv[1]))
