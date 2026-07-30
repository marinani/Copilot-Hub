import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.lib.colors import HexColor

_FONTS_REGISTERED = False
def _ensure_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED: return
    fd = r'C:\Windows\Fonts'
    for nome, f in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf'),('Arial-BoldItalic','arialbi.ttf')]:
        p = os.path.join(fd, f)
        if os.path.exists(p): registerFont(TTFont(nome, p))
    for n,b,i,fn in [('Arial',0,0,'Arial'),('Arial',1,0,'Arial-Bold'),('Arial',0,1,'Arial-Italic'),('Arial',1,1,'Arial-BoldItalic')]:
        addMapping(n,b,i,fn)
    _FONTS_REGISTERED = True

_ensure_fonts()
pw, ph = A4
frame_w = pw - 5*cm
AZUL = HexColor('#4472C4')

def make_cell(text, italic=False, bold=False, size=8, align=0, pad_top=2, pad_bot=2):
    r = str(text).replace('\n','<br/>') if text else ' '
    key = f'{size}_{align}'
    style = ParagraphStyle(key, fontName='Arial', fontSize=size, leading=size*1.35, alignment=align, spaceBefore=1, spaceAfter=1)
    return Paragraph(r, style)

def make_th(text,size=8):
    return make_cell(text,bold=True,size=size)

def azul_style():
    return TableStyle([('BACKGROUND',(0,0),(-1,0),AZUL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.5,colors.black),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)])

for label, pt in [('BEFORE (pad=10)', 10), ('AFTER (pad=30)', 30)]:
    doc = BaseDocTemplate(f'C:/Projetos/git/DEVOPS/copilot/RDMs/test_{pt}.pdf', pagesize=A4)
    f = Frame(2.5*cm, 2.5*cm, frame_w, ph-5*cm, id='main')
    doc.addPageTemplates([PageTemplate(id='M', frames=[f])])
    story = []
    story.append(Paragraph(f'APPROVAL TABLE (pad_top=pad_bot={pt})', ParagraphStyle('H', fontName='Arial-Bold', fontSize=12)))
    story.append(Spacer(1, 1*cm))
    aprov = [[make_th('Name'), make_th('Department'), make_th('Date'), make_th('Signature')]]
    for _ in range(6):
        aprov.append([make_cell('', size=8, pad_top=pt, pad_bot=pt)] * 4)
    t = Table(aprov, colWidths=[frame_w*0.28, frame_w*0.24, frame_w*0.18, frame_w*0.30])
    t.setStyle(azul_style())
    story.append(t)
    doc.build(story)
    sz = os.path.getsize(f'C:/Projetos/git/DEVOPS/copilot/RDMs/test_{pt}.pdf')
    print(f'{label}: {sz} bytes')

sz10 = os.path.getsize('C:/Projetos/git/DEVOPS/copilot/RDMs/test_10.pdf')
sz30 = os.path.getsize('C:/Projetos/git/DEVOPS/copilot/RDMs/test_30.pdf')
print(f'\nDifference: {sz30 - sz10} bytes more (pad=30 is larger than pad=10)')

# Cleanup
os.remove('C:/Projetos/git/DEVOPS/copilot/RDMs/test_10.pdf')
os.remove('C:/Projetos/git/DEVOPS/copilot/RDMs/test_30.pdf')
