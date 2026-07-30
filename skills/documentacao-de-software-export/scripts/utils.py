"""
utils.py — Shared functions for the documentacao-de-software-export skill.

Markdown metadata extraction, Mermaid validation, cross-reference parsing.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Regex patterns for artifact identification
# ---------------------------------------------------------------------------

PATTERNS: dict[str, re.Pattern[str]] = {
    "req": re.compile(r"^req-(\d{4})-(.+)\.md$", re.IGNORECASE),
    "tec_req": re.compile(r"^tec-req-(\d{4})-(.+)\.md$", re.IGNORECASE),
    "apf_req": re.compile(r"^apf-req-(\d{4})(?:-(.+))?\.(?:md|MD)$", re.IGNORECASE),
    "cri_req": re.compile(r"^cri-req-(\d{4})-(.+)\.md$", re.IGNORECASE),
    "api": re.compile(r"^api-(.+)\.md$", re.IGNORECASE),
    "der": re.compile(r"^der-(.+)\.md$", re.IGNORECASE),
    "did": re.compile(r"^did-(.+)\.md$", re.IGNORECASE),
    "dcl": re.compile(r"^dcl-(.+)\.md$", re.IGNORECASE),
    "min": re.compile(r"^min-(.+)\.md$", re.IGNORECASE),
    "vis": re.compile(r"^vis-(.+)\.md$", re.IGNORECASE),
    "apr_req": re.compile(r"^apr_req-(.+)\.md$", re.IGNORECASE),
    "regras_rf": re.compile(r"^requisitos-funcionais\.md$", re.IGNORECASE),
    "regras_rn": re.compile(r"^regras-negocios\.md$", re.IGNORECASE),
}

# Mapping of prefix → sidebar menu section
SECTION_MAP: dict[str, str] = {
    "req": "Requisitos",
    "tec_req": "Requisitos Técnicos",
    "apf_req": "Análise de Pontos de Função",
    "cri_req": "Critérios de Aceitação",
    "api": "APIs",
    "der": "Diagrama ER",
    "did": "Dicionário de Dados",
    "dcl": "Diagrama de Classes",
    "min": "Diagrama de Integração",
    "vis": "Visão",
    "apr_req": "Aprovações",
    "regras_rf": "Regras Funcionais",
    "regras_rn": "Regras de Negócio",
}

# Root artifacts (outside of processo_unificado/)
ROOT_ARTIFACTS: dict[str, str] = {
    "arquitetura-tech-stack.md": "Arquitetura",
    "matriz-risco-sistema.md": "Matriz de Risco",
    "mapeamento-investigacao-sistema.md": "Mapeamento",
    "tamanho-aplicacao.md": "Tamanho",
    "padrao-visual.md": "Padrão Visual",
}

# Database artifacts
BANCO_DIR = "banco_dados"


# ---------------------------------------------------------------------------
# Artifact classification
# ---------------------------------------------------------------------------

def classify_artifact(filename: str) -> tuple[str, str] | None:
    """Classify a .md file and return (type, friendly_name) or None."""
    for tipo, pattern in PATTERNS.items():
        m = pattern.match(filename)
        if m:
            return tipo, m.group(0)
    return None


def get_section(tipo: str) -> str:
    """Return the sidebar menu section for an artifact type."""
    return SECTION_MAP.get(tipo, "Outros")


# ---------------------------------------------------------------------------
# Markdown metadata extraction
# ---------------------------------------------------------------------------

def extract_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter from a Markdown file."""
    fm: dict[str, str] = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            block = content[3:end].strip()
            for line in block.splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def extract_table_metadata(content: str) -> dict[str, str]:
    """Extract metadata from markdown tables (Version, Date, Author, Status)."""
    meta: dict[str, str] = {}
    # Search for table with header | Field | Value |
    table_pattern = re.compile(
        r"\|\s*(Vers[ãa]o|Version)\s*\|\s*(.+?)\s*\|", re.IGNORECASE
    )
    for m in table_pattern.finditer(content):
        meta["versao"] = m.group(2).strip()

    table_pattern = re.compile(
        r"\|\s*(Data|Date)\s*\|\s*(.+?)\s*\|", re.IGNORECASE
    )
    for m in table_pattern.finditer(content):
        meta["data"] = m.group(2).strip()

    table_pattern = re.compile(
        r"\|\s*Autor\s*\|\s*(.+?)\s*\|", re.IGNORECASE
    )
    for m in table_pattern.finditer(content):
        meta["autor"] = m.group(1).strip()

    table_pattern = re.compile(
        r"\|\s*Status\s*\|\s*(.+?)\s*\|", re.IGNORECASE
    )
    for m in table_pattern.finditer(content):
        meta["status"] = m.group(1).strip()

    return meta


def extract_title(content: str, filename: str) -> str:
    """Extract the document title (first # heading or metadata)."""
    # Try frontmatter
    fm = extract_frontmatter(content)
    if "title" in fm:
        return fm["title"]

    # Try first heading
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    # Fallback: filename without extension
    return Path(filename).stem


def extract_metadata(content: str, filename: str) -> dict[str, str]:
    """Extract all available metadata from a Markdown file."""
    meta = extract_frontmatter(content)
    table_meta = extract_table_metadata(content)
    meta.update(table_meta)

    if "title" not in meta:
        meta["title"] = extract_title(content, filename)

    meta.setdefault("versao", "")
    meta.setdefault("data", "")
    meta.setdefault("autor", "")
    meta.setdefault("status", "")

    return meta


# ---------------------------------------------------------------------------
# Cross-reference extraction
# ---------------------------------------------------------------------------

# Reference patterns in content
REF_REQ = re.compile(r"\breq-(\d{4})\b", re.IGNORECASE)
REF_TEC = re.compile(r"\btec-req-(\d{4})\b", re.IGNORECASE)
REF_API = re.compile(r"\bapi-([a-zA-Z0-9_-]+)\b", re.IGNORECASE)
REF_DER = re.compile(r"\bder-([a-zA-Z0-9_-]+)\b", re.IGNORECASE)
REF_DID = re.compile(r"\bdid-([a-zA-Z0-9_-]+)\b", re.IGNORECASE)
REF_DCL = re.compile(r"\bdcl-([a-zA-Z0-9_-]+)\b", re.IGNORECASE)
REF_MIN = re.compile(r"\bmin-([a-zA-Z0-9_-]+)\b", re.IGNORECASE)
REF_VIS = re.compile(r"\bvis-([a-zA-Z0-9_-]+)\b", re.IGNORECASE)
REF_RF = re.compile(r"\bRF-(\d{4})\b")
REF_RN = re.compile(r"\bRN-(\d{4})\b")
REF_APF = re.compile(r"\bapf-req-(\d{4})\b", re.IGNORECASE)
REF_CRI = re.compile(r"\bcri-req-(\d{4})\b", re.IGNORECASE)

# Pattern for markdown links [text](path)
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def extract_references(content: str) -> dict[str, list[str]]:
    """Extract all cross-references from Markdown content."""
    refs: dict[str, list[str]] = {
        "req": [],
        "tec_req": [],
        "api": [],
        "der": [],
        "did": [],
        "dcl": [],
        "min": [],
        "vis": [],
        "rf": [],
        "rn": [],
        "apf": [],
        "cri": [],
        "links": [],
    }

    def _add(key: str, value: str) -> None:
        if value not in refs[key]:
            refs[key].append(value)

    for m in REF_REQ.finditer(content):
        _add("req", f"req-{m.group(1)}")
    for m in REF_TEC.finditer(content):
        _add("tec_req", f"tec-req-{m.group(1)}")
    for m in REF_API.finditer(content):
        _add("api", f"api-{m.group(1)}")
    for m in REF_DER.finditer(content):
        _add("der", f"der-{m.group(1)}")
    for m in REF_DID.finditer(content):
        _add("did", f"did-{m.group(1)}")
    for m in REF_DCL.finditer(content):
        _add("dcl", f"dcl-{m.group(1)}")
    for m in REF_MIN.finditer(content):
        _add("min", f"min-{m.group(1)}")
    for m in REF_VIS.finditer(content):
        _add("vis", f"vis-{m.group(1)}")
    for m in REF_RF.finditer(content):
        _add("rf", f"RF-{m.group(1)}")
    for m in REF_RN.finditer(content):
        _add("rn", f"RN-{m.group(1)}")
    for m in REF_APF.finditer(content):
        _add("apf", f"apf-req-{m.group(1)}")
    for m in REF_CRI.finditer(content):
        _add("cri", f"cri-req-{m.group(1)}")

    # Markdown links
    for m in MD_LINK.finditer(content):
        target = m.group(2)
        if target.endswith(".md") and not target.startswith("http"):
            _add("links", target)

    return refs


# ---------------------------------------------------------------------------
# Mermaid validation
# ---------------------------------------------------------------------------

MERMAID_DIAGRAM_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "classDiagram",
    "erDiagram", "stateDiagram-v2", "gantt", "pie", "journey",
    "gitGraph", "mindmap", "timeline", "sankey", "block",
}


def validate_mermaid_block(block: str) -> list[str]:
    """Validate a Mermaid block and return a list of errors found."""
    errors: list[str] = []
    lines = block.strip().splitlines()

    if not lines:
        errors.append("Empty Mermaid block")
        return errors

    first_line = lines[0].strip()
    diagram_type = first_line.split()[0] if first_line.split() else ""

    if diagram_type not in MERMAID_DIAGRAM_TYPES:
        errors.append(f"Unknown diagram type: '{diagram_type}'")

    # Check subgraph/end balance
    subgraph_count = sum(1 for l in lines if l.strip().startswith("subgraph"))
    end_count = sum(1 for l in lines if l.strip() == "end")
    if subgraph_count != end_count:
        errors.append(
            f"Unbalanced subgraph/end: {subgraph_count} subgraph(s), {end_count} end(s)"
        )

    # Check bracket/parenthesis balance (simplified)
    for i, line in enumerate(lines, 1):
        if line.count("[") != line.count("]"):
            # Only report if it's a node definition line
            if any(c in line for c in ["[", "{", "("]):
                errors.append(f"Line {i}: possibly unbalanced brackets/parentheses")

    return errors


def find_mermaid_blocks(content: str) -> list[tuple[int, str]]:
    """Find all Mermaid blocks in content and return (line, block)."""
    blocks: list[tuple[int, str]] = []
    in_block = False
    current: list[str] = []
    start_line = 0

    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```mermaid"):
            in_block = True
            current = []
            start_line = i
        elif stripped == "```" and in_block:
            in_block = False
            blocks.append((start_line, "\n".join(current)))
        elif in_block:
            current.append(line)

    return blocks


# ---------------------------------------------------------------------------
# Markdown → HTML conversion (wrapper)
# ---------------------------------------------------------------------------

def markdown_to_html(content: str) -> str:
    """Convert Markdown to HTML with standard extensions."""
    try:
        import markdown
        md = markdown.Markdown(
            extensions=[
                "tables",
                "fenced_code",
                "toc",
                "md_in_html",
                "sane_lists",
            ],
            output_format="html",
        )
        html = md.convert(content)
        # Convert ```mermaid blocks to <div class="mermaid">
        html = re.sub(
            r'<pre><code class="language-mermaid">(.*?)</code></pre>',
            r'<div class="mermaid">\1</div>',
            html,
            flags=re.DOTALL,
        )
        return html
    except ImportError:
        # Fallback: return raw content
        return f"<pre>{content}</pre>"


# ---------------------------------------------------------------------------
# Path utilities
# ---------------------------------------------------------------------------

def md_filename_to_html(filename: str) -> str:
    """Convert .md filename to .html."""
    return str(Path(filename).with_suffix(".html"))


def safe_filename(name: str) -> str:
    """Generate a safe filename (no special characters)."""
    safe = re.sub(r'[<>:"/\\|?*]', '_', name)
    safe = re.sub(r'\s+', '_', safe)
    return safe[:200]  # Limit size
