#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert XHTML Bottom-Up estimation files to Markdown."""

import re
import os
import html
from pathlib import Path

BASE_DIR = Path(r"C:\ICI\Git\Copilot\copilot\skills\estimativa-bottom-up-ici")
OUTPUT_DIR = BASE_DIR / "base-conhecimento"


def get_cell_text(cell_html: str) -> str:
    """Extract visible text from an HTML table cell."""
    # Remove comment elements
    clean = re.sub(r'<comment>.*?</comment>', '', cell_html, flags=re.DOTALL)
    # Remove anchor tags
    clean = re.sub(r'<a[^>]*>.*?</a>', '', clean, flags=re.DOTALL)
    # Extract text from font tags
    font_texts = re.findall(r'<font[^>]*>(.*?)</font>', clean, re.DOTALL)
    if font_texts:
        texts = []
        for t in font_texts:
            t = re.sub(r'<br\s*/?>', ' ', t)
            t = re.sub(r'<[^>]+>', '', t)
            t = html.unescape(t)
            t = re.sub(r'\s+', ' ', t).strip()
            if t:
                texts.append(t)
        if texts:
            return ' '.join(texts).strip()
    # Fallback: strip all HTML
    text = re.sub(r'<[^>]+>', ' ', clean)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def get_field_value(id_html: str, label_text: str) -> str:
    """Find the value cell after a label cell in the identification section."""
    esc = re.escape(label_text)
    pattern = (
        r'<td[^>]*>\s*(?:<b>)?\s*<font[^>]*>\s*(?:<b>)?' + esc +
        r'\s*(?:</b>)?\s*</font>\s*(?:</b>)?\s*</td>\s*<td[^>]*>(.*?)</td>'
    )
    m = re.search(pattern, id_html, re.DOTALL)
    if m:
        return get_cell_text(m.group(1))
    return ''


def try_field(id_html: str, *labels) -> str:
    """Try multiple label variants, return first match."""
    for label in labels:
        val = get_field_value(id_html, label)
        if val:
            return val
    return ''


def escape_md(text: str) -> str:
    """Escape pipe characters for Markdown tables and clean whitespace."""
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    text = text.replace('|', r'\|')
    return text.strip()


def get_escopo(id_html: str) -> str:
    """Extract the scope text from the identification section."""
    m = re.search(
        r'Escopo da Estimativa.*?</td>.*?</tr>.*?<tr>.*?<td[^>]*>(.*?)</td>',
        id_html, re.DOTALL
    )
    if m:
        text = get_cell_text(m.group(1))
        if len(text) > 10:
            return text
    return ''


def parse_req_table(req_html: str):
    """Parse requirements table; returns (rows, totals, distribs)."""
    rows = []
    totals = ['0:00'] * 6
    distribs = ['0,00%'] * 5 + ['100,00%']

    table_m = re.search(r'<table[^>]*>(.*?)</table>', req_html, re.DOTALL)
    if not table_m:
        return rows, totals, distribs

    table_html = table_m.group(1)
    all_rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
    data_mode = False

    for row_html in all_rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
        if not tds:
            continue
        cells = [get_cell_text(td) for td in tds]

        # Detect column header row
        if 'Funcionalidade' in cells:
            data_mode = True
            continue
        if not data_mode:
            continue

        # "Total de horas" summary row
        total_idx = next((i for i, c in enumerate(cells) if 'Total de horas' in c), -1)
        if total_idx >= 0:
            for i in range(6):
                vi = total_idx + 1 + i
                if vi < len(cells) and cells[vi]:
                    totals[i] = cells[vi]
            continue

        # "Distribuicao das horas" row (accent insensitive match)
        dist_idx = next((i for i, c in enumerate(cells) if 'Distribui' in c), -1)
        if dist_idx >= 0:
            for i in range(6):
                vi = dist_idx + 1 + i
                if vi < len(cells) and cells[vi]:
                    distribs[i] = cells[vi]
            continue

        # Skip other summary/footer rows
        if any('Homologa' in c or 'Implanta' in c or 'Total em Horas' in c for c in cells):
            continue

        # Data row: must have Funcionalidade (index 1)
        if len(cells) >= 2 and cells[1]:
            rows.append(cells)

    return rows, totals, distribs


def convert_file(xhtml_path: Path, output_dir: Path = None) -> bool:
    """Convert a single XHTML file to Markdown. Returns True on success."""
    content = xhtml_path.read_text(encoding='utf-8', errors='replace')

    t1 = content.find('NAME="table1"')
    t2 = content.find('NAME="table2"')

    if t1 < 0:
        print(f'  SKIP (no identification section)')
        return False

    id_html = content[t1:t2] if t2 > 0 else content[t1:]
    req_html = content[t2:] if t2 > 0 else ''

    # ===== IDENTIFICATION =====
    cliente   = try_field(id_html, 'Cliente:')
    sistema   = try_field(id_html, 'Sistema:')
    orgao     = try_field(id_html, '\u00d3rg\u00e3o:', 'Orgao:', 'Org\u00e3o:')
    requisicao = try_field(id_html,
                           'Requisi\u00e7\u00e3o/Of\u00edcio:',
                           'Requisi\u00e7\u00e3o:',
                           'Requisi\u00e7\u00e3o /Of\u00edcio:')
    sgc       = try_field(id_html, 'Identificador SGC:', 'Identificador SGC')
    analista  = try_field(id_html,
                          'Analista Respons\u00e1vel:',
                          'Analista Responsavel:',
                          'Analista Respons\u00e1vel')
    tecnologia = try_field(id_html, 'Tecnologia:', 'Tecnologia')
    data_est  = try_field(id_html,
                          'Data Estimativa: ',
                          'Data Estimativa:',
                          'Data Estimativa')

    # ===== ESCOPO =====
    escopo = get_escopo(id_html)

    # ===== REQUIREMENTS TABLE =====
    req_rows, totals, distribs = parse_req_table(req_html)

    # ===== TITLE =====
    num_m = re.search(r'\d+', xhtml_path.stem)
    req_num = num_m.group(0) if num_m else xhtml_path.stem
    is_sd = '_SD_' in xhtml_path.name
    title_type = 'SD' if is_sd else 'Requisi\u00e7\u00e3o'

    # ===== GENERATE MARKDOWN =====
    lines = []
    lines.append(f'# Estimativa Bottom-Up: {title_type} {req_num}')
    lines.append('')
    lines.append('## Identifica\u00e7\u00e3o da Estimativa')
    lines.append('')
    lines.append('| Campo | Valor |')
    lines.append('|-------|-------|')
    lines.append(f'| **Cliente** | {escape_md(cliente)} |')
    lines.append(f'| **Sistema** | {escape_md(sistema)} |')
    lines.append(f'| **\u00d3rg\u00e3o** | {escape_md(orgao)} |')
    lines.append(f'| **Requisi\u00e7\u00e3o/Of\u00edcio** | {escape_md(requisicao)} |')
    lines.append(f'| **Identificador SGC** | {escape_md(sgc)} |')
    lines.append(f'| **Analista Respons\u00e1vel** | {escape_md(analista)} |')
    lines.append(f'| **Tecnologia** | {escape_md(tecnologia)} |')
    lines.append(f'| **Data da Estimativa** | {escape_md(data_est)} |')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Escopo da Estimativa')
    lines.append('')
    if escopo:
        lines.append(escopo)
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Tabela de Requisitos Funcionais')
    lines.append('')
    lines.append(
        '| Funcionalidade | Requisito | Tipo | '
        'Descri\u00e7\u00e3o da Funcionalidade | '
        'Eng. Requisitos (40%) | Arquitetura (40%) | '
        'Implementa\u00e7\u00e3o (75%) | Teste (20%) | '
        'Cientista de Dados (10%) | **Total Horas** |'
    )
    lines.append('|---|---|---|---|---|---|---|---|---|---|')

    for row in req_rows:
        func  = escape_md(row[1] if len(row) > 1 and row[1] else '')
        req   = escape_md(row[2] if len(row) > 2 and row[2] else '-')
        tipo  = escape_md(row[3] if len(row) > 3 and row[3] else '')
        desc  = escape_md(row[4] if len(row) > 4 and row[4] else '')
        er    = row[5] if len(row) > 5 and row[5] else '0:00'
        arq   = row[6] if len(row) > 6 and row[6] else '0:00'
        impl  = row[7] if len(row) > 7 and row[7] else '0:00'
        test  = row[8] if len(row) > 8 and row[8] else '0:00'
        cd    = row[9] if len(row) > 9 and row[9] else '0:00'
        tot   = row[10] if len(row) > 10 and row[10] else '0:00'
        lines.append(
            f'| {func} | {req} | {tipo} | {desc} | '
            f'{er} | {arq} | {impl} | {test} | {cd} | **{tot}** |'
        )

    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Resumo de Horas')
    lines.append('')
    lines.append('| Atividade | Total Horas | Distribui\u00e7\u00e3o |')
    lines.append('|-----------|-------------|--------------|')
    lines.append(f'| Eng. Requisitos (40%) | {totals[0]} | {distribs[0]} |')
    lines.append(f'| Arquitetura (40%) | {totals[1]} | {distribs[1]} |')
    lines.append(f'| Implementa\u00e7\u00e3o (75%) | {totals[2]} | {distribs[2]} |')
    lines.append(f'| Teste (20%) | {totals[3]} | {distribs[3]} |')
    lines.append(f'| Cientista de Dados (10%) | {totals[4]} | {distribs[4]} |')
    lines.append(f'| **TOTAL ESTIMADO** | **{totals[5]}** | **{distribs[5]}** |')
    lines.append('')

    if output_dir is None:
        output_dir = xhtml_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / (xhtml_path.stem + '.md')
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    return True


def main():
    xhtml_files = sorted(BASE_DIR.glob('*.xhtml'))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    processed = 0
    errors = 0

    for xhtml_path in xhtml_files:
        print(f'Processing: {xhtml_path.name}', end='')
        try:
            _, totals, _ = parse_req_table(
                xhtml_path.read_text(encoding='utf-8', errors='replace')
            )
            req_rows, _, _ = parse_req_table(
                xhtml_path.read_text(encoding='utf-8', errors='replace')
            )
            ok = convert_file(xhtml_path, OUTPUT_DIR)
            if ok:
                processed += 1
                _, _, _ = parse_req_table('')  # dummy
                # Re-read to count rows
                content = xhtml_path.read_text(encoding='utf-8', errors='replace')
                t2 = content.find('NAME="table2"')
                req_html = content[t2:] if t2 > 0 else ''
                rows, _, _ = parse_req_table(req_html)
                print(f' - OK ({len(rows)} rows)')
            else:
                print()
        except Exception as e:
            errors += 1
            print(f' - ERROR: {e}')

    print(f'\nDone! Processed: {processed}/{len(xhtml_files)}, Errors: {errors}')


if __name__ == '__main__':
    main()
