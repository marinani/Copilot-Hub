"""
doc_scanner.py — Scans the documentacao/ directory and generates manifest.yaml.

Phase 1 of the HTML export workflow.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

# Add current directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    BANCO_DIR,
    ROOT_ARTIFACTS,
    SECTION_MAP,
    classify_artifact,
    extract_metadata,
    get_section,
)


def scan_directory(doc_root: Path) -> dict[str, list[dict]]:
    """
    Recursively scan the documentation directory.

    Returns a dict with key = sidebar menu section, value = list of artifacts.
    """
    artifacts_by_section: dict[str, list[dict]] = {}

    for md_file in sorted(doc_root.rglob("*.md")):
        rel = md_file.relative_to(doc_root)
        parts = rel.parts

        # Skip root README.md (it becomes index.html)
        if rel.name == "README.md" and len(parts) == 1:
            continue

        # Read content
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  [WARNING] Error reading {rel}: {e}")
            continue

        # Classify the artifact
        classification = classify_artifact(rel.name)
        filename = rel.name

        # Root artifacts (architecture, risk-matrix, etc.)
        if len(parts) == 1 and filename in ROOT_ARTIFACTS:
            section = ROOT_ARTIFACTS[filename]
            artifact_type = "root"
        # Database artifacts
        elif len(parts) >= 2 and parts[0] == BANCO_DIR:
            section = "Banco de Dados"
            artifact_type = "banco"
        # Visual standard
        elif len(parts) >= 2 and parts[0] == "padrao_visual":
            section = "Padrão Visual"
            artifact_type = "design"
        # Support documents
        elif len(parts) >= 3 and "documentos_de_apoio" in parts:
            section = "Documentos de Apoio"
            artifact_type = "apoio"
        # Artifacts classified by prefix
        elif classification:
            tipo, _ = classification
            section = get_section(tipo)
            artifact_type = tipo
        else:
            # Unclassified — place in "Outros"
            section = "Outros"
            artifact_type = "unknown"

        # Extract metadata
        meta = extract_metadata(content, filename)
        meta["title"] = meta.get("title", Path(filename).stem)

        artifact = {
            "file": str(rel),
            "filename": filename,
            "type": artifact_type,
            "title": meta["title"],
            "versao": meta.get("versao", ""),
            "data": meta.get("data", ""),
            "autor": meta.get("autor", ""),
            "status": meta.get("status", ""),
            "section": section,
            "html_filename": str(rel.with_suffix(".html")),
        }

        artifacts_by_section.setdefault(section, []).append(artifact)

    return artifacts_by_section


def build_navigation_tree(artifacts: dict[str, list[dict]]) -> list[dict]:
    """
    Build the navigation tree for the sidebar menu.

    Returns a list of sections, each with its artifacts.
    """
    # Preferred section order
    section_order = [
        "Requisitos",
        "Requisitos Técnicos",
        "Análise de Pontos de Função",
        "Critérios de Aceitação",
        "Regras Funcionais",
        "Regras de Negócio",
        "APIs",
        "Diagrama ER",
        "Dicionário de Dados",
        "Diagrama de Classes",
        "Diagrama de Integração",
        "Visão",
        "Aprovações",
        "Arquitetura",
        "Matriz de Risco",
        "Mapeamento",
        "Tamanho",
        "Banco de Dados",
        "Padrão Visual",
        "Documentos de Apoio",
        "Outros",
    ]

    nav_tree = []
    for section_name in section_order:
        if section_name in artifacts:
            items = sorted(artifacts[section_name], key=lambda a: a["filename"])
            nav_tree.append({
                "section": section_name,
                "items": items,
                "count": len(items),
            })

    # Add sections that are in artifacts but not in the defined order
    for section_name, items in artifacts.items():
        if section_name not in section_order:
            nav_tree.append({
                "section": section_name,
                "items": sorted(items, key=lambda a: a["filename"]),
                "count": len(items),
            })

    return nav_tree


def generate_manifest(doc_root: Path, output_path: Path, project_name: str | None = None) -> dict:
    """
    Generate the complete manifest.yaml.

    Returns the manifest as a dict for later use.
    """
    print(f"[1/3] Scanning {doc_root}...")

    artifacts = scan_directory(doc_root)

    total = sum(len(v) for v in artifacts.values())
    print(f"  Found {total} artifacts in {len(artifacts)} sections")

    for section, items in sorted(artifacts.items()):
        print(f"    {section}: {len(items)} file(s)")

    print("[2/3] Building navigation tree...")
    nav_tree = build_navigation_tree(artifacts)

    # Read README.md for index
    readme_path = doc_root / "README.md"
    readme_content = ""
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8")

    # Determine project name: explicit param > README first heading > directory name
    if not project_name:
        # Try to extract from README first heading
        for line in readme_content.splitlines():
            line = line.strip()
            if line.startswith("# "):
                project_name = line[2:].strip()
                break
        # Fallback to directory name
        if not project_name:
            project_name = doc_root.name

    manifest = {
        "project_root": str(doc_root),
        "project_name": project_name,
        "total_artifacts": total,
        "sections_count": len(artifacts),
        "readme_content": readme_content,
        "navigation": nav_tree,
        "all_artifacts": [],
    }

    # Flat list of all artifacts (for trace_builder)
    for section_items in artifacts.values():
        manifest["all_artifacts"].extend(section_items)

    print("[3/3] Saving manifest...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            manifest,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )

    print(f"  Manifest saved to: {output_path}")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan documentacao/ and generate manifest.yaml"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Documentation root directory (e.g.: documentacao/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output path for manifest.yaml",
    )
    parser.add_argument(
        "--project-name",
        type=str,
        default=None,
        help="Project name for sidebar header (optional, extracted from README if not provided)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: Directory '{args.input}' does not exist.")
        sys.exit(1)

    if not args.input.is_dir():
        print(f"ERROR: '{args.input}' is not a directory.")
        sys.exit(1)

    generate_manifest(args.input, args.output, project_name=args.project_name)


if __name__ == "__main__":
    main()
