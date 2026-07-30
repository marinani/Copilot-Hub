#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def fmt_num(value: float) -> str:
    return f"{value:.2f}"


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def md_table(headers: List[str], rows: List[List[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] + ["---:" for _ in headers[1:]]) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([head, sep] + body)


def sum_hours(items: List[Dict[str, Any]]) -> float:
    return float(sum(float(item.get("hours", 0.0)) for item in items))


def sum_est(items: List[Dict[str, Any]]) -> float:
    return float(sum(float(item.get("estimated", 0.0)) for item in items))


def sum_entries(items: List[Dict[str, Any]]) -> int:
    return int(sum(int(item.get("entries", 0)) for item in items))


def mermaid_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def limit_chart_items(items: List[Dict[str, Any]], label_key: str = "name", max_items: int = 10, other_label: str = "Outros") -> List[Dict[str, Any]]:
    ranked = sorted(items, key=lambda item: float(item.get("hours", 0.0)), reverse=True)
    if len(ranked) <= max_items:
        return ranked

    head = ranked[:max_items]
    tail = ranked[max_items:]
    other_hours = sum(float(item.get("hours", 0.0)) for item in tail)
    other_estimated = sum(float(item.get("estimated", 0.0)) for item in tail)
    other_entries = sum(int(item.get("entries", 0)) for item in tail)

    aggregated_other = {
        label_key: other_label,
        "hours": other_hours,
        "estimated": other_estimated,
        "delta": other_hours - other_estimated,
        "entries": other_entries,
    }
    return head + [aggregated_other]


def build_mermaid_total(total_hours: float, total_est: float) -> str:
    return "\n".join(
        [
            "```mermaid",
            "xychart-beta",
            '    title "Carga total: lançadas x estimadas"',
            "    x-axis [Lancadas, Estimadas]",
            '    y-axis "Horas"',
            f"    bar [{int(round(total_hours))}, {int(round(total_est))}]",
            "```",
        ]
    )


def build_mermaid_pie(title: str, items: List[Dict[str, Any]], label_key: str = "name", max_items: int = 12) -> str:
    chart_items = limit_chart_items(items, label_key=label_key, max_items=max_items)
    palette = [
        "#0B84A5", "#F6C85F", "#6F4E7C", "#9DD866", "#CA472F", "#FFA056",
        "#8DDDD0", "#2E86AB", "#A23B72", "#3BCEAC", "#F18F01", "#C73E1D",
        "#1D6996", "#73AF48", "#EDAD08", "#E17C05", "#CC503E", "#94346E",
        "#6F4070", "#994E95", "#666666", "#4A90E2", "#50E3C2", "#B8E986",
    ]
    theme_vars = ", ".join(f'\"pie{index + 1}\": \"{color}\"' for index, color in enumerate(palette))
    lines = [
        "```mermaid",
        f"%%{{init: {{\"pie\": {{\"textPosition\": 0.92}}, \"themeVariables\": {{{theme_vars}}} }} }}%%",
        "pie showData",
        f"    title {title}",
    ]
    for item in chart_items:
        label = str(item.get(label_key, "Não informado"))
        value = float(item.get("hours", 0.0))
        lines.append(f'    "{label}" : {int(round(value))}')
    lines.append("```")
    return "\n".join(lines)


def build_collaborator_pie_with_two_column_legend(collaborators: List[Dict[str, Any]]) -> str:
    chart_items = limit_chart_items(collaborators, label_key="name", max_items=1000)
    labels = [mermaid_quote(str(item.get("name", "Não informado"))) for item in chart_items]
    values = [str(int(round(float(item.get("hours", 0.0))))) for item in chart_items]
    chart_height = max(700, 28 * len(chart_items) + 220)

    return "\n".join(
        [
            "```mermaid",
            "---",
            "config:",
            "    xyChart:",
            "        width: 1400",
            f"        height: {chart_height}",
            "---",
            "xychart-beta horizontal",
            '    title "Distribuição de horas por colaborador"',
            f"    x-axis [{', '.join(labels)}]",
            '    y-axis "Horas"',
            f"    bar [{', '.join(values)}]",
            "```",
        ]
    )


def build_mermaid_project_bar(projects: List[Dict[str, Any]]) -> str:
    chart_projects = limit_chart_items(projects, max_items=15)
    labels = [f"P{index + 1}" for index, _ in enumerate(chart_projects)]
    values = [str(int(round(float(p.get("hours", 0.0))))) for p in chart_projects]
    chart = "\n".join(
        [
            "```mermaid",
            "xychart-beta horizontal",
            '    title "Distribuição de horas por projeto"',
            f"    x-axis [{', '.join(labels)}]",
            '    y-axis "Horas"',
            f"    bar [{', '.join(values)}]",
            "```",
        ]
    )

    legend_rows = [
        [f"P{index + 1}", str(item.get("name", "Projeto")), f"{fmt_num(float(item.get('hours', 0.0)))}h"]
        for index, item in enumerate(chart_projects)
    ]
    legend = md_table(["Código", "Projeto", "Horas"], legend_rows)
    return "\n\n".join([chart, "**Legenda do gráfico 2.4**", legend])


def pct(hours: float, total: float) -> str:
    if total <= 0:
        return "0.00%"
    return fmt_pct((hours / total) * 100)


def _pdf_escape(text: str) -> str:
    result = ""
    for ch in text:
        code = ord(ch)
        if code == 92:
            result += "\\\\"
        elif code == 40:
            result += "\\("
        elif code == 41:
            result += "\\)"
        elif code < 32 or code > 126:
            result += f"\\{code:03o}"
        else:
            result += ch
    return result


def _split_long_text(text: str, max_chars: int = 80) -> List[str]:
    if len(text) <= max_chars:
        return [text]
    words = text.split(" ")
    lines: List[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) > max_chars and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


class PdfBuilder:
    FONT_REG = "/F1"
    FONT_BOLD = "/F2"

    def __init__(self) -> None:
        self.objects: Dict[int, bytes] = {}
        self.page_objs: List[int] = []
        self.content_objs: List[int] = []
        self._next_obj_id = 5
        self._setup_fonts()

    def _setup_fonts(self) -> None:
        self.objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
        self.objects[3] = (
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        )
        self.objects[4] = (
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
        )

    def _next_obj(self) -> int:
        obj_id = self._next_obj_id
        self._next_obj_id += 1
        return obj_id

    def add_page(self, stream_data: bytes) -> None:
        page_obj = self._next_obj()
        content_obj = self._next_obj()
        self.page_objs.append(page_obj)
        self.content_objs.append(content_obj)

        self.objects[content_obj] = (
            b"<< /Length "
            + str(len(stream_data)).encode("ascii")
            + b" >>\nstream\n"
            + stream_data
            + b"\nendstream"
        )
        self.objects[page_obj] = (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            + b"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            + b"/Contents "
            + str(content_obj).encode("ascii")
            + b" 0 R >>"
        )

    def write(self, file_path: Path) -> None:
        kids = " ".join(f"{p} 0 R" for p in self.page_objs)
        self.objects[2] = (
            f"<< /Type /Pages /Count {len(self.page_objs)} /Kids [{kids}] >>".encode("ascii")
        )

        max_obj = max(self.objects.keys())
        output = bytearray()
        output.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

        offsets = [0] * (max_obj + 1)
        for obj_num in range(1, max_obj + 1):
            offsets[obj_num] = len(output)
            output.extend(f"{obj_num} 0 obj\n".encode("ascii"))
            output.extend(self.objects[obj_num])
            output.extend(b"\nendobj\n")

        xref_start = len(output)
        output.extend(f"xref\n0 {max_obj + 1}\n".encode("ascii"))
        output.extend(b"0000000000 65535 f \n")
        for obj_num in range(1, max_obj + 1):
            output.extend(f"{offsets[obj_num]:010} 00000 n \n".encode("ascii"))

        output.extend(
            f"trailer\n<< /Size {max_obj + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode("ascii")
        )
        file_path.write_bytes(output)


class PageRenderer:
    MARGIN_LEFT = 42
    MARGIN_RIGHT = 553
    MARGIN_TOP = 800
    MARGIN_BOTTOM = 55
    PAGE_HEIGHT = 842
    PAGE_WIDTH = 595
    FONT_SIZES = {
        "h1": 16,
        "h2": 13,
        "h3": 11,
        "text": 9,
        "table_header": 8,
        "table_cell": 8,
        "chart_title": 11,
        "chart_label": 8,
    }
    LINE_H = {
        "h1": 22,
        "h2": 18,
        "h3": 15,
        "text": 12,
        "table": 12,
        "sep": 8,
    }

    def __init__(self, builder: PdfBuilder) -> None:
        self.builder = builder
        self.content: List[str] = []
        self.y = self.MARGIN_TOP
        self.page_num = 0
        self._start_page()

    def _start_page(self) -> None:
        self.y = self.MARGIN_TOP
        self.page_num += 1

    def _fits(self, need: int) -> bool:
        return self.y - need >= self.MARGIN_BOTTOM

    def _brk(self, need: int) -> None:
        if not self._fits(need):
            self._flush()

    def _flush(self) -> None:
        if self.content:
            stream = "\n".join(self.content).encode("latin-1", errors="replace")
            self.builder.add_page(stream)
        self.content = []
        self._start_page()

    def _add(self, s: str) -> None:
        self.content.append(s)

    def _t(self, x: float, y: float, txt: str, font: str = PdfBuilder.FONT_REG, size: float = 9) -> None:
        self._add(f"BT {font} {size:.1f} Tf 1 0 0 1 {x:.1f} {y:.1f} Tm ({_pdf_escape(txt)}) Tj ET")

    def _tb(self, x: float, y: float, txt: str, size: float = 9) -> None:
        self._t(x, y, txt, PdfBuilder.FONT_BOLD, size)

    def _rect(self, x: float, y: float, w: float, h: float) -> str:
        return f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re"

    def render_h(self, level: int, text: str) -> None:
        text = text.strip()
        if level == 1:
            sz, lh = 16, 22
        elif level == 2:
            sz, lh = 13, 18
        elif level == 3:
            sz, lh = 11, 15
        else:
            sz, lh = 11, 14
        self._brk(lh + 6)
        self._tb(self.MARGIN_LEFT, self.y, text, sz)
        if level == 1:
            ly = self.y - 2
            self._add(f"0.2 w 0.30 0.55 0.85 RG {self.MARGIN_LEFT} {ly:.1f} m {self.MARGIN_RIGHT} {ly:.1f} l S")
        self.y -= lh

    def render_t(self, text: str, bold: bool = False) -> None:
        raw = text.strip()
        if not raw:
            self.y -= self.LINE_H["text"] // 2
            return
        # Split long lines
        lines = [raw]
        if len(raw) > 95:
            lines = _split_long_text(raw, 95)
        need = len(lines) * self.LINE_H["text"]
        self._brk(need + 6)
        for ln in lines:
            if bold:
                self._tb(self.MARGIN_LEFT, self.y, ln, self.FONT_SIZES["text"])
            else:
                self._t(self.MARGIN_LEFT, self.y, ln, PdfBuilder.FONT_REG, self.FONT_SIZES["text"])
            self.y -= self.LINE_H["text"]

    def render_sep(self) -> None:
        self._brk(10)
        self._add(f"0.2 w 0.80 0.80 0.80 RG {self.MARGIN_LEFT} {self.y:.1f} m {self.MARGIN_RIGHT} {self.y:.1f} l S")
        self.y -= self.LINE_H["sep"]

    def render_table(self, table_text: str) -> None:
        lines = [ln.strip() for ln in table_text.strip().split("\n") if ln.strip()]
        if len(lines) < 2:
            return

        sep_i = None
        for i, ln in enumerate(lines):
            if all(c in "-:| " for c in ln):
                sep_i = i
                break
        if sep_i is None:
            return

        hdr_line = lines[sep_i - 1] if sep_i > 0 else ""
        raw_rows = lines[sep_i + 1:]

        headers = [c.strip().replace("**", "") for c in hdr_line.strip("|").split("|")]
        rows = []
        for ln in raw_rows:
            if all(c in "-:| " for c in ln) or not ln.startswith("|"):
                continue
            rows.append([c.strip().replace("**", "") for c in ln.strip("|").split("|")])

        if not headers:
            return

        cols = len(headers)
        col_w = min(110, (self.MARGIN_RIGHT - self.MARGIN_LEFT) / cols)
        total_w = col_w * cols
        sx = self.MARGIN_LEFT + ((self.MARGIN_RIGHT - self.MARGIN_LEFT) - total_w) / 2

        rh = self.LINE_H["table"]
        hh = rh + 2
        nr = len(rows)

        # Estimate total height and check if it fits
        total_h = hh + nr * rh + 6
        self._brk(int(total_h) + 6)

        y0 = self.y
        hdr_bg = "0.30 0.55 0.85"
        bdr = "0.65 0.70 0.75"
        alt = "0.96 0.97 0.98"

        xpos = [sx + i * col_w for i in range(cols + 1)]

        # Max chars that fit in a cell at 8pt
        max_cell_chars = max(5, int(col_w / 4.5))

        def cell(cx: float, cy: float, cw: float, ch: float, fill: str = "") -> None:
            if fill:
                self._add(f"q {fill} rg {self._rect(cx, cy - ch, cw, ch)} f Q")
            self._add(f"q {bdr} RG 0.2 w {self._rect(cx, cy - ch, cw, ch)} S Q")

        def trunc(txt: str, mx: int) -> str:
            if len(txt) <= mx:
                return txt
            return txt[:mx-1] + "~"

        # Max rows per page
        max_rpp = max(1, int((self.y - self.MARGIN_BOTTOM - hh) / (rh + 1)))
        chunks = [rows[i:i + max_rpp] for i in range(0, nr, max_rpp)]

        for ci, chunk in enumerate(chunks):
            if ci > 0:
                self._flush()
                y0 = self.y

            fy = y0
            # Header row
            for cj in range(cols):
                cell(xpos[cj], fy, col_w, hh, hdr_bg)
                self._tb(xpos[cj] + 3, fy - hh + 4, trunc(headers[cj] if cj < cols else "", max_cell_chars), self.FONT_SIZES["table_header"])
            self._add(f"q {hdr_bg} RG 0.2 w {self._rect(sx, fy - hh, total_w, hh)} S Q")

            fy -= hh + 1
            # Data rows
            for ri, row in enumerate(chunk):
                fill = alt if ri % 2 == 0 else ""
                for cj in range(cols):
                    cell(xpos[cj], fy, col_w, rh, fill)
                    txt = row[cj] if cj < len(row) else ""
                    self._t(xpos[cj] + 3, fy - rh + 3, trunc(txt, max_cell_chars), PdfBuilder.FONT_REG, self.FONT_SIZES["table_cell"])
                self._add(f"q {bdr} RG 0.2 w {self._rect(sx, fy - rh, total_w, rh)} S Q")
                fy -= rh + 1

            self.y = fy - 3

    def render_chart(self, cfg: Dict[str, Any]) -> None:
        title = cfg.get("title", "")
        items = cfg.get("items", [])
        lk = cfg.get("label_key", "name")
        citems = limit_chart_items(items, label_key=lk, max_items=14)
        if not citems:
            return

        mv = max(float(x.get("hours", 0.0)) for x in citems) or 1.0
        n = len(citems)
        chart_h = 30 + n * 17
        self._brk(chart_h + 10)

        self._tb(self.MARGIN_LEFT, self.y, title, self.FONT_SIZES["chart_title"])
        self.y -= 14

        bl = 175
        bmw = 310
        bh = 9
        rg = 17
        pals = ["0.17 0.41 0.64", "0.20 0.60 0.86", "0.91 0.64 0.15", "0.28 0.70 0.55",
                 "0.82 0.33 0.26", "0.47 0.34 0.75", "0.55 0.45 0.65", "0.65 0.55 0.45",
                 "0.35 0.55 0.75", "0.75 0.35 0.55", "0.55 0.75 0.35", "0.45 0.65 0.55",
                 "0.85 0.45 0.35", "0.35 0.75 0.55"]

        yy = self.y
        for idx, item in enumerate(citems):
            label = str(item.get(lk, ""))
            val = float(item.get("hours", 0.0))
            w = max(2.0, (val / mv) * bmw)
            self._t(self.MARGIN_LEFT, yy - 3, label[:55], PdfBuilder.FONT_REG, self.FONT_SIZES["chart_label"])
            rgb = pals[idx % len(pals)]
            self._add(f"q {rgb} rg {self._rect(bl, yy - bh, w, bh)} f Q")
            self._t(bl + w + 3, yy - 3, f"{fmt_num(val)}h", PdfBuilder.FONT_REG, self.FONT_SIZES["chart_label"])
            yy -= rg

        self.y = yy - 8

    def finish(self) -> None:
        if self.content:
            self._flush()


def _clean(text: str) -> str:
    return text.replace("**", "").replace("__", "")


def parse_markdown_elements(content: str) -> List:
    elements = []
    lines = content.split("\n")
    i = 0
    in_table = False
    table_lines: List[str] = []
    in_code = False
    code_lines: List[str] = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                in_code = False
                code_block = "\n".join(code_lines)
                # Check if this is a mermaid chart or just code
                if code_lines and "mermaid" not in code_lines[0]:
                    elements.append(("code", code_block))
                else:
                    elements.append(("code", code_block))
                code_lines = []
                i += 1
                continue
            code_lines.append(line)
            i += 1
            continue

        if stripped.startswith("```"):
            in_code = True
            code_lines = []
            i += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
            i += 1
            continue
        else:
            if in_table:
                in_table = False
                table_text = "\n".join(table_lines)
                # Check if it's a real table (has separator row)
                if any("---" in ln for ln in table_lines):
                    elements.append(("table", table_text))
                else:
                    elements.append(("text", table_text))
                table_lines = []

        if not stripped:
            i += 1
            continue

        if stripped.startswith("#### "):
            elements.append(("h4", _clean(stripped[5:])))
        elif stripped.startswith("### "):
            elements.append(("h3", _clean(stripped[4:])))
        elif stripped.startswith("## "):
            elements.append(("h2", _clean(stripped[3:])))
        elif stripped.startswith("# "):
            elements.append(("h1", _clean(stripped[2:])))
        elif stripped == "---":
            elements.append(("separator", ""))
        elif stripped.startswith("**") and stripped.endswith("**"):
            elements.append(("bold_text", stripped.strip("*")))
        elif stripped.startswith("- "):
            text = stripped[2:]
            elements.append(("text", f"  - {_clean(text)}"))
        else:
            elements.append(("text", _clean(stripped)))

        i += 1

    if in_table and table_lines:
        if any("---" in ln for ln in table_lines):
            elements.append(("table", "\n".join(table_lines)))
        else:
            elements.append(("text", "\n".join(table_lines)))

    return elements


def write_pdf(file_path: Path, content: str, charts: List[Dict[str, Any]]) -> None:
    builder = PdfBuilder()
    r = PageRenderer(builder)

    elements = parse_markdown_elements(content)

    chart_index = 0
    for elem_type, elem_data in elements:
        if elem_type == "h1":
            r.render_h(1, elem_data)
        elif elem_type == "h2":
            r.render_h(2, elem_data)
        elif elem_type == "h3":
            r.render_h(3, elem_data)
        elif elem_type == "h4":
            r.render_h(4, elem_data)
        elif elem_type == "text":
            r.render_t(elem_data)
        elif elem_type == "bold_text":
            r.render_t(elem_data, bold=True)
        elif elem_type == "separator":
            r.render_sep()
        elif elem_type == "table":
            r.render_table(elem_data)
        elif elem_type == "code":
            if chart_index < len(charts):
                r.render_chart(charts[chart_index])
                chart_index += 1

    r.finish()
    builder.write(file_path)


def build_pdf_charts(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    collaborators = data.get("collaborators", [])
    projects = data.get("projects", [])
    service_desk = data.get("service_desk", [])
    meta = data.get("meta", {})
    total_hours = float(meta.get("total_hours", sum_hours(collaborators)))
    total_estimated = float(meta.get("total_estimated_unique_issues", sum_est(projects)))

    return [
        {
            "title": "2.1 Carga total: lancadas x estimadas",
            "items": [
                {"name": "Lancadas", "hours": total_hours},
                {"name": "Estimadas", "hours": total_estimated},
            ],
        },
        {
            "title": "2.2 Distribuicao de horas por colaborador",
            "items": collaborators,
        },
        {
            "title": "2.3 Distribuicao Service Desk por horas",
            "items": [{"name": item.get("classification", "Nao classificado"), "hours": item.get("hours", 0.0)} for item in service_desk],
        },
        {
            "title": "2.4 Distribuicao de horas por projeto",
            "items": projects,
        },
    ]


def get_default_data() -> Dict[str, Any]:
    return {
        "collaborators": [
            {"name": "João Silva", "hours": 160.0, "estimated": 150.0, "delta": 10.0, "entries": 28},
            {"name": "Maria Santos", "hours": 152.0, "estimated": 160.0, "delta": -8.0, "entries": 25},
            {"name": "Carlos Oliveira", "hours": 144.0, "estimated": 144.0, "delta": 0.0, "entries": 22},
            {"name": "Ana Costa", "hours": 136.0, "estimated": 140.0, "delta": -4.0, "entries": 20},
        ],
        "projects": [
            {"name": "ICI-DOC", "hours": 240.0, "estimated": 235.0, "delta": 5.0, "entries": 38},
            {"name": "CSDE DevOps", "hours": 176.0, "estimated": 180.0, "delta": -4.0, "entries": 28},
            {"name": "Portal Interno", "hours": 104.0, "estimated": 104.0, "delta": 0.0, "entries": 16},
            {"name": "Infraestrutura", "hours": 72.0, "estimated": 75.0, "delta": -3.0, "entries": 13},
        ],
        "activity_types": [
            {"name": "Desenvolvimento", "hours": 380.0, "estimated": 390.0, "delta": -10.0, "entries": 62},
            {"name": "Análise e Planejamento", "hours": 120.0, "estimated": 120.0, "delta": 0.0, "entries": 18},
            {"name": "Testes", "hours": 60.0, "estimated": 60.0, "delta": 0.0, "entries": 10},
            {"name": "Documentação", "hours": 24.0, "estimated": 20.0, "delta": 4.0, "entries": 3},
            {"name": "Administrativa", "hours": 8.0, "estimated": 4.0, "delta": 4.0, "entries": 2},
        ],
        "service_desk": [
            {
                "classification": "Requisição de Service Desk",
                "hours": 120.0,
                "estimated": 118.0,
                "delta": 2.0,
                "entries": 20,
            },
            {
                "classification": "Incidente de Service Desk",
                "hours": 84.0,
                "estimated": 82.0,
                "delta": 2.0,
                "entries": 14,
            },
            {
                "classification": "Não classificado",
                "hours": 16.0,
                "estimated": 14.0,
                "delta": 2.0,
                "entries": 3,
            },
        ],
        "subtables": {
            "ICI-DOC": {
                "Desenvolvimento": [
                    {"name": "João Silva", "hours": 88.0, "estimated": 85.0, "delta": 3.0, "entries": 14},
                    {"name": "Maria Santos", "hours": 80.0, "estimated": 85.0, "delta": -5.0, "entries": 12},
                    {"name": "Carlos Oliveira", "hours": 40.0, "estimated": 40.0, "delta": 0.0, "entries": 6},
                ],
                "Análise e Planejamento": [
                    {"name": "Carlos Oliveira", "hours": 40.0, "estimated": 40.0, "delta": 0.0, "entries": 6}
                ],
            },
            "CSDE DevOps": {
                "Desenvolvimento": [
                    {"name": "Carlos Oliveira", "hours": 80.0, "estimated": 80.0, "delta": 0.0, "entries": 11},
                    {"name": "Ana Costa", "hours": 56.0, "estimated": 60.0, "delta": -4.0, "entries": 9},
                ],
                "Análise e Planejamento": [
                    {"name": "Maria Santos", "hours": 40.0, "estimated": 40.0, "delta": 0.0, "entries": 8}
                ],
            },
        },
        "service_desk_subtables": {
            "ICI-DOC": {
                "Análise e Planejamento": [
                    {
                        "name": "Carlos Oliveira",
                        "classification": "Requisição de Service Desk",
                        "hours": 24.0,
                        "estimated": 24.0,
                        "delta": 0.0,
                        "entries": 4,
                    }
                ],
                "Testes": [
                    {
                        "name": "Ana Costa",
                        "classification": "Incidente de Service Desk",
                        "hours": 12.0,
                        "estimated": 10.0,
                        "delta": 2.0,
                        "entries": 2,
                    },
                    {
                        "name": "Ana Costa",
                        "classification": "Não classificado",
                        "hours": 12.0,
                        "estimated": 10.0,
                        "delta": 2.0,
                        "entries": 2,
                    },
                ],
            }
        },
        "planning_stats": [
            {
                "name": "Capacidade média semanal da equipe",
                "formula": "Horas lançadas / semanas do mês",
                "value": "148.00h/semana",
            },
            {
                "name": "Carga média por projeto",
                "formula": "Horas lançadas / projetos ativos",
                "value": "148.00h/projeto",
            },
            {
                "name": "Carga média por lançamento",
                "formula": "Horas lançadas / lançamentos",
                "value": "6.23h/lancamento",
            },
            {
                "name": "Cobertura de estimativas",
                "formula": "Issues com estimativa / issues totais",
                "value": "83.00%",
            },
            {
                "name": "Variação relativa de esforço",
                "formula": "(L-E) / E",
                "value": "-0.34%",
            },
        ],
    }


def build_report(data: Dict[str, Any], start: str, end: str, project: str, generated_at: str) -> str:
    collaborators = data.get("collaborators", [])
    projects = data.get("projects", [])
    activity_types = data.get("activity_types", [])
    service_desk = data.get("service_desk", [])
    subtables = data.get("subtables", {})
    sd_subtables = data.get("service_desk_subtables", {})
    planning_stats = data.get("planning_stats", [])
    meta = data.get("meta", {})

    total_hours = sum_hours(collaborators)
    total_est = float(meta.get("total_estimated_unique_issues", sum_est(projects) or sum_est(collaborators)))
    total_delta = total_hours - total_est
    total_entries = sum_entries(collaborators)
    collaborator_est_total = sum_est(collaborators)
    activity_est_total = sum_est(activity_types)

    top_collabs = sorted(collaborators, key=lambda item: float(item.get("hours", 0.0)), reverse=True)
    top_projects = sorted(projects, key=lambda item: float(item.get("hours", 0.0)), reverse=True)

    top3_collab_hours = sum(float(item.get("hours", 0.0)) for item in top_collabs[:3])
    top3_proj_hours = sum(float(item.get("hours", 0.0)) for item in top_projects[:3])

    sd_total = sum_hours(service_desk)
    sd_total_est = sum_est(service_desk)
    sd_entries = sum_entries(service_desk)

    indicators_rows = [
        ["Horas lançadas totais", f"{fmt_num(total_hours)}h"],
        ["Horas estimadas totais", f"{fmt_num(total_est)}h"],
        ["Aderência estimativa", fmt_pct((total_hours / total_est) * 100 if total_est > 0 else 0.0)],
        ["Colaboradores ativos", str(len(collaborators))],
        ["Projetos ativos", str(len(projects))],
        ["Classificações Service Desk mapeadas", str(len(service_desk))],
    ]

    collab_rows: List[List[str]] = []
    for item in top_collabs:
        hours = float(item.get("hours", 0.0))
        collab_rows.append(
            [
                str(item.get("name", "Não informado")),
                fmt_num(hours),
                fmt_num(float(item.get("estimated", 0.0))),
                fmt_num(float(item.get("delta", 0.0))),
                str(int(item.get("entries", 0))),
                pct(hours, total_hours),
            ]
        )
    collab_rows.append(["**Total**", f"**{fmt_num(total_hours)}**", f"**{fmt_num(total_est)}**", f"**{fmt_num(total_delta)}**", f"**{total_entries}**", "**100.00%**"])

    project_rows: List[List[str]] = []
    for item in top_projects:
        hours = float(item.get("hours", 0.0))
        project_rows.append(
            [
                str(item.get("name", "Projeto")),
                fmt_num(hours),
                fmt_num(float(item.get("estimated", 0.0))),
                fmt_num(float(item.get("delta", 0.0))),
                str(int(item.get("entries", 0))),
                pct(hours, total_hours),
            ]
        )
    project_rows.append(["**Total**", f"**{fmt_num(total_hours)}**", f"**{fmt_num(total_est)}**", f"**{fmt_num(total_delta)}**", f"**{total_entries}**", "**100.00%**"])

    activity_rows: List[List[str]] = []
    for item in sorted(activity_types, key=lambda row: float(row.get("hours", 0.0)), reverse=True):
        hours = float(item.get("hours", 0.0))
        activity_rows.append(
            [
                str(item.get("name", "Tipo")),
                fmt_num(hours),
                fmt_num(float(item.get("estimated", 0.0))),
                fmt_num(float(item.get("delta", 0.0))),
                str(int(item.get("entries", 0))),
                pct(hours, total_hours),
            ]
        )
    activity_rows.append(["**Total**", f"**{fmt_num(total_hours)}**", f"**{fmt_num(total_est)}**", f"**{fmt_num(total_delta)}**", f"**{total_entries}**", "**100.00%**"])

    sd_rows: List[List[str]] = []
    for item in sorted(service_desk, key=lambda row: float(row.get("hours", 0.0)), reverse=True):
        hours = float(item.get("hours", 0.0))
        sd_rows.append(
            [
                str(item.get("classification", "Não classificado")),
                fmt_num(hours),
                fmt_num(float(item.get("estimated", 0.0))),
                fmt_num(float(item.get("delta", 0.0))),
                str(int(item.get("entries", 0))),
                pct(hours, sd_total),
            ]
        )
    sd_rows.append(["**Total SD**", f"**{fmt_num(sd_total)}**", f"**{fmt_num(sd_total_est)}**", f"**{fmt_num(sd_total - sd_total_est)}**", f"**{sd_entries}**", "**100.00%**"])

    kpi_rows = [
        ["Total de horas lançadas", f"{fmt_num(total_hours)}h"],
        ["Total de horas estimadas", f"{fmt_num(total_est)}h"],
        ["Aderência estimativa (%)", fmt_pct((total_hours / total_est) * 100 if total_est > 0 else 0.0)],
        ["Desvio absoluto (|L-E|)", f"{fmt_num(abs(total_delta))}h"],
        ["Nº colaboradores ativos", str(len(collaborators))],
        ["Nº projetos ativos", str(len(projects))],
        ["Nº tipos de atividade", str(len(activity_types))],
        ["Média de horas por colaborador", f"{fmt_num((total_hours / len(collaborators)) if collaborators else 0.0)}h"],
        [
            "Colaborador com maior carga",
            f"{top_collabs[0].get('name', '-') if top_collabs else '-'} ({fmt_num(float(top_collabs[0].get('hours', 0.0)) if top_collabs else 0.0)}h)",
        ],
        [
            "Projeto com maior carga",
            f"{top_projects[0].get('name', '-') if top_projects else '-'} ({fmt_num(float(top_projects[0].get('hours', 0.0)) if top_projects else 0.0)}h)",
        ],
        [
            "Taxa de atividades administrativas (%)",
            pct(
                float(next((row.get("hours", 0.0) for row in activity_types if str(row.get("name", "")).lower() == "administrativa"), 0.0)),
                total_hours,
            ),
        ],
        ["Concentração top 3 colaboradores (%)", pct(top3_collab_hours, total_hours)],
        ["Concentração top 3 projetos (%)", pct(top3_proj_hours, total_hours)],
        ["Índice de concentração da equipe (top1/total)", pct(float(top_collabs[0].get("hours", 0.0)) if top_collabs else 0.0, total_hours)],
        ["Índice de concentração de projeto (top1/total)", pct(float(top_projects[0].get("hours", 0.0)) if top_projects else 0.0, total_hours)],
        ["Índice de participação de Service Desk (%)", pct(sd_total, total_hours)],
    ]

    planning_rows = [[str(item.get("name", "")), str(item.get("formula", "")), str(item.get("value", ""))] for item in planning_stats]

    sections: List[str] = []
    sections.append("# Relatório de Atividades dos Desenvolvedores")
    sections.append("")
    sections.append(f"**Período:** {start} a {end}  ")
    sections.append(f"**Projeto:** {project}  ")
    sections.append(f"**Gerado em:** {generated_at}")
    sections.append("")
    sections.append("## Índice")
    sections.append("")
    sections.append("- [1) Painel Executivo](#1-painel-executivo)")
    sections.append("- [2) Carga Total e Distribuições](#2-carga-total-e-distribuições)")
    sections.append("- [3) Colaboradores](#3-colaboradores)")
    sections.append("- [4) Projetos](#4-projetos)")
    sections.append("- [5) Tipos de Atividade](#5-tipos-de-atividade)")
    sections.append("- [6) Projeto > Tipo > Colaborador (Subtabelas)](#6-projeto--tipo--colaborador-subtabelas)")
    sections.append("- [7) Service Desk (Subtabelas)](#7-service-desk-subtabelas)")
    sections.append("- [8) KPIs e Índices de Planejamento](#8-kpis-e-índices-de-planejamento)")
    sections.append("- [9) Estatísticas para Planejamento](#9-estatísticas-para-planejamento)")
    sections.append("- [10) Observações](#10-observações)")
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 1) Painel Executivo")
    sections.append("")
    sections.append(md_table(["Indicador Chave", "Valor"], indicators_rows))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 2) Carga Total e Distribuições")
    sections.append("")
    sections.append("### 2.1 Carga total lançada x estimada")
    sections.append("")
    sections.append(build_mermaid_total(total_hours, total_est))
    sections.append("")
    sections.append("### 2.2 Distribuição de horas por colaborador")
    sections.append("")
    sections.append(build_collaborator_pie_with_two_column_legend(top_collabs))
    sections.append("")
    sections.append("### 2.3 Distribuição de horas por classificação Service Desk")
    sections.append("")
    sections.append(build_mermaid_pie("Distribuição Service Desk por horas", [{"name": s.get("classification", "Não classificado"), "hours": s.get("hours", 0.0)} for s in service_desk]))
    sections.append("")
    sections.append("### 2.4 Distribuição de horas por projeto")
    sections.append("")
    sections.append(build_mermaid_project_bar(top_projects))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 3) Colaboradores")
    sections.append("")
    sections.append(md_table(["Colaborador", "Horas Lançadas", "Horas Estimadas", "Delta (L-E)", "Atividades com Horas", "% da Carga"], collab_rows))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 4) Projetos")
    sections.append("")
    sections.append(md_table(["Projeto", "Horas Lançadas", "Horas Estimadas", "Delta (L-E)", "Atividades com Horas", "% da Carga"], project_rows))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 5) Tipos de Atividade")
    sections.append("")
    sections.append(md_table(["Tipo de Atividade", "Horas Lançadas", "Horas Estimadas", "Delta (L-E)", "Atividades com Horas", "% da Carga"], activity_rows))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 6) Projeto > Tipo > Colaborador (Subtabelas)")
    sections.append("")
    for project_name, type_map in subtables.items():
        sections.append(f"### 6.{len(sections)} Projeto: {project_name}")
        sections.append("")
        for type_name, rows in type_map.items():
            sections.append(f"#### Tipo: {type_name}")
            sections.append("")
            sub_rows: List[List[str]] = []
            for row in rows:
                sub_rows.append(
                    [
                        str(row.get("name", "")),
                        fmt_num(float(row.get("hours", 0.0))),
                        fmt_num(float(row.get("estimated", 0.0))),
                        fmt_num(float(row.get("delta", 0.0))),
                        str(int(row.get("entries", 0))),
                    ]
                )
            sub_hours = sum_hours(rows)
            sub_est = sum_est(rows)
            sub_delta = sub_hours - sub_est
            sub_entries = sum_entries(rows)
            sub_rows.append([f"**Subtotal ({project_name} > {type_name})**", f"**{fmt_num(sub_hours)}**", f"**{fmt_num(sub_est)}**", f"**{fmt_num(sub_delta)}**", f"**{sub_entries}**"])
            sections.append(md_table(["Colaborador", "Horas Lançadas", "Horas Estimadas", "Delta (L-E)", "Atividades com Horas"], sub_rows))
            sections.append("")

    sections.append("---")
    sections.append("")
    sections.append("## 7) Service Desk (Subtabelas)")
    sections.append("")
    sections.append("### 7.1 Visão consolidada por classificação")
    sections.append("")
    sections.append(md_table(["Classificação Service Desk", "Horas Lançadas", "Horas Estimadas", "Delta (L-E)", "Atividades com Horas", "% sobre SD"], sd_rows))
    sections.append("")
    for project_name, type_map in sd_subtables.items():
        sections.append(f"### Projeto: {project_name}")
        sections.append("")
        for type_name, rows in type_map.items():
            sections.append(f"#### Tipo: {type_name}")
            sections.append("")
            sd_detail_rows: List[List[str]] = []
            for row in rows:
                sd_detail_rows.append(
                    [
                        str(row.get("name", "")),
                        str(row.get("classification", "Não classificado")),
                        fmt_num(float(row.get("hours", 0.0))),
                        fmt_num(float(row.get("estimated", 0.0))),
                        fmt_num(float(row.get("delta", 0.0))),
                        str(int(row.get("entries", 0))),
                    ]
                )
            sd_sub_hours = sum_hours(rows)
            sd_sub_est = sum_est(rows)
            sd_sub_delta = sd_sub_hours - sd_sub_est
            sd_sub_entries = sum_entries(rows)
            sd_detail_rows.append([f"**Subtotal ({project_name} > {type_name})**", "-", f"**{fmt_num(sd_sub_hours)}**", f"**{fmt_num(sd_sub_est)}**", f"**{fmt_num(sd_sub_delta)}**", f"**{sd_sub_entries}**"])
            sections.append(md_table(["Colaborador", "Classificação Service Desk", "Horas Lançadas", "Horas Estimadas", "Delta (L-E)", "Atividades com Horas"], sd_detail_rows))
            sections.append("")

    sections.append("---")
    sections.append("")
    sections.append("## 8) KPIs e Índices de Planejamento")
    sections.append("")
    sections.append(md_table(["KPI / Índice", "Valor"], kpi_rows))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 9) Estatísticas para Planejamento")
    sections.append("")
    sections.append(md_table(["Estatística", "Fórmula", "Resultado"], planning_rows))
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## 10) Observações")
    sections.append("")
    sections.append("- Algumas issues não possuem horas estimadas no Redmine; nesses casos foi considerado 0.00.")
    sections.append("- Subtabelas foram aplicadas para melhorar leitura em visões hierárquicas (Projeto > Tipo > Colaborador).")
    sections.append("- Classificação Service Desk segue a taxonomia: Requisição, Incidente e Não classificado.")
    sections.append("- A coluna 'Atividades com Horas' representa a quantidade de atividades distintas com apontamento no agrupamento; quando não há issue associada, o apontamento individual conta como uma atividade.")
    if abs(collaborator_est_total - total_est) > 0.009 or abs(activity_est_total - total_est) > 0.009:
        sections.append("- O resumo executivo e os KPIs usam horas estimadas únicas por issue no escopo; visões por colaborador e por tipo de atividade podem repetir a mesma estimativa quando a issue aparece em mais de um agrupamento.")
    sections.append("")

    return "\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera relatório em Markdown com índice, gráficos e subtabelas.")
    parser.add_argument("--input", help="JSON de entrada com os dados consolidados.")
    parser.add_argument("--output", required=True, help="Arquivo Markdown de saída.")
    parser.add_argument("--period-start", required=True, help="Data inicial no formato DD/MM/YYYY.")
    parser.add_argument("--period-end", required=True, help="Data final no formato DD/MM/YYYY.")
    parser.add_argument("--project", default="Todos", help="Nome do projeto ou 'Todos'.")
    parser.add_argument("--generated-at", default=datetime.now().strftime("%d/%m/%Y %H:%M"), help="Data/hora de geração.")
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
        data = json.loads(input_path.read_text(encoding="utf-8"))
    else:
        data = get_default_data()

    report = build_report(data, args.period_start, args.period_end, args.project, args.generated_at)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    pdf_output_path = output_path.with_suffix(".pdf")
    write_pdf(pdf_output_path, report, build_pdf_charts(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
