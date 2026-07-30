#!/usr/bin/env python3
"""
gerar_planilha_estimativa.py
Gera planilha Bottom-Up XLSX idêntica ao template planilha_bottom_up.xlsx.

Uso:
    py gerar_planilha_estimativa.py --dados <arquivo.json> [--saida <arquivo.xlsx>]
    py gerar_planilha_estimativa.py --interativo

Dependências: openpyxl  (pip install openpyxl)
"""

import argparse
import json
import math
import os
import sys
from datetime import timedelta, date
from pathlib import Path

try:
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side, GradientFill
    from openpyxl.utils import get_column_letter
    from openpyxl.drawing.image import Image as XLImage
    from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor, AnchorMarker
except ImportError:
    print("Dependencia ausente. Instale com: pip install openpyxl")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paleta de cores exata do template
# ---------------------------------------------------------------------------
# Extraídas diretamente do arquivo planilha_bottom_up.xlsx
RGB_TITULO_BG      = "FF244061"   # linha 2: "Estimativa Bottom-Up"
RGB_DARK_BLUE      = "FF1F497D"   # título A1 Requisitos + Distribuição + Total Geral
RGB_HEADER_BG      = "FF4F81BD"   # theme accent1 — cabeçalho colunas + Total horas + homo/impl
RGB_WHITE          = "FFFFFFFF"   # fonte em fundos escuros
RGB_BLACK          = "FF000000"   # fonte padrão

# ---------------------------------------------------------------------------
# Helpers de estilo
# ---------------------------------------------------------------------------
def _fill(rgb: str) -> PatternFill:
    return PatternFill(fill_type="solid", fgColor=rgb)

def _no_fill() -> PatternFill:
    return PatternFill(fill_type=None)

def _font(bold=False, size=10, color=RGB_BLACK, italic=False, name="Calibri") -> Font:
    return Font(bold=bold, size=size, color=color, italic=italic, name=name)

def _align(h="general", v="center", wrap=False) -> Alignment:
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def _side(style=None) -> Side:
    return Side(style=style)

def _border(left=None, right=None, top=None, bottom=None) -> Border:
    return Border(
        left=_side(left), right=_side(right),
        top=_side(top),   bottom=_side(bottom),
    )

def _h_to_td(horas: float) -> timedelta:
    return timedelta(seconds=int(horas * 3600))

# ---------------------------------------------------------------------------
# Aba Instruções
# ---------------------------------------------------------------------------
def _aba_instrucoes(wb: Workbook) -> None:
    ws = wb.create_sheet("Instruções")
    ws.column_dimensions["A"].width = 110

    linhas = [
        ("INSTRUÇÕES", True, 14, False),
        ("Esta aba contém instruções gerais para preenchimento da planilha.", False, 10, False),
        ("Quando necessário, algumas células possuem comentários mais detalhados sobre seu preenchimento e significado.", False, 10, False),
        ("", False, 10, False),
        ("1. IDENTIFICAÇÃO", True, 11, False),
        ("Preencher com informações gerais da estimativa.", False, 10, False),
        ("Cliente: Nome do cliente solicitante.", False, 10, False),
        ("Sistema: Nome do sistema.", False, 10, False),
        ("Identificador SGC: Número de identificação do sistema no SGC.", False, 10, False),
        ("Tecnologia: Tecnologia a ser usada na requisição.", False, 10, False),
        ("Órgão: Órgão que solicitou a requisição.", False, 10, False),
        ("Requisição/Ofício: Número de origem (requisição do service desk ou ofício).", False, 10, False),
        ("Analista Responsável: Nome do analista responsável pela estimativa.", False, 10, False),
        ("Data Estimativa: Data da realização da estimativa.", False, 10, False),
        ("Escopo da Estimativa: Resumo da estimativa realizada.", False, 10, False),
        ("Material de Apoio: Listagem dos materiais de apoio utilizados.", False, 10, False),
        ("", False, 10, False),
        ("2. REQUISITOS", True, 11, False),
        ("Aba para preenchimento dos requisitos/funcionalidades e suas estimativas.", False, 10, False),
        ("As estimativas devem ser preenchidas por tipo de atividade.", False, 10, False),
        ("O valor estimado por tipo deve respeitar o percentual máximo descrito em contrato.", False, 10, False),
        ("O total por requisito e o total da estimativa serão calculados pela soma das estimativas.", False, 10, False),
        ("", False, 10, False),
        ("2.1 IDENTIFICAÇÃO DOS REQUISITOS", True, 10, False),
        ("Item RDM: Número que identifica o item no documento de escopo.", False, 10, False),
        ("Funcionalidade: Identificador da funcionalidade.", False, 10, False),
        ("Requisito: Identificador do requisito (ex: REQ001-Cadastro de Usuário).", False, 10, False),
        ("Tipo: MELHORIA para ajuste em funcionalidade existente, NOVO para funcionalidade nova.", False, 10, False),
        ("Descrição da Funcionalidade: Descrição detalhada do que será realizado.", False, 10, False),
        ("", False, 10, False),
        ("2.2 ESTIMATIVA POR TIPO DE ATIVIDADE", True, 10, False),
        ("Engenharia de Requisitos (40%): levantamento, negociação, prototipação, documentação.", False, 10, False),
        ("Implementação (75%): estudo técnico e codificação.", False, 10, False),
        ("Teste (20%): casos de teste, testes manuais/automatizados, regressivos, relatório.", False, 10, False),
        ("Homologação (15%): acompanhamento com o cliente na validação — condicional.", False, 10, False),
        ("Implantação (10%): atividades de publicação em produção — condicional.", False, 10, False),
        ("Cientista de Dados (10%): BI, IA, IoT — quando aplicável.", False, 10, False),
        ("", False, 10, False),
        ("OBS: Itens de Machine Learning (ML) serão tratados em outra planilha.", False, 10, False),
    ]

    for i, (texto, bold, sz, italic) in enumerate(linhas, start=1):
        c = ws.cell(row=i, column=1, value=texto)
        c.font = Font(bold=bold, size=sz, italic=italic)
        c.alignment = Alignment(wrap_text=True, vertical="center")


# ---------------------------------------------------------------------------
# Aba Identificação — fiel ao template
# ---------------------------------------------------------------------------
def _aba_identificacao(wb: Workbook, dados: dict, logo_path: str | None) -> None:
    ws = wb.create_sheet("Identificação")

    # --- Larguras de coluna (exatas do template) ---
    # A=estreita (margem), B..F=conteúdo, G=estreita, H=estreita
    # Tabelas e imagem cobrem A..H — mesma largura total
    ws.column_dimensions["A"].width = 1.89
    ws.column_dimensions["B"].width = 22.0   # aumentado para caber "Documento(s) utilizado(s):"
    ws.column_dimensions["C"].width = 8.89
    ws.column_dimensions["D"].width = 32.33
    ws.column_dimensions["E"].width = 22.0
    ws.column_dimensions["F"].width = 23.33
    ws.column_dimensions["G"].width = 5.44
    ws.column_dimensions["H"].width = 5.44

    # --- Alturas de linha (do template) ---
    ws.row_dimensions[1].height  = 64.2
    ws.row_dimensions[2].height  = 16.5
    ws.row_dimensions[3].height  = 5.25
    ws.row_dimensions[4].height  = 12.75
    ws.row_dimensions[5].height  = 9.0
    for r in range(6, 12):
        ws.row_dimensions[r].height = 12.75
    ws.row_dimensions[11].height = 6.75
    ws.row_dimensions[12].height = 12.75
    ws.row_dimensions[13].height = 173.25
    ws.row_dimensions[14].height = 8.25
    ws.row_dimensions[15].height = 12.75
    ws.row_dimensions[16].height = 12.75
    ws.row_dimensions[17].height = 12.75
    ws.row_dimensions[18].height = 12.75
    ws.row_dimensions[19].height = 12.75
    ws.row_dimensions[20].height = 12.75

    # Colunas usadas pelas tabelas (mesma extensão da imagem: A..H = cols 1..8)
    COL_FIRST = 1   # A
    COL_LAST  = 8   # H

    def _col(n):
        return get_column_letter(n)

    def _fill_row_bg(row, col_start, col_end, rgb, borda_esq=None, borda_dir=None,
                     borda_top=None, borda_bot=None):
        """Aplica fill e bordas a uma linha inteira de col_start..col_end."""
        for col in range(col_start, col_end + 1):
            c = ws.cell(row, col)
            c.fill = _fill(rgb)
            c.border = _border(
                left="thin"  if (col == col_start and borda_esq) else None,
                right="thin" if (col == col_end   and borda_dir) else None,
                top=borda_top,
                bottom=borda_bot,
            )

    # ------------------------------------------------------------------ #
    # LINHA 1 — Logo ICI com TwoCellAnchor (de A1 a H1 exatamente)
    # Usa os mesmos offsets do template:
    #   from: col=0, row=0, colOff=129540, rowOff=0
    #   to:   col=7, row=0, colOff=373194, rowOff=800100
    # ------------------------------------------------------------------ #
    if logo_path and Path(logo_path).exists():
        img = XLImage(logo_path)
        marker_from = AnchorMarker(col=0, colOff=0, row=0, rowOff=0)
        # to.col=COL_LAST (0-based index 8 = início da col I) significa que
        # a imagem ocupa até o fim da col H — alinhado com a borda direita das tabelas
        marker_to   = AnchorMarker(col=COL_LAST, colOff=0, row=0, rowOff=800100)
        anchor      = TwoCellAnchor(editAs="oneCell", _from=marker_from, to=marker_to)
        img.anchor  = anchor
        ws.add_image(img)

    # ------------------------------------------------------------------ #
    # LINHA 2 — "Estimativa Bottom-Up" (A2..G2) + "Versão 1.3" (H2)
    # ------------------------------------------------------------------ #
    ws.merge_cells(f"A2:{_col(COL_LAST - 1)}2")   # A2:G2
    c = ws["A2"]
    c.value     = "Estimativa Bottom-Up"
    c.font      = _font(bold=True, size=11, color=RGB_WHITE)
    c.fill      = _fill(RGB_TITULO_BG)
    c.alignment = _align("center")
    c.border    = _border(top="thin")
    for col in range(2, COL_LAST):
        ws.cell(2, col).fill   = _fill(RGB_TITULO_BG)
        ws.cell(2, col).border = _border(top="thin")

    c = ws.cell(2, COL_LAST, value="Versão 1.3")
    c.font      = _font(bold=True, size=11, color=RGB_WHITE)
    c.fill      = _fill(RGB_TITULO_BG)
    c.alignment = _align("right")
    c.border    = _border(top="thin")

    # ------------------------------------------------------------------ #
    # LINHA 4 — "Identificação da Estimativa" (A4:H4)
    # ------------------------------------------------------------------ #
    ws.merge_cells(f"A4:{_col(COL_LAST)}4")
    c = ws["A4"]
    c.value     = "Identificação da Estimativa"
    c.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c.fill      = _fill(RGB_DARK_BLUE)
    c.alignment = _align("center")
    c.border    = _border(left="thin", top="thin")
    for col in range(2, COL_LAST + 1):
        ws.cell(4, col).fill   = _fill(RGB_DARK_BLUE)
        ws.cell(4, col).border = _border(
            top="thin",
            right="thin" if col == COL_LAST else None,
        )

    # bordas laterais linhas 5..10 (caixa da seção de identificação)
    for r in range(5, 11):
        ws.cell(r, COL_FIRST).border = _border(left="thin")
        ws.cell(r, COL_LAST ).border = _border(right="thin")
    # fundo linha 10 (linha vazia de fechamento)
    for col in range(COL_FIRST, COL_LAST + 1):
        ws.cell(10, col).border = _border(
            left="thin"  if col == COL_FIRST else None,
            right="thin" if col == COL_LAST  else None,
            bottom="thin",
        )

    # ------------------------------------------------------------------ #
    # Linhas 6-9 — campos de identificação
    # Layout: [A=margem] [B=label] [C:D=valor] [E=label] [F:G=valor] [H=margem]
    # ------------------------------------------------------------------ #
    def _campo_label(row, col_lbl, texto_lbl, col_val_s, col_val_e, valor):
        c_lbl = ws.cell(row, col_lbl, value=texto_lbl)
        c_lbl.font      = _font(size=10)
        c_lbl.alignment = _align("right")

        ws.merge_cells(start_row=row, start_column=col_val_s,
                       end_row=row,   end_column=col_val_e)
        c_val = ws.cell(row, col_val_s, value=valor)
        c_val.font      = _font(size=10)
        c_val.alignment = _align("left")
        c_val.border    = _border(left="thin", right="thin", top="thin", bottom="thin")
        for col in range(col_val_s + 1, col_val_e + 1):
            ws.cell(row, col).border = _border(
                top="thin", bottom="thin",
                right="thin" if col == col_val_e else None,
            )

    # Col B=label, C:D=valor | Col E=label, F:G=valor
    _campo_label(6, 2, "Cliente:",              3, 4, dados.get("cliente", ""))
    _campo_label(6, 5, "Órgão:",                6, 7, dados.get("orgao",   ""))
    _campo_label(7, 2, "Sistema:",              3, 4, dados.get("sistema", ""))
    _campo_label(7, 5, "Requisição/Ofício:",    6, 7, dados.get("requisicao", ""))
    _campo_label(8, 2, "Identificador SGC:",    3, 4, dados.get("sgc", ""))
    _campo_label(8, 5, "Analista Responsável:", 6, 7, dados.get("analista", ""))
    _campo_label(9, 2, "Tecnologia",            3, 4, dados.get("tecnologia", "DotNet"))
    _campo_label(9, 5, "Data Estimativa: ",     6, 7, dados.get("data_estimativa",
                                                                  date.today().strftime("%d/%m/%Y")))

    # ------------------------------------------------------------------ #
    # LINHA 12 — "Escopo de Estimativa" (A12:H12)
    # ------------------------------------------------------------------ #
    ws.merge_cells(f"A12:{_col(COL_LAST)}12")
    c = ws["A12"]
    c.value     = "Escopo de Estimativa"
    c.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c.fill      = _fill(RGB_DARK_BLUE)
    c.alignment = _align("left")
    c.border    = _border(left="thin", top="thin", bottom="thin")
    for col in range(2, COL_LAST + 1):
        ws.cell(12, col).fill   = _fill(RGB_DARK_BLUE)
        ws.cell(12, col).border = _border(
            top="thin", bottom="thin",
            right="thin" if col == COL_LAST else None,
        )

    # ------------------------------------------------------------------ #
    # LINHA 13 — conteúdo do escopo (A13:H13)
    # ------------------------------------------------------------------ #
    ws.merge_cells(f"A13:{_col(COL_LAST)}13")
    c = ws["A13"]
    c.value     = dados.get("escopo", "")
    c.font      = _font(size=10)
    c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    c.border    = _border(left="thin", top="thin", bottom="thin")
    for col in range(2, COL_LAST + 1):
        ws.cell(13, col).border = _border(
            top="thin", bottom="thin",
            right="thin" if col == COL_LAST else None,
        )

    # ------------------------------------------------------------------ #
    # LINHA 15 — "Material de Apoio" (A15:H15)
    # ------------------------------------------------------------------ #
    ws.merge_cells(f"A15:{_col(COL_LAST)}15")
    c = ws["A15"]
    c.value     = "Material de Apoio"
    c.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c.fill      = _fill(RGB_DARK_BLUE)
    c.alignment = _align("left")
    c.border    = _border(left="thin", top="thin", bottom="thin")
    for col in range(2, COL_LAST + 1):
        ws.cell(15, col).fill   = _fill(RGB_DARK_BLUE)
        ws.cell(15, col).border = _border(
            top="thin", bottom="thin",
            right="thin" if col == COL_LAST else None,
        )

    # ------------------------------------------------------------------ #
    # LINHA 16 — linha vazia com bordas laterais (dentro da caixa)
    # ------------------------------------------------------------------ #
    ws.cell(16, COL_FIRST).border = _border(left="thin")
    ws.cell(16, COL_LAST ).border = _border(right="thin")

    # ------------------------------------------------------------------ #
    # LINHAS 17-19 — Documento(s) utilizado(s)
    # Label: A17:B17 merged (alinhado direita)
    # Valor: C17:G17 merged (com borda)
    # ------------------------------------------------------------------ #
    materiais = dados.get("material_apoio", "")

    for r in range(17, 20):
        # label: A:B merged
        ws.merge_cells(f"A{r}:B{r}")
        c_lbl = ws.cell(r, 1, value="Documento(s) utilizado(s): " if r == 17 else None)
        c_lbl.font      = _font(size=10)
        c_lbl.alignment = _align("right", "center")
        c_lbl.border    = _border(left="thin")

        # valor: C:G merged (deixa H como margem direita)
        ws.merge_cells(f"C{r}:{_col(COL_LAST - 1)}{r}")
        c_val = ws.cell(r, 3, value=materiais if r == 17 else None)
        c_val.font      = _font(size=10)
        c_val.alignment = _align("left", "center", wrap=True)
        c_val.border    = _border(left="thin", right="thin", top="thin", bottom="thin")
        for col in range(4, COL_LAST):
            ws.cell(r, col).border = _border(
                top="thin", bottom="thin",
                right="thin" if col == COL_LAST - 1 else None,
            )

        ws.cell(r, COL_LAST).border = _border(right="thin")

    # linha 20 — fechar caixa
    for col in range(COL_FIRST, COL_LAST + 1):
        ws.cell(20, col).border = _border(
            left="thin"  if col == COL_FIRST else None,
            right="thin" if col == COL_LAST  else None,
            bottom="thin",
        )


# ---------------------------------------------------------------------------
# Aba Requisitos — fiel ao template
# ---------------------------------------------------------------------------
def _aba_requisitos(wb: Workbook, dados: dict) -> None:
    ws = wb.create_sheet("Requisitos")

    # --- Larguras de coluna ---
    ws.column_dimensions["A"].width = 9.66
    ws.column_dimensions["B"].width = 37.55
    ws.column_dimensions["C"].width = 25.66
    ws.column_dimensions["D"].width = 7.89
    ws.column_dimensions["E"].width = 46.66
    ws.column_dimensions["F"].width = 12.89
    ws.column_dimensions["G"].width = 13.66
    ws.column_dimensions["H"].width = 14.55
    ws.column_dimensions["I"].width = 28.0
    ws.column_dimensions["J"].width = 13.89
    ws.column_dimensions["K"].width = 9.66
    ws.column_dimensions["L"].width = 8.66

    # --- Altura fixa de linhas de dados ---
    ws.row_dimensions[1].height  = 18.75
    ws.row_dimensions[2].height  = 45.0

    # ------------------------------------------------------------------ #
    # LINHA 1 — título (A1:J1)
    # ------------------------------------------------------------------ #
    ws.merge_cells("A1:J1")
    c = ws["A1"]
    c.value     = "Requisitos Funcionais / Migração / Treinamento"
    c.font      = _font(bold=True, size=11, color=RGB_WHITE)
    c.fill      = _fill(RGB_DARK_BLUE)
    c.alignment = _align("center")
    c.border    = _border(left="thin", right="thin", top="thin", bottom="thin")
    for col in range(2, 11):
        ws.cell(1, col).fill   = _fill(RGB_DARK_BLUE)
        ws.cell(1, col).border = _border(
            top="thin", bottom="thin",
            right="thin" if col == 10 else None,
        )

    # ------------------------------------------------------------------ #
    # LINHA 2 — cabeçalhos das colunas
    # ------------------------------------------------------------------ #
    headers = [
        (1,  "Item RDM"),
        (2,  "Funcionalidade"),
        (3,  "Requisito"),
        (4,  "Tipo"),
        (5,  "Descrição da Funcionalidade"),
        (6,  "Engenharia de\n Requisitos \n(40%)"),
        (7,  "Implementação \n(75%)"),
        (8,  "Teste \n(20%)"),
        (9,  "Cientista \nde Dados \n(10%)"),
        (10, "Total Horas"),
    ]
    for col, txt in headers:
        c = ws.cell(2, col, value=txt)
        c.font      = _font(bold=False, size=10, color=RGB_WHITE)
        c.fill      = _fill(RGB_HEADER_BG)
        c.alignment = _align("center", "center", wrap=True)
        c.border    = _border(left="thin", right="thin", top="thin", bottom="thin")

    # ------------------------------------------------------------------ #
    # LINHAS DE DADOS (3..25) — 23 linhas
    # ------------------------------------------------------------------ #
    itens        = dados.get("itens", [])
    DATA_START   = 3
    MAX_ROWS     = 23     # linhas 3..25

    for i in range(MAX_ROWS):
        row = DATA_START + i
        ws.row_dimensions[row].height = 14.4 if i < 8 else 15.75

        if i < len(itens):
            item  = itens[i]
            eng   = float(item.get("eng_req", 0))
            impl  = float(item.get("impl",    0))
            teste = float(item.get("teste",   0))
            ds    = float(item.get("ds",      0))

            def _set_text(col, val, halign="left"):
                c = ws.cell(row, col, value=val)
                c.font      = _font(size=10)
                c.alignment = _align(halign, "center", wrap=True)
                c.border    = _border()  # sem borda (fiel ao template)

            def _set_h(col, horas, halign="center"):
                c = ws.cell(row, col, value=_h_to_td(horas))
                c.number_format = "[h]:mm"
                c.font          = _font(size=10)
                c.alignment     = _align(halign, "center")
                c.border        = _border()

            _set_text(1, str(item.get("item_rdm", str(i + 1))), "center")
            _set_text(2, item.get("funcionalidade", ""),         "left")
            _set_text(3, item.get("requisito", ""),              "general")
            _set_text(4, item.get("tipo", "Melhoria"),           "center")
            _set_text(5, item.get("descricao", ""),              "left")
            _set_h(6, eng);  _set_h(7, impl);  _set_h(8, teste);  _set_h(9, ds)

            # coluna J — Total (formula + fill accent1)
            c = ws.cell(row, 10, value=f"=SUM(F{row}:I{row})")
            c.number_format = "[h]:mm"
            c.font          = _font(size=10)
            c.fill          = _fill(RGB_HEADER_BG)
            c.alignment     = _align("center", "center")
            c.border        = _border()
        else:
            # linha vazia
            for col in range(1, 10):
                c = ws.cell(row, col, value=timedelta(0) if col >= 6 else None)
                if col >= 6:
                    c.number_format = "[h]:mm"
                c.font      = _font(size=10)
                c.alignment = _align("center", "center")
                c.border    = _border()

            c = ws.cell(row, 10, value=f"=SUM(F{row}:I{row})")
            c.number_format = "[h]:mm"
            c.font          = _font(size=10)
            c.fill          = _fill(RGB_HEADER_BG)
            c.alignment     = _align("center", "center")
            c.border        = _border()

    # ------------------------------------------------------------------ #
    # LINHA 26 — Total de horas  (fill accent1, fonte branca, bold)
    # ------------------------------------------------------------------ #
    ROW_TOT  = DATA_START + MAX_ROWS    # = 26
    ROW_DIST = ROW_TOT + 1             # = 27
    ROW_HOMO = ROW_DIST + 1            # = 28
    ROW_IMPL = ROW_HOMO + 1            # = 29
    ROW_GRAL = ROW_IMPL + 1            # = 30

    ws.row_dimensions[ROW_TOT].height  = 15.75
    ws.row_dimensions[ROW_DIST].height = 15.75
    ws.row_dimensions[ROW_HOMO].height = 15.75
    ws.row_dimensions[ROW_IMPL].height = 15.75
    ws.row_dimensions[ROW_GRAL].height = 15.75

    # A..D row 26 — com bordas thin (template mostra toda a linha com borda)
    for col in range(1, 6):
        c = ws.cell(ROW_TOT, col)
        c.fill   = _fill(RGB_HEADER_BG)
        c.border = _border(left="thin", right="thin", top="thin", bottom="thin")

    c_lbl = ws.cell(ROW_TOT, 5, value="Total de horas:")
    c_lbl.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c_lbl.fill      = _fill(RGB_HEADER_BG)
    c_lbl.alignment = _align("right")
    c_lbl.border    = _border(left="thin", right="thin", top="thin", bottom="thin")

    for col_idx, col_l in [(6,"F"), (7,"G"), (8,"H"), (9,"I")]:
        c = ws.cell(ROW_TOT, col_idx,
                    value=f"=SUM({col_l}{DATA_START}:{col_l}{DATA_START+MAX_ROWS-1})")
        c.number_format = "[h]:mm"
        c.font          = _font(bold=True, size=10, color=RGB_WHITE)
        c.fill          = _fill(RGB_HEADER_BG)
        c.alignment     = _align("center")
        c.border        = _border(left="thin", right="thin", top="thin", bottom="thin")

    c = ws.cell(ROW_TOT, 10,
                value=f"=SUM(J{DATA_START}:J{DATA_START+MAX_ROWS-1})")
    c.number_format = "[h]:mm"
    c.font          = _font(bold=True, size=10, color=RGB_WHITE)
    c.fill          = _fill(RGB_HEADER_BG)
    c.alignment     = _align("center")
    c.border        = _border(left="thin", right="thin", top="thin", bottom="thin")

    # ------------------------------------------------------------------ #
    # LINHA 27 — Distribuição das horas  (fill dark blue, fonte branca)
    # ------------------------------------------------------------------ #
    for col in range(1, 6):
        c = ws.cell(ROW_DIST, col)
        c.fill   = _fill(RGB_DARK_BLUE)
        c.border = _border(left="thin" if col == 1 else None,
                           right="thin" if col == 5 else None)

    c_lbl = ws.cell(ROW_DIST, 5, value="Distribuição das horas:")
    c_lbl.font      = _font(bold=True, size=11, color=RGB_WHITE)
    c_lbl.fill      = _fill(RGB_DARK_BLUE)
    c_lbl.alignment = _align("right")

    for col_idx, col_l in [(6,"F"), (7,"G"), (8,"H"), (9,"I"), (10,"J")]:
        c = ws.cell(ROW_DIST, col_idx,
                    value=f"={col_l}{ROW_TOT}/$J{ROW_TOT}")
        c.number_format = "0.00%"
        c.font          = _font(bold=True, size=10, color=RGB_WHITE)
        c.fill          = _fill(RGB_DARK_BLUE)
        c.alignment     = _align("center")

    # ------------------------------------------------------------------ #
    # LINHA 28 — Homologação (15%)  (fill accent1)
    # ------------------------------------------------------------------ #
    homo_horas = float(dados.get("homologacao_horas", 0))

    for col in range(1, 9):
        c = ws.cell(ROW_HOMO, col)
        c.fill   = _fill(RGB_HEADER_BG)
        c.border = _border(left="thin" if col == 1 else None,
                           top="thin", bottom="thin",
                           right=None)

    c_lbl = ws.cell(ROW_HOMO, 9, value="Homologação (15%)")
    c_lbl.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c_lbl.fill      = _fill(RGB_HEADER_BG)
    c_lbl.alignment = _align("right")
    c_lbl.border    = _border(left="thin", right="thin", top="thin", bottom="thin")

    c_val = ws.cell(ROW_HOMO, 10, value=_h_to_td(homo_horas))
    c_val.number_format = "[h]:mm"
    c_val.font          = _font(bold=False, size=10, color=RGB_WHITE)
    c_val.fill          = _fill(RGB_HEADER_BG)
    c_val.alignment     = _align("center")
    c_val.border        = _border(top="thin", bottom="thin")

    # ------------------------------------------------------------------ #
    # LINHA 29 — Implantação (10%)  (fill accent1)
    # ------------------------------------------------------------------ #
    impl_horas = float(dados.get("implantacao_horas", 0))

    for col in range(1, 9):
        c = ws.cell(ROW_IMPL, col)
        c.fill   = _fill(RGB_HEADER_BG)
        c.border = _border(left="thin" if col == 1 else None,
                           top="thin", bottom="thin")

    c_lbl = ws.cell(ROW_IMPL, 9, value="Implantação (10%)")
    c_lbl.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c_lbl.fill      = _fill(RGB_HEADER_BG)
    c_lbl.alignment = _align("right")
    c_lbl.border    = _border(left="thin", right="thin", top="thin", bottom="thin")

    c_val = ws.cell(ROW_IMPL, 10, value=_h_to_td(impl_horas))
    c_val.number_format = "[h]:mm"
    c_val.font          = _font(bold=False, size=10, color=RGB_WHITE)
    c_val.fill          = _fill(RGB_HEADER_BG)
    c_val.alignment     = _align("center")
    c_val.border        = _border(top="thin", bottom="thin")

    # ------------------------------------------------------------------ #
    # LINHA 30 — Total em Horas da Estimativa  (fill dark blue)
    # ------------------------------------------------------------------ #
    for col in range(1, 9):
        c = ws.cell(ROW_GRAL, col)
        c.fill   = _fill(RGB_DARK_BLUE)
        c.border = _border(left="thin" if col == 1 else None,
                           bottom="thin")

    c_lbl = ws.cell(ROW_GRAL, 9, value="Total em Horas da Estimativa")
    c_lbl.font      = _font(bold=True, size=10, color=RGB_WHITE)
    c_lbl.fill      = _fill(RGB_DARK_BLUE)
    c_lbl.alignment = _align("right")
    c_lbl.border    = _border(left="thin", top="thin", bottom="thin")

    c_val = ws.cell(ROW_GRAL, 10,
                    value=f"=SUM(J{ROW_TOT},J{ROW_HOMO},J{ROW_IMPL})")
    c_val.number_format = "[h]:mm"
    c_val.font          = _font(bold=True, size=10, color=RGB_WHITE)
    c_val.fill          = _fill(RGB_DARK_BLUE)
    c_val.alignment     = _align("center")
    c_val.border        = _border(left="thin", right="thin", top="thin", bottom="thin")

    # Congelar após cabeçalho
    ws.freeze_panes = "A3"


# ---------------------------------------------------------------------------
# Função principal de geração
# ---------------------------------------------------------------------------
def gerar_planilha(dados: dict, caminho_saida: str) -> str:
    wb = Workbook()
    wb.remove(wb.active)   # remove aba default

    # Localiza o logo ICI junto ao próprio script
    script_dir = Path(__file__).resolve().parent
    logo_path  = str(script_dir / "logo_ici.png")

    _aba_instrucoes(wb)
    _aba_identificacao(wb, dados, logo_path)
    _aba_requisitos(wb, dados)

    wb.active = wb["Requisitos"]

    caminho = Path(caminho_saida).resolve()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(caminho))
    return str(caminho)


# ---------------------------------------------------------------------------
# Modo interativo
# ---------------------------------------------------------------------------
def _input_float(prompt: str, default: float = 0.0) -> float:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return float(raw.replace(",", "."))
    except ValueError:
        print(f"  Valor inválido, usando {default}")
        return default


def modo_interativo() -> dict:
    print("\n=== Gerador de Planilha Bottom-Up (modo interativo) ===\n")
    dados = {}
    dados["cliente"]         = input("Cliente: ").strip()
    dados["orgao"]           = input("Órgão: ").strip()
    dados["sistema"]         = input("Sistema [Sigesguarda Pro]: ").strip() or "Sigesguarda Pro"
    dados["requisicao"]      = input("Requisição/Ofício (nº do chamado): ").strip()
    dados["sgc"]             = input("Identificador SGC (ou vazio): ").strip()
    dados["analista"]        = input("Analista Responsável: ").strip()
    dados["tecnologia"]      = input("Tecnologia [DotNet]: ").strip() or "DotNet"
    dados["data_estimativa"] = input(f"Data [{date.today().strftime('%d/%m/%Y')}]: ").strip() \
                               or date.today().strftime("%d/%m/%Y")
    dados["escopo"]          = input("Escopo da Estimativa: ").strip()
    dados["material_apoio"]  = input("Material de Apoio: ").strip()

    itens = []
    print("\n--- Itens (Enter sem digitar para encerrar) ---")
    i = 1
    while True:
        print(f"\n  Item {i}:")
        rdm  = input(f"    Item RDM [{i}]: ").strip() or str(i)
        func = input("    Funcionalidade: ").strip()
        if not func:
            break
        req  = input("    Requisito: ").strip()
        tipo = input("    Tipo [Melhoria/Novo]: ").strip() or "Melhoria"
        desc = input("    Descrição: ").strip()
        eng  = _input_float("    Eng. Requisitos (h)", 0)
        impl = _input_float("    Implementação (h)", 0)
        test = _input_float("    Teste (h)", 0)
        ds   = _input_float("    Cientista de Dados (h)", 0)
        itens.append({"item_rdm": rdm, "funcionalidade": func, "requisito": req,
                      "tipo": tipo, "descricao": desc,
                      "eng_req": eng, "impl": impl, "teste": test, "ds": ds})
        i += 1

    dados["itens"] = itens
    subtotal = sum(float(it.get("eng_req", 0)) + float(it.get("impl", 0)) +
                   float(it.get("teste", 0)) + float(it.get("ds", 0)) for it in itens)

    homo = input("\nHomologação assistida? (s/N): ").strip().lower() in ("s", "sim")
    dados["homologacao_horas"] = math.ceil(subtotal * 0.15 * 2) / 2 if homo else 0.0
    dados["implantacao_horas"] = 0.0
    print(f"\n  Subtotal: {subtotal}h | Homo: {dados['homologacao_horas']}h | "
          f"Total: {subtotal + dados['homologacao_horas']}h")
    return dados


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Gera planilha XLSX de estimativa Bottom-Up")
    parser.add_argument("--dados",      "-d", help="JSON com dados da estimativa")
    parser.add_argument("--saida",      "-o", help="Caminho de saída do XLSX")
    parser.add_argument("--interativo", "-i", action="store_true",
                        help="Entrada via terminal")
    args = parser.parse_args()

    if args.interativo:
        dados = modo_interativo()
    elif args.dados:
        with open(args.dados, encoding="utf-8") as f:
            dados = json.load(f)
    else:
        parser.print_help()
        print("\nERRO: use --dados <arquivo.json> ou --interativo")
        sys.exit(1)

    if args.saida:
        saida = args.saida
    else:
        req      = dados.get("requisicao", "sem-numero").replace("/", "-").replace(" ", "-")
        raiz     = Path(__file__).resolve().parent
        for _ in range(6):
            raiz = raiz.parent
            if (raiz / "estimativas-bottom-up").exists() or (raiz / ".git").exists():
                break
        saida = str(raiz / "estimativas-bottom-up" / f"Estimativa_{req}.xlsx")

    caminho = gerar_planilha(dados, saida)
    print(f"\nPlanilha gerada: {caminho}")


if __name__ == "__main__":
    main()
