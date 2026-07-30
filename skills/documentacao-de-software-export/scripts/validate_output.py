"""
validate_output.py — Smoke test validation of the generated HTML site.

Verifies basic site integrity: existing files, internal links, Mermaid blocks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Force stdout to UTF-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def validate_site(site_dir: Path) -> list[dict]:
    """Run all validations on the generated site."""
    issues: list[dict] = []

    # 1. index.html exists and references CSS
    index = site_dir / "index.html"
    if not index.exists():
        issues.append({"level": "ERROR", "msg": "index.html not found"})
    else:
        content = index.read_text(encoding="utf-8")
        if "integrated-theme.css" not in content:
            issues.append({"level": "WARNING", "msg": "index.html does not reference integrated-theme.css"})
        if "mermaid" not in content.lower():
            issues.append({"level": "WARNING", "msg": "index.html does not include Mermaid.js"})

    # 2. nav.json exists and is valid JSON
    nav_json_path = site_dir / "nav.json"
    if not nav_json_path.exists():
        issues.append({"level": "ERROR", "msg": "nav.json not found"})
    else:
        try:
            with open(nav_json_path, "r", encoding="utf-8") as f:
                nav_data = json.load(f)
            if not isinstance(nav_data, list) or len(nav_data) == 0:
                issues.append({"level": "WARNING", "msg": "nav.json is empty or in invalid format"})
        except json.JSONDecodeError as e:
            issues.append({"level": "ERROR", "msg": f"nav.json is invalid JSON: {e}"})

    # 3. CSS exists
    css_path = site_dir / "css" / "integrated-theme.css"
    if not css_path.exists():
        issues.append({"level": "ERROR", "msg": "css/integrated-theme.css not found"})

    # 4. Validate internal links in all HTML pages
    html_files = list(site_dir.rglob("*.html"))
    all_html_names = {f.name for f in html_files}

    link_pattern = re.compile(r'href="([^"#]+\.html)"')
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        for m in link_pattern.finditer(content):
            target = m.group(1)
            # Resolve relative path
            target_path = (html_file.parent / target).resolve()
            if not target_path.exists():
                rel_from = html_file.relative_to(site_dir)
                issues.append({
                    "level": "WARNING",
                    "msg": f"Broken link in {rel_from}: href=\"{target}\" → file does not exist",
                })

    # 5. Check for empty Mermaid blocks
    mermaid_pattern = re.compile(r'<div class="mermaid">(.*?)</div>', re.DOTALL)
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        for m in mermaid_pattern.finditer(content):
            block = m.group(1).strip()
            if not block:
                rel_from = html_file.relative_to(site_dir)
                issues.append({"level": "WARNING", "msg": f"Empty Mermaid block in {rel_from}"})

    # 6. Check traceability/matrix.html (if it exists)
    matrix_path = site_dir / "traceability" / "matrix.html"
    if not matrix_path.exists():
        issues.append({"level": "INFO", "msg": "traceability/matrix.html not generated (optional)"})

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated HTML site")
    parser.add_argument(
        "--site", type=Path, required=True, help="Generated site directory"
    )
    args = parser.parse_args()

    if not args.site.exists():
        print(f"ERROR: Directory '{args.site}' does not exist.")
        sys.exit(1)

    print(f"Validating site at: {args.site}\n")

    issues = validate_site(args.site)

    errors = [i for i in issues if i["level"] == "ERROR"]
    warnings = [i for i in issues if i["level"] == "WARNING"]
    infos = [i for i in issues if i["level"] == "INFO"]

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  [ERROR] {e['msg']}")
        print()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  [WARNING] {w['msg']}")
        print()

    if infos:
        print("INFO:")
        for i in infos:
            print(f"  [INFO] {i['msg']}")
        print()

    total = len(issues)
    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    else:
        print(f"Validation OK: {len(warnings)} warning(s), {len(infos)} info(s)")
        sys.exit(0)


if __name__ == "__main__":
    main()
