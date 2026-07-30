"""
html_generator.py — Generates a navigable HTML site from manifest and traceability.

Phase 3 of the HTML export workflow.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))

from utils import markdown_to_html, extract_metadata


# ---------------------------------------------------------------------------
# Inline HTML templates (Jinja2-like, no external dependency)
# ---------------------------------------------------------------------------

BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Documentação</title>
  <link rel="stylesheet" href="{base_url}css/integrated-theme.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: var(--text-primary); }}
    .layout {{ display: flex; min-height: 100vh; }}
    .sidebar {{ width: 280px; background: var(--bg-white); border-right: 1px solid var(--border-color); position: fixed; top: 0; left: 0; bottom: 0; overflow-y: auto; z-index: 100; transition: transform 0.3s ease; }}
    .sidebar-header {{ padding: 1.5rem 1rem; border-bottom: 2px solid var(--primary-color); }}
    .sidebar-header h2 {{ color: var(--primary-color); font-size: 1rem; margin-bottom: 0.25rem; }}
    .sidebar-header p {{ color: var(--text-secondary); font-size: 0.75rem; }}
    .sidebar-nav {{ padding: 0.5rem 0; }}
    .nav-section {{ margin: 0; }}
    .nav-section-header {{ padding: 0.5rem 1rem; font-weight: 600; font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
    .nav-section-header:hover {{ background: var(--bg-light); }}
    .nav-section-header .count {{ background: var(--bg-gray); padding: 1px 6px; border-radius: 10px; font-size: 0.7rem; }}
    .nav-section-items {{ display: none; }}
    .nav-section-items.open {{ display: block; }}
    .nav-item {{ display: block; padding: 0.3rem 1rem 0.3rem 2rem; color: var(--text-secondary); text-decoration: none; font-size: 0.85rem; border-left: 3px solid transparent; }}
    .nav-item:hover {{ background: var(--bg-light); color: var(--primary-color); border-left-color: var(--primary-light); }}
    .nav-item.active {{ background: #f0f4ff; color: var(--primary-color); border-left-color: var(--primary-color); font-weight: 500; }}
    .main-content {{ margin-left: 280px; flex: 1; padding: 2rem 3rem; max-width: 900px; }}
    .breadcrumb {{ margin-bottom: 1.5rem; font-size: 0.85rem; color: var(--text-secondary); }}
    .breadcrumb a {{ color: var(--primary-light); text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .content-body h1 {{ font-size: 1.8rem; margin: 1.5rem 0 1rem; }}
    .content-body h2 {{ font-size: 1.4rem; margin: 1.5rem 0 0.75rem; padding-bottom: 0.3rem; border-bottom: 1px solid var(--border-color); }}
    .content-body h3 {{ font-size: 1.15rem; margin: 1.2rem 0 0.5rem; }}
    .content-body p {{ margin: 0.5rem 0; line-height: 1.7; }}
    .content-body ul, .content-body ol {{ margin: 0.5rem 0 0.5rem 1.5rem; }}
    .content-body li {{ margin: 0.25rem 0; line-height: 1.6; }}
    .content-body table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
    .content-body table th {{ background: var(--primary-color); color: white; padding: 0.6rem; text-align: left; }}
    .content-body table td {{ padding: 0.6rem; border: 1px solid var(--border-color); }}
    .content-body table tbody tr:nth-child(odd) {{ background: var(--bg-light); }}
    .content-body pre {{ background: #f5f5f5; border-left: 4px solid var(--primary-color); padding: 1rem; overflow-x: auto; margin: 1rem 0; }}
    .content-body code {{ background: var(--bg-gray); padding: 2px 5px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 0.9em; }}
    .content-body pre code {{ background: transparent; padding: 0; }}
    .trace-section {{ margin-top: 2rem; padding: 1rem; background: var(--bg-light); border: 1px solid var(--border-color); border-radius: 4px; }}
    .trace-section h3 {{ margin-top: 0; font-size: 0.95rem; color: var(--primary-color); text-transform: uppercase; letter-spacing: 0.5px; }}
    .trace-links {{ list-style: none; padding: 0; }}
    .trace-links li {{ margin: 0.25rem 0; }}
    .trace-links a {{ color: var(--primary-light); text-decoration: none; }}
    .trace-links a:hover {{ text-decoration: underline; }}
    .page-nav {{ display: flex; justify-content: space-between; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border-color); }}
    .page-nav a {{ color: var(--primary-light); text-decoration: none; font-size: 0.9rem; }}
    .page-nav a:hover {{ text-decoration: underline; }}
    .toc {{ position: fixed; top: 100px; right: 2rem; width: 220px; font-size: 0.8rem; }}
    .toc h4 {{ color: var(--primary-color); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }}
    .toc ul {{ list-style: none; padding-left: 0.5rem; border-left: 2px solid var(--border-color); }}
    .toc li a {{ text-decoration: none; color: var(--text-secondary); display: block; padding: 0.25rem 0; }}
    .toc li a:hover {{ color: var(--primary-color); }}
    .toc li a.active {{ color: var(--primary-color); font-weight: 600; }}
    @media (max-width: 1200px) {{ .toc {{ display: none; }} }}
    @media (max-width: 768px) {{
      .sidebar {{ transform: translateX(-100%); }}
      .sidebar.open {{ transform: translateX(0); }}
      .main-content {{ margin-left: 0; padding: 1rem; }}
      .menu-toggle {{ display: block; }}
    }}
    .menu-toggle {{ display: none; position: fixed; top: 1rem; left: 1rem; z-index: 200; background: var(--primary-color); color: white; border: none; padding: 0.5rem; border-radius: 4px; cursor: pointer; font-size: 1.2rem; }}
  </style>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
  <button class="menu-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">&#9776;</button>
  <div class="layout">
    <nav class="sidebar">
      <div class="sidebar-header">
        <h2><a href="{base_url}index.html">{project_title}</a></h2>
        <p>Documentação do Projeto</p>
      </div>
      <div class="sidebar-nav">
        {nav_sections}
      </div>
    </nav>
    <main class="main-content">
      {breadcrumb}
      <div class="content-with-toc">
        <div class="content-body-wrapper">
            {content}
        </div>
        <div class="toc">
            <h4>Nesta Página</h4>
            <ul id="toc-container"></ul>
        </div>
      </div>
      {page_nav}
    </main>
  </div>
  <script>
    mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    // Open active section in menu
    document.querySelectorAll('.nav-section-header').forEach(function(h) {{
      h.addEventListener('click', function() {{
        this.nextElementSibling.classList.toggle('open');
        const icon = h.querySelector('.toggle-icon');
        icon.classList.toggle('fa-chevron-down');
        icon.classList.toggle('fa-chevron-right');
      }});
    }});
    // Automatically open the section containing the active item
    document.querySelectorAll('.nav-item.active').forEach(function(item) {{
      var section = item.closest('.nav-section-items');
      if (section) {{
          section.classList.add('open');
          const header = section.previousElementSibling;
          const icon = header.querySelector('.toggle-icon');
          if(icon) {{
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-chevron-down');
          }}
      }}
    }});

    // TOC generation
    const contentBody = document.querySelector('.content-body');
    const tocContainer = document.getElementById('toc-container');
    if (contentBody && tocContainer) {{
        const headings = contentBody.querySelectorAll('h2, h3');
        let tocHtml = '';
        headings.forEach(h => {{
            const id = h.textContent.trim().toLowerCase().replace(/\\s+/g, '-');
            h.id = id;
            const tagName = h.tagName.toLowerCase();
            tocHtml += `<li class="toc-${{tagName}}"><a href="#${{id}}">${{h.textContent}}</a></li>`;
        }});
        tocContainer.innerHTML = tocHtml;
    }}
  </script>
</body>
</html>"""


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Documentação</title>
  <link rel="stylesheet" href="css/integrated-theme.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: var(--text-primary); }}
    .layout {{ display: flex; min-height: 100vh; }}
    .sidebar {{ width: 280px; background: var(--bg-white); border-right: 1px solid var(--border-color); position: fixed; top: 0; left: 0; bottom: 0; overflow-y: auto; z-index: 100; }}
    .sidebar-header {{ padding: 1.5rem 1rem; border-bottom: 2px solid var(--primary-color); }}
    .sidebar-header h2 {{ color: var(--primary-color); font-size: 1rem; }}
    .sidebar-header p {{ color: var(--text-secondary); font-size: 0.75rem; }}
    .sidebar-nav {{ padding: 0.5rem 0; }}
    .nav-section {{ margin: 0; }}
    .nav-section-header {{ padding: 0.5rem 1rem; font-weight: 600; font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
    .nav-section-header:hover {{ background: var(--bg-light); }}
    .nav-section-header .count {{ background: var(--bg-gray); padding: 1px 6px; border-radius: 10px; font-size: 0.7rem; }}
    .nav-section-items {{ display: none; }}
    .nav-section-items.open {{ display: block; }}
    .nav-item {{ display: block; padding: 0.3rem 1rem 0.3rem 2rem; color: var(--text-secondary); text-decoration: none; font-size: 0.85rem; border-left: 3px solid transparent; }}
    .nav-item:hover {{ background: var(--bg-light); color: var(--primary-color); border-left-color: var(--primary-light); }}
    .main-content {{ margin-left: 280px; flex: 1; padding: 2rem 3rem; max-width: 900px; }}
    .content-body h1 {{ font-size: 1.8rem; margin: 1.5rem 0 1rem; }}
    .content-body h2 {{ font-size: 1.4rem; margin: 1.5rem 0 0.75rem; padding-bottom: 0.3rem; border-bottom: 1px solid var(--border-color); }}
    .content-body p {{ margin: 0.5rem 0; line-height: 1.7; }}
    .content-body ul, .content-body ol {{ margin: 0.5rem 0 0.5rem 1.5rem; }}
    .content-body li {{ margin: 0.25rem 0; line-height: 1.6; }}
    .content-body table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
    .content-body table th {{ background: var(--primary-color); color: white; padding: 0.6rem; text-align: left; }}
    .content-body table td {{ padding: 0.6rem; border: 1px solid var(--border-color); }}
    .content-body table tbody tr:nth-child(odd) {{ background: var(--bg-light); }}
    .content-body a {{ color: var(--primary-light); text-decoration: none; border-bottom: 1px dotted var(--primary-light); }}
    .content-body a:hover {{ color: var(--secondary-color); border-bottom-color: var(--secondary-color); }}
  </style>
</head>
<body>
  <div class="layout">
    <nav class="sidebar">
      <div class="sidebar-header">
        <h2><a href="index.html">{project_title}</a></h2>
        <p>Documentação do Projeto</p>
      </div>
      <div class="sidebar-nav">
        {nav_sections}
      </div>
    </nav>
    <main class="main-content">
      {content}
    </main>
  </div>
  <script>
    mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    document.querySelectorAll('.nav-section-header').forEach(function(h) {{
      h.addEventListener('click', function() {{
        this.nextElementSibling.classList.toggle('open');
      }});
    }});
  </script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def build_nav_html(navigation: list[dict], current_file: str = "", base_url: str = "./") -> str:
    """Generate sidebar menu HTML."""
    sections = []
    icon_map = {
        "Requirements": "fa-file-alt",
        "Technical Requirements": "fa-cogs",
        "Function Point Analysis": "fa-calculator",
        "Acceptance Criteria": "fa-check-square",
        "Functional Rules": "fa-list-ol",
        "Business Rules": "fa-briefcase",
        "APIs": "fa-code",
        "ER Diagram": "fa-project-diagram",
        "Data Dictionary": "fa-book",
        "Class Diagram": "fa-sitemap",
        "Database": "fa-database",
        "Default": "fa-folder"
    }

    for nav in navigation:
        section_name = nav["section"]
        items = nav["items"]
        count = nav["count"]
        icon_class = icon_map.get(section_name, icon_map["Default"])

        items_html = []
        for item in items:
            active = " active" if item["file"] == current_file else ""
            html_file = Path(item["file"]).with_suffix(".html")
            items_html.append(
                f'<a class="nav-item{active}" href="{base_url}{html_file}">{item["title"]}</a>'
            )

        sections.append(f"""<div class="nav-section">
  <div class="nav-section-header">
    <span><i class="fas {icon_class} nav-icon"></i> {section_name}</span>
    <span class="count-and-toggle">
        <span class="count">{count}</span>
        <i class="fas fa-chevron-right toggle-icon"></i>
    </span>
  </div>
  <div class="nav-section-items">
    {"".join(items_html)}
  </div>
</div>""")

    return "\n".join(sections)


def build_breadcrumb(parts: list[str], base_url: str = "./") -> str:
    """Generate HTML breadcrumb."""
    if not parts:
        return ""
    links = [f'<a href="{base_url}index.html">Início</a>']
    # The first part is the project name, which is already covered by "Início"
    path_parts = parts[1:-1]
    
    for part in path_parts:
        links.append(f'<span>{part}</span>')

    links.append(f'<strong>{parts[-1]}</strong>')
    return f'<div class="breadcrumb">{" &raquo; ".join(links)}</div>'


def build_trace_section(trace_info: dict | None, base_url: str = "./") -> str:
    """Generate traceability section for an artifact."""
    if not trace_info:
        return ""

    html_parts = ['<div class="trace-section"><h3>Rastreabilidade</h3>']

    # Forward references
    fwd = trace_info.get("forward_refs", [])
    if fwd:
        html_parts.append("<p><strong>Referências:</strong></p><ul class='trace-links'>")
        for ref in fwd:
            badge_type = ref.get("type", "default")
            badge_text = ref.get("ref", badge_type.upper())
            badge = f'<span class="doc-badge doc-badge-{badge_type}">{badge_text}</span>'
            
            if ref.get("file"):
                html_parts.append(
                    f'<li>{badge} '
                    f'<a href="{base_url}{Path(ref["file"]).with_suffix(".html")}">{ref.get("title", ref["ref"])}</a></li>'
                )
            else:
                html_parts.append(
                    f'<li>{badge} {ref.get("title", "")}</li>'
                )
        html_parts.append("</ul>")

    # Back references
    bwd = trace_info.get("back_refs", [])
    if bwd:
        html_parts.append("<p><strong>Referenciado por:</strong></p><ul class='trace-links'>")
        for ref in bwd:
            badge_type = ref.get("type", "default")
            badge_text = ref.get("ref", badge_type.upper())
            badge = f'<span class="doc-badge doc-badge-{badge_type}">{badge_text}</span>'
            html_parts.append(
                f'<li>{badge} '
                f'<a href="{base_url}{Path(ref["source_file"]).with_suffix(".html")}">{ref.get("source_title", ref["ref"])}</a></li>'
            )
        html_parts.append("</ul>")

    # Gaps
    gaps = trace_info.get("gaps", [])
    if gaps:
        html_parts.append("<p style='color: var(--danger-color);'><strong>Itens Pendentes:</strong></p><ul>")
        for gap in gaps:
            html_parts.append(f'<li style="color: var(--danger-color);">{gap["ref"]}: {gap["reason"]}</li>')
        html_parts.append("</ul>")

    html_parts.append("</div>")
    return "\n".join(html_parts)


def build_page_nav(
    artifacts: list[dict], current_file: str, base_url: str = "./"
) -> tuple[str, str]:
    """Generate previous/next navigation."""
    files = [a["file"] for a in artifacts]
    try:
        idx = files.index(current_file)
    except ValueError:
        return "", ""

    prev_link = ""
    next_link = ""

    if idx > 0:
        prev_art = artifacts[idx - 1]
        prev_file = Path(prev_art["file"]).with_suffix(".html")
        prev_link = f'<a href="{base_url}{prev_file}">&larr; {prev_art["title"]}</a>'

    if idx < len(artifacts) - 1:
        next_art = artifacts[idx + 1]
        next_file = Path(next_art["file"]).with_suffix(".html")
        next_link = f'<a href="{base_url}{next_file}">{next_art["title"]} &rarr;</a>'

    return prev_link, next_link


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate_site(
    manifest: dict,
    trace_result: dict,
    doc_root: Path,
    output_dir: Path,
    css_path: Path,
) -> None:
    """Generate the complete HTML site."""
    navigation = manifest.get("navigation", [])
    all_artifacts = manifest.get("all_artifacts", [])
    trace_map = trace_result.get("trace_map", {})
    readme_content = manifest.get("readme_content", "")

    # Create directory structure
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "css").mkdir(exist_ok=True)
    (output_dir / "js").mkdir(exist_ok=True)

    # Copy CSS
    if css_path.exists():
        shutil.copy2(css_path, output_dir / "css" / "integrated-theme.css")

    # Generate nav.json
    nav_json = []
    for nav in navigation:
        nav_json.append({
            "section": nav["section"],
            "count": nav["count"],
            "items": [{"title": a["title"], "file": str(Path(a["file"]).with_suffix(".html"))} for a in nav["items"]],
        })
    with open(output_dir / "nav.json", "w", encoding="utf-8") as f:
        json.dump(nav_json, f, ensure_ascii=False, indent=2)

    # Generate shared nav HTML (default base for index)
    nav_html = build_nav_html(navigation, base_url="./")
    project_title = manifest.get("project_name", "Documentação do Projeto")

    # Generate index.html from README
    print("  Generating index.html...")
    index_content = markdown_to_html(readme_content) if readme_content else "<h1>Documentação do Projeto</h1>"
    index_html = INDEX_TEMPLATE.format(
        title=project_title,
        project_title=project_title,
        nav_sections=nav_html,
        content=f'<div class="content-body">{index_content}</div>',
    )
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Generate pages for each artifact
    total = len(all_artifacts)
    for i, artifact in enumerate(all_artifacts, 1):
        art_file = artifact["file"]
        art_path = doc_root / art_file

        if not art_path.exists():
            print(f"  [WARNING] File not found: {art_file}")
            continue

        print(f"  [{i}/{total}] Generating {artifact['filename']}...")

        # Calculate relative base_url FIRST (needed by nav, trace, breadcrumb)
        depth = len(Path(art_file).parts) - 1
        base_url = "../" * depth if depth > 0 else "./"

        # Read and convert
        content = art_path.read_text(encoding="utf-8")
        meta = extract_metadata(content, artifact["filename"])
        html_body = markdown_to_html(content)

        # Traceability
        trace_info = trace_map.get(art_file)
        trace_html = build_trace_section(trace_info, base_url=base_url)

        # Navigation (prev/next)
        prev_link, next_link = build_page_nav(all_artifacts, art_file, base_url=base_url)
        page_nav_html = ""
        if prev_link or next_link:
            page_nav_html = f'<div class="page-nav"><div>{prev_link}</div><div>{next_link}</div></div>'

        # Breadcrumb
        section = artifact.get("section", "Outros")
        breadcrumb = build_breadcrumb([project_title, section, artifact["title"]], base_url=base_url)

        # Document metadata
        meta_html = '<div class="doc-meta">'
        if meta.get("versao"):
            meta_html += f'<div class="doc-meta-item"><span class="doc-meta-label">Versão:</span> <span class="doc-meta-value">{meta["versao"]}</span></div>'
        if meta.get("data"):
            meta_html += f'<div class="doc-meta-item"><span class="doc-meta-label">Data:</span> <span class="doc-meta-value">{meta["data"]}</span></div>'
        if meta.get("autor"):
            meta_html += f'<div class="doc-meta-item"><span class="doc-meta-label">Autor:</span> <span class="doc-meta-value">{meta["autor"]}</span></div>'
        if meta.get("status"):
            meta_html += f'<div class="doc-meta-item"><span class="doc-meta-label">Status:</span> <span class="doc-badge doc-badge-proc">{meta["status"]}</span></div>'
        meta_html += '</div>'

        # Assemble page
        content_full = f'<div class="content-body">{html_body}</div>{trace_html}'

        # Per-page sidebar nav with correct base_url
        sidebar_nav_html = build_nav_html(navigation, current_file=art_file, base_url=base_url)

        page_html = BASE_TEMPLATE.format(
            title=artifact["title"],
            base_url=base_url,
            project_title=project_title,
            nav_sections=sidebar_nav_html,
            breadcrumb=breadcrumb,
            content=content_full,
            page_nav=page_nav_html,
        )

        # Save HTML
        html_path = output_dir / Path(art_file).with_suffix(".html")
        html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page_html)

    # Generate pages for database artifacts
    banco_dir = doc_root / "banco_dados"
    if banco_dir.exists():
        print("  Generating database pages...")
        for md_file in sorted(banco_dir.glob("*.md")):
            rel = md_file.relative_to(doc_root)
            content = md_file.read_text(encoding="utf-8")
            html_body = markdown_to_html(content)

            html_path = output_dir / "banco" / md_file.with_suffix(".html").name
            html_path.parent.mkdir(parents=True, exist_ok=True)

            banco_base = "../"
            banco_nav = build_nav_html(navigation, base_url=banco_base)
            page_html = BASE_TEMPLATE.format(
                title=md_file.stem,
                base_url=banco_base,
                project_title=project_title,
                nav_sections=banco_nav,
                breadcrumb=build_breadcrumb([project_title, "Banco de Dados", md_file.stem], base_url=banco_base),
                content=f'<div class="content-body">{html_body}</div>',
                page_nav="",
            )
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(page_html)

    # Copy images (wireframes)
    wireframes_dir = doc_root / "padrao_visual" / "wireframes"
    if wireframes_dir.exists():
        img_out = output_dir / "assets" / "img"
        img_out.mkdir(parents=True, exist_ok=True)
        for img_file in wireframes_dir.glob("*"):
            if img_file.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg"):
                shutil.copy2(img_file, img_out / img_file.name)

    print(f"\nSite generated successfully at: {output_dir}")
    print(f"  Total pages: {total + 1} (including index.html)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate navigable HTML site from manifest"
    )
    parser.add_argument(
        "--manifest", type=Path, required=True, help="Path to manifest.yaml"
    )
    parser.add_argument(
        "--traceability", type=Path, required=True, help="Path to traceability.json"
    )
    parser.add_argument(
        "--input", type=Path, required=True, help="Documentation root directory"
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Site output directory"
    )
    parser.add_argument(
        "--css", type=Path, required=True, help="Path to integrated-theme.css"
    )
    args = parser.parse_args()

    # Validations
    for path, label in [
        (args.manifest, "Manifest"),
        (args.traceability, "Traceability"),
        (args.input, "Input directory"),
        (args.css, "CSS"),
    ]:
        if not path.exists():
            print(f"ERROR: {label} '{path}' not found.")
            sys.exit(1)

    print("[1/3] Loading data...")
    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    with open(args.traceability, "r", encoding="utf-8") as f:
        trace_result = json.load(f)

    print(f"  Artifacts: {manifest.get('total_artifacts', 0)}")
    print(f"  Sections: {manifest.get('sections_count', 0)}")

    print("[2/3] Generating HTML site...")
    generate_site(manifest, trace_result, args.input, args.output, args.css)

    print("[3/3] Done!")


if __name__ == "__main__":
    main()
