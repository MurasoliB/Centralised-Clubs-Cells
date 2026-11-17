import re

with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update add_para to default to JUSTIFY alignment
old_add_para = code[code.find("def add_para"):code.find("def add_bullet")]
new_add_para = '''def add_para(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_before=0, space_after=6, line_spacing=1.5):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = COLOR_BLACK
        return p

    '''

code = code.replace(old_add_para, new_add_para, 1)

# 2. Add Section Break before CHAPTER 1: INTRODUCTION
ch1_target = '# =========================================================================\n    # CHAPTER 1: INTRODUCTION\n    # ========================================================================='
ch1_replacement = '''# =========================================================================
    # CHAPTER 1: INTRODUCTION (New Section with Page Number Restart at 1)
    # =========================================================================
    s2 = doc.add_section(docx.enum.section.WD_SECTION_START.NEW_PAGE)
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(1.25)
    s2.right_margin = Inches(1.0)
    s2.page_width = Inches(8.27)
    s2.page_height = Inches(11.69)
    s2.header.is_linked_to_previous = False
    s2.footer.is_linked_to_previous = False

    sectPr2 = s2._sectPr
    pgNumType2 = sectPr2.find(qn('w:pgNumType'))
    if pgNumType2 is not None:
        sectPr2.remove(pgNumType2)
    sectPr2.append(parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1"/>'))

    footer2 = s2.footer
    f_p = footer2.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_p.paragraph_format.space_before = Pt(0)
    f_p.paragraph_format.space_after = Pt(0)
    f_run = f_p.add_run()
    f_run.font.name = "Times New Roman"
    f_run.font.size = Pt(11)
    f_p._p.append(parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>'))
'''

code = code.replace(ch1_target, ch1_replacement, 1)

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated add_para and added Section 2 with page number restart!")
