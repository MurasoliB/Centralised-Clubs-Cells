import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_corrected_report():
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

    # 100% COMPLETE VISIBLE BORDERS (Outer box + inner horizontal + inner vertical)
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

    # Reference book-style table (Thick Top/Bottom, Inside Horizontal, NO vertical) for specific summary tables if needed, but user strictly requested:
    # "Add proper visible borders to ALL tables throughout the document. Every table must have: Outer border, Inner horizontal borders, Inner vertical borders."
    # So we apply set_full_visible_borders to ALL tables!

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

    def add_ch_title(ch_num, ch_title):
        doc.add_page_break()
        p1 = add_para(f"CHAPTER {ch_num}", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=18, space_after=4, line_spacing=1.15)
        p2 = add_para(ch_title, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=18, line_spacing=1.15)
        return p2

    def add_sec_heading(sec_num, sec_title):
        return add_para(f"{sec_num}   {sec_title}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=14, space_after=6, line_spacing=1.15)

    def add_subsec_heading(subsec_num, subsec_title):
        return add_para(f"{subsec_num}   {subsec_title}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=10, space_after=4, line_spacing=1.15)

    def add_table_title(tbl_num, tbl_name):
        return add_para(f"Table {tbl_num}   {tbl_name}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=11, space_before=14, space_after=6, line_spacing=1.15)

    # CLEAN EMPTY SPACE FOR IMAGE (NO BORDERS, NO DASHED BOXES, NO UNDERSCORES)
    def add_clean_figure_space(fig_num, fig_caption, empty_lines=12):
        # Insert clean empty paragraphs
        for _ in range(empty_lines):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run("")
            r.font.name = "Times New Roman"
        
        # Caption strictly below clean area
        fp = add_para(f"Figure {fig_num}   {fig_caption}", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=6, space_after=16, line_spacing=1.15)
        return fp

    print("Building expanded 42+ page document with all 7 corrections...")

    # =========================================================================
    # FRONT MATTER: 1. TITLE PAGE
    # =========================================================================
    add_para("CENTRALISED CLUBS AND CELL MANAGEMENT SYSTEM FOR COLLEGES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=18, space_after=14, line_spacing=1.2)
    add_para("DESIGN THINKING LABORATORY REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=4, line_spacing=1.15)
    add_para("(24ITL34 – DESIGN THINKING LABORATORY)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=0, space_after=18, line_spacing=1.15)
    
    add_para("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_before=0, space_after=8, line_spacing=1.15)

    # Team Members Table
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
    # FRONT MATTER: 6. TABLE OF CONTENTS (Pages vi-vii)
    # =========================================================================
    add_para("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False
    set_full_visible_borders(toc_table, border_sz="4")

    col_widths = [Inches(0.8), Inches(4.4), Inches(1.0)]
    hdr_cells = toc_table.rows[0].cells
    for idx, w in enumerate(col_widths):
        hdr_cells[idx].width = w; set_cell_margins(hdr_cells[idx])
    
    r0 = hdr_cells[0].paragraphs[0].add_run("S. NO."); r0.font.bold = True
    r1 = hdr_cells[1].paragraphs[0].add_run("TITLE"); r1.font.bold = True
    p_pg = hdr_cells[2].paragraphs[0]; p_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p_pg.add_run("PAGE NO."); r2.font.bold = True
    for c in hdr_cells:
        for r in c.paragraphs[0].runs: r.font.name = "Times New Roman"; r.font.size = Pt(11)

    toc_entries = [
        ("", "ABSTRACT", "iv", True, 0),
        ("", "ACKNOWLEDGEMENT", "v", True, 0),
        ("", "LIST OF TABLES", "viii", True, 0),
        ("", "LIST OF FIGURES", "ix", True, 0),
        ("", "LIST OF ABBREVIATIONS", "x", True, 0),
        ("1.", "INTRODUCTION", "1", True, 0),
        ("", "1.1   INTRODUCTION", "1", False, 1),
        ("", "1.2   OBJECTIVE", "3", False, 1),
        ("", "1.3   SCOPE", "4", False, 1),
        ("2.", "PROBLEM DEFINITION", "6", True, 0),
        ("", "2.1   EXISTING SYSTEM", "6", False, 1),
        ("", "2.2   PROBLEM STATEMENT", "8", False, 1),
        ("", "2.3   CONSTRAINTS", "9", False, 1),
        ("", "2.4   PEOPLE AFFECTED", "10", False, 1),
        ("", "2.5   DESIGN CHALLENGE", "11", False, 1),
        ("3.", "REQUIREMENTS AND ESTIMATES", "13", True, 0),
        ("", "3.1   HARDWARE REQUIREMENTS", "13", False, 1),
        ("", "3.2   SOFTWARE REQUIREMENTS", "14", False, 1),
        ("", "3.3   SOFTWARE DESCRIPTION", "16", False, 1),
        ("", "3.4   DATABASE DESIGN & SCHEMA SPECIFICATIONS", "18", False, 1),
        ("", "3.5   ESTIMATES", "21", False, 1),
        ("4.", "DESIGN THINKING PROCESS", "22", True, 0),
        ("", "4.1   OVERVIEW", "22", False, 1),
        ("", "4.2   PROBLEM IDENTIFICATION", "23", False, 1),
        ("", "4.3   EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "25", False, 1),
        ("", "4.4   EMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "30", False, 1),
        ("", "4.5   DEFINE: NEEDS, INSIGHTS AND PERSONA", "34", False, 1),
        ("", "4.6   IDEATE: STORYTELLING", "37", False, 1),
        ("5.", "PROTOTYPE IMPLEMENTATION", "39", True, 0),
        ("", "5.1   PROPOSED SYSTEM ARCHITECTURE", "39", False, 1),
        ("", "5.2   LOW-FIDELITY PROTOTYPE (EXERCISE 8)", "41", False, 1),
        ("", "5.3   MEDIUM-FIDELITY PROTOTYPE", "42", False, 1),
        ("", "5.4   DETAILED MODULE SPECIFICATIONS", "44", False, 1),
        ("6.", "RESULTS AND DISCUSSION", "47", True, 0),
        ("", "6.1   OUTCOMES OF THE DESIGN PROCESS", "47", False, 1),
        ("", "6.2   ASSESSMENT AGAINST THE SUCCESS CRITERIA", "48", False, 1),
        ("", "6.3   SOFTWARE TESTING PROCEDURES AND TEST CASES", "50", False, 1),
        ("", "6.4   DISCUSSION", "53", False, 1),
        ("7.", "CONCLUSION AND FUTURE WORK", "55", True, 0),
        ("", "APPENDIX – 1: USER INTERVIEW DOCUMENTATION", "57", True, 0),
        ("", "REFERENCES", "58", True, 0),
        ("", "MAPPING OF PROJECT GOALS TO SDG", "59", True, 0),
    ]

    for ch, title, pg, is_bld, ind in toc_entries:
        row_c = toc_table.add_row().cells
        for idx, w in enumerate(col_widths):
            row_c[idx].width = w; set_cell_margins(row_c[idx], top=40, bottom=40)
        
        p0 = row_c[0].paragraphs[0]; p0.paragraph_format.space_before = Pt(1); p0.paragraph_format.space_after = Pt(1)
        r = p0.add_run(ch); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = is_bld
        
        p1 = row_c[1].paragraphs[0]; p1.paragraph_format.space_before = Pt(1); p1.paragraph_format.space_after = Pt(1)
        if ind > 0: p1.paragraph_format.left_indent = Inches(0.2)
        r = p1.add_run(title); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = is_bld
        
        p2 = row_c[2].paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.paragraph_format.space_before = Pt(1); p2.paragraph_format.space_after = Pt(1)
        r = p2.add_run(pg); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = is_bld

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 7. LIST OF TABLES (Page viii)
    # =========================================================================
    add_para("LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    lot_table = doc.add_table(rows=1, cols=3)
    lot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(lot_table, border_sz="4")
    
    col_w_lot = [Inches(1.2), Inches(4.0), Inches(1.0)]
    hcells = lot_table.rows[0].cells
    for idx, w in enumerate(col_w_lot):
        hcells[idx].width = w; set_cell_margins(hcells[idx])
    
    hcells[0].paragraphs[0].add_run("TABLE NO.").font.bold = True
    hcells[1].paragraphs[0].add_run("TABLE NAME").font.bold = True
    p = hcells[2].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run("PAGE NO.").font.bold = True
    for c in hcells:
        for run in c.paragraphs[0].runs: run.font.name = "Times New Roman"; run.font.size = Pt(11)

    tables_data = [
        ("3.1", "Hardware requirements for clients and development environment", "13"),
        ("3.2", "Software tools, frameworks and cloud services", "14"),
        ("3.3", "Database schema: Organizations entity", "18"),
        ("3.4", "Database schema: Events entity", "19"),
        ("3.5", "Database schema: Memberships and Attendance entities", "20"),
        ("4.1", "Laboratory exercises mapped to design thinking phases", "22"),
        ("4.2", "Prioritised STEEP trends for club ecosystem", "27"),
        ("4.3", "Stakeholder classification and engagement strategy", "29"),
        ("4.4", "Profile of the primary stakeholder interviewee", "31"),
        ("4.5", "Post-interview synthesis and insight extraction", "33"),
        ("4.6", "SPICE analysis for Clubs and Cells Management System", "35"),
        ("4.7", "Persona summary: Active Student Leader & Campus Member", "36"),
        ("4.8", "Storyboard of the persona narrative", "38"),
        ("5.1", "Screens and functional modules of the web prototype", "43"),
        ("6.1", "Results of each design thinking phase", "47"),
        ("6.2", "Prototype assessment against success criteria", "48"),
        ("6.3", "Coverage of the design challenge questions", "49"),
        ("6.4", "Test cases for core authentication, RSVP, and roll-call modules", "51"),
        ("A1.1", "Formal interview record", "57")
    ]
    for t_num, t_name, t_pg in tables_data:
        rc = lot_table.add_row().cells
        for idx, w in enumerate(col_w_lot):
            rc[idx].width = w; set_cell_margins(rc[idx], top=40, bottom=40)
        p0 = rc[0].paragraphs[0]; p0.add_run(t_num).font.name = "Times New Roman"
        p1 = rc[1].paragraphs[0]; p1.add_run(t_name).font.name = "Times New Roman"
        p2 = rc[2].paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.add_run(t_pg).font.name = "Times New Roman"
        for cell in rc:
            for r in cell.paragraphs[0].runs: r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 8. LIST OF FIGURES (Page ix)
    # =========================================================================
    add_para("LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    lof_table = doc.add_table(rows=1, cols=3)
    lof_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(lof_table, border_sz="4")
    
    col_w_lof = [Inches(1.2), Inches(4.0), Inches(1.0)]
    hcells = lof_table.rows[0].cells
    for idx, w in enumerate(col_w_lof):
        hcells[idx].width = w; set_cell_margins(hcells[idx])
    
    hcells[0].paragraphs[0].add_run("FIGURE NO.").font.bold = True
    hcells[1].paragraphs[0].add_run("FIGURE NAME").font.bold = True
    p = hcells[2].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run("PAGE NO.").font.bold = True
    for c in hcells:
        for run in c.paragraphs[0].runs: run.font.name = "Times New Roman"; run.font.size = Pt(11)

    figures_data = [
        ("1.1", "System Architecture Diagram of the Centralised Management Ecosystem", "3"),
        ("1.2", "Overall System Workflow from Student Discovery to Attendance Clearance", "5"),
        ("2.1", "Use Case Diagram for Multi-Tier Stakeholder Roles", "8"),
        ("2.2", "Data Flow Diagram (Level 1) of Event Management and Attendance", "11"),
        ("3.1", "Entity Relationship Diagram (ERD) of PostgreSQL Relational Model", "17"),
        ("3.2", "Database Structure and Referential Integrity Relationships", "20"),
        ("4.1", "STEEP Analysis Framework for Campus Extracurricular Governance", "26"),
        ("4.2", "STEEP Prioritisation Matrix (Impact vs Likelihood)", "27"),
        ("4.3", "Activity System Map of the Clubs and Cells Management System", "28"),
        ("4.4", "Stakeholder Power-Interest Matrix", "29"),
        ("4.5", "Stakeholder Linkages and Communication Networks", "30"),
        ("4.6", "Empathy Map for Undergraduate Student Co-curricular Participation", "32"),
        ("4.7", "User Journey Map of Traditional Event Registration vs ClubHub Experience", "33"),
        ("4.8", "SPICE Needs Assessment Framework Canvas", "34"),
        ("4.9", "Student Leader and Active Participant Persona Canvas", "36"),
        ("4.10", "Five-Stage Narrative Storyboard Canvas", "38"),
        ("5.1", "Low-Fidelity Wireframe Architecture of the System", "41"),
        ("5.2", "Landing Page Interface with Single-Click Role Access", "42"),
        ("5.3", "Administrator and Executive Management Analytics Dashboard", "44"),
        ("5.4", "Faculty Coordinator Management and Event Approval Console", "45"),
        ("5.5", "Student Discovery Portal and Club Membership Recruitment Console", "45"),
        ("5.6", "Event Management and Capacity Reservation Hub", "46"),
        ("5.7", "Real-Time Digital Roll-Call and On-Duty Generation Console", "46")
    ]
    for f_num, f_name, f_pg in figures_data:
        rc = lof_table.add_row().cells
        for idx, w in enumerate(col_w_lof):
            rc[idx].width = w; set_cell_margins(rc[idx], top=40, bottom=40)
        p0 = rc[0].paragraphs[0]; p0.add_run(f_num).font.name = "Times New Roman"
        p1 = rc[1].paragraphs[0]; p1.add_run(f_name).font.name = "Times New Roman"
        p2 = rc[2].paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.add_run(f_pg).font.name = "Times New Roman"
        for cell in rc:
            for r in cell.paragraphs[0].runs: r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 9. LIST OF ABBREVIATIONS (Page x)
    # =========================================================================
    add_para("LIST OF ABBREVIATIONS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    abbr_table = doc.add_table(rows=0, cols=2)
    abbr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(abbr_table, border_sz="4")
    
    col_w_abbr = [Inches(1.8), Inches(4.4)]
    abbr_list = [
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
        rc = abbr_table.add_row().cells
        rc[0].width = col_w_abbr[0]; rc[1].width = col_w_abbr[1]
        set_cell_margins(rc[0], top=40, bottom=40); set_cell_margins(rc[1], top=40, bottom=40)
        r0 = rc[0].paragraphs[0].add_run(ab)
        r0.font.name = "Times New Roman"; r0.font.size = Pt(11); r0.font.bold = True
        r1 = rc[1].paragraphs[0].add_run(desc)
        r1.font.name = "Times New Roman"; r1.font.size = Pt(11)

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_ch_title("1", "INTRODUCTION")
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
    
    # Figure 1.1 Clean area
    add_clean_figure_space("1.1", "System Architecture Diagram of the Centralised Management Ecosystem", empty_lines=14)

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
    
    # Figure 1.2 Clean area
    add_clean_figure_space("1.2", "Overall System Workflow from Student Discovery to Attendance Clearance", empty_lines=14)

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

    # Figure 2.1 Clean area
    add_clean_figure_space("2.1", "Use Case Diagram for Multi-Tier Stakeholder Roles", empty_lines=14)

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

    # Figure 2.2 Clean area
    add_clean_figure_space("2.2", "Data Flow Diagram (Level 1) of Event Management and Attendance", empty_lines=14)

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
    h_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(h_table, border_sz="4")
    h_col_w = [Inches(1.8), Inches(1.8), Inches(2.6)]
    h_headers = ["Hardware Component", "Target User Group", "Functional Purpose"]
    for j, h in enumerate(h_headers):
        c = h_table.rows[0].cells[j]; c.width = h_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    h_data = [
        ("Mobile Smartphone / Tablet (Android / iOS)", "Students, Student Coordinators", "Accessing mobile-responsive web portal, discovering clubs, reserving event RSVPs, and conducting real-time roll-call attendance."),
        ("Desktop Computer / Laptop (Standard Browser)", "Faculty Advisors, College Administrators", "Managing institutional club appointments, approving event proposals, reviewing achievement submissions, and exporting accreditation dossiers."),
        ("Development Workstation (8GB RAM, Quad-Core CPU)", "Software Engineering Team", "Executing Vite development server, compiling TypeScript source modules, local database testing, and staging Supabase edge deployments.")
    ]
    for i, row in enumerate(h_data):
        for j, val in enumerate(row):
            c = h_table.rows[i+1].cells[j]; c.width = h_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("3.2", "SOFTWARE REQUIREMENTS")
    add_para(
        "To guarantee high concurrency, lightning-fast virtual DOM updates, and military-grade database security, the platform was developed "
        "utilizing the industry-standard software ecosystem detailed in Table 3.2."
    )
    
    add_table_title("3.2", "Software tools, frameworks and cloud services")
    s_table = doc.add_table(rows=8, cols=3)
    s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(s_table, border_sz="4")
    s_col_w = [Inches(1.6), Inches(2.2), Inches(2.4)]
    s_headers = ["Architectural Layer", "Technology Platform", "Functional Responsibility"]
    for j, h in enumerate(s_headers):
        c = s_table.rows[0].cells[j]; c.width = s_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    s_data = [
        ("Client Frontend Framework", "React 18 with TypeScript 5", "Component-based reactive single-page architecture enforcing strict compile-time type safety."),
        ("CSS Styling Architecture", "Tailwind CSS 3", "High-performance utility-first CSS engine customized with Wikipedia Vector academic theme."),
        ("Build Tool & Bundler", "Vite 5", "Next-generation native ES modules frontend development server and optimized production tree-shaking."),
        ("Client Routing System", "React Router DOM v7", "Declarative browser-side routing, query parameter synchronization, and role-protected route guards."),
        ("Data Visualization Engine", "Recharts Library", "SVG-driven analytics visualizations for membership demographics and event attendance ratios."),
        ("Cloud Backend Suite (BaaS)", "Supabase Platform", "Auto-generated REST APIs, secure user session management, and real-time database websockets."),
        ("Relational Database", "PostgreSQL Engine (RLS)", "ACID-compliant relational database enforcing granular Row-Level Security data protection policies.")
    ]
    for i, row in enumerate(s_data):
        for j, val in enumerate(row):
            c = s_table.rows[i+1].cells[j]; c.width = s_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    # Figure 3.1 Clean area
    add_clean_figure_space("3.1", "Entity Relationship Diagram (ERD) of PostgreSQL Relational Model", empty_lines=14)

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
        "The relational database schema was designed to support high transactional integrity across multi-tier stakeholder interactions. "
        "Tables 3.3, 3.4, and 3.5 detail the key relational entities, primary keys, foreign constraints, and attribute definitions."
    )

    add_table_title("3.3", "Database schema: Organizations entity")
    t33 = doc.add_table(rows=7, cols=4)
    t33.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(t33, border_sz="4")
    t33_hdrs = ["Attribute", "Data Type", "Constraint", "Description"]
    for j, h in enumerate(t33_hdrs):
        c = t33.rows[0].cells[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    t33_data = [
        ("id", "UUID", "PRIMARY KEY, DEFAULT gen_random_uuid()", "Unique system identifier for the club or cell."),
        ("name", "VARCHAR(150)", "NOT NULL, UNIQUE", "Official institutional title of the organization."),
        ("code", "VARCHAR(30)", "NOT NULL, UNIQUE", "Short alphanumeric acronym (e.g., CC, EDC, IIC)."),
        ("type", "VARCHAR(20)", "CHECK (type IN ('club', 'cell'))", "Categorization determining statutory governance level."),
        ("description", "TEXT", "NULLABLE", "Detailed charter, mandate, and objectives of the entity."),
        ("faculty_advisor_id", "UUID", "FOREIGN KEY -> profiles(id)", "Relational link to appointed faculty coordinator.")
    ]
    for i, row in enumerate(t33_data):
        for j, val in enumerate(row):
            c = t33.rows[i+1].cells[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_table_title("3.4", "Database schema: Events entity")
    t34 = doc.add_table(rows=8, cols=4)
    t34.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(t34, border_sz="4")
    for j, h in enumerate(t33_hdrs):
        c = t34.rows[0].cells[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    t34_data = [
        ("id", "UUID", "PRIMARY KEY, DEFAULT gen_random_uuid()", "Unique event transaction identifier."),
        ("organization_id", "UUID", "FOREIGN KEY -> organizations(id)", "Host club or statutory cell organizing the event."),
        ("title", "VARCHAR(200)", "NOT NULL", "Official title of symposium, workshop, or hackathon."),
        ("event_date", "TIMESTAMP WITH TIME ZONE", "NOT NULL", "Scheduled start timestamp for venue clash checking."),
        ("venue", "VARCHAR(100)", "NOT NULL", "Sanctioned campus venue (e.g., IT Seminar Hall)."),
        ("capacity", "INTEGER", "NOT NULL, CHECK (capacity > 0)", "Strict maximum attendee quota preventing overcrowding."),
        ("status", "VARCHAR(20)", "DEFAULT 'draft'", "Lifecycle state (draft, published, completed, cancelled).")
    ]
    for i, row in enumerate(t34_data):
        for j, val in enumerate(row):
            c = t34.rows[i+1].cells[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    # Figure 3.2 Clean area
    add_clean_figure_space("3.2", "Database Structure and Referential Integrity Relationships", empty_lines=14)

    add_table_title("3.5", "Database schema: Memberships and Attendance entities")
    t35 = doc.add_table(rows=7, cols=4)
    t35.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(t35, border_sz="4")
    for j, h in enumerate(t33_hdrs):
        c = t35.rows[0].cells[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    t35_data = [
        ("membership_id", "UUID", "PRIMARY KEY", "Unique student club enrollment record."),
        ("user_id", "UUID", "FOREIGN KEY -> profiles(id)", "Registered student applicant identifier."),
        ("membership_status", "VARCHAR(20)", "DEFAULT 'applied'", "Onboarding state (applied, reviewed, inducted, rejected)."),
        ("attendance_id", "UUID", "PRIMARY KEY", "Unique event roll-call ledger entry."),
        ("event_id", "UUID", "FOREIGN KEY -> events(id)", "Event associated with the roll-call record."),
        ("od_status", "VARCHAR(20)", "DEFAULT 'pending'", "Official On-Duty regularization state (pending, approved, synchronized).")
    ]
    for i, row in enumerate(t35_data):
        for j, val in enumerate(row):
            c = t35.rows[i+1].cells[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

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
    dt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(dt_table, border_sz="4")
    dt_col_w = [Inches(0.8), Inches(2.2), Inches(1.3), Inches(1.9)]
    dt_hdrs = ["Ex. No.", "Exercise Name", "Design Phase", "Key Concrete Artifacts Produced"]
    for j, h in enumerate(dt_hdrs):
        c = dt_table.rows[0].cells[j]; c.width = dt_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    dt_data = [
        ("1", "Identify Problem & Project Scope", "Problem Framing", "Situation analysis, operational constraints, affected stakeholders, workflow diagram."),
        ("2", "User Research using Explore Tools", "Explore", "STEEP trend matrix, organization activity map, stakeholder influence matrices, project brief."),
        ("4", "Customer Interview & User Mapping", "Empathize", "Empathy map canvas, student journey map, field interview notes, post-interview synthesis."),
        ("5", "User Persona & Need Formulation", "Define", "SPICE framework analysis, user need statements, core insight statement, persona canvas."),
        ("7", "User Scenario & Storytelling", "Ideate", "5-stage narrative storyboard canvas contrasting manual struggle with digital resolution."),
        ("8", "Low-Fidelity Wireframe Prototyping", "Prototype", "Three paper-style architectural layout wireframes establishing UI flow."),
        ("9", "Medium-Fidelity Web Implementation", "Prototype / Test", "Fully functional 11-module reactive single page web application with live cloud database.")
    ]
    for i, row in enumerate(dt_data):
        for j, val in enumerate(row):
            c = dt_table.rows[i+1].cells[j]; c.width = dt_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_sec_heading("4.2", "PROBLEM IDENTIFICATION")
    add_para(
        "Laboratory Exercise 1 crystallized the core operational bottlenecks observed within the college campus. Rather than viewing "
        "extracurricular management as a set of static web pages, the team analyzed the complete end-to-end operational flow. Figure 4.1 "
        "illustrates the high-level workflow envisioned during this initial framing exercise. When a student opens the portal, they are presented "
        "with an authoritative directory of recognized clubs and cells. They can review upcoming event schedules, execute single-click RSVP reservations, "
        "and present digital passes during event check-in. Simultaneously, authorized student coordinators conduct digital roll-calls, and faculty "
        "advisors endorse verified attendance records that instantly translate into sanctioned On-Duty approvals."
    )

    add_sec_heading("4.3", "EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)")
    add_subsec_heading("4.3.1", "STEEP Trends Analysis")
    add_para(
        "To comprehend the macro-environmental forces impacting collegiate co-curricular administration, an exhaustive STEEP analysis "
        "(Social, Technological, Economic, Environmental, Political/Regulatory) was conducted, as visualized in Figure 4.1."
    )
    
    # Figure 4.1 Clean area
    add_clean_figure_space("4.1", "STEEP Analysis Framework for Campus Extracurricular Governance", empty_lines=14)

    steep_expanded = [
        ("Social and Demographic Trends:", "Undergraduate engineering students increasingly expect high-speed, consumer-grade digital experiences mirroring commercial web applications. Having grown up with intuitive mobile software, they exhibit low tolerance for physical paper bureaucracy, long administrative queues, and fragmented notice boards. Furthermore, students place immense value upon peer collaboration, technical community building, and verified digital portfolios that enhance their competitiveness during corporate campus placement interviews."),
        ("Technological Trends:", "Pervasive 5G and high-speed campus Wi-Fi connectivity, coupled with ubiquitous smartphone ownership among college students, create an ideal substrate for real-time cloud computing. Modern reactive frontend frameworks (React, Vite) and serverless cloud databases (Supabase, PostgreSQL) enable the development of zero-latency, mobile-responsive single-page applications capable of managing concurrent event registrations and instant roll-call updates."),
        ("Economic Trends:", "Operating a collegiate institution involves continuous optimization of operational expenditure. Traditional extracurricular administration consumes vast quantities of paper reams, physical printing cartridges, and administrative labor dedicated to transcribing records. A centralized digital operating system completely eliminates printing overheads, conserves administrative person-hours, and prevents fiscal waste associated with disorganized event planning."),
        ("Environmental Trends:", "Higher educational institutions are under institutional and civic pressure to embrace green campus initiatives and reduce their carbon footprint. Traditional paper notices, paper registration forms, printed hall passes, and manual attendance sheets generate substantial recurring paper waste. Transitioning to a paperless cloud platform directly advances campus environmental sustainability and environmental governance."),
        ("Political, Statutory and Accreditation Trends:", "National accreditation agencies, including the National Assessment and Accreditation Council (NAAC) under Criterion 5, the National Board of Accreditation (NBA), and national ranking bodies (NIRF), mandate that educational institutions provide verifiable, auditable records of student co-curricular activities, leadership development programs, and community engagement. Failure to produce authenticated event rosters during accreditation committee visits threatens institutional standing.")
    ]
    for t, d in steep_expanded:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    add_subsec_heading("4.3.2", "STEEP Matrix and Trend Prioritization")
    add_para(
        "The identified trends were plotted across an Impact versus Likelihood Prioritization Matrix (Figure 4.2). The highest priority trends—demanding "
        "immediate architectural accommodation—were categorized in Table 4.2."
    )
    
    # Figure 4.2 Clean area
    add_clean_figure_space("4.2", "STEEP Prioritisation Matrix (Impact vs Likelihood)", empty_lines=14)

    add_table_title("4.2", "Prioritised STEEP trends for club ecosystem")
    stp_table = doc.add_table(rows=5, cols=3)
    stp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(stp_table, border_sz="4")
    stp_col_w = [Inches(1.8), Inches(1.8), Inches(2.6)]
    stp_hdrs = ["Quadrant", "Prioritized Trend", "Strategic Architectural Implication"]
    for j, h in enumerate(stp_hdrs):
        c = stp_table.rows[0].cells[j]; c.width = stp_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    stp_data = [
        ("High Impact / Likely to Occur", "Paperless campus drive & digital convenience demand", "The platform must be 100% paperless; all onboarding, event RSVPs, and roll-calls must execute natively in the browser."),
        ("High Impact / Likely to Occur", "Stringent NAAC/NBA co-curricular audit scrutiny", "Database must store immutable audit logs and support single-click export of Criterion 5 compliance reports."),
        ("High Impact / Uncertain", "Adoption velocity among senior faculty advisors", "The user interface must adopt a calm, utilitarian Wikipedia Vector aesthetic that requires zero specialized technical training."),
        ("Low Impact / Likely to Occur", "Mobile-first student browsing patterns", "Frontend layouts must be fluidly responsive across mobile viewports to enable instant roll-calls inside seminar halls.")
    ]
    for i, row in enumerate(stp_data):
        for j, val in enumerate(row):
            c = stp_table.rows[i+1].cells[j]; c.width = stp_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_subsec_heading("4.3.3", "Activity System Mapping")
    add_para(
        "The Activity System Map (Figure 4.3) articulated the institutional mission of the project: “To establish a centralized, auditable, "
        "and human-centered digital operating environment that unifies club administration, event orchestration, attendance roll-calls, "
        "and achievement tracking across Kongu Engineering College.” Four core operational strategies were architected: (1) Identify Stakeholder Needs, "
        "(2) Map and Structure Campus Entities, (3) Engineer the Unified Management Portal, and (4) Automate Compliance and Accreditation."
    )
    
    # Figure 4.3 Clean area
    add_clean_figure_space("4.3", "Activity System Map of the Clubs and Cells Management System", empty_lines=14)

    add_subsec_heading("4.3.4", "Stakeholder Mapping and Engagement Strategies")
    add_para(
        "Extracurricular administration touches diverse institutional personas. Stakeholders were mapped by interest and influence (Figure 4.4) "
        "and relational communication networks (Figure 4.5). Table 4.3 codifies the stakeholder engagement protocol."
    )
    
    # Figure 4.4 Clean area
    add_clean_figure_space("4.4", "Stakeholder Power-Interest Matrix", empty_lines=14)

    # Figure 4.5 Clean area
    add_clean_figure_space("4.5", "Stakeholder Linkages and Communication Networks", empty_lines=14)

    add_table_title("4.3", "Stakeholder classification and engagement strategy")
    stk_table = doc.add_table(rows=5, cols=3)
    stk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(stk_table, border_sz="4")
    stk_col_w = [Inches(1.8), Inches(2.0), Inches(2.4)]
    stk_hdrs = ["Influence / Interest", "Stakeholder Personas", "System Engagement Protocol"]
    for j, h in enumerate(stk_hdrs):
        c = stk_table.rows[0].cells[j]; c.width = stk_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    stk_data = [
        ("High Interest / High Influence", "College Principal, Department Heads, IQAC / NAAC Coordinators, Faculty Advisors", "Manage Closely: Conduct iterative review sessions, standardize accreditation report schemas, and validate role-based permissions."),
        ("High Interest / Low Influence", "General Undergraduate Students, Club Members, Event Attendees", "Keep Satisfied: Deliver lightning-fast mobile responsiveness, instant event RSVPs, transparent recruitment vetting, and immediate On-Duty letters."),
        ("Low Interest / High Influence", "Institutional IT & Central ERP System Administrators", "Keep Informed: Establish clean RESTful synchronization protocols to allow seamless ingestion of On-Duty attendance records into central ledgers."),
        ("Low Interest / Low Influence", "External Accreditation Inspectors, Alumni Network, Event Sponsors", "Monitor: Provide authenticated verification portals allowing external entities to validate student achievement certificates via unique hashes.")
    ]
    for i, row in enumerate(stk_data):
        for j, val in enumerate(row):
            c = stk_table.rows[i+1].cells[j]; c.width = stk_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_sec_heading("4.4", "EMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)")
    add_para(
        "To avoid designing based upon detached assumptions, Laboratory Exercise 4 engaged directly with real users within their authentic "
        "operational environment. An Empathy Map (Figure 4.6) was synthesized to explore what campus users think, feel, say, do, hear, and see. "
        "Concurrently, a User Journey Map (Figure 4.7) charted the emotional trajectory of students attempting to register for hackathons and "
        "secure On-Duty approvals under current manual methods."
    )
    
    # Figure 4.6 Clean area
    add_clean_figure_space("4.6", "Empathy Map for Undergraduate Student Co-curricular Participation", empty_lines=14)

    # Figure 4.7 Clean area
    add_clean_figure_space("4.7", "User Journey Map of Traditional Event Registration vs ClubHub Experience", empty_lines=14)

    add_subsec_heading("4.4.1", "Primary Stakeholder Interview Record")
    add_para(
        "A formal semi-structured interview was conducted inside the Department of Information Technology at Kongu Engineering College "
        "by project team members Sahana S, Saran Karthik S, Sharan V, Vignesh M, and Murasoli B. Table 4.4 details the profile of the primary interviewee."
    )
    
    add_table_title("4.4", "Profile of the primary stakeholder interviewee")
    int_table = doc.add_table(rows=7, cols=2)
    int_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(int_table, border_sz="4")
    int_col_w = [Inches(2.0), Inches(4.2)]
    
    int_data = [
        ("Interviewee Name", "Dr. K. Sangeetha / Active Student Coordinator"),
        ("Designation / Role", "Faculty In-Charge, Technical Coding Club & Assistant Professor (Dept. of IT)"),
        ("Institution", "Kongu Engineering College (Autonomous), Perundurai, Erode"),
        ("Professional Background", "8+ years in engineering education; 4 years managing departmental technical student associations"),
        ("Core Responsibilities", "Overseeing club operational budgets, sanctioning event proposals, verifying On-Duty eligibility, compiling annual audit logs"),
        ("Interview Setting & Date", "22.10.2026; IT Department Faculty Room & Laboratories, Kongu Engineering College")
    ]
    for i, (k, v) in enumerate(int_data):
        c0 = int_table.rows[i].cells[0]; c0.width = int_col_w[0]; set_cell_margins(c0)
        c0.paragraphs[0].add_run(k).font.bold = True
        c1 = int_table.rows[i].cells[1]; c1.width = int_col_w[1]; set_cell_margins(c1)
        c1.paragraphs[0].add_run(v)
        for c in [c0, c1]:
            for r in c.paragraphs[0].runs: r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_subsec_heading("4.4.2", "Post-Interview Discussion and Synthesis")
    add_para(
        "The qualitative feedback gathered during the interview was transcribed, categorized, and synthesized into core design takeaways, "
        "as codified in Table 4.5."
    )
    
    add_table_title("4.5", "Post-interview synthesis and insight extraction")
    syn_table = doc.add_table(rows=5, cols=3)
    syn_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(syn_table, border_sz="4")
    syn_col_w = [Inches(1.8), Inches(2.2), Inches(2.2)]
    syn_hdrs = ["Analytical Dimension", "Empirical Field Observations", "Actionable Architectural Response"]
    for j, h in enumerate(syn_hdrs):
        c = syn_table.rows[0].cells[j]; c.width = syn_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    syn_data = [
        ("Faculty Workload Burden", "Faculty advisors spend hours reviewing physical paper On-Duty applications during short class intervals, disrupting academic preparation.", "Implement one-click bulk digital On-Duty sanctioning derived directly from verified roll-call rosters."),
        ("Attendance Inaccuracy & Proxies", "Paper sign-in sheets passed through large lecture halls result in proxy signatures and illegible roll numbers.", "Provide authorized coordinators with a real-time checkbox roll-call interface tied to authenticated student accounts."),
        ("Accreditation Audit Stress", "During NAAC/NBA inspection cycles, faculty coordinators spend weeks manually aggregating disparate event reports and photos.", "Build an automated executive reporting engine that compiles Criterion 5 compliance tables in a single click."),
        ("Core Human Takeaway", "Faculty and students do not resist administrative governance; they are simply exhausted by manual physical friction.", "Engineer a calm, utilitarian Wikipedia Vector interface that delivers immediate operational relief.")
    ]
    for i, row in enumerate(syn_data):
        for j, val in enumerate(row):
            c = syn_table.rows[i+1].cells[j]; c.width = syn_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_sec_heading("4.5", "DEFINE: NEEDS, INSIGHTS AND PERSONA")
    add_subsec_heading("4.5.1", "SPICE Framework Analysis")
    add_para(
        "To uncover deep subconscious needs beyond superficial operational requests, the interview data was analyzed across the five dimensions "
        "of the SPICE framework (Social, Physical, Identity, Communication, Emotional), illustrated in Figure 4.8 and Table 4.6."
    )
    
    # Figure 4.8 Clean area
    add_clean_figure_space("4.8", "SPICE Needs Assessment Framework Canvas", empty_lines=14)

    add_table_title("4.6", "SPICE analysis for Clubs and Cells Management System")
    spc_table = doc.add_table(rows=6, cols=2)
    spc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(spc_table, border_sz="4")
    spc_col_w = [Inches(1.8), Inches(4.4)]
    spc_hdrs = ["SPICE Dimension", "Underlying Human Need & Engineering Response"]
    for j, h in enumerate(spc_hdrs):
        c = spc_table.rows[0].cells[j]; c.width = spc_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    spc_data = [
        ("Social Dimension", "Community & Cross-Departmental Peer Collaboration: Students crave a transparent platform to discover technical groups, connect with senior mentors, and collaborate across departmental boundaries without artificial administrative silos."),
        ("Physical Dimension", "Zero Paperwork & Elimination of Physical Lines: Eradication of paper circulars, physical notice-board checking, manual sign-in sheets, and exhausting corridor queues outside faculty staff rooms."),
        ("Identity Dimension", "Accredited Professional Reputation: Students desire a verified digital identity showcasing certified club memberships, event achievements, and validated leadership portfolios that authenticate their co-curricular credentials."),
        ("Communication Dimension", "Instant, Unambiguous Institutional Broadcasts: Real-time notification streams regarding event schedule changes, venue confirmations, application review statuses, and On-Duty clearance approvals."),
        ("Emotional Dimension", "Relief, Confidence & Psychological Security: Complete removal of the constant fear of being marked absent in academic courses during approved events, replaced by confidence in an accountable digital system.")
    ]
    for i, row in enumerate(spc_data):
        for j, val in enumerate(row):
            c = spc_table.rows[i+1].cells[j]; c.width = spc_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_subsec_heading("4.5.2", "Persona Canvas Formulation")
    add_para(
        "The synthesis of user research culminated in the definition of a primary user persona: Arun Kumar, a dedicated third-year "
        "undergraduate engineering student and aspiring student leader (Figure 4.9, Table 4.7)."
    )
    
    # Figure 4.9 Clean area
    add_clean_figure_space("4.9", "Student Leader and Active Participant Persona Canvas", empty_lines=14)

    add_table_title("4.7", "Persona summary: Active Student Leader & Campus Member")
    per_table = doc.add_table(rows=8, cols=2)
    per_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(per_table, border_sz="4")
    per_col_w = [Inches(2.0), Inches(4.2)]
    
    per_data = [
        ("Demographic Profile", "Arun Kumar; 20 Years Old; 3rd Year B.Tech Information Technology; Kongu Engineering College; Active campus member."),
        ("Core Objectives", "Eager to join premier technical societies, lead hackathon initiatives, and accumulate verified co-curricular achievements for placement."),
        ("Primary Frustrations", "Misses club inductions due to unread notice-board posters; experiences severe stress when paper OD forms are delayed, causing attendance shortages."),
        ("Technology Habits", "Heavy smartphone user; expects instant mobile-responsive interfaces; impatient with slow, paper-bound administrative bureaucracy."),
        ("Campus Lifestyle", "Resides in college hostel; balances rigorous academic coursework with evening technical club hackathons and peer coding projects."),
        ("Emotional State", "Motivated and ambitious, but frequently disheartened by bureaucratic red tape and the physical chore of securing faculty signatures."),
        ("Deep Unmet Need", "A unified digital platform where he can discover campus clubs, reserve event passes in one click, and receive automated On-Duty credit.")
    ]
    for i, (k, v) in enumerate(per_data):
        c0 = per_table.rows[i].cells[0]; c0.width = per_col_w[0]; set_cell_margins(c0)
        c0.paragraphs[0].add_run(k).font.bold = True
        c1 = per_table.rows[i].cells[1]; c1.width = per_col_w[1]; set_cell_margins(c1)
        c1.paragraphs[0].add_run(v)
        for c in [c0, c1]:
            for r in c.paragraphs[0].runs: r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("4.6", "IDEATE: STORYTELLING")
    add_para(
        "To translate persona needs into functional software specifications, the team formulated an empathetic narrative storyboard canvas "
        "(Figure 4.10). The storyboard visualizes Arun's campus life across five distinct chronological stages (Table 4.8), highlighting how "
        "ClubHub transforms administrative frustration into streamlined co-curricular empowerment."
    )
    
    # Figure 4.10 Clean area
    add_clean_figure_space("4.10", "Five-Stage Narrative Storyboard Canvas", empty_lines=14)

    add_table_title("4.8", "Storyboard of the persona narrative")
    sty_table = doc.add_table(rows=6, cols=2)
    sty_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(sty_table, border_sz="4")
    sty_col_w = [Inches(1.8), Inches(4.4)]
    sty_hdrs = ["Narrative Phase", "Detailed User Journey Storyline"]
    for j, h in enumerate(sty_hdrs):
        c = sty_table.rows[0].cells[j]; c.width = sty_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    sty_data = [
        ("1. The Persona", "Arun, an enthusiastic undergraduate student passionate about artificial intelligence and open-source software, seeking to expand his skills through active club participation."),
        ("2. The Setting", "A bustling autonomous college campus housing over 40 clubs and cells, where announcements are pinned to physical boards and registrations require paper slips."),
        ("3. The Conflict", "Arun misses a flagship regional hackathon because the notice board was in another building, and for a workshop he did attend, his paper OD slip was lost, causing him to be marked absent."),
        ("4. The Intervention (ClubHub)", "Arun logs into ClubHub, views a unified calendar of upcoming events, reserves a confirmed seat with one click, and receives a digital entry pass on his smartphone."),
        ("5. The Resolution", "At the workshop, the coordinator checks Arun in on a tablet; an authenticated On-Duty clearance is instantly generated and synchronized with the college ERP. Arun receives a verified digital achievement badge.")
    ]
    for i, row in enumerate(sty_data):
        for j, val in enumerate(row):
            c = sty_table.rows[i+1].cells[j]; c.width = sty_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    # =========================================================================
    # CHAPTER 5: PROTOTYPE IMPLEMENTATION
    # =========================================================================
    add_ch_title("5", "PROTOTYPE IMPLEMENTATION")
    add_sec_heading("5.1", "PROPOSED SYSTEM ARCHITECTURE")
    add_para(
        "The proposed Centralised Clubs and Cell Management System (ClubHub) is architected as an enterprise-grade, three-tier cloud web application. "
        "The architecture rigorously decouples the client presentation tier from the backend API gateway and the relational persistence database. "
        "The presentation tier executes natively within modern web browsers using React 18, TypeScript, and Tailwind CSS. The middle application "
        "tier utilizes Supabase's high-speed auto-generated PostgREST engine, which translates client REST queries into optimized SQL executions. "
        "The persistence tier is anchored by a PostgreSQL relational engine executing Row-Level Security (RLS) policies and automated triggers."
    )

    add_sec_heading("5.2", "LOW-FIDELITY PROTOTYPE (EXERCISE 8)")
    add_para(
        "To test structural information hierarchy prior to software engineering, a low-fidelity wireframe prototype was created in Laboratory "
        "Exercise 8 (Figure 5.1). The paper prototype established three critical user touchpoints: (1) Unified Directory Layout, "
        "(2) Event RSVP Reservation Card, and (3) Digital Roll-Call / On-Duty Generation Panel. Usability testing with student peers confirmed "
        "that single-click primary actions, clean tabular data grids, and rectangular button geometry minimized cognitive friction."
    )
    
    # Figure 5.1 Clean area
    add_clean_figure_space("5.1", "Low-Fidelity Wireframe Architecture of the System", empty_lines=14)

    add_sec_heading("5.3", "MEDIUM-FIDELITY PROTOTYPE")
    add_para(
        "The medium-fidelity prototype was engineered as a production-ready single page application. Table 5.1 details the functional modules "
        "and corresponding screens implemented within the platform."
    )
    
    add_table_title("5.1", "Screens and functional modules of the web prototype")
    mod_table = doc.add_table(rows=8, cols=3)
    mod_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(mod_table, border_sz="4")
    mod_col_w = [Inches(1.8), Inches(2.2), Inches(2.2)]
    mod_hdrs = ["Interface / Module", "Core Technical Capabilities", "Operational Need Addressed"]
    for j, h in enumerate(mod_hdrs):
        c = mod_table.rows[0].cells[j]; c.width = mod_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    mod_data = [
        ("Portal Landing Page (Fig. 5.2)", "Executive Wikipedia Vector header, institution branding badge, single-click demo role logins, and quick feature index.", "Authoritative, welcoming entry portal ensuring immediate authentication access across roles."),
        ("Executive Analytics Dashboard (Fig. 5.3)", "Real-time metrics: active organizations, upcoming symposia, membership totals, participation ratios, and audit logs.", "High-level institutional governance and live activity monitoring for administrators."),
        ("Faculty Management Hub (Fig. 5.4)", "Event sanctioning console, faculty appointment interface, roster authorization, and achievement verification panel.", "Streamlined faculty governance eliminating manual physical signature seeking."),
        ("Clubs & Cells Directory (Fig. 5.5)", "Searchable catalog of 18+ technical societies and cells, category filters, leadership lists, and 1-click recruitment modal.", "Centralized discovery, breaking departmental information silos and paper inductions."),
        ("Event Scheduling & RSVP Hub (Fig. 5.6)", "Calendar scheduling, automated venue clash detection, attendee capacity limits, RSVP ticketing, and digital pass generation.", "Orderly event coordination preventing venue overcrowding and chaotic lines."),
        ("Real-Time Roll-Call & OD Console (Fig. 5.7)", "Interactive mobile checkbox attendance roster generating authenticated On-Duty clearance records for ERP sync.", "Tamper-proof attendance logging and instant academic On-Duty regularization."),
        ("Verified Achievement Portfolio Vault", "Digital credentials repository where students upload certificates, validated by faculty to generate an authenticated portfolio.", "Accredited student co-curricular record enhancing placement credentials.")
    ]
    for i, row in enumerate(mod_data):
        for j, val in enumerate(row):
            c = mod_table.rows[i+1].cells[j]; c.width = mod_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    # Figures 5.2 to 5.7 Clean areas
    add_clean_figure_space("5.2", "Landing Page Interface with Single-Click Role Access", empty_lines=14)
    add_clean_figure_space("5.3", "Administrator and Executive Management Analytics Dashboard", empty_lines=14)
    add_clean_figure_space("5.4", "Faculty Coordinator Management and Event Approval Console", empty_lines=14)
    add_clean_figure_space("5.5", "Student Discovery Portal and Club Membership Recruitment Console", empty_lines=14)
    add_clean_figure_space("5.6", "Event Management and Capacity Reservation Hub", empty_lines=14)
    add_clean_figure_space("5.7", "Real-Time Digital Roll-Call and On-Duty Generation Console", empty_lines=14)

    add_sec_heading("5.4", "DETAILED MODULE SPECIFICATIONS")
    add_subsec_heading("5.4.1", "Module 1: Authentication and Role-Based Access Control (RBAC)")
    add_para(
        "The authentication module leverages Supabase Auth backed by cryptographically signed JSON Web Tokens (JWT). Users authenticate using their "
        "official institutional email address. Upon successful credential verification, the system inspects the user's role stored in the profiles "
        "table and injects corresponding role claims. The application router evaluates these claims, dynamically restricting unauthorized navigation "
        "and rendering specialized portal interfaces tailored to Administrators, Faculty Advisors, Student Coordinators, or General Students."
    )
    add_subsec_heading("5.4.2", "Module 2: Organization Catalog and Membership Lifecycle")
    add_para(
        "This module manages the operational directory of campus organizations. Each club or cell record maintains descriptive metadata, category "
        "classification, assigned faculty coordinators, and active student office bearers. Students can submit digital membership applications "
        "directly through the interface. Coordinators access a dedicated review pipeline allowing them to transition applications across structured "
        "stages (Applied, Under Review, Interview Scheduled, and Inducted). Once inducted, the student's profile is automatically synchronized with "
        "the active membership roster."
    )
    add_subsec_heading("5.4.3", "Module 3: Conflict-Free Event Management and Quota RSVPs")
    add_para(
        "Event planning is centralized to eliminate venue scheduling clashes. When a coordinator drafts an event, the system executes an automated "
        "SQL verification to confirm that the requested venue (e.g., IT Seminar Hall) is not already booked during the selected timestamp. "
        "Furthermore, coordinators specify a strict attendee capacity cap. When students reserve seats, atomic database transactions decrement "
        "available slots. When the capacity is reached, the RSVP button automatically switches to a waitlist state, preventing hall overcrowding."
    )
    add_subsec_heading("5.4.4", "Module 4: Mobile Roll-Call and Instant On-Duty (OD) Generation")
    add_para(
        "During live event execution, authorized student coordinators access the Real-Time Roll-Call Console on their mobile smartphones or tablets. "
        "The console displays the pre-registered attendee list. Coordinators verify student presence with a single touch on the attendance checkbox. "
        "Upon concluding the roll-call, the system locks the attendance ledger and automatically formats an authenticated On-Duty clearance letter "
        "containing student roll numbers, event title, date, and verified timestamps. This document is routed digitally to the faculty advisor for "
        "instant electronic endorsement, eliminating days of corridor paperwork."
    )
    add_subsec_heading("5.4.5", "Module 5: Executive Analytics and NAAC/NBA Compliance Suite")
    add_para(
        "The compliance suite aggregates transactional records into structured institutional reports. Administrators can filter co-curricular "
        "data by department, academic year, or organization type. In a single click, the module exports comprehensive dossiers formatted specifically "
        "to satisfy NAAC Criterion 5.3 (Student Participation and Activities) and NBA Outcome-Based Education documentation parameters."
    )

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # =========================================================================
    add_ch_title("6", "RESULTS AND DISCUSSION")
    add_sec_heading("6.1", "OUTCOMES OF THE DESIGN PROCESS")
    add_para(
        "The disciplined execution of the Design Thinking methodology ensured that technical implementations were continually validated "
        "against user needs. Table 6.1 traces the direct evolutionary link between laboratory research artifacts and final prototype capabilities."
    )
    
    add_table_title("6.1", "Results of each design thinking phase")
    res_table = doc.add_table(rows=7, cols=3)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(res_table, border_sz="4")
    res_col_w = [Inches(1.8), Inches(2.2), Inches(2.2)]
    res_hdrs = ["Design Thinking Phase", "Artifact Produced", "Influence on Final Solution"]
    for j, h in enumerate(res_hdrs):
        c = res_table.rows[0].cells[j]; c.width = res_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    res_data = [
        ("Problem Framing", "Constraints, affected people, estimates, scope.", "Established core mandate: 4-tier role-based governance with zero licensing costs."),
        ("Explore", "STEEP trends, activity system map, stakeholder maps.", "Identified paperless campus drive and NAAC compliance as primary drivers."),
        ("Empathize", "Empathy map, journey map, faculty interview.", "Uncovered severe On-Duty signature friction and proxy attendance concerns."),
        ("Define", "SPICE framework, need statements, student persona.", "Prioritized real-time roll-call and automated OD letter generation."),
        ("Ideate", "Storyboard canvas tracing persona life cycle.", "Structured user journey from discovery to certified achievement storage."),
        ("Prototype & Test", "Low-fidelity wireframes and reactive web application.", "Delivered working portal with live Supabase authentication and PostgreSQL RLS.")
    ]
    for i, row in enumerate(res_data):
        for j, val in enumerate(row):
            c = res_table.rows[i+1].cells[j]; c.width = res_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_sec_heading("6.2", "ASSESSMENT AGAINST THE SUCCESS CRITERIA")
    add_para(
        "The functional capabilities of the engineered prototype were evaluated against the success criteria stipulated in the initial project brief "
        "(Table 6.2) and the seven core design challenge questions (Table 6.3)."
    )
    
    add_table_title("6.2", "Prototype assessment against success criteria")
    suc_table = doc.add_table(rows=5, cols=3)
    suc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(suc_table, border_sz="4")
    suc_col_w = [Inches(2.0), Inches(2.6), Inches(1.6)]
    suc_hdrs = ["Success Criterion", "Evidence in Working Prototype", "Validation Status"]
    for j, h in enumerate(suc_hdrs):
        c = suc_table.rows[0].cells[j]; c.width = suc_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    suc_data = [
        ("Centralized Discovery & Access", "Unified directory of 18+ campus clubs & cells with active leader portfolios and recruitment forms.", "Validated in Prototype"),
        ("Eradication of Paperwork", "Digital membership screening, quota event RSVPs, and paperless roll-calls.", "Fully Addressed"),
        ("Automated On-Duty Processing", "Instant roll-call checkbox logging generating authenticated OD participant rosters.", "Validated with Faculty"),
        ("Accreditation Audit Readiness", "1-click data export dossiers matching NAAC Criterion 5 and NBA evaluation parameters.", "Operational")
    ]
    for i, row in enumerate(suc_data):
        for j, val in enumerate(row):
            c = suc_table.rows[i+1].cells[j]; c.width = suc_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_table_title("6.3", "Coverage of the design challenge questions")
    cov_table = doc.add_table(rows=8, cols=2)
    cov_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(cov_table, border_sz="4")
    cov_col_w = [Inches(2.6), Inches(3.6)]
    cov_hdrs = ["Design Challenge Question", "Implementation Solution"]
    for j, h in enumerate(cov_hdrs):
        c = cov_table.rows[0].cells[j]; c.width = cov_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    cov_data = [
        ("1. Single-source club directory", "Directory module with instant search, category filtering, and leadership contacts."),
        ("2. Paperless membership recruitment", "Digital application pipeline with multi-stage review (Applied, Review, Admitted)."),
        ("3. Event clash & quota management", "Event scheduler enforcing venue clash validation and automatic attendee limits."),
        ("4. Tamper-proof attendance & OD", "Live roll-call interface instantly compiling authenticated OD attendance sheets."),
        ("5. Verified achievement portfolios", "Achievement vault with faculty advisor verification and student digital badges."),
        ("6. Four-tier role security (RBAC)", "PostgreSQL Row-Level Security (RLS) policies guarding all database tables."),
        ("7. One-click NAAC/NBA compliance", "Executive reporting module exporting Criterion 5 compliant metrics and logs.")
    ]
    for i, row in enumerate(cov_data):
        for j, val in enumerate(row):
            c = cov_table.rows[i+1].cells[j]; c.width = cov_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

    add_sec_heading("6.3", "SOFTWARE TESTING PROCEDURES AND TEST CASES")
    add_para(
        "To verify reliability and security, the system underwent comprehensive software testing, including unit testing of authentication "
        "tokens, integration testing of event RSVP quotas, and security audit testing of database Row-Level Security policies. "
        "Table 6.4 documents the execution and results of key test cases."
    )

    add_table_title("6.4", "Test cases for core authentication, RSVP, and roll-call modules")
    tst_table = doc.add_table(rows=6, cols=5)
    tst_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(tst_table, border_sz="4")
    tst_col_w = [Inches(0.8), Inches(1.4), Inches(1.8), Inches(1.4), Inches(0.8)]
    tst_hdrs = ["Test ID", "Module Under Test", "Test Scenario & Input", "Expected System Behavior", "Result"]
    for j, h in enumerate(tst_hdrs):
        c = tst_table.rows[0].cells[j]; c.width = tst_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    tst_data = [
        ("TC-01", "Authentication", "Valid institutional email and correct password entered.", "Authenticate user, issue signed JWT, redirect to role-specific dashboard.", "PASS"),
        ("TC-02", "Role Authorization", "Student account attempts unauthorized POST to faculty appointment endpoint.", "PostgreSQL RLS policy blocks transaction; returns 403 Forbidden.", "PASS"),
        ("TC-03", "Event Capacity Cap", "Student attempts RSVP after capacity counter reaches configured maximum.", "Atomic transaction blocks registration; UI disables button and displays 'Full'.", "PASS"),
        ("TC-04", "Venue Clash Check", "Coordinator attempts to schedule event in occupied seminar hall at same time.", "System validation detects overlap; displays conflict error with conflicting event title.", "PASS"),
        ("TC-05", "Roll-Call & OD Sync", "Coordinator marks attendance on roll-call console and clicks 'Generate OD'.", "Attendance marked 'present'; verified On-Duty roster compiled with immutable timestamp.", "PASS")
    ]
    for i, row in enumerate(tst_data):
        for j, val in enumerate(row):
            c = tst_table.rows[i+1].cells[j]; c.width = tst_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(10)

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
        "The engineered system possesses several decisive operational strengths: (1) Zero Recurring Software Licensing: Built entirely upon "
        "open-source technologies and free-tier cloud architectures, the system imposes zero operational cost upon college budgets. "
        "(2) Strict Relational Security: Leveraging PostgreSQL Row-Level Security guarantees that student data and attendance ledgers cannot be "
        "tampered with, even if client-side code is examined. (3) Universally Accessible Wikipedia Vector Design: The clean, utilitarian UI guarantees "
        "instant visual comprehension across first-year students and senior faculty alike. (4) Direct Accreditation Utility: The ability to export "
        "NAAC Criterion 5 compliance dossiers in a single click relieves faculty advisors of weeks of manual administrative burden."
    )
    add_subsec_heading("6.4.3", "System Limitations")
    add_para(
        "While highly effective, the current prototype exhibits certain operational boundaries: (1) Active Internet Requirement: The application "
        "relies upon continuous cloud synchronization with Supabase, requiring an active internet or campus Wi-Fi connection. (2) Pre-Configured "
        "Role Mapping: Institutional roles are currently provisioned through administrative console management rather than automated real-time "
        "directory federation. (3) Academic ERP Integration: Although On-Duty documents are generated in standardized digital formats, automated "
        "database injection into the college's legacy ERP requires dedicated institutional middleware authorization."
    )

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE WORK
    # =========================================================================
    add_ch_title("7", "CONCLUSION AND FUTURE WORK")
    add_para(
        "This project successfully applied the human-centered Design Thinking methodology to solve the chronic administrative fragmentation, "
        "attendance vulnerabilities, and bureaucratic delays surrounding collegiate extracurricular governance. By systematically navigating through "
        "macro-environmental trend exploration, deep stakeholder empathy interviews, need framing via SPICE, narrative storyboarding, and rapid "
        "iterative prototyping, the team engineered the Centralised Clubs and Cell Management System for Colleges (ClubHub)."
    )
    add_para(
        "The engineered single-page web platform unifies over 40 diverse technical clubs and statutory cells into an interactive digital directory, "
        "automates candidate onboarding, orchestrates conflict-free event scheduling with intelligent venue clash prevention, enforces tamper-proof "
        "mobile roll-call attendance, and completely eradicates corridor signature queues through instant digital On-Duty generation. Furthermore, "
        "by archiving verified student achievements and providing single-click compliance reporting for NAAC Criterion 5 and NBA accreditation reviews, "
        "ClubHub transforms extracurricular administration from an exhausting bureaucratic chore into an auditable institutional asset."
    )
    add_para("Planned future enhancements include:", bold=True, space_before=6, space_after=4)
    future_work = [
        ("Direct Autonomous College ERP Webhook Integration:", "Establishing secure bi-directional REST webhooks with the central Autonomous College ERP attendance database to automatically update daily course attendance ledgers the moment a faculty coordinator electronically signs an On-Duty roster."),
        ("Dynamic QR-Code Ticket Scanning:", "Embedding time-based, cryptographically signed dynamic QR codes on student event RSVP passes, scanned instantaneously using coordinator smartphone cameras at the auditorium entrance for zero-contact, fraud-proof roll-call validation."),
        ("Automated Cryptographic Certificate Issuance:", "Integrating a headless vector graphics rendering service that dynamically generates personalized participant and tournament winner certificates stamped with unique cryptographic SHA-256 verification hashes."),
        ("Multi-College Multi-Tenant Cloud Scaling:", "Partitioning the Supabase cloud database schema to support multi-tenant SaaS deployments across autonomous engineering colleges and state universities throughout Tamil Nadu under a unified co-curricular network.")
    ]
    for t, d in future_work:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    # =========================================================================
    # BACK MATTER: APPENDIX - 1
    # =========================================================================
    doc.add_page_break()
    add_para("APPENDIX – 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=4, line_spacing=1.15)
    add_para("USER INTERVIEW DOCUMENTATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=16, line_spacing=1.15)
    
    add_para(
        "The formal record of the primary stakeholder field interview conducted during Laboratory Exercise 4 is documented in Table A1.1. "
        "The interview protocol was structured directly from the combined empathy map and student journey map."
    )
    
    add_table_title("A1.1", "Interview record")
    app_table = doc.add_table(rows=8, cols=2)
    app_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_full_visible_borders(app_table, border_sz="4")
    app_col_w = [Inches(2.0), Inches(4.2)]
    
    app_data = [
        ("Interviewers (Project Team)", "Sahana S (25ITR121), Saran Karthik S (25ITR128), Sharan V (25ITR134), Vignesh M (25ITR171), Murasoli B (25ITL188)"),
        ("Interviewee Persona", "Dr. K. Sangeetha, Faculty Advisor, Technical Coding Club & Assistant Professor, Department of IT, KEC"),
        ("Date and Setting", "22.10.2026; IT Staff Room & Laboratory Complex, Kongu Engineering College"),
        ("Primary Observation 1", "Students lose substantial academic learning time chasing physical signatures across department buildings for On-Duty leave forms."),
        ("Primary Observation 2", "Faculty coordinators lack unified digital records; compiling participant rosters and photos for NAAC audits requires weeks of manual effort."),
        ("What Went Well", "The interviewee shared practical administrative pain points openly, confirmed proxy attendance concerns, and strongly endorsed a digital roll-call system."),
        ("What Did Not Go Well", "Obtaining precise statistical counts of annual club attendance records was impossible because physical paper logs had been archived or discarded."),
        ("Actionable Design Decisions", "Built instant mobile roll-call logging, automated On-Duty PDF generation, and one-click NAAC Criterion 5 data export into the prototype.")
    ]
    for i, (k, v) in enumerate(app_data):
        c0 = app_table.rows[i].cells[0]; c0.width = app_col_w[0]; set_cell_margins(c0)
        c0.paragraphs[0].add_run(k).font.bold = True
        c1 = app_table.rows[i].cells[1]; c1.width = app_col_w[1]; set_cell_margins(c1)
        c1.paragraphs[0].add_run(v)
        for c in [c0, c1]:
            for r in c.paragraphs[0].runs: r.font.name = "Times New Roman"; r.font.size = Pt(11)

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

    out_final = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx"
    doc.save(out_final)
    print("SUCCESS: Generated complete corrected document at:", out_final)

if __name__ == "__main__":
    build_corrected_report()
