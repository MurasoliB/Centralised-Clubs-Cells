with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    text = f.read()

helpers = '''def add_para(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_before=0, space_after=6, line_spacing=1.5):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = COLOR_BLACK
        return p

    def add_ch_title(ch_num, ch_title, add_break=True):
        if add_break:
            doc.add_page_break()
        p1 = add_para(f"CHAPTER {ch_num}", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=18, space_after=4, line_spacing=1.15)
        p2 = add_para(ch_title, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=18, line_spacing=1.15)
        return p2

    def add_sec_heading(sec_num, sec_title):
        return add_para(f"{sec_num}   {sec_title}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=14, space_after=6, line_spacing=1.15)

    def add_subsec_heading(subsec_num, subsec_title):
        return add_para(f"{subsec_num}   {subsec_title}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=10, space_after=4, line_spacing=1.15)

    def add_bullet(txt):
        p = add_para(f"•   {txt}", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=1, space_after=3)
        p.paragraph_format.left_indent = Inches(0.25)
        return p

    '''

# Replace from def add_para to def add_table_title
start_idx = text.find("def add_para")
end_idx = text.find("def add_table_title")

text = text[:start_idx] + helpers + text[end_idx:]

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Restored all helpers with JUSTIFIED alignment!")
