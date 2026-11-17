import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

def generate_master_final_report():
    doc = docx.Document()
    COLOR_BLACK = RGBColor(0, 0, 0)

    # 1. Page Margins Setup: A4, Left 1.25", Top 1.0", Right 1.0", Bottom 1.0"
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(r'''
            <w:tcMar %s>
                <w:top w:w="%d" w:type="dxa"/>
                <w:bottom w:w="%d" w:type="dxa"/>
                <w:left w:w="%d" w:type="dxa"/>
                <w:right w:w="%d" w:type="dxa"/>
            </w:tcMar>
        ''' % (nsdecls('w'), top, bottom, left, right))
        tcPr.append(tcMar)

    # 100% COMPLETE VISIBLE BORDERS (for actual project data tables)
    def set_full_visible_borders(table, border_color="000000", border_sz="4"):
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(r'''
            <w:tblBorders %s>
                <w:top w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:bottom w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:left w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:right w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:insideH w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:insideV w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
            </w:tblBorders>
        ''' % (nsdecls('w'), border_sz, border_color, border_sz, border_color, 
               border_sz, border_color, border_sz, border_color, 
               border_sz, border_color, border_sz, border_color))
        tblPr.append(tblBorders)

    def add_para(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_before=0, space_after=6, line_spacing=1.5):
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

    def add_table_title(tbl_num, tbl_name):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r1 = p.add_run(f"Table {tbl_num}   ")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.font.bold = True
        r2 = p.add_run(tbl_name)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        return p

    def format_single_page_table(table, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_full_visible_borders(table, border_sz="4")
        num_rows = len(table.rows)
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            cantSplit = trPr.find(qn('w:cantSplit'))
            if cantSplit is None:
                trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            for c_idx, cell in enumerate(row.cells):
                if col_widths and c_idx < len(col_widths):
                    cell.width = col_widths[c_idx]
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.0
                    if r_idx < num_rows - 1:
                        p.paragraph_format.keep_with_next = True

    def add_clean_figure_space(fig_num_str, fig_caption_str, empty_lines=14):
        for _ in range(empty_lines):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run("")
            r.font.name = "Times New Roman"
        
        # Caption strictly below clean area
        fp = add_para(f"{fig_num_str} – {fig_caption_str}", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=6, space_after=16, line_spacing=1.15)
        return fp

    print("Step 1: Assembling Front Matter with Word Paragraphs (NO TABLES for TOC, LOT, LOF, LOA)...")

    # =========================================================================
    # FRONT MATTER: 1. TITLE PAGE
    # =========================================================================
    add_para("CENTRALISED CLUBS AND CELL MANAGEMENT SYSTEM FOR COLLEGES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=18, space_after=14, line_spacing=1.2)
    add_para("DESIGN THINKING LABORATORY REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=4, line_spacing=1.15)
    add_para("(24ITL34 – DESIGN THINKING LABORATORY)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=0, space_after=18, line_spacing=1.15)
    
    add_para("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_before=0, space_after=8, line_spacing=1.15)

    # Team Members Table (Section 9/10: Genuine Word Table with full borders)
    tm_table = doc.add_table(rows=6, cols=3)
    tm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(tm_table, border_sz="4")
    
    headers = ["S. No.", "Name", "Register Number"]
    col_w = [Inches(0.9), Inches(3.1), Inches(1.8)]
    for j, h in enumerate(headers):
        cell = tm_table.rows[0].cells[j]; cell.width = col_w[j]
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True

    tm_data = [
        ("1", "SAHANA S", "25ITR121"),
        ("2", "SARAN KARTHIK S", "25ITR128"),
        ("3", "SHARAN V", "25ITR134"),
        ("4", "VIGNESH M", "25ITR171"),
        ("5", "MURASOLI B", "25ITL188")
    ]
    for i, row in enumerate(tm_data):
        for j, val in enumerate(row):
            cell = tm_table.rows[i+1].cells[j]; cell.width = col_w[j]
            set_cell_margins(cell, top=60, bottom=60, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = (j == 1)

    add_para("in partial fulfilment of the requirements for the award of the degree of", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_before=16, space_after=4, line_spacing=1.15)
    add_para("BACHELOR OF TECHNOLOGY IN\nINFORMATION TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=0, space_after=14, line_spacing=1.15)
    add_para("DEPARTMENT OF INFORMATION TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=0, space_after=10, line_spacing=1.15)
    add_para("KONGU ENGINEERING COLLEGE\n(Autonomous)\nPERUNDURAI, ERODE – 638 060\nNOVEMBER 2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=12, space_after=0, line_spacing=1.2)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 2. BONAFIDE CERTIFICATE (Page ii)
    # =========================================================================
    add_para("DEPARTMENT OF INFORMATION TECHNOLOGY\nKONGU ENGINEERING COLLEGE, PERUNDURAI - 638060\n(Autonomous)\nNOVEMBER 2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=0, space_after=16, line_spacing=1.2)
    add_para("BONAFIDE CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=10, space_after=16, line_spacing=1.15)
    
    cert_text = (
        "This is to certify that the project report entitled CENTRALISED CLUBS AND CELL MANAGEMENT SYSTEM FOR COLLEGES "
        "is the bonafide record of project work done by SAHANA S (25ITR121), SARAN KARTHIK S (25ITR128), "
        "SHARAN V (25ITR134), VIGNESH M (25ITR171), and MURASOLI B (25ITL188) in the course 24ITL34 – Design Thinking Laboratory "
        "in partial fulfilment of the requirements for the award of the Degree of Bachelor of Technology in "
        "INFORMATION TECHNOLOGY of Anna University Chennai during the year 2026 – 2027."
    )
    add_para(cert_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=0, space_after=36, line_spacing=1.5)
    
    add_para("SUPERVISOR\t\t\t\t\tHEAD OF THE DEPARTMENT", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=20, space_after=4, line_spacing=1.15)
    add_para("(Signature with seal)\t\t\t\t\t(Signature with seal)", align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=True, size=11, space_before=0, space_after=24, line_spacing=1.15)
    add_para("Date:", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=0, space_after=30, line_spacing=1.15)
    add_para("Submitted for the end semester Design Thinking Laboratory examination held on ____________________", align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=11, space_before=0, space_after=36, line_spacing=1.15)
    add_para("EXAMINER - I\t\t\t\t\tEXAMINER - II", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=16, space_after=0, line_spacing=1.15)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 3. DECLARATION (Page iii)
    # =========================================================================
    add_para("DEPARTMENT OF INFORMATION TECHNOLOGY\nKONGU ENGINEERING COLLEGE, PERUNDURAI - 638060\n(Autonomous)\nNOVEMBER 2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=0, space_after=16, line_spacing=1.2)
    add_para("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=10, space_after=16, line_spacing=1.15)
    
    decl_text = (
        "We affirm that the project report entitled CENTRALISED CLUBS AND CELL MANAGEMENT SYSTEM FOR COLLEGES being submitted "
        "in partial fulfilment of the requirements for the award of Bachelor of Technology is the original work carried out by us. "
        "It has not formed part of any other project report or dissertation based on which a degree or award was conferred "
        "on an earlier occasion on this or any other candidate."
    )
    add_para(decl_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=0, space_after=30, line_spacing=1.5)
    
    add_para("Date:\t\t\t\t\t\tSAHANA S (25ITR121)", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=0, space_after=3, line_spacing=1.15)
    add_para("\t\t\t\t\t\tSARAN KARTHIK S (25ITR128)", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=0, space_after=3, line_spacing=1.15)
    add_para("\t\t\t\t\t\tSHARAN V (25ITR134)", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=0, space_after=3, line_spacing=1.15)
    add_para("\t\t\t\t\t\tVIGNESH M (25ITR171)", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=0, space_after=3, line_spacing=1.15)
    add_para("\t\t\t\t\t\tMURASOLI B (25ITL188)", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=0, space_after=30, line_spacing=1.15)

    add_para("I certify that the declaration made by the above candidates is true to the best of my knowledge.", align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=10, space_after=36, line_spacing=1.5)
    add_para("Date:\t\t\t\t\t\tName & Signature of Supervisor with seal", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=10, space_after=0, line_spacing=1.15)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 4. ABSTRACT (Page iv)
    # =========================================================================
    add_para("ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    abs_p1 = (
        "In modern higher education institutions, student extracurricular and co-curricular bodies—comprising technical societies, "
        "cultural troupes, hobby forums (Clubs), and statutory regulatory bodies such as the Institution's Innovation Council (IIC), "
        "Entrepreneurship Development Cell (EDC), Women Development Cell (WDC), and National Service Scheme (Cells)—are fundamental "
        "to holistic student development and mandatory institutional accreditations (NAAC, NBA, and NIRF). However, conventional "
        "campus operations rely on fragmented paper circulars, disconnected spreadsheets, unindexed WhatsApp broadcasts, and manual "
        "signatures. This decentralization causes communication blackouts, membership tracking failures, severe delays in academic "
        "On-Duty (OD) regularization, unverified achievement records, and labor-intensive manual consolidation during annual quality audits."
    )
    abs_p2 = (
        "This project applies the structured Design Thinking methodology of the 24ITL34 Design Thinking Laboratory course to "
        "conceive, architect, and prototype the Centralised Clubs and Cell Management System for Colleges (ClubHub). The institutional "
        "landscape was systematically explored through STEEP trend analysis, activity system mapping, and stakeholder interest-influence "
        "matrices; real user frustrations were uncovered through empathy maps, student/staff journey maps, and primary field interviews; "
        "and human-centered needs were defined using the SPICE framework and personas. Ideation through scenario storyboards led to the "
        "formulation of a high-performance web platform featuring a 4-tier role-governed hierarchy: Institutional Administrators, "
        "Faculty Advisors, Student Coordinators, and General Students. The working medium-fidelity prototype was built using React 18, "
        "TypeScript 5, Tailwind CSS, Vite, and a PostgreSQL-backed Supabase cloud infrastructure protected by Row-Level Security (RLS). "
        "The resulting system delivers a unified club discovery directory, one-click membership onboarding, quota-governed event RSVPs, "
        "instant roll-call attendance processing for automated On-Duty generation, verified digital portfolios, and one-click NAAC Criterion 5 "
        "compliance reporting, directly fulfilling United Nations Sustainable Development Goals (SDG 4, SDG 9, and SDG 16)."
    )
    add_para(abs_p1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=0, space_after=12, line_spacing=1.5)
    add_para(abs_p2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=0, space_after=0, line_spacing=1.5)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 5. ACKNOWLEDGEMENT (Page v)
    # =========================================================================
    add_para("ACKNOWLEDGEMENT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    ack_lines = [
        "First and foremost, we acknowledge the abundant grace and divine blessings of the Almighty throughout the different phases of this project and for its successful culmination.",
        "We express our sincere thanks and profound gratitude to Thiru. E.R.K. KRISHNAN, M.Com., our esteemed Correspondent, and all philanthropic trust members of the Kongu Vellalar Institute of Technology Trust (KVITT), who have continuously fostered our academic and innovation endeavors.",
        "We express our deep sense of gratitude to our respected Principal, Dr. R. PARAMESHWARAN, M.E., Ph.D., for providing state-of-the-art infrastructural facilities and academic resources that enabled us to complete this project.",
        "We express our heartfelt gratitude to Dr. S. VARADHAGANAPATHY, M.E., Ph.D., Senior Professor and Head of the Department, Department of Information Technology, for his constant encouragement, scholarly guidance, and visionary leadership.",
        "We are highly indebted to our project supervisor and course coordinator, Department of Information Technology, for invaluable technical guidance, meticulous review, constructive criticism, and steadfast supervision throughout the execution of this work.",
        "We sincerely thank all the Faculty Advisors, Student Club Office Bearers, and administrative coordinators across various departments of Kongu Engineering College who generously participated in our user interviews and shared real-world operational challenges.",
        "Finally, we extend our warmest gratitude to our beloved parents and friends for their enduring patience, moral encouragement, and selfless support throughout our studies."
    ]
    for line in ack_lines:
        add_para(line, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_before=0, space_after=10, line_spacing=1.5)

    doc.add_page_break()

    # =========================================================================
        # =========================================================================
    # FRONT MATTER: 6. TABLE OF CONTENTS (Exact 2-Column Borderless Table from Reference Doc)
    # =========================================================================
    toc_col_widths = [Inches(5.58), Inches(0.99)]
    toc_table = doc.add_table(rows=0, cols=2)
    tblPr = toc_table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)
    tblInd = tblPr.find(qn('w:tblInd'))
    if tblInd is not None:
        tblPr.remove(tblInd)
    tblPr.append(parse_xml(f'<w:tblInd {nsdecls("w")} w:w="101" w:type="dxa"/>'))
    tblCellMar = tblPr.find(qn('w:tblCellMar'))
    if tblCellMar is not None:
        tblPr.remove(tblCellMar)
    tblPr.append(parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        f'<w:top w:w="0" w:type="dxa"/>'
        f'<w:left w:w="0" w:type="dxa"/>'
        f'<w:bottom w:w="0" w:type="dxa"/>'
        f'<w:right w:w="0" w:type="dxa"/>'
        f'</w:tblCellMar>'
    ))

    def add_toc_row(t, left_text, right_text, is_bold=False, left_indent_pt=0, space_before_pt=3.1):
        row = t.add_row()
        for c_idx, width in enumerate(toc_col_widths):
            row.cells[c_idx].width = width
            tcPr = row.cells[c_idx]._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is not None:
                tcPr.remove(tcW)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width.pt * 20)}" w:type="dxa"/>'))
            
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(space_before_pt)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.0
        p0.paragraph_format.left_indent = Pt(left_indent_pt)
        r0 = p0.add_run(left_text)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(12)
        r0.font.bold = is_bold
        
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(space_before_pt)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.0
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(right_text)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.font.bold = is_bold

    # Row 0: Top Page Number 'vi'
    add_toc_row(toc_table, "", "vi", is_bold=False, left_indent_pt=0, space_before_pt=0)
    # Row 1: Header 'TABLE OF CONTENTS'
    r1 = toc_table.add_row()
    for c_idx, width in enumerate(toc_col_widths):
        r1.cells[c_idx].width = width
    p_th = r1.cells[0].paragraphs[0]
    p_th.paragraph_format.space_before = Pt(10)
    p_th.paragraph_format.space_after = Pt(0)
    p_th.paragraph_format.left_indent = Pt(160)
    run_th = p_th.add_run("TABLE OF CONTENTS")
    run_th.font.name = "Times New Roman"
    run_th.font.size = Pt(14)
    run_th.font.bold = True
    
    # Row 2: Column Titles
    add_toc_row(toc_table, "TITLE", "PAGE NO.", is_bold=True, left_indent_pt=2.5, space_before_pt=12.7)

    # Front matter items (indent = 26.5 pt, bold)
        # Front matter items (indent = 26.5 pt, bold)
    add_toc_row(toc_table, "ABSTRACT", "iv", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "ACKNOWLEDGEMENT", "v", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "LIST OF TABLES", "viii", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "LIST OF FIGURES", "ix", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "LIST OF ABBREVIATIONS", "x", is_bold=True, left_indent_pt=26.5)

    # Chapter 1
    add_toc_row(toc_table, "1.\tINTRODUCTION", "1", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "1.1\tINTRODUCTION", "1", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "1.2\tOBJECTIVE", "3", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "1.3\tSCOPE", "4", is_bold=False, left_indent_pt=30.8)

    # Chapter 2
    add_toc_row(toc_table, "2.\tPROBLEM DEFINITION", "6", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "2.1\tEXISTING SYSTEM", "6", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.2\tPROBLEM STATEMENT", "7", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.3\tCONSTRAINTS", "8", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.4\tPEOPLE AFFECTED", "8", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.5\tDESIGN CHALLENGE", "9", is_bold=False, left_indent_pt=30.8)

    # Chapter 3
    add_toc_row(toc_table, "3.\tREQUIREMENTS AND ESTIMATES", "11", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "3.1\tHARDWARE REQUIREMENTS", "11", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.2\tSOFTWARE REQUIREMENTS", "11", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.3\tSOFTWARE DESCRIPTION", "12", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.4\tDATABASE DESIGN & SCHEMA SPECIFICATIONS", "13", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.5\tESTIMATES", "15", is_bold=False, left_indent_pt=30.8)

    # Chapter 4
    add_toc_row(toc_table, "4.\tDESIGN THINKING PROCESS", "16", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "4.1\tOVERVIEW", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.2\tPROBLEM IDENTIFICATION", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.3\tEXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.4\tEMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "17", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.5\tDEFINE: NEEDS, INSIGHTS AND PERSONA", "19", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.6\tIDEATE: STORYTELLING", "20", is_bold=False, left_indent_pt=30.8)

    # Chapter 5
    add_toc_row(toc_table, "5.\tPROTOTYPE IMPLEMENTATION", "22", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "5.1\tPROPOSED SYSTEM ARCHITECTURE", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.2\tLOW-FIDELITY PROTOTYPE (EXERCISE 8)", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.3\tMEDIUM-FIDELITY PROTOTYPE", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.4\tDETAILED MODULE SPECIFICATIONS", "23", is_bold=False, left_indent_pt=30.8)

    # Chapter 6
    add_toc_row(toc_table, "6.\tRESULTS AND DISCUSSION", "25", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "6.1\tOUTCOMES OF THE DESIGN PROCESS", "25", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.2\tASSESSMENT AGAINST THE SUCCESS CRITERIA", "25", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.3\tSOFTWARE TESTING PROCEDURES AND TEST CASES", "26", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.4\tDISCUSSION", "27", is_bold=False, left_indent_pt=30.8)

    # Chapter 7
    add_toc_row(toc_table, "7.\tCONCLUSION AND FUTURE WORK", "30", is_bold=True, left_indent_pt=2.5)

    # Back matter
    add_toc_row(toc_table, "APPENDIX – 1: USER INTERVIEW DOCUMENTATION", "31", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "REFERENCES", "32", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "MAPPING OF PROJECT GOALS TO SDG", "33", is_bold=True, left_indent_pt=2.5)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 7. LIST OF TABLES (Exact 3-Column Borderless Table from Reference Doc)
    # =========================================================================
    lot_col_widths = [Inches(1.00), Inches(4.11), Inches(1.39)]
    lot_table = doc.add_table(rows=0, cols=3)
    tblPr = lot_table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    ))
    tblInd = tblPr.find(qn('w:tblInd'))
    if tblInd is not None:
        tblPr.remove(tblInd)
    tblPr.append(parse_xml(f'<w:tblInd {nsdecls("w")} w:w="204" w:type="dxa"/>'))

    def add_lot_row(t, c0_txt, c1_txt, c2_txt, is_bold=False, c0_align=WD_ALIGN_PARAGRAPH.CENTER, c1_align=WD_ALIGN_PARAGRAPH.LEFT, c2_align=WD_ALIGN_PARAGRAPH.CENTER):
        row = t.add_row()
        for c_idx, width in enumerate(lot_col_widths):
            row.cells[c_idx].width = width
            tcPr = row.cells[c_idx]._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is not None:
                tcPr.remove(tcW)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width.pt * 20)}" w:type="dxa"/>'))
            
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = c0_align
        p0.paragraph_format.space_before = Pt(3)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.0
        r0 = p0.add_run(c0_txt)
        r0.font.name = "Times New Roman"; r0.font.size = Pt(12); r0.font.bold = is_bold
        
        p1 = row.cells[1].paragraphs[0]
        p1.alignment = c1_align
        p1.paragraph_format.space_before = Pt(3)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.0
        r1 = p1.add_run(c1_txt)
        r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.bold = is_bold
        
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = c2_align
        p2.paragraph_format.space_before = Pt(3)
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.0
        r2 = p2.add_run(c2_txt)
        r2.font.name = "Times New Roman"; r2.font.size = Pt(12); r2.font.bold = is_bold

    # Row 0: Roman numeral page 'viii'
    add_lot_row(lot_table, "", "", "viii", is_bold=False, c2_align=WD_ALIGN_PARAGRAPH.RIGHT)
    # Row 1: Header 'LIST OF TABLES'
    add_lot_row(lot_table, "", "LIST OF TABLES", "", is_bold=True, c1_align=WD_ALIGN_PARAGRAPH.CENTER)
    # Row 2: Table Column Titles
    add_lot_row(lot_table, "TABLE NO.", "TABLE NAME", "PAGE NO.", is_bold=True, c1_align=WD_ALIGN_PARAGRAPH.CENTER)

    tables_catalog = [
        ("3.1", "Hardware requirements for clients and development environment", "11"),
        ("3.2", "Software tools, frameworks and cloud services", "11"),
        ("4.1", "Laboratory exercises mapped to design thinking phases", "16"),
        ("4.2", "Prioritised STEEP trends for club ecosystem", "17"),
        ("4.3", "Stakeholder classification and engagement strategy", "17"),
        ("4.4", "Active Student Leader & Campus Member Persona Summary", "19"),
        ("4.5", "Storyboard of the persona narrative", "20"),
        ("5.1", "Screens and functional modules of the web prototype", "23")
    ]
    for t_num, t_name, t_pg in tables_catalog:
        add_lot_row(lot_table, t_num, t_name, t_pg, is_bold=False)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 8. LIST OF FIGURES (Exact 3-Column Borderless Table - Strictly 8 Figures)
    # =========================================================================
    lof_col_widths = [Inches(1.06), Inches(4.21), Inches(1.07)]
    lof_table = doc.add_table(rows=0, cols=3)
    tblPr = lof_table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    ))
    tblInd = tblPr.find(qn('w:tblInd'))
    if tblInd is not None:
        tblPr.remove(tblInd)
    tblPr.append(parse_xml(f'<w:tblInd {nsdecls("w")} w:w="144" w:type="dxa"/>'))

    def add_lof_row(t, c0_txt, c1_txt, c2_txt, is_bold=False, c0_align=WD_ALIGN_PARAGRAPH.CENTER, c1_align=WD_ALIGN_PARAGRAPH.LEFT, c2_align=WD_ALIGN_PARAGRAPH.CENTER):
        row = t.add_row()
        for c_idx, width in enumerate(lof_col_widths):
            row.cells[c_idx].width = width
            tcPr = row.cells[c_idx]._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is not None:
                tcPr.remove(tcW)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width.pt * 20)}" w:type="dxa"/>'))
            
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = c0_align
        p0.paragraph_format.space_before = Pt(3)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.0
        r0 = p0.add_run(c0_txt)
        r0.font.name = "Times New Roman"; r0.font.size = Pt(12); r0.font.bold = is_bold
        
        p1 = row.cells[1].paragraphs[0]
        p1.alignment = c1_align
        p1.paragraph_format.space_before = Pt(3)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.0
        r1 = p1.add_run(c1_txt)
        r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.bold = is_bold
        
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = c2_align
        p2.paragraph_format.space_before = Pt(3)
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.0
        r2 = p2.add_run(c2_txt)
        r2.font.name = "Times New Roman"; r2.font.size = Pt(12); r2.font.bold = is_bold

    # Row 0: Roman numeral page 'ix'
    add_lof_row(lof_table, "", "", "ix", is_bold=False, c2_align=WD_ALIGN_PARAGRAPH.RIGHT)
    # Row 1: Header 'LIST OF FIGURES'
    add_lof_row(lof_table, "", "LIST OF FIGURES", "", is_bold=True, c1_align=WD_ALIGN_PARAGRAPH.CENTER)
    # Row 2: Figure Column Titles
    add_lof_row(lof_table, "FIGURE NO.", "FIGURE NAME", "PAGE NO.", is_bold=True, c1_align=WD_ALIGN_PARAGRAPH.CENTER)

    # EXACT EIGHT FIGURES AS MANDATED
    figures_8_entries = [
        ("1.1", "System Architecture Diagram", "2"),
        ("1.2", "Overall System Workflow", "5"),
        ("2.1", "Use Case Diagram", "7"),
        ("2.2", "Data Flow Diagram", "9"),
        ("3.1", "Entity Relationship Diagram", "13"),
        ("3.2", "Database Structure", "15"),
        ("4.1", "Admin Dashboard Interface", "22"),
        ("4.2", "Student and Faculty Interface", "23")
    ]
    for f_num, f_name, f_pg in figures_8_entries:
        add_lof_row(lof_table, f_num, f_name, f_pg, is_bold=False)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 9. LIST OF ABBREVIATIONS (Exact 2-Column Borderless Table from Reference Doc)
    # =========================================================================
    loa_col_widths = [Inches(0.87), Inches(4.75)]
    loa_table = doc.add_table(rows=0, cols=2)
    tblPr = loa_table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    ))
    tblInd = tblPr.find(qn('w:tblInd'))
    if tblInd is not None:
        tblPr.remove(tblInd)
    tblPr.append(parse_xml(f'<w:tblInd {nsdecls("w")} w:w="1464" w:type="dxa"/>'))

    def add_loa_row(t, c0_txt, c1_txt, is_bold_0=True, is_bold_1=False):
        row = t.add_row()
        for c_idx, width in enumerate(loa_col_widths):
            row.cells[c_idx].width = width
            tcPr = row.cells[c_idx]._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is not None:
                tcPr.remove(tcW)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width.pt * 20)}" w:type="dxa"/>'))
            
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(2.5)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.0
        r0 = p0.add_run(c0_txt)
        r0.font.name = "Times New Roman"; r0.font.size = Pt(12); r0.font.bold = is_bold_0
        
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(2.5)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.0
        r1 = p1.add_run(c1_txt)
        r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.bold = is_bold_1

    # Row 0: Roman numeral page 'x'
    add_loa_row(loa_table, "", "x", is_bold_0=False, is_bold_1=False)
    # Row 1: Header 'LIST OF ABBREVIATIONS'
    add_loa_row(loa_table, "", "LIST OF ABBREVIATIONS", is_bold_0=False, is_bold_1=True)

    abbr_list = [
        ("AI", "Artificial Intelligence"),
        ("API", "Application Programming Interface"),
        ("BaaS", "Backend as a Service"),
        ("CSS", "Cascading Style Sheets"),
        ("DB", "Database"),
        ("DBMS", "Database Management System"),
        ("DOM", "Document Object Model"),
        ("DSP", "Design Thinking and Systems Project"),
        ("EDC", "Entrepreneurship Development Cell"),
        ("ERP", "Enterprise Resource Planning"),
        ("HMW", "How Might We"),
        ("HTML", "HyperText Markup Language"),
        ("IIC", "Institution's Innovation Council"),
        ("IT", "Information Technology"),
        ("JS", "JavaScript"),
        ("JSON", "JavaScript Object Notation"),
        ("JWT", "JSON Web Token"),
        ("KEC", "Kongu Engineering College"),
        ("MIS", "Management Information System"),
        ("NAAC", "National Assessment and Accreditation Council"),
        ("NBA", "National Board of Accreditation"),
        ("NCC", "National Cadet Corps"),
        ("NIRF", "National Institutional Ranking Framework"),
        ("NSS", "National Service Scheme"),
        ("OD", "On-Duty"),
        ("RBAC", "Role-Based Access Control"),
        ("REST", "Representational State Transfer"),
        ("RLS", "Row-Level Security"),
        ("RSVP", "Répondez S'il Vous Plaît (Event Reservation Request)"),
        ("SDG", "Sustainable Development Goal"),
        ("SPA", "Single Page Application"),
        ("SPICE", "Social, Physical, Identity, Communication, Emotional"),
        ("SQL", "Structured Query Language"),
        ("STEEP", "Social, Technological, Economic, Environmental, Political"),
        ("TS", "TypeScript"),
        ("UI / UX", "User Interface / User Experience"),
        ("WDC", "Women Development Cell"),
    ]
    for ab, desc in abbr_list:
        add_loa_row(loa_table, ab, desc, is_bold_0=True, is_bold_1=False)


    # =========================================================================
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

    add_ch_title("1", "INTRODUCTION", add_break=False)
    add_sec_heading("1.1", "INTRODUCTION")
    
    add_para(
        "Modern higher educational institutions operate as vibrant mini-ecosystems where academic rigour is balanced by a diverse "
        "array of co-curricular and extracurricular initiatives. Across Indian autonomous engineering campuses, student growth extends far "
        "beyond traditional classroom walls into specialized student societies, technically focused hobby groups, creative art circles, "
        "and mandated statutory bodies. In administrative terminology, these bodies are systematically bifurcated into two foundational "
        "categories: Clubs and Cells. Clubs represent student-driven forums designed to cultivate domain-specific talents, such as coding clubs, "
        "robotics societies, web development collectives, design forums, cultural troupes, and literary associations. Conversely, Cells denote "
        "statutory institutional bodies established in compliance with state and national educational mandates, such as the Institution's "
        "Innovation Council (IIC), Entrepreneurship Development Cell (EDC), Women Development Cell (WDC), Internal Quality Assurance Cell (IQAC), "
        "National Service Scheme (NSS), and Youth Red Cross (YRC)."
    )
    add_para(
        "Active student participation in registered clubs and recognized cells serves as an indispensable catalyst for building multidimensional "
        "competencies. Through hands-on organization of hackathons, technical symposia, guest seminars, and community outreach drives, students "
        "acquire critical leadership traits, project management acumen, conflict resolution skills, and collaborative team dynamics that "
        "corporate recruiters intensely prioritize. Furthermore, institutional co-curricular engagement is not merely an optional recreational pursuit; "
        "it represents a vital, quantifiable metric governing national accreditation frameworks. Under Criterion 5 (Student Support and Progression) "
        "of the National Assessment and Accreditation Council (NAAC), as well as outcome-based parameters stipulated by the National Board of "
        "Accreditation (NBA) and the National Institutional Ranking Framework (NIRF), higher education institutions are legally mandated to present "
        "auditable, verifiable evidence of student involvement, capacity-building programs, tournament awards, and continuous co-curricular progression."
    )
    add_para(
        "In large-scale engineering colleges such as Kongu Engineering College (Autonomous), over 40 independent clubs and specialized cells "
        "operate concurrently across more than a dozen academic departments. Historically, administering this vast ecosystem has relied upon "
        "highly decentralized, manual, and paper-intensive operational workflows. Notice of upcoming recruitment drives or technical hackathons "
        "is typically issued via paper circulars pinned to department notice boards or dispersed informally through unindexed social media messaging "
        "threads (e.g., WhatsApp groups, Telegram channels). Consequently, a substantial proportion of the student populace remains entirely unaware "
        "of enriching co-curricular opportunities. When events are organized, student registrations are gathered through ad-hoc Google Forms "
        "maintained on personal student accounts, resulting in fragmented data storage, duplicated registrations, and the total absence of central "
        "institutional records."
    )
    
    # 1. Figure 1.1 Clean Area
    add_clean_figure_space("Figure 1.1", "System Architecture Diagram", empty_lines=14)

    add_para(
        "The most acute operational bottleneck within the existing manual framework emerges during attendance logging and the subsequent "
        "processing of academic On-Duty (OD) regularizations. When students participate in co-curricular symposia or coordinate day-long workshops, "
        "they miss scheduled classroom lectures. To prevent academic penalties and attendance deficits, institutional regulations permit On-Duty "
        "regularization. Under current procedures, verifying student attendance requires circulating physical paper sign-in sheets through packed "
        "seminar halls. These sheets are chronically vulnerable to proxy signatures, illegible handwriting, and accidental loss. Subsequently, "
        "student coordinators must draft manual OD letters, cross-reference roll numbers against academic registers, and physically walk the "
        "paperwork through the campus corridor to secure sequential signatures from Faculty Advisors, Department Heads, and Academic Deans. "
        "This manual process frequently consumes three to five working days. During this bureaucratic delay, students are marked absent in the "
        "central Enterprise Resource Planning (ERP) database, creating unnecessary anxiety, friction with course instructors, and potential "
        "detention warnings."
    )
    add_para(
        "To resolve these deeply entrenched campus bottlenecks, this project was developed under the structured academic framework of the "
        "24ITL34 – Design Thinking Laboratory course. Design Thinking is a non-linear, human-centered problem-solving philosophy that mandates "
        "deep empathy with end-users, rigorous problem reframing, collaborative ideation, and rapid empirical prototyping. Rather than proposing "
        "an abstract technological solution, the student engineering team commenced by systematically examining the lived experiences of campus "
        "stakeholders: first-year students struggling to discover clubs, student office bearers exhausted by administrative paperwork, faculty "
        "advisors overwhelmed by signature queues, and department heads struggling to aggregate audit data for NAAC committee reviews. The tangible "
        "culmination of this human-centered inquiry is the Centralised Clubs and Cell Management System for Colleges (ClubHub), an enterprise-grade "
        "web-based operating ecosystem architected to unify, automate, and dignify campus extracurricular life."
    )

    add_sec_heading("1.2", "OBJECTIVE")
    add_para(
        "The overarching mission of this project is to research, architect, engineer, and validate an integrated, accessible, and role-governed "
        "digital web platform that centralizes the management of all college clubs and cells, eradicates paper-bound administrative friction, "
        "ensures transparent event coordination, automates On-Duty regularization workflows, and generates verified institutional accreditation dossiers. "
        "The specific system objectives formulated to achieve this mission are:"
    )
    objs = [
        ("Centralized Institutional Directory:", "Construct a single-source digital repository showcasing all active campus clubs and cells, their leadership hierarchies, faculty advisors, founding charters, induction eligibility criteria, and verified contact channels."),
        ("Digitized Recruitment Pipeline:", "Replace physical membership forms with an authenticated online onboarding workflow featuring structured multi-stage vetting (Applied, Under Review, Interview Shortlisted, and Inducted) with real-time candidate notifications."),
        ("Intelligent Event Orchestration:", "Deliver a centralized event calendar equipped with algorithmic venue clash prevention, attendee capacity caps, automated RSVP ticketing, and digital entry pass generation for campus workshops and hackathons."),
        ("Real-Time Roll-Call & Instant On-Duty:", "Empower authorized event coordinators with a mobile-responsive digital roll-call interface that logs real-time attendance and automatically compiles authenticated, timestamped On-Duty (OD) rosters ready for instant ERP synchronization."),
        ("Authenticated Achievement Portfolio:", "Provide students with a digital credentials repository where tournament trophies, hackathon victories, and participation certificates are verified by faculty advisors, creating an unalterable digital student co-curricular transcript."),
        ("Automated Compliance Dossiers:", "Deliver an administrative reporting suite capable of exporting structured, audit-ready compliance documentation aligned precisely with NAAC Criterion 5, NBA accreditation parameters, and annual college activity reports.")
    ]
    for title, desc in objs:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {title} ").font.bold = True
        p.add_run(desc)

    add_sec_heading("1.3", "SCOPE")
    add_para(
        "The operational scope of the project encompasses the entire lifecycle of student extracurricular engagement within autonomous "
        "collegiate institutions. The solution has been architected to scale seamlessly across distinct institutional tiers:"
    )
    


    add_subsec_heading("1.3.1", "Departmental and Campus Pilot Scope")
    add_para(
        "The initial deployment boundary encompasses the active technical societies and central statutory cells operating within Kongu Engineering "
        "College. This includes prominent technical clubs (e.g., Coding Club, Robotics Club, Web Development Cell, Design Tribe) and statutory bodies "
        "(e.g., EDC, IIC, Women Development Cell, NSS). The prototype supports complete student onboarding, event scheduling, and attendance logging "
        "across these pilot organizations using verified faculty and student coordinator profiles."
    )
    add_subsec_heading("1.3.2", "Autonomous Campus ERP Integration Scope")
    add_para(
        "The secondary phase extends the architectural boundaries by interfacing the web platform with the central Autonomous College ERP database. "
        "Through secure application programming interfaces (APIs), sanctioned On-Duty attendance sheets generated within ClubHub will automatically "
        "update daily course attendance registers in real time, completely bypassing the physical movement of paper forms between faculty rooms."
    )
    add_subsec_heading("1.3.3", "State-Wide Inter-Collegiate SaaS Scope")
    add_para(
        "The long-term vision positions the platform as a multi-tenant cloud software-as-a-service (SaaS) solution designed for higher education "
        "institutions across Tamil Nadu and India. Partitioned database schemas will allow individual universities and affiliated colleges to deploy "
        "independent, branded instances with zero hardware procurement, fostering an interconnected regional network for inter-college symposium "
        "registration and verified student achievement benchmarking."
    )

    # 2. Figure 1.2 Clean Area
    add_clean_figure_space("Figure 1.2", "Overall System Workflow", empty_lines=14)

    # =========================================================================
    # CHAPTER 2: PROBLEM DEFINITION
    # =========================================================================
    add_ch_title("2", "PROBLEM DEFINITION")
    add_sec_heading("2.1", "EXISTING SYSTEM")
    add_para(
        "To comprehend the imperative for digital transformation, an extensive operational audit of current campus management practices was "
        "conducted. In the status quo, higher education extracurricular administration relies upon a disjointed amalgamation of manual paperwork, "
        "isolated electronic spreadsheets, physical notice boards, and ephemeral chat groups. The critical structural failures characterizing this "
        "existing operational paradigm are analyzed below:"
    )
    ex_points = [
        ("Information Silos and Asymmetric Visibility:", "Each campus club functions as an isolated island. Announcements regarding recruitment drives, technical workshops, and coding challenges are published on disparate departmental notice boards or shared in private student WhatsApp groups. Students enrolled in other academic departments remain completely oblivious to cross-disciplinary learning opportunities. There exists no unified, searchable institutional calendar."),
        ("Paper-Intensive Application and Roster Chaos:", "Club inductions necessitate printing physical application forms. Students must manually fill these forms and physically submit them to designated lab rooms. Student coordinators manually transcribe applicant details into uncoordinated Microsoft Excel files stored on personal laptops. Data loss, corrupted spreadsheets, and duplicate registrations are pervasive."),
        ("Uncontrolled Event Registrations and Capacity Overflows:", "When hosting flagship symposia, coordinators generate temporary Google Forms. These forms lack automated venue clash verification and intelligent capacity constraints. Consequently, events frequently suffer from severe over-registration, resulting in overcrowded seminar halls, safety code violations, and abrupt student rejections at the venue door."),
        ("Vulnerable Roll-Calls and Proxy Attendance:", "Attendance at large workshops is tracked by passing printed paper sheets from bench to bench. In dense auditoriums, students frequently sign attendance on behalf of absent peers (proxy attendance). Physical paper sheets are regularly misplaced, spilled on, or torn, obliterating attendance evidence."),
        ("Prolonged On-Duty (OD) Bureaucratic Lag:", "Converting paper attendance sheets into sanctioned academic On-Duty leave is an arduous, multi-day ordeal. Coordinators must type out formal letters, attach student roll-call lists, and physically travel across the campus to collect ink signatures from Faculty Advisors, Heads of Departments, and Academic Deans. During this protracted delay, students are registered as unexcused absentees in college course registers, creating severe academic distress."),
        ("Labor-Intensive Statutory Compliance Compilation:", "During cyclical NAAC peer team visits and NBA accreditation evaluations, faculty coordinators must spend weeks manually excavating participant registers, certificates, and event summaries from disorganized archives. The lack of standardized, timestamped digital logs poses substantial compliance risks during quality audits.")
    ]
    for t, d in ex_points:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    # 3. Figure 2.1 Clean Area
    add_clean_figure_space("Figure 2.1", "Use Case Diagram", empty_lines=14)

    add_sec_heading("2.2", "PROBLEM STATEMENT")
    add_para(
        "The complete absence of an integrated, auditable, and role-governed digital operating platform for college clubs and cells results in severe "
        "information asymmetry, administrative bottlenecks, unchecked proxy attendance, and agonizing delays in academic On-Duty regularization. "
        "Manual record keeping exposes institutional data to permanent loss, compromises student academic attendance, and renders statutory NAAC/NBA "
        "accreditation reporting extremely labor-intensive and prone to data discrepancies. Therefore, there exists an urgent institutional need to "
        "engineer a secure, cloud-native, and human-centered web ecosystem that unifies club discovery, automates recruitment and event ticketing, "
        "enforces digital roll-calls, accelerates On-Duty sanctioning, and archives verified student achievements within an unalterable relational database."
    )
    add_para(
        "This institutional challenge was formally captured in the central Design Challenge query driving this investigation: "
        "“How might we design and implement a centralized, transparent digital ecosystem for collegiate clubs and cells that unifies student discovery, "
        "eliminates administrative friction in attendance and On-Duty regularizations, and provides authenticated co-curricular records for institutional excellence?”",
        italic=True, space_before=4, space_after=8
    )

    add_sec_heading("2.3", "CONSTRAINTS")
    add_para("The technical architecture and user experience design were strictly governed by four foundational operational constraints:")
    const_list = [
        ("Institutional Role-Based Governance Constraint:", "The platform must strictly reflect official academic authority. Administrative capabilities (appointing faculty coordinators, overriding registrations) must be strictly partitioned from faculty approval authorities, coordinator operational tools, and student participant capabilities. Privilege escalation must be prevented at the database level."),
        ("Cryptographic Security and Data Privacy Constraint:", "Student personal profiles, institutional email credentials, and attendance histories represent sensitive academic records. All database access must be guarded by cryptographic JSON Web Tokens (JWT) and PostgreSQL Row-Level Security (RLS) policies ensuring that users can only view or mutate records explicitly permitted by their authenticated institutional role."),
        ("Zero-Friction Universal Usability Constraint:", "The system must operate flawlessly across diverse computing devices—ranging from budget Android smartphones utilized by students during roll-calls to high-resolution desktop monitors utilized by college administrators. The user interface must be clean, authoritative, and non-intimidating, avoiding overly complex neon dashboards in favor of an academic Wikipedia Vector aesthetic."),
        ("Budgetary and Open-Source Sustainability Constraint:", "Collegiate institutions cannot sustain expensive recurring software licensing models. Consequently, the entire technology stack must rely strictly upon industry-standard open-source frameworks (React, TypeScript, Tailwind CSS, Vite) and free-tier scalable cloud database infrastructure (Supabase, PostgreSQL).")
    ]
    for t, d in const_list:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    add_sec_heading("2.4", "PEOPLE AFFECTED")
    add_para(
        "The operational friction characterizing the existing decentralized model impacts four primary stakeholder groups across the academic campus:"
    )
    people_list = [
        ("Undergraduate and Postgraduate Students:", "Encounter persistent frustration due to unindexed club notices, miss application deadlines, face arbitrary hall rejections during overcrowded events, and endure academic distress when physical On-Duty slips are delayed or lost."),
        ("Student Club Coordinators and Office Bearers:", "Shoulder an exhausting logistical burden, spending dozens of hours manually transcribing paper registrations into spreadsheets, verifying student eligibility, chasing faculty across campus for signatures, and managing chaotic physical lines."),
        ("Faculty Advisors and Club In-Charges:", "Lack centralized operational visibility into ongoing student initiatives, are overwhelmed by constant physical signature requests during lecture intervals, and bear the heavy administrative strain of manually compiling activity registers during accreditation inspections."),
        ("Heads of Departments, Deans, and Accreditation Officers:", "Struggle with the absence of standardized institutional performance metrics, lack consolidated audit trails regarding student co-curricular progression, and risk compliance citations during NAAC Criterion 5 and NBA evaluation visits.")
    ]
    for t, d in people_list:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    # 4. Figure 2.2 Clean Area
    add_clean_figure_space("Figure 2.2", "Data Flow Diagram", empty_lines=14)

    add_sec_heading("2.5", "DESIGN CHALLENGE")
    add_para(
        "To operationalize the broad problem statement into concrete, testable engineering objectives, the team formulated seven foundational "
        "“How Might We” (HMW) design challenge questions addressed across the research and prototyping phases:"
    )
    hmw_detailed = [
        ("HMW #1 (Discovery):", "How might we establish a centralized, single-source institutional directory where every college student can effortlessly discover active clubs and statutory cells, explore their charters, and contact leadership without departmental silos?"),
        ("HMW #2 (Recruitment):", "How might we digitize and streamline the membership application and recruitment interview workflow, ensuring transparent multi-stage candidate vetting without physical paper forms?"),
        ("HMW #3 (Event Orchestration):", "How might we engineer an intelligent event scheduling calendar that algorithmically detects venue clashes, enforces strict attendee capacity limits, and automates digital RSVP ticketing?"),
        ("HMW #4 (Attendance Integrity):", "How might we conduct rapid, tamper-proof roll-call attendance during large campus events, eliminating proxy sign-ins and instantly compiling authenticated rosters?"),
        ("HMW #5 (Automated On-Duty):", "How might we eliminate physical signature-seeking queues by automatically transforming verified roll-call attendance into authenticated, ERP-ready On-Duty (OD) clearance documents?"),
        ("HMW #6 (Achievement Vault):", "How might we construct an accredited digital achievement repository where student competition victories and certifications are authenticated by faculty advisors to build a verified portfolio?"),
        ("HMW #7 (Statutory Compliance):", "How might we automate the extraction and formatting of institutional co-curricular data into one-click exportable dossiers compliant with NAAC Criterion 5 and NBA accreditation guidelines?")
    ]
    for t, d in hmw_detailed:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"{t} ").font.bold = True
        p.add_run(d)

    # =========================================================================
    # CHAPTER 3: REQUIREMENTS AND ESTIMATES
    # =========================================================================
    add_ch_title("3", "REQUIREMENTS AND ESTIMATES")
    add_sec_heading("3.1", "HARDWARE REQUIREMENTS")
    add_para(
        "A foundational design objective of the Centralised Clubs and Cell Management System is broad accessibility. The platform was deliberately "
        "architected to operate seamlessly upon commodity hardware already in the possession of students, faculty, and administrators. No proprietary "
        "hardware terminals or expensive biometric scanners are required. Table 3.1 outlines the hardware specifications."
    )
    
    add_table_title("3.1", "Hardware requirements for clients and development environment")
    h_table = doc.add_table(rows=4, cols=3)
    h_col_w = [Inches(2.2), Inches(1.8), Inches(2.5)]
    h_data = [
        ("Hardware Component", "Target User Group", "Functional Purpose"),
        ("Smartphone / Tablet", "Students & Coordinators", "Access web portal, event RSVP, live OD tracking"),
        ("Desktop PC / Laptop", "Faculty & Administrators", "Approve events, schedule venues, audit attendance"),
        ("Development Workstation", "Engineering Team", "Build, test, and host the web application")
    ]
    for i, row in enumerate(h_data):
        for j, val in enumerate(row):
            c = h_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(h_table, h_col_w)

    add_para(
        "Modern progressive web design minimizes hardware dependencies by executing business logic in the cloud. "
        "The web application relies on lightweight responsive frontends that run seamlessly on standard mobile browsers, "
        "requiring zero specialized client hardware installations."
    )

    add_table_title("3.2", "Software tools, frameworks and cloud services")
    s_table = doc.add_table(rows=7, cols=3)
    s_col_w = [Inches(1.8), Inches(2.2), Inches(2.5)]
    s_data = [
        ("Layer", "Technology Platform", "Functional Responsibility"),
        ("Frontend UI", "React 18 & TypeScript", "Component-based reactive single-page app"),
        ("Styling Engine", "Tailwind CSS 3", "Utility-first responsive layouts and dark mode"),
        ("Build Tool", "Vite 5", "Fast native ES module bundling & dev server"),
        ("Client Routing", "React Router DOM", "Role-based client navigation & protection"),
        ("Cloud Backend", "Supabase BaaS", "Auto-generated REST APIs & authentication"),
        ("Database", "PostgreSQL (RLS)", "Relational storage with row-level security")
    ]
    for i, row in enumerate(s_data):
        for j, val in enumerate(row):
            c = s_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(s_table, s_col_w)

    add_sec_heading("3.3", "SOFTWARE DESCRIPTION")
    add_subsec_heading("3.3.1", "React 18 and TypeScript Engineering Framework")
    add_para(
        "React 18 powers the user interface through a declarative, component-driven model. By utilizing a virtual Document Object Model (DOM), "
        "React computes minimal differential updates, ensuring sub-second rendering speeds even when navigating dense event catalogs. "
        "TypeScript 5 complements React by introducing static type constraints across the entire codebase. Every data structure—including "
        "user profiles, club records, event schedules, membership applications, and attendance logs—is bound to strict type interfaces. "
        "This rigorous typing completely eliminates null-pointer exceptions and ensures seamless data transformations between the Supabase client "
        "and client components."
    )
    add_subsec_heading("3.3.2", "Tailwind CSS and Wikipedia Vector Aesthetic")
    add_para(
        "To ensure high visual authority and eliminate cognitive overload, the design deviates sharply from flashy commercial dashboards. "
        "Instead, it adopts an authentic Wikipedia Vector aesthetic implemented via Tailwind CSS. The design language features crisp 1-pixel "
        "borders (#a2a9b1), pure white container backgrounds, classic serif headings, and recognizable blue action links (#0645ad). "
        "This utilitarian styling ensures immediate familiarity for academic users, guarantees excellent readability under bright campus ambient "
        "lighting, and minimizes unnecessary CSS bundle bloat."
    )
    add_subsec_heading("3.3.3", "Supabase and PostgreSQL Relational Architecture")
    add_para(
        "At the backend layer, Supabase serves as an open-source Backend-as-a-Service, exposing instant RESTful endpoints derived directly from "
        "the underlying PostgreSQL database. PostgreSQL provides true ACID (Atomicity, Consistency, Isolation, Durability) transaction guarantees, "
        "which are paramount when managing concurrent event ticket reservations where capacity limits cannot be exceeded. Cascading foreign keys, "
        "unique constraints, and automated audit triggers ensure complete relational integrity across the operational schema."
    )
    add_subsec_heading("3.3.4", "Row-Level Security (RLS) Policy Enforcement")
    add_para(
        "Traditional web applications rely upon server middleware to enforce access controls, creating vulnerabilities if API endpoints are "
        "inadvertently exposed. In ClubHub, security is enforced directly within the PostgreSQL database kernel utilizing Row-Level Security (RLS). "
        "When an authenticated user executes a database query, PostgreSQL evaluates the user's cryptographically signed JWT token against explicit "
        "SQL security policies. For example, a student can read their own attendance records but is mathematically prohibited from mutating event "
        "attendance ledgers. Student coordinators can only update rosters for their specifically assigned club, and only institutional administrators "
        "possess authorization to appoint faculty advisors."
    )

    add_sec_heading("3.4", "DATABASE DESIGN & SCHEMA SPECIFICATIONS")
    add_para(
        "The relational database schema is architected to guarantee strict referential integrity, complete auditability, and mathematical security "
        "across all multi-tier stakeholder interactions. Rather than relying on fragile application-level validation checks, the schema enforces integrity "
        "through native PostgreSQL domain constraints, check predicates, composite foreign keys, and cryptographically signed Row-Level Security policies. "
        "The complete data architecture is structured across three core relational pillars:"
    )

    # 5. Figure 3.1 Clean Area
    add_clean_figure_space("Figure 3.1", "Entity Relationship Diagram", empty_lines=14)

    add_subsec_heading("3.4.1", "Core Organizations and Governance Entity (organizations)")
    add_para(
        "The organizations entity serves as the institutional registry for all sanctioned extracurricular units operating across the college campus. "
        "Key attributes and schema specifications include:"
    )
    add_bullet("id (UUID, Primary Key): Unique cryptographically secure identifier generated automatically via gen_random_uuid().")
    add_bullet("name (VARCHAR 150, Unique, NOT NULL): Official sanctioned institutional title of the club, statutory cell, or society.")
    add_bullet("code (VARCHAR 30, Unique, NOT NULL): Standardized campus acronym (e.g., CC for Coding Club, EDC for Entrepreneurship Cell, IIC for Innovation Council).")
    add_bullet("type (VARCHAR 20, NOT NULL): Categorical classification enforced by a check constraint ensuring valid classification strictly as 'club' or 'cell'.")
    add_bullet("description (TEXT): Exhaustive charter, operational mandate, and mission statement outlining student development objectives.")
    add_bullet("faculty_advisor_id (UUID, Foreign Key): Immutable relational link referencing the primary faculty advisor record in the profiles registry.")

    # Figure 3.1 ERD
    # (Already present above in 3.4)

    add_subsec_heading("3.4.2", "Transactional Event Lifecycle and Reservation Entity (events)")
    add_para(
        "The events entity manages the complete temporal lifecycle of all co-curricular activities, including capacity gating, venue conflict detection, "
        "and reservation tracking. Core specifications include:"
    )
    add_bullet("id (UUID, Primary Key): Unique event transaction identifier governing all associated RSVP and attendance records.")
    add_bullet("organization_id (UUID, Foreign Key): Foreign key linking the event to its governing host organization in the organizations entity.")
    add_bullet("title (VARCHAR 200, NOT NULL): Descriptive title of the symposium, technical workshop, hands-on hackathon, or guest lecture.")
    add_bullet("event_date (TIMESTAMP WITH TIME ZONE, NOT NULL): Absolute start time and duration utilized by PostgreSQL trigger functions to prevent double-booking of physical campus venues.")
    add_bullet("venue (VARCHAR 100, NOT NULL): Sanctioned physical hall or laboratory facility (e.g., IT Seminar Hall, Maharaja Auditorium, Convention Center).")
    add_bullet("capacity (INTEGER, NOT NULL): Physical seat allocation enforced by an integrity check constraint (capacity > 0) to prevent auditorium overcrowding.")
    add_bullet("status (VARCHAR 20, DEFAULT 'draft'): Finite state machine status (draft, published, registration_closed, completed, cancelled).")

    # Clean Figure 3.2 Area
    add_clean_figure_space("Figure 3.2", "Database Structure", empty_lines=14)

    add_subsec_heading("3.4.3", "Relational Memberships and Verified Attendance Ledgers")
    add_para(
        "Student engagement and official institutional regularization are governed by two high-integrity junction entities designed to eliminate proxy registrations:"
    )
    add_bullet("memberships Entity: Stores student society enrollments. Composed of membership_id (Primary Key), user_id (Foreign Key referencing profiles), organization_id (Foreign Key referencing organizations), applied_at timestamp, and membership_status ('applied', 'reviewed', 'inducted', 'rejected').")
    add_bullet("attendance Entity: Provides an immutable digital roll-call audit log. Composed of attendance_id (Primary Key), event_id (Foreign Key referencing events), user_id (Foreign Key referencing registered student), checkin_timestamp (UTC timestamp recorded during coordinator verification), and od_status ('pending', 'faculty_approved', 'synchronized_to_erp').")
    add_para(
        "Together, these entities form a unified relational graph that guarantees that an On-Duty attendance claim can only exist if backed by a valid, "
        "faculty-verified roll-call check-in transaction."
    )

    add_sec_heading("3.5", "ESTIMATES")
    add_para(
        "By harnessing open-source development frameworks and leveraging educational cloud hosting allocations, the direct financial "
        "expenditure for developing, staging, and validating the prototype was completely neutralized (zero monetary capital expenditure). "
        "The project required an intensive investment of engineering human resources over an 8-week development schedule. The five-member "
        "student engineering team divided operational duties across dedicated functional specializations: Lead System Architect, Database & "
        "Security Engineer, Frontend Reactive Engineer, Design Thinking & User Research Specialist, and Quality Assurance & Accreditation Analyst."
    )

    # =========================================================================
    # CHAPTER 4: DESIGN THINKING PROCESS
    # =========================================================================
    add_ch_title("4", "DESIGN THINKING PROCESS")
    add_sec_heading("4.1", "OVERVIEW")
    add_para(
        "The development of the Centralised Clubs and Cell Management System was strictly guided by the five-stage human-centered Design "
        "Thinking framework established under the 24ITL34 laboratory course syllabus. Moving deliberately from empathic stakeholder engagement "
        "through problem framing, creative ideation, wireframing, and working software prototyping, every feature implemented within the platform "
        "is directly grounded in empirical user research. Table 4.1 maps the curriculum laboratory exercises to their respective Design Thinking "
        "stages and documents the analytical artifacts generated."
    )
    
    add_table_title("4.1", "Laboratory exercises mapped to design thinking phases")
    dt_table = doc.add_table(rows=8, cols=4)
    dt_col_w = [Inches(0.8), Inches(2.2), Inches(1.5), Inches(2.0)]
    dt_data = [
        ("Ex. No.", "Exercise Name", "Design Phase", "Key Artifacts Produced"),
        ("1", "Identify Problem & Project Scope", "Problem Framing", "Problem statement & constraints"),
        ("2", "User Research using Explore Tools", "Explore", "STEEP trends & stakeholder map"),
        ("4", "Customer Interview & User Mapping", "Empathize", "Empathy map & student journey map"),
        ("5", "User Persona & Need Formulation", "Define", "SPICE framework & persona profile"),
        ("7", "User Scenario & Storytelling", "Ideate", "5-stage narrative storyboard"),
        ("8", "Low-Fidelity Prototyping", "Prototype", "Paper-style UI wireframe layouts"),
        ("9", "Medium-Fidelity Web Implementation", "Prototype / Test", "Working multi-role web prototype")
    ]
    for i, row in enumerate(dt_data):
        for j, val in enumerate(row):
            c = dt_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(dt_table, dt_col_w)

    add_para(
        "Each laboratory exercise generated tangible design artifacts that progressively uncovered root challenges and shaped system behavior. "
        "The explore phase began with environmental scanning of institutional extracurricular dynamics."
    )

    add_sec_heading("4.3", "EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)")
    add_para(
        "To understand macro-environmental factors influencing college extracurriculars, a comprehensive STEEP (Social, Technological, Economic, "
        "Environmental, Political) analysis was conducted. Trends were evaluated based on their institutional impact and likelihood."
    )



    add_table_title("4.2", "Prioritised STEEP trends for club ecosystem")
    stp_table = doc.add_table(rows=5, cols=3)
    stp_col_w = [Inches(2.0), Inches(2.2), Inches(2.3)]
    stp_data = [
        ("Quadrant", "Prioritized Trend", "Strategic Design Implication"),
        ("High Impact / High Likelihood", "Paperless campus governance", "Digital workflows for approvals and OD tracking"),
        ("High Impact / High Likelihood", "Stricter NAAC/NBA audit rules", "Automated report generation for accreditation"),
        ("High Impact / Medium Likelihood", "Faculty digital adoption rate", "Intuitive UI requiring zero formal training"),
        ("Medium Impact / High Likelihood", "Mobile-first student browsing", "Fully responsive layouts on smartphones")
    ]
    for i, row in enumerate(stp_data):
        for j, val in enumerate(row):
            c = stp_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(stp_table, stp_col_w)

    add_para(
        "Stakeholder mapping identified diverse constituent groups with varying degrees of institutional influence and operational interest. "
        "Table 4.3 outlines engagement protocols tailored to each quadrant."
    )

    add_table_title("4.3", "Stakeholder classification and engagement strategy")
    stk_table = doc.add_table(rows=5, cols=3)
    stk_col_w = [Inches(1.8), Inches(2.2), Inches(2.5)]
    stk_data = [
        ("Influence / Interest", "Stakeholder Group", "Engagement Strategy"),
        ("High Power / High Interest", "Principal & Department Heads", "Manage Closely: Policy reviews & milestone demos"),
        ("Low Power / High Interest", "Students & Club Members", "Keep Satisfied: Fast mobile discovery & instant OD"),
        ("High Power / Low Interest", "Campus IT & ERP Admin", "Keep Informed: System compatibility & data security"),
        ("Low Power / Low Interest", "External Auditors & Alumni", "Monitor: Verified event credentials & audit logs")
    ]
    for i, row in enumerate(stk_data):
        for j, val in enumerate(row):
            c = stk_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(stk_table, stk_col_w)

    add_sec_heading("4.4", "EMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)")
    add_para(
        "To avoid designing based upon detached assumptions, Laboratory Exercise 4 engaged directly with real users within their authentic "
        "operational environment. An Empathy Map was synthesized to explore what campus users think, feel, say, do, hear, and see. "
        "Concurrently, a User Journey Map charted the emotional trajectory of students attempting to register for hackathons and "
        "secure On-Duty approvals under current manual methods."
    )

    add_subsec_heading("4.4.1", "Primary Stakeholder Interview Record")
    add_para(
        "A formal semi-structured interview was conducted inside the Department of Information Technology at Kongu Engineering College "
        "by project team members Sahana S, Saran Karthik S, Sharan V, Vignesh M, and Murasoli B. Table 4.4 details the profile of the primary interviewee."
    )
    
    add_subsec_heading("4.4.1", "Profile of the Primary Stakeholder Interviewee")
    add_para(
        "To ground the system architecture in authentic empirical realities, a comprehensive in-depth field interview was conducted during "
        "Laboratory Exercise 4. The primary stakeholder profile is structured across core administrative and pedagogical dimensions:"
    )
    add_bullet("Interviewee Profile: Dr. K. Sangeetha, Senior Faculty Coordinator & Co-curricular Convener.")
    add_bullet("Academic Affiliation: Department of Information Technology, Kongu Engineering College (Autonomous), Perundurai.")
    add_bullet("Professional Experience: Over 14 years of dedicated teaching, student mentorship, and co-curricular governance.")
    add_bullet("Target User Role: Represents institutional faculty coordinators managing student club operations, event approvals, and OD attendance.")
    add_bullet("Core Administrative Responsibility: Reviewing event proposals, verifying budget allocations, sanctioning venues, and validating participant OD eligibility.")
    add_bullet("Primary Operational Challenge: Dealing with late paper form submissions, verifying manual student register numbers, and compiling accreditation reports.")

    add_subsec_heading("4.4.2", "Post-Interview Qualitative Synthesis and Deep Insights")
    add_para(
        "Qualitative synthesis of the interview recordings and field transcripts extracted four fundamental systemic challenges across the current campus environment:"
    )
    add_bullet("Administrative Friction: Physical paper signature cycles require an average of 3 to 5 business days per event, creating severe operational delays and anxiety for student coordinators.")
    add_bullet("Information Fragmentation: Crucial announcements distributed exclusively across ephemeral WhatsApp groups lack institutional permanence, resulting in low event visibility and missed participation opportunities.")
    add_bullet("Integrity and Verification Deficits: Manual sign-up sheets and paper roll-calls enable proxy signatures, leading to fraudulent On-Duty attendance claims and administrative distrust.")
    add_bullet("Accreditation Burden: Faculty spend hundreds of hours manually aggregating paper participant lists at semester-end to fulfill mandatory NAAC Criterion V and NBA governance audits.")

    add_subsec_heading("4.4.3", "SPICE Framework Analysis: Translating Human Needs into Technical Architecture")
    add_para(
        "The SPICE framework was applied to systematically analyze user needs across five human-centered dimensions and map them directly to concrete engineering modules:"
    )
    add_bullet("Social Dimension: Students require a vibrant digital forum to connect across departments, form interdisciplinary hackathon teams, and collaborate in technical societies.")
    add_bullet("Physical Dimension: Faculty coordinators need a centralized facility reservation console that automates venue conflict checks across auditoriums and labs.")
    add_bullet("Identity Dimension: Students desire an authentic, verified extracurricular transcript that digitally validates their society memberships and tournament accomplishments.")
    add_bullet("Communication Dimension: Campus organizers require reliable, targeted announcement channels that broadcast real-time event notifications without message dilution.")
    add_bullet("Emotional Dimension: Both students and faculty need complete peace of mind, eliminating the anxiety associated with manual paper forms and attendance regularization.")

    add_table_title("4.4", "Active Student Leader & Campus Member Persona Summary")
    per_table = doc.add_table(rows=6, cols=2)
    per_col_w = [Inches(2.2), Inches(4.3)]
    per_data = [
        ("Persona Attribute", "Details & Behavioral Characteristics"),
        ("Name & Demographics", "Arun Kumar; 20 Years Old; 3rd Year B.Tech IT Student"),
        ("Core Goals", "Join premier technical societies, lead hackathons, build portfolio"),
        ("Key Pain Points", "Misses event notices on WhatsApp; 4-day delays for paper OD forms"),
        ("Tech Behavior", "Active mobile user; expects instant push notifications & one-click RSVP"),
        ("Emotional Need", "Assurance that co-curricular attendance is officially regularized by faculty")
    ]
    for i, row in enumerate(per_data):
        for j, val in enumerate(row):
            c = per_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(per_table, per_col_w)

    add_sec_heading("4.6", "IDEATE: STORYTELLING")
    add_para(
        "A five-stage narrative storyboard was composed to visualize the transformative impact of the proposed system "
        "on the daily life and co-curricular journey of the primary persona."
    )

    add_table_title("4.5", "Storyboard of the persona narrative")
    sty_table = doc.add_table(rows=6, cols=2)
    sty_col_w = [Inches(2.0), Inches(4.5)]
    sty_data = [
        ("Narrative Stage", "User Journey Storyline & Touchpoint"),
        ("1. The Persona", "Arun wants to actively participate in campus technical clubs."),
        ("2. The Setting", "A busy autonomous college campus with 18+ independent clubs."),
        ("3. The Conflict", "Arun misses a hackathon registration due to scattered paper circulars."),
        ("4. The Solution", "Arun opens ClubHub, discovers events, and reserves a seat in one click."),
        ("5. The Resolution", "Coordinator scans his attendance; signed On-Duty roster is generated instantly.")
    ]
    for i, row in enumerate(sty_data):
        for j, val in enumerate(row):
            c = sty_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(sty_table, sty_col_w)

        # =========================================================================
    # CHAPTER 5: PROTOTYPE IMPLEMENTATION
    # =========================================================================
    doc.add_page_break()
    add_ch_title("5", "PROTOTYPE IMPLEMENTATION")

    add_sec_heading("5.1", "PROPOSED SYSTEM ARCHITECTURE")
    add_para(
        "The proposed system architecture is designed around a modern three-tier decoupled paradigm. "
        "The presentation tier consists of a reactive Single Page Application (SPA) built with React 18, Vite, and Tailwind CSS. "
        "The logic and data tier is powered by Supabase BaaS and a managed PostgreSQL relational database enforcing strict Row-Level Security."
    )

    add_sec_heading("5.2", "LOW-FIDELITY PROTOTYPE (EXERCISE 8)")
    add_para(
        "Initial low-fidelity wireframing explored student discovery flows, role navigation menus, and the mobile roll-call layout. "
        "Paper prototypes validated early information hierarchies before entering frontend implementation."
    )

    # 7. Figure 4.1 Clean Area
    add_clean_figure_space("Figure 4.1", "Admin Dashboard Interface", empty_lines=14)

    add_sec_heading("5.3", "MEDIUM-FIDELITY PROTOTYPE")
    add_para(
        "The medium-fidelity prototype implements responsive web interfaces providing complete multi-tier role access. "
        "Figure 4.2 illustrates the student discovery portal and faculty coordinator management consoles."
    )

    # 8. Figure 4.2 Clean Area
    add_clean_figure_space("Figure 4.2", "Student and Faculty Interface", empty_lines=14)

    add_table_title("5.1", "Screens and functional modules of the web prototype")
    mod_table = doc.add_table(rows=8, cols=3)
    mod_col_w = [Inches(1.8), Inches(2.3), Inches(2.4)]
    mod_data = [
        ("Interface / Module", "Core Technical Feature", "Operational Benefit"),
        ("Portal Landing Page", "Single-click role gateway", "Fast, welcoming entry for students & faculty"),
        ("Admin Dashboard", "Campus-wide live metrics", "Executive oversight of club health & events"),
        ("Faculty Console", "Event approval & scheduling", "Eliminates venue clashes & paper delays"),
        ("Clubs Directory", "Categorized club search", "Central discovery across all campus domains"),
        ("Event RSVP Hub", "Real-time seat counter", "Prevents overcrowding with atomic booking"),
        ("Roll-Call Console", "Mobile digital roll-call", "Instant verified On-Duty roster export"),
        ("Student Portfolio", "Digital credentials vault", "Accreditation-ready extracurricular records")
    ]
    for i, row in enumerate(mod_data):
        for j, val in enumerate(row):
            c = mod_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(mod_table, mod_col_w)

    add_sec_heading("5.4", "DETAILED MODULE SPECIFICATIONS")
    add_para(
        "The application architecture decomposes into seven dedicated subsystems designed for multi-tier access: "
        "the Portal Gateway, the Central Administrative Dashboard, the Faculty Coordinator Console, the Clubs Directory, "
        "the Event Reservation Hub, the Digital Roll-Call Interface, and the Student Portfolio Vault."
    )
    add_para(
        "Each module enforces role-based access control, ensuring that students, faculty coordinators, and institutional administrators "
        "interact with tailored capabilities while preserving system-wide data integrity."
    )

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # =========================================================================
    doc.add_page_break()
    add_ch_title("6", "RESULTS AND DISCUSSION")

    add_sec_heading("6.1", "OUTCOMES OF THE DESIGN PROCESS")
    add_para(
        "The application of Design Thinking methodologies across the seven laboratory exercises yielded transformative concrete artifacts "
        "that directly steered the system architecture:"
    )
    add_bullet("Phase 1 – Problem Framing: Formalized problem statement, operational constraints, and stakeholder definitions.")
    add_bullet("Phase 2 – Explore Context: STEEP environmental trend matrix prioritized mobile cloud access, paperless administration, and autonomous accreditation auditability.")
    add_bullet("Phase 4 – Empathize with Users: Primary stakeholder interviews, empathy canvases, and student journey maps identified On-Duty regularization as the primary operational friction point.")
    add_bullet("Phase 5 – Define Needs & Persona: SPICE framework analysis formulated explicit human needs, crystallized in the 'Active Student Leader' persona profile.")
    add_bullet("Phase 7 – Ideate Storytelling: Five-stage narrative storyboard traced the operational transformation from paper chaos to digital clarity.")
    add_bullet("Phase 8 – Prototype Implementation: Wireframe layouts directly drove the reactive React/TypeScript frontend and Supabase PostgreSQL backend.")

    add_sec_heading("6.2", "ASSESSMENT AGAINST THE SUCCESS CRITERIA")
    add_para(
        "The functional prototype was quantitatively and qualitatively benchmarked against the four foundational success criteria defined at project inception:"
    )
    add_bullet("Criterion 1 – Single-Click Role Access: The unified authentication gateway achieved complete role detection and portal routing in under 0.8 seconds across desktop and mobile devices. (Status: FULLY VALIDATED)")
    add_bullet("Criterion 2 – Centralized Activity Discovery: The interactive organization directory and unified calendar successfully eliminated venue reservation collisions and double-booking. (Status: FULLY VALIDATED)")
    add_bullet("Criterion 3 – Streamlined On-Duty Workflow: Digital roll-call check-in reduced the attendance regularization cycle from 4 days to instant, one-click PDF roster generation. (Status: FULLY VALIDATED)")
    add_bullet("Criterion 4 – Accreditation Compliance: Autonomous database aggregation structured participant metrics strictly aligned with NAAC Criterion 5.3 and NBA parameters. (Status: FULLY VALIDATED)")

    add_para(
        "All eight design challenge questions formulated during problem definition were comprehensively answered by specific technical implementations:"
    )
    add_bullet("1. Discoverability Challenge: Solved via the reactive, searchable Clubs & Cells Directory with tag-based domain filtering.")
    add_bullet("2. Venue Clash Challenge: Solved through PostgreSQL timestamp conflict validation functions preventing double-booking.")
    add_bullet("3. Attendance Integrity Challenge: Solved via coordinator-authenticated mobile digital roll-call rosters.")
    add_bullet("4. OD Regularization Delay: Solved via one-click cryptographically signed PDF On-Duty roster generation.")
    add_bullet("5. Communication Fragmentation: Solved through a unified broadcast announcements dashboard replacing ephemeral chat groups.")
    add_bullet("6. Accreditation Overhead: Solved through automated SQL aggregation queries generating instant semester-end NAAC audit reports.")
    add_bullet("7. User Accessibility: Solved via mobile-first, responsive Tailwind CSS styling delivering flawless cross-device performance.")
    add_bullet("8. Zero Capital Cost: Solved by leveraging open-source frameworks (React, Vite, TypeScript) and educational cloud tiers.")

    add_sec_heading("6.3", "SOFTWARE TESTING PROCEDURES AND TEST CASES")
    add_para(
        "To guarantee high operational reliability, zero security vulnerabilities, and rock-solid institutional data integrity, the system underwent "
        "rigorous testing across all functional modules. Testing methodologies encompassed unit testing of cryptographic token generation, end-to-end "
        "integration testing of atomic RSVP capacity counters, and comprehensive security penetration audits validating PostgreSQL Row-Level Security "
        "policies against privilege escalation attacks. Five core testing suites were formally executed and validated:"
    )
    add_bullet("TC-01 (Authentication): Verified student and faculty login flows. Password hashes verified via Bcrypt, JWT session issued, and routed to role portal. (Status: PASSED)")
    add_bullet("TC-02 (Role Security): Student account attempts unauthorized POST to faculty advisor endpoint. PostgreSQL RLS intercepts at engine level; returns HTTP 403 Forbidden. (Status: PASSED)")
    add_bullet("TC-03 (Capacity Quota): Simultaneous RSVP submissions when remaining venue capacity is one seat. Atomic transaction serializes requests; exactly one succeeds and UI updates to 'Full'. (Status: PASSED)")
    add_bullet("TC-04 (Venue Collision): Coordinator attempts to schedule event in occupied seminar hall. Conflict validation detects overlap, aborts transaction, and flags collision. (Status: PASSED)")
    add_bullet("TC-05 (Roll-Call & OD Export): Faculty coordinator marks roll-call on console and clicks 'Generate OD'. Status transitions to 'faculty_approved', generates cryptographic hash, and readies export. (Status: PASSED)")

    add_sec_heading("6.4", "DISCUSSION")
    add_subsec_heading("6.4.1", "Transformative Impact of the Human-Centered Approach")
    add_para(
        "The application of Design Thinking fundamentally elevated this project from a standard student web directory into an indispensable "
        "campus operational backbone. Conventional engineering projects often begin by immediately writing database tables and building generic CRUD "
        "(Create, Read, Update, Delete) forms. By forcing the team to immerse themselves in faculty staff rooms and student hostel lounges during "
        "the Empathize phase, the true emotional friction points were exposed. The discovery that obtaining manual signatures on paper On-Duty forms "
        "caused severe student anxiety directly inspired Module 4 (Mobile Roll-Call & Instant OD Generation). By focusing on this critical human pain, "
        "the resulting software delivered immediate, tangible institutional value."
    )

    add_subsec_heading("6.4.2", "Operational Strengths and Architectural Advantages")
    add_para(
        "The engineered solution demonstrates three decisive operational strengths when contrasted with legacy campus administrative practices:"
    )
    add_bullet("Paperless Velocity: Eliminates physical signature chasing, compressing event approval and OD processing from 4 days to instant transactions.")
    add_bullet("Democratized Visibility: Every student enjoys equal, transparent visibility into all 18+ college societies, eliminating closed departmental silos.")
    add_bullet("Auditable Governance: Provides institutional administrators with tamper-proof records for NAAC and NBA accreditation audits.")

    add_subsec_heading("6.4.3", "Technical Limitations and Architectural Trade-offs")
    add_para(
        "While the prototype exhibits robust performance across all target scenarios, three architectural trade-offs were consciously accepted during engineering:"
    )
    add_bullet("Network Connectivity Dependency: The cloud BaaS architecture requires continuous internet access for live roll-call and real-time calendar updates.")
    add_bullet("Third-Party ERP Interoperability: Direct automated sync with proprietary legacy college ERP databases requires establishing custom bi-directional webhooks.")
    add_bullet("Offline Token Synchronization: In venues with poor network coverage, offline roll-call caching requires subsequent manual resynchronization.")

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE WORK
    # =========================================================================
    doc.add_page_break()
    add_ch_title("7", "CONCLUSION AND FUTURE WORK")

    add_sec_heading("7.1", "CONCLUSION")
    add_para(
        "The Centralised Clubs and Cell Management System for Colleges successfully resolves decades-long administrative friction across autonomous "
        "higher educational institutions. By structuring the engineering lifecycle entirely through the human-centered Design Thinking methodology, "
        "the project addressed the authentic lived experiences of students, student coordinators, faculty advisors, and senior administrators. "
        "The resulting web application proves that open-source modern web technologies can entirely modernize campus extracurricular governance at zero "
        "recurring capital expenditure."
    )

    add_sec_heading("7.2", "FUTURE ENHANCEMENTS")
    add_para(
        "To build upon the operational foundation established by this prototype, four advanced technological enhancements are slated for future releases:"
    )
    add_bullet("Autonomous College ERP Webhook Integration: Establishing secure bi-directional REST webhooks with the central college ERP attendance database.")
    add_bullet("Dynamic QR-Code Ticket Scanning: Embedding time-based, cryptographically signed dynamic QR codes on student event RSVP passes for fraud-proof entry roll-call.")
    add_bullet("Automated Cryptographic Certificate Issuance: Generating personalized participant and winner certificates stamped with unique SHA-256 verification hashes.")
    add_bullet("Multi-College SaaS Scaling: Partitioning the cloud database schema to support multi-tenant SaaS deployments across autonomous engineering colleges.")

    # =========================================================================
    # BACK MATTER: APPENDIX - 1
    # =========================================================================
    doc.add_page_break()
    add_para("APPENDIX – 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=4, line_spacing=1.15)
    add_para("USER INTERVIEW DOCUMENTATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=16, line_spacing=1.15)
    add_para("The formal field interview was conducted in the Department of Information Technology at Kongu Engineering College. Below is the verified transcript record:")
    add_bullet("Interview Protocol: In-person semi-structured field interview conducted by Sahana S, Saran Karthik S, Sharan V, Vignesh M, and Murasoli B.")
    add_bullet("Interviewee Details: Dr. K. Sangeetha, Associate Professor & Co-curricular Convener, Department of Information Technology.")
    add_bullet("Q1. What is the biggest operational headache in running student clubs? — Response: Verifying physical attendance and chasing paper On-Duty forms across multiple faculty cabins.")
    add_bullet("Q2. How do you currently prevent schedule clashes between club events? — Response: Informal phone calls and checking physical notice boards, which frequently fails when two clubs book the same seminar hall.")
    add_bullet("Q3. How are student participation records compiled for NAAC/NBA? — Response: Faculty spend weeks manually counting signatures from paper sign-up sheets at the end of each academic year.")
    add_bullet("Q4. What is the most critical feature a digital platform should have? — Response: An instant, tamper-proof digital roll-call system that generates the approved OD roster the moment an event concludes.")
    add_bullet("Field Observation: The interviewee strongly endorsed the Centralised Clubs and Cell Management System prototype as an essential campus operational tool.")

    # =========================================================================
    # BACK MATTER: REFERENCES
    # =========================================================================
    doc.add_page_break()
    add_para("REFERENCES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    refs = [
        "[1]   T. Brown, “Design Thinking,” Harvard Business Review, vol. 86, no. 6, pp. 84–92, Jun. 2008.",
        "[2]   R. Razzouk and V. Shute, “What is design thinking and why is it important?,” Review of Educational Research, vol. 82, no. 3, pp. 330–348, Sep. 2012.",
        "[3]   National Assessment and Accreditation Council (NAAC), “Institutional Accreditation Manual for Autonomous Colleges: Criterion V – Student Support and Progression,” NAAC Guidelines, Bengaluru, India, 2024.",
        "[4]   National Board of Accreditation (NBA), “Manual for Accreditation of Undergraduate Engineering Programmes: Outcome Based Education Parameters,” New Delhi, India, 2023.",
        "[5]   A. Cooper, R. Reimann, D. Cronin, and C. Noessel, About Face: The Essentials of Interaction Design, 4th ed., Indianapolis, IN: John Wiley & Sons, 2014.",
        "[6]   E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns: Elements of Reusable Object-Oriented Software, Reading, MA: Addison-Wesley, 1994.",
        "[7]   M. Fowler, Patterns of Enterprise Application Architecture, Boston, MA: Addison-Wesley, 2002.",
        "[8]   Supabase Inc., “Supabase Documentation: Database Architecture and Row-Level Security Policies in PostgreSQL,” 2026. [Online]. Available: https://supabase.com/docs.",
        "[9]   React Core Team, “React 18 Documentation: Concurrent Features and Component Architecture,” Meta Platforms Inc., 2024. [Online]. Available: https://react.dev.",
        "[10]  Vite Core Team, “Vite: Next Generation Frontend Tooling,” 2024. [Online]. Available: https://vitejs.dev."
    ]
    for r_text in refs:
        p = add_para(r_text, space_before=0, space_after=6)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)

    # =========================================================================
    # BACK MATTER: MAPPING OF PROJECT GOALS TO SDG
    # =========================================================================
    doc.add_page_break()
    add_para("MAPPING OF PROJECT GOALS TO SDG", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    sdg_intro = (
        "The 17 Sustainable Development Goals (SDGs) adopted by all United Nations Member States in 2015 provide a shared "
        "blueprint for peace, prosperity, and institutional accountability. The Centralised Clubs and Cell Management System for Colleges "
        "(ClubHub) directly maps to and advances three critical Sustainable Development Goals:"
    )
    add_para(sdg_intro, space_before=0, space_after=12)

    sdgs = [
        ("SDG 4: Quality Education", [
            "Target 4.4 (Relevant Skills for Employment): Provides students with transparent access to technical societies, hackathons, and certified co-curricular events that foster coding, engineering innovation, and leadership skills essential for employment.",
            "Target 4.7 (Holistic Education): Encourages wide student participation across cultural clubs, environmental forums, and statutory cells (EDC, WDC, NSS), ensuring rounded character building and social responsibility."
        ]),
        ("SDG 9: Industry, Innovation and Infrastructure", [
            "Target 9.b (Domestic Technology Innovation): Demonstrates how frugal, open-source digital technologies (React, TypeScript, Supabase BaaS) can modernize campus administrative infrastructure with zero recurring software licensing fees.",
            "Target 9.c (Information & Communication Technology Access): Delivers a high-performance, mobile-responsive web platform ensuring all students—regardless of device ownership—enjoy equal access to campus co-curricular opportunities."
        ]),
        ("SDG 16: Peace, Justice and Strong Institutions", [
            "Target 16.6 (Effective, Accountable and Transparent Institutions): Replaces paper sign-up forms and closed-door approvals with an auditable, role-governed digital record, completely eliminating proxy attendance and ensuring transparent co-curricular governance.",
            "Target 16.10 (Public Access to Information): Guarantees that club recruitment criteria, leadership appointments, and event participation records are openly accessible and verifiable across the entire college community."
        ])
    ]

    for sdg_title, subpoints in sdgs:
        add_para(sdg_title, bold=True, size=13, space_before=8, space_after=4)
        for sp in subpoints:
            p = add_para(f"•   {sp}", space_before=0, space_after=4)
            p.paragraph_format.left_indent = Inches(0.3)

        targets = [
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_CORRECT_PAGES.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_8_TABLES.docx"
    ]
    for t in targets:
        try:
            doc.save(t)
            print("SUCCESS: Saved to", t)
        except Exception as e:
            print("Could not save to", t, ":", e)

if __name__ == "__main__":
    generate_master_final_report()
