#!/usr/bin/env python3
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer
from reportlab.platypus import Image as RLImage, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.lib.colors import HexColor

# ---------------------------------------------------------------------------
# Arial TrueType Font
# ---------------------------------------------------------------------------
_FONTS_REGISTERED = False

def _ensure_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    fd = r'C:\Windows\Fonts'
    font_map = {
        'Arial': (fd, 'arial.ttf'),
        'Arial-Bold': (fd, 'arialbd.ttf'),
        'Arial-Italic': (fd, 'ariali.ttf'),
        'Arial-BoldItalic': (fd, 'arialbi.ttf'),
    }
    for nome, (d, f) in font_map.items():
        p = os.path.join(d, f)
        if os.path.exists(p):
            registerFont(TTFont(nome, p))
    addMapping('Arial', 0, 0, 'Arial')
    addMapping('Arial', 1, 0, 'Arial-Bold')
    addMapping('Arial', 0, 1, 'Arial-Italic')
    addMapping('Arial', 1, 1, 'Arial-BoldItalic')
    _FONTS_REGISTERED = True

# ---------------------------------------------------------------------------
# Canvas with page numbering at the TOP
# ---------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for idx, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self._draw_footer_and_page(idx, total)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_footer_and_page(self, idx, total):
        pw, ph = A4
        # idx 0 = cover, idx 1 = TOC (SUMÁRIO), idx >= 2 = content pages
        internal = idx >= 1
        show_page_num = idx >= 2

        # Page number visible only from IDENTIFICAÇÃO onwards
        # Count starts at TOC (page 1), so content starts at page 2
        if show_page_num:
            num = idx  # TOC = page 1, IDENTIFICAÇÃO = page 2, ...
            ttl = total - 1  # exclude cover
            self.setFont("Arial", 8)
            self.drawRightString(pw - 2.5*cm, ph - 1.2*cm, f"Página {num} de {ttl}")

        # Institutional footer (internal pages only)
        if internal:
            self.saveState()
            self.setFont('Arial', 6.5)
            self.setFillColor(HexColor('#555555'))
            parts = [
                "Todos os direitos autorais do conteúdo deste documento pertencem ao Instituto Curitiba de Informática, não podendo ser",
                "reproduzido ou divulgado, no todo ou em parte, ou utilizado para fins diferentes daqueles para os quais é fornecido, sem prévia",
                "e expressa autorização do Instituto Curitiba de Informática.",
            ]
            y0 = 1.5*cm
            for i, part in enumerate(parts):
                self.drawCentredString(pw / 2.0, y0 - i*0.35*cm, part)
            self.restoreState()

# ---------------------------------------------------------------------------
# Page templates
# ---------------------------------------------------------------------------
class IcyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, skill_dir, **kw):
        super().__init__(filename, pagesize=A4, **kw)
        self.skill_dir = skill_dir

    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText().strip()
            style = flowable.style.name
            if style == 'H1' and text not in ('SUMÁRIO',):
                # Subtract 1 to align with our numbering (cover excluded, TOC = page 1)
                toc_page = self.page - 1
                self.notify('TOCEntry', (0, text, toc_page))

def _find_asset(skill_dir, filename):
    """Search the skill's assets directory for a file."""
    candidates = [
        os.path.join(skill_dir, 'assets', filename),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def draw_cover_bg(c, doc):
    bg = _find_asset(doc.skill_dir, 'timbre_1.jpg')
    if bg:
        p = A4
        c.drawImage(bg, 0, 0, width=p[0], height=p[1])

def draw_internal_bg(c, doc):
    bg = _find_asset(doc.skill_dir, 'timbre_2.jpg')
    if bg:
        p = A4
        c.drawImage(bg, 0, 0, width=p[0], height=p[1])

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
_styles = {}

def fmt(text, italic=False, bold=False):
    if not text:
        return ""
    r = str(text).replace('\n', '<br/>')
    if italic: r = f"<i>{r}</i>"
    if bold: r = f"<b>{r}</b>"
    return r

def make_cell(text, italic=False, bold=False, size=8, align=0, pad_top=2, pad_bot=2):
    content = fmt(text, italic=italic, bold=bold)
    if not content:
        content = " "
    key = f"C{size}_{align}"
    if key not in _styles:
        _styles[key] = ParagraphStyle(
            key, fontName='Arial', fontSize=size,
            leading=size * 1.35, alignment=align,
            spaceBefore=1, spaceAfter=1,
        )
    return Paragraph(content, _styles[key])

def make_th(text, size=8):
    return make_cell(text, bold=True, size=size)

AZUL = HexColor('#4472C4')
CINZA = HexColor('#D9D9D9')

def azul_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ])

def cinza_label_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), CINZA),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])

def table_grid():
    return TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ])

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_ici_pdf.py <data.json> <output.pdf> <skill_dir>")
        sys.exit(1)

    json_path, output_path, skill_dir = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)

    _ensure_fonts()

    global _styles
    _styles['H1'] = ParagraphStyle('H1', fontName='Arial-Bold', fontSize=12, leading=16, spaceBefore=10, spaceAfter=6)
    _styles['H2'] = ParagraphStyle('H2', fontName='Arial-Bold', fontSize=10, leading=14, spaceBefore=8, spaceAfter=4)
    _styles['Normal'] = ParagraphStyle('Normal', fontName='Arial', fontSize=9, leading=13, spaceBefore=2, spaceAfter=2, alignment=4)
    _styles['Body'] = ParagraphStyle('Body', fontName='Arial', fontSize=9, leading=13, spaceBefore=2, spaceAfter=2, alignment=4)
    _styles['TOCEntry'] = ParagraphStyle('TOCEntry', fontName='Arial-Bold', fontSize=10, leading=15, leftIndent=0, spaceBefore=2, spaceAfter=2)

    H1, H2, N, B = _styles['H1'], _styles['H2'], _styles['Normal'], _styles['Body']

    doc = IcyDocTemplate(output_path, skill_dir)
    pw, ph = A4
    frame_w = pw - 5*cm

    f_cover = Frame(2.5*cm, 2.5*cm, frame_w, ph - 5*cm, id='cover')
    f_internal = Frame(2.5*cm, 2.5*cm, frame_w, ph - 5*cm, id='internal')

    cover_tpl = PageTemplate(id='Cover', frames=[f_cover], onPage=draw_cover_bg)
    internal_tpl = PageTemplate(id='Internal', frames=[f_internal], onPage=draw_internal_bg)
    doc.addPageTemplates([cover_tpl, internal_tpl])

    story = []

    # ======================================================================
    # 1. COVER PAGE
    # ======================================================================
    logo_path = _find_asset(skill_dir, 'ici_logo.png')
    logo = RLImage(logo_path, width=3.2*cm, height=3.2*cm) if logo_path else Spacer(1, 3.2*cm)

    dc = data.get('data_criacao', '')
    nc = data.get('numero_chamado', '')
    asst = data.get('assunto', '')
    elab = data.get('elaboracao', '')
    ver = data.get('versao', '1.0')

    # Identification table (right side)
    fw_right = frame_w - 3.2*cm - 0.4*cm
    cover_right = Table([
        [make_cell(f"<b>Data Criação:</b>  {dc}", size=7)],
        [make_cell(f"<b>Nº Chamado/Ofício:</b>  {nc}", size=7)],
        [make_cell(f"<b>Assunto:</b><br/>{asst}", bold=True, italic=True, size=7)],
        [make_cell(f"<b>Elaborado por:</b>  {elab}<br/><b>Versão:</b>  {ver}", size=7)],
    ], colWidths=[fw_right])
    cover_right.setStyle(table_grid())

    topo = Table([
        [logo, Spacer(0.4*cm, 0.1*cm), cover_right]
    ], colWidths=[3.2*cm, 0.4*cm, fw_right])
    topo.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(topo)
    story.append(Spacer(1, 1.5*cm))

    # Approvals
    story.append(Paragraph("<b>APROVAÇÕES</b>", N))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Este documento requer as seguintes aprovações, indicando o aceite da solução proposta, esforço e demais condições apresentadas nesta requisição de mudança.", B))
    story.append(Spacer(1, 0.5*cm))

    ap_w = frame_w
    aprov = [[
        make_th('Nome', size=8),
        make_th('Setor', size=8),
        make_th('Data', size=8),
        make_th('Assinatura', size=8),
    ]]
    for _ in range(6):
        aprov.append([
            make_cell('', size=8),
            make_cell('', size=8),
            make_cell('', size=8),
            make_cell('', size=8),
        ])
    t_aprov = Table(aprov, colWidths=[ap_w*0.28, ap_w*0.24, ap_w*0.18, ap_w*0.30])
    t_aprov.setStyle(azul_style())
    t_aprov.setStyle(TableStyle([
        ('TOPPADDING', (0, 1), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 15),
    ]))
    story.append(t_aprov)

    # ======================================================================
    # 2. TABLE OF CONTENTS (automatic TOC)
    # ======================================================================
    story.append(PageBreak())
    story.append(Paragraph("SUMÁRIO", H1))
    story.append(Spacer(1, 0.5*cm))

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle('TOC1', fontName='Arial-Bold', fontSize=10, leading=14,
                        leftIndent=0, spaceBefore=0, spaceAfter=0),
    ]
    story.append(toc)

    # ======================================================================
    # 3. CONTENT
    # ======================================================================
    story.append(PageBreak())

    # 1 - IDENTIFICATION
    story.append(Paragraph("1  IDENTIFICAÇÃO", H1))
    ident = [
        [make_th("Nº Chamado/Ofício:"), make_cell(data.get('numero_chamado', ''), italic=True)],
        [make_th("Serviço:"), make_cell(data.get('servico', ''), italic=True)],
        [make_th("Solicitado por:"), make_cell(data.get('solicitante', ''), italic=True)],
        [make_th("Órgão:"), make_cell(data.get('orgao', ''), italic=True)],
    ]
    t_ident = Table(ident, colWidths=[4.5*cm, frame_w - 4.5*cm])
    t_ident.setStyle(cinza_label_style())
    story.append(t_ident)
    story.append(Spacer(1, 0.3*cm))

    # 2 - SUMMARY
    story.append(Paragraph("2  RESUMO DA SOLICITAÇÃO", H1))
    story.append(Paragraph(fmt(data.get('resumo', 'Não preenchido.'), italic=True), B))
    story.append(Spacer(1, 0.2*cm))

    # 3 - SOLUTION
    story.append(Paragraph("3  SOLUÇÃO PROPOSTA", H1))
    story.append(Paragraph(fmt(data.get('solucao', 'Não preenchido.'), italic=True), B))
    story.append(Spacer(1, 0.2*cm))

    # 4 - FUNCIONALIDADES
    story.append(Paragraph("4  FUNCIONALIDADES", H1))
    story.append(Paragraph(
        "Descrição das funcionalidades incluídas, modificadas e removidas nesta requisição:", B))
    story.append(Spacer(1, 0.2*cm))

    funcs = data.get('funcionalidades', [])
    frows = [[make_th("ID da Func.", size=8), make_th("Nome da Funcionalidade", size=8)]]
    if not funcs:
        frows.append([make_cell(''), make_cell('')])
    else:
        for i, f in enumerate(funcs, 1):
            frows.append([
                make_cell(str(i), italic=True),
                make_cell(f.get('nome', ''), italic=True),
            ])
    t_func = Table(frows, colWidths=[2.5*cm, frame_w - 2.5*cm])
    t_func.setStyle(azul_style())
    story.append(t_func)
    story.append(Spacer(1, 0.4*cm))

    for idx, f in enumerate(funcs, 1):
        story.append(Paragraph(fmt(f"{idx}. {f.get('nome', '')}", bold=True), H2))
        story.append(Paragraph(fmt(f.get('descricao', ''), italic=True), B))
        story.append(Spacer(1, 0.2*cm))

    # 5 - TREINAMENTO
    story.append(Paragraph("5  TREINAMENTO", H1))
    story.append(Paragraph(fmt(data.get('treinamento', 'Não aplicável.'), italic=True), B))
    story.append(Spacer(1, 0.2*cm))

    # 6 - ESCOPO NÃO INCLUÍDO
    story.append(Paragraph("6  ESCOPO NÃO INCLUÍDO", H1))
    story.append(Paragraph(fmt(data.get('escopo_nao_incluido', 'Não preenchido.'), italic=True), B))
    story.append(Spacer(1, 0.2*cm))

    # 7 - RISCOS
    story.append(Paragraph("7  RISCOS", H1))
    story.append(Paragraph(
        "<i>O quadro abaixo descreve os riscos identificados, respectivos impactos e as ações a serem tomadas para minimizar ou contornar o impacto.</i>", B))
    story.append(Spacer(1, 0.2*cm))

    riscos = data.get('riscos', [])
    rcw = frame_w / 3
    rrows = [[make_th("Descrição do Risco"), make_th("Impacto"), make_th("Resposta ao Risco")]]
    if not riscos:
        for _ in range(4):
            rrows.append([make_cell(''), make_cell(''), make_cell('')])
    else:
        for r in riscos:
            rrows.append([
                make_cell(r.get('descricao', ''), italic=True),
                make_cell(r.get('impacto', ''), italic=True),
                make_cell(r.get('resposta', ''), italic=True),
            ])
    t_riscos = Table(rrows, colWidths=[rcw, rcw, rcw])
    t_riscos.setStyle(azul_style())
    story.append(t_riscos)
    story.append(Spacer(1, 0.3*cm))

    # 8 - ESTIMATIVA EM HORAS
    story.append(Paragraph("8  ESTIMATIVA EM HORAS", H1))

    pf_val = data.get('pf', 0)
    prod_val = data.get('produtividade', 0)
    esf_val = data.get('esforco_horas', '00:00')
    ecw = frame_w / 3

    est1 = [
        [make_th("Pontos de Função"), make_th("Produtividade"), make_th("Esforço em horas")],
        [make_cell(f"{pf_val} PF", italic=True), make_cell(f"{prod_val} H/PF", italic=True), make_cell(str(esf_val), italic=True)],
    ]
    t_est1 = Table(est1, colWidths=[ecw, ecw, ecw])
    t_est1.setStyle(azul_style())
    story.append(t_est1)
    story.append(Spacer(1, 0.3*cm))

    #story.append(Paragraph("<i>* Para calcular o esforço em horas, multiplique o total de pontos de função pela produtividade.</i>", B))
    #story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "<i>A execução do serviço compreende as seguintes fases e seus respectivos esforços:</i>", B))
    story.append(Spacer(1, 0.2*cm))

    fases = data.get('fases', {})
    fcw1, fcw2 = frame_w * 0.62, frame_w * 0.38
    est2 = [
        [make_th("Fases do Serviço"), make_th("Esforço")],
        [make_cell("Engenharia de Requisitos (40%):", italic=True), make_cell(fases.get('engenharia_requisitos', '00:00'), italic=True)],
        [make_cell("Implementação (75%):", italic=True), make_cell(fases.get('implementacao', '00:00'), italic=True)],
        [make_cell("Teste (20%):", italic=True), make_cell(fases.get('teste', '00:00'), italic=True)],
        [make_cell("Homologação/Implantação (25%):", italic=True), make_cell(fases.get('homologacao', '00:00'), italic=True)],
        [make_cell("Arquitetura (40%):", italic=True), make_cell(fases.get('arquitetura', '00:00'), italic=True)],
        [make_cell("Cientista de Dados (10%):", italic=True), make_cell(fases.get('cientista_dados', '00:00'), italic=True)],
        [make_cell("Treinamento:", italic=True), make_cell(fases.get('treinamento', '00:00'), italic=True)],
        [make_cell("Esforço Total:", bold=True), make_cell(fases.get('total', esf_val), italic=True)],
    ]
    t_est2 = Table(est2, colWidths=[fcw1, fcw2])
    t_est2.setStyle(azul_style())
    t_est2.setStyle(TableStyle([
        ('BACKGROUND', (0, -1), (-1, -1), CINZA),
    ]))
    story.append(t_est2)

    # --- Generation (multiBuild = 2-pass, automatic TOC) ---
    doc.multiBuild(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {output_path}")

if __name__ == '__main__':
    main()
