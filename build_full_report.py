import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def generate_report():
    doc = docx.Document()

    # Define color constants
    COLOR_BLACK = RGBColor(0, 0, 0)

    # 1. Page Margins Setup: A4, Left 1.25", Top 1.0", Right 1.0", Bottom 1.0"
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        # uncheck different first page if needed or handle headers
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

    # Helper function for setting cell margins & borders
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

    def set_table_borders(table, border_color="000000", border_sz="4"):
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(r'''
            <w:tblBorders %s>
                <w:top w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:bottom w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:insideH w:val="single" w:sz="%s" w:space="0" w:color="%s"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''' % (nsdecls('w'), border_sz, border_color, border_sz, border_color, border_sz, border_color))
        tblPr.append(tblBorders)

    def set_full_box_table_borders(table, border_color="000000", border_sz="4"):
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
        ''' % (nsdecls('w'), border_sz, border_color, border_sz, border_color, border_sz, border_color, border_sz, border_color, border_sz, border_color, border_sz, border_color))
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

    def add_ch_title(ch_num, ch_title):
        p1 = add_para(f"CHAPTER {ch_num}", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=12, space_after=4, line_spacing=1.15)
        p2 = add_para(ch_title, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=18, line_spacing=1.15)
        return p2

    def add_sec_heading(sec_num, sec_title):
        return add_para(f"{sec_num}   {sec_title}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=12, space_after=6, line_spacing=1.15)

    def add_subsec_heading(subsec_num, subsec_title):
        return add_para(f"{subsec_num}   {subsec_title}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=8, space_after=4, line_spacing=1.15)

    def add_table_title(tbl_num, tbl_name):
        p = add_para(f"Table {tbl_num}   {tbl_name}", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=11, space_before=12, space_after=6, line_spacing=1.15)
        return p

    def add_figure_placeholder(fig_num, fig_caption, height_inches=3.0):
        # Create a blank box table representing the figure area for manual insertion
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(5.8)
        
        # Border dashed / light gray box
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(r'''
            <w:tcBorders %s>
                <w:top w:val="dashed" w:sz="4" w:space="0" w:color="A0A0A0"/>
                <w:left w:val="dashed" w:sz="4" w:space="0" w:color="A0A0A0"/>
                <w:bottom w:val="dashed" w:sz="4" w:space="0" w:color="A0A0A0"/>
                <w:right w:val="dashed" w:sz="4" w:space="0" w:color="A0A0A0"/>
            </w:tcBorders>
        ''' % nsdecls('w'))
        tcPr.append(tcBorders)
        
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(height_inches * 30)
        cp.paragraph_format.space_after = Pt(height_inches * 30)
        r = cp.add_run(f"[ BLANK IMAGE SPACE FOR: {fig_caption.upper()} ]")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.italic = True
        r.font.color.rgb = RGBColor(128, 128, 128)
        
        # Caption below figure
        fp = add_para(f"Figure {fig_num}   {fig_caption}", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_before=6, space_after=14, line_spacing=1.15)
        return tbl, fp

    print("Framework initialized. Writing report sections...")

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
    set_full_box_table_borders(tm_table, border_sz="4")
    
    headers = ["S. No.", "Name", "Register Number"]
    col_w = [Inches(0.8), Inches(3.2), Inches(1.8)]
    for j, h in enumerate(headers):
        cell = tm_table.rows[0].cells[j]
        cell.width = col_w[j]
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = COLOR_BLACK

    tm_data = [
        ("1", "SAHANA S", "25ITR121"),
        ("2", "SARAN KARTHIK S", "25ITR128"),
        ("3", "SHARAN V", "25ITR134"),
        ("4", "VIGNESH M", "25ITR171"),
        ("5", "MURASOLI B", "25ITL188")
    ]
    for i, row in enumerate(tm_data):
        for j, val in enumerate(row):
            cell = tm_table.rows[i+1].cells[j]
            cell.width = col_w[j]
            set_cell_margins(cell, top=60, bottom=60, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.bold = (j == 1)
            r.font.color.rgb = COLOR_BLACK

    add_para("in partial fulfilment of the requirements for the award of the degree of", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_before=16, space_after=4, line_spacing=1.15)
    add_para("BACHELOR OF TECHNOLOGY IN\nINFORMATION TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=0, space_after=14, line_spacing=1.15)
    add_para("DEPARTMENT OF INFORMATION TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=0, space_after=10, line_spacing=1.15)
    
    # Institution info
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
    
    sig_p = add_para("SUPERVISOR\t\t\t\t\tHEAD OF THE DEPARTMENT", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=True, size=12, space_before=20, space_after=4, line_spacing=1.15)
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
    
    # Transparent borders
    tblPr = toc_table._tbl.tblPr
    tblBorders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
            <w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(tblBorders)

    col_widths = [Inches(0.6), Inches(4.6), Inches(1.0)]
    hdr_cells = toc_table.rows[0].cells
    for idx, w in enumerate(col_widths):
        hdr_cells[idx].width = w
    
    hdr_cells[0].paragraphs[0].text = ""
    r1 = hdr_cells[1].paragraphs[0].add_run("TITLE")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.bold = True
    p_pg = hdr_cells[2].paragraphs[0]
    p_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p_pg.add_run("PAGE NO.")
    r2.font.name = "Times New Roman"; r2.font.size = Pt(12); r2.font.bold = True

    toc_entries = [
        ("", "ABSTRACT", "iv", True, 0),
        ("", "ACKNOWLEDGEMENT", "v", True, 0),
        ("", "LIST OF TABLES", "viii", True, 0),
        ("", "LIST OF FIGURES", "ix", True, 0),
        ("", "LIST OF ABBREVIATIONS", "x", True, 0),
        ("1.", "INTRODUCTION", "1", True, 0),
        ("", "1.1   INTRODUCTION", "1", False, 1),
        ("", "1.2   OBJECTIVE", "2", False, 1),
        ("", "1.3   SCOPE", "3", False, 1),
        ("2.", "PROBLEM DEFINITION", "4", True, 0),
        ("", "2.1   EXISTING SYSTEM", "4", False, 1),
        ("", "2.2   PROBLEM STATEMENT", "4", False, 1),
        ("", "2.3   CONSTRAINTS", "5", False, 1),
        ("", "2.4   PEOPLE AFFECTED", "5", False, 1),
        ("", "2.5   DESIGN CHALLENGE", "6", False, 1),
        ("3.", "REQUIREMENTS AND ESTIMATES", "7", True, 0),
        ("", "3.1   HARDWARE REQUIREMENTS", "7", False, 1),
        ("", "3.2   SOFTWARE REQUIREMENTS", "7", False, 1),
        ("", "3.3   SOFTWARE DESCRIPTION", "8", False, 1),
        ("", "3.4   ESTIMATES", "9", False, 1),
        ("4.", "DESIGN THINKING PROCESS", "10", True, 0),
        ("", "4.1   OVERVIEW", "10", False, 1),
        ("", "4.2   PROBLEM IDENTIFICATION", "11", False, 1),
        ("", "4.3   EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "12", False, 1),
        ("", "4.4   EMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "19", False, 1),
        ("", "4.5   DEFINE: NEEDS, INSIGHTS AND PERSONA", "24", False, 1),
        ("", "4.6   IDEATE: STORYTELLING", "27", False, 1),
        ("5.", "PROTOTYPE IMPLEMENTATION", "29", True, 0),
        ("", "5.1   PROPOSED SYSTEM", "29", False, 1),
        ("", "5.2   LOW-FIDELITY PROTOTYPE (EXERCISE 8)", "29", False, 1),
        ("", "5.3   MEDIUM-FIDELITY PROTOTYPE", "30", False, 1),
        ("6.", "RESULTS AND DISCUSSION", "34", True, 0),
        ("", "6.1   OUTCOMES OF THE DESIGN PROCESS", "34", False, 1),
        ("", "6.2   ASSESSMENT AGAINST THE SUCCESS CRITERIA", "35", False, 1),
        ("", "6.3   DISCUSSION", "36", False, 1),
        ("7.", "CONCLUSION AND FUTURE WORK", "38", True, 0),
        ("", "APPENDIX – 1: USER INTERVIEW DOCUMENTATION", "39", True, 0),
        ("", "REFERENCES", "40", True, 0),
        ("", "MAPPING OF PROJECT GOALS TO SDG", "41", True, 0),
    ]

    for ch, title, pg, is_bld, ind in toc_entries:
        row_c = toc_table.add_row().cells
        for idx, w in enumerate(col_widths):
            row_c[idx].width = w
        
        p0 = row_c[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(2); p0.paragraph_format.space_after = Pt(2)
        r = p0.add_run(ch)
        r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.bold = is_bld
        
        p1 = row_c[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(2); p1.paragraph_format.space_after = Pt(2)
        if ind > 0:
            p1.paragraph_format.left_indent = Inches(0.2)
        r = p1.add_run(title)
        r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.bold = is_bld
        
        p2 = row_c[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_before = Pt(2); p2.paragraph_format.space_after = Pt(2)
        r = p2.add_run(pg)
        r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.bold = is_bld

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 7. LIST OF TABLES (Page viii)
    # =========================================================================
    add_para("LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    lot_table = doc.add_table(rows=1, cols=3)
    lot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lot_table)
    
    col_w_lot = [Inches(1.2), Inches(4.0), Inches(1.0)]
    hcells = lot_table.rows[0].cells
    hcells[0].paragraphs[0].add_run("TABLE NO.").font.bold = True
    hcells[1].paragraphs[0].add_run("TABLE NAME").font.bold = True
    p = hcells[2].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run("PAGE NO.").font.bold = True
    for c in hcells:
        for run in c.paragraphs[0].runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

    tables_data = [
        ("3.1", "Hardware requirements", "7"),
        ("3.2", "Software tools and platforms", "7"),
        ("4.1", "Laboratory exercises mapped to design thinking phases", "10"),
        ("4.2", "Prioritised STEEP trends for club ecosystem", "13"),
        ("4.3", "Stakeholder classification and engagement strategy", "15"),
        ("4.4", "Profile of the interviewee", "22"),
        ("4.5", "Post-interview synthesis", "23"),
        ("4.6", "SPICE analysis for Clubs and Cells Management System", "24"),
        ("4.7", "Persona summary: Active Student Leader & Campus Member", "26"),
        ("4.8", "Storyboard of the persona", "27"),
        ("5.1", "Screens and functional modules of the web prototype", "30"),
        ("6.1", "Results of each design thinking phase", "34"),
        ("6.2", "Prototype assessment against success criteria", "35"),
        ("6.3", "Coverage of the design challenge questions", "35"),
        ("A1.1", "Interview record", "39")
    ]
    for t_num, t_name, t_pg in tables_data:
        rc = lot_table.add_row().cells
        set_cell_margins(rc[0]); set_cell_margins(rc[1]); set_cell_margins(rc[2])
        p0 = rc[0].paragraphs[0]; p0.add_run(t_num).font.name = "Times New Roman"
        p1 = rc[1].paragraphs[0]; p1.add_run(t_name).font.name = "Times New Roman"
        p2 = rc[2].paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.add_run(t_pg).font.name = "Times New Roman"
        for cell in rc:
            for r in cell.paragraphs[0].runs:
                r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 8. LIST OF FIGURES (Page ix)
    # =========================================================================
    add_para("LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    lof_table = doc.add_table(rows=1, cols=3)
    lof_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lof_table)
    
    hcells = lof_table.rows[0].cells
    hcells[0].paragraphs[0].add_run("FIGURE NO.").font.bold = True
    hcells[1].paragraphs[0].add_run("FIGURE NAME").font.bold = True
    p = hcells[2].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run("PAGE NO.").font.bold = True
    for c in hcells:
        for run in c.paragraphs[0].runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

    figures_data = [
        ("4.1", "Workflow of Centralised Clubs and Cell Management System", "11"),
        ("4.2", "STEEP analysis for campus clubs and cells challenge", "12"),
        ("4.3", "STEEP analysis matrix", "14"),
        ("4.4", "Activity system map for Clubs and Cells Management System", "15"),
        ("4.5", "Stakeholder mapping matrix", "16"),
        ("4.6", "Stakeholder links and relationship mapping", "17"),
        ("4.7", "Stakeholder priority mapping matrix", "18"),
        ("4.8", "Reframing the opportunities", "19"),
        ("4.9", "Empathy map used to generate interview questions", "20"),
        ("4.10", "Journey map of a student participating in club activities", "21"),
        ("4.11", "Combined empathy map and user journey", "21"),
        ("4.12", "Geo-tagged photograph of team with interviewee at KEC", "22"),
        ("4.13", "SPICE framework for understanding deep user needs", "25"),
        ("4.14", "Persona canvas", "26"),
        ("4.15", "Storyboard canvas for the persona", "28"),
        ("5.1", "Low-fidelity screens: discovery, event RSVP and OD tracker", "30"),
        ("5.2", "Landing page of the prototype", "31"),
        ("5.3", "Administrator and coordinator analytics dashboard", "32"),
        ("5.4", "Clubs and cells directory with active membership application", "32"),
        ("5.5", "Event creation and real-time attendance roll-call interface", "33")
    ]
    for f_num, f_name, f_pg in figures_data:
        rc = lof_table.add_row().cells
        set_cell_margins(rc[0]); set_cell_margins(rc[1]); set_cell_margins(rc[2])
        p0 = rc[0].paragraphs[0]; p0.add_run(f_num).font.name = "Times New Roman"
        p1 = rc[1].paragraphs[0]; p1.add_run(f_name).font.name = "Times New Roman"
        p2 = rc[2].paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.add_run(f_pg).font.name = "Times New Roman"
        for cell in rc:
            for r in cell.paragraphs[0].runs:
                r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: 9. LIST OF ABBREVIATIONS (Page x)
    # =========================================================================
    add_para("LIST OF ABBREVIATIONS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    abbr_table = doc.add_table(rows=0, cols=2)
    abbr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(abbr_table)
    
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
        set_cell_margins(rc[0]); set_cell_margins(rc[1])
        r0 = rc[0].paragraphs[0].add_run(ab)
        r0.font.name = "Times New Roman"; r0.font.size = Pt(11); r0.font.bold = True
        r1 = rc[1].paragraphs[0].add_run(desc)
        r1.font.name = "Times New Roman"; r1.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION (Page 1)
    # =========================================================================
    add_ch_title("1", "INTRODUCTION")
    add_sec_heading("1.1", "INTRODUCTION")
    
    p_intro_1 = (
        "Higher educational institutions foster dynamic student extracurricular ecosystems composed of both specialized "
        "Clubs (such as coding forums, robotics societies, cultural troupes, literature circles, and fine arts clubs) and "
        "mandated statutory Cells (including the Institution's Innovation Council - IIC, Entrepreneurship Development Cell - EDC, "
        "Women Development Cell - WDC, National Service Scheme - NSS, and Youth Red Cross). These extracurricular bodies are "
        "indispensable to the holistic growth of undergraduate students, serving as vital incubators for technical ingenuity, "
        "managerial competencies, ethical awareness, and leadership capabilities. Furthermore, documented student involvement "
        "in registered clubs and certified participation in institutional symposiums represent critical benchmark data required "
        "for statutory accreditations under NAAC Criterion 5 (Student Support and Progression), NBA Outcome-Based Education parameters, "
        "and national ranking evaluations under NIRF."
    )
    p_intro_2 = (
        "In institutional campuses such as Kongu Engineering College (Autonomous), over 40 distinct clubs, technical societies, "
        "and cells actively function across multiple academic departments. Traditionally, the governance and administration of these "
        "entities are performed via highly fragmented, legacy operational pathways. Notice circulars are physically printed or "
        "disseminated casually via unindexed social media groups (e.g., WhatsApp, Telegram). Membership sign-ups, event registrations, "
        "seat quotas, and roll-calls are collected manually across disparate Google Forms or physical paper logs. Crucially, when students "
        "participate in inter-college hackathons or campus symposiums, securing official academic On-Duty (OD) regularization requires "
        "physically obtaining sequential signatures from Student Coordinators, Faculty Advisors, Head of Department, and Academic Deans. "
        "This laborious procedure frequently causes missing attendance records, administrative backlogs, and lost credentials."
    )
    p_intro_3 = (
        "This project was executed as part of the 24ITL34 – Design Thinking Laboratory course. Design Thinking is a creative, "
        "human-centered, iterative methodology that tackles ill-defined societal and operational challenges by transitioning "
        "through the rigorous phases of empathizing with real users, defining actionable core problems, ideating viable alternatives, "
        "and developing testable prototypes. Rather than imposing technology arbitrarily, the team commenced by deeply studying "
        "the human stakeholders: undergraduate students seeking skill enrichment, student office bearers overwhelmed by logistics, "
        "faculty advisors burdened by compliance audits, and academic administrators overseeing quality metrics. The outcome is "
        "the Centralised Clubs and Cell Management System for Colleges (ClubHub), an integrated digital operating system designed "
        "to unify campus extracurricular life into an efficient, transparent, and auditable web platform."
    )
    add_para(p_intro_1)
    add_para(p_intro_2)
    add_para(p_intro_3)

    add_para("The principal contributions of this work are:", bold=True, space_before=6, space_after=6)
    contribs = [
        "A structured systemic exploration of campus extracurricular administration using STEEP analysis, activity system mapping, and stakeholder interest-influence matrices.",
        "Primary user research conducted through empathy maps, user journey maps, and field interviews with institutional stakeholders, synthesized using the SPICE framework and detailed personas.",
        "Comprehensive ideation via scenario storytelling and storyboard canvases tracing end-to-end user workflows before and after the digital intervention.",
        "Low-fidelity architectural wireframes and an engineered, functional medium-fidelity web application built on modern reactive full-stack technologies (React, TypeScript, Tailwind CSS, Vite, Supabase, PostgreSQL).",
        "A verifiable On-Duty (OD) and accreditation framework directly mapped to United Nations Sustainable Development Goals (SDG 4, SDG 9, and SDG 16)."
    ]
    for c in contribs:
        p = add_para(f"•   {c}", space_before=0, space_after=4)
        p.paragraph_format.left_indent = Inches(0.3)

    add_sec_heading("1.2", "OBJECTIVE")
    obj_p = (
        "The overarching objective of this project is to research, design, and prototype a centralized, accessible, "
        "and role-governed digital web portal that streamlines the operational lifecycle of all campus clubs and cells, "
        "eliminates paper-based processes, guarantees transparent event management, and automates attendance and accreditation "
        "tracking. The specific objectives driving the system design include:"
    )
    add_para(obj_p)
    
    specific_objs = [
        ("Centralize Discovery:", "Provide a unified digital directory showcasing all campus clubs and cells, their leadership portfolios, mandates, membership eligibility, and social links."),
        ("Streamline Recruitment:", "Enable online membership applications with automated portfolio generation and transparent screening stages (Applied, Under Review, Interview, Admitted)."),
        ("Orchestrate Events:", "Deliver an administrative scheduling hub with automated venue clash detection, attendee capacity quotas, RSVP reservations, and downloadable hall passes."),
        ("Automate On-Duty (OD):", "Facilitate real-time roll-call attendance logging that automatically generates certified OD student lists for instant academic regularization with ERP systems."),
        ("Authenticate Achievements:", "Implement a digital verification vault where tournament winners and attendees upload credentials for faculty advisor verification, establishing an authenticated portfolio."),
        ("Ensure Compliance:", "Provide one-click export of structured reports and visual analytics formatted specifically for NAAC Criterion 5, NBA accreditation visits, and internal audits.")
    ]
    for title, desc in specific_objs:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(f"•   {title} ")
        r1.font.name = "Times New Roman"; r1.font.bold = True
        r2 = p.add_run(desc)
        r2.font.name = "Times New Roman"

    add_sec_heading("1.3", "SCOPE")
    scope_p = (
        "The project scope encompasses the full Design Thinking cycle from human context exploration to medium-fidelity prototype "
        "development and deployment. The solution is planned to scale through progressive institutional tiers:"
    )
    add_para(scope_p)
    scopes = [
        ("Institutional Pilot Scope:", "Deployment within Kongu Engineering College across its active department clubs (Information Technology, Computer Science, EEE, Mechanical, Civil) and central cells (EDC, IIC, Women Development Cell, NSS)."),
        ("Autonomous Campus Expansion Scope:", "Interfacing with the central College ERP attendance database to automatically synchronize sanctioned On-Duty approvals directly with course attendance ledgers."),
        ("Inter-Collegiate Consortium Scope:", "Extending the platform architecture as a multi-tenant SaaS solution for engineering colleges and autonomous universities across the state of Tamil Nadu.")
    ]
    for title, desc in scopes:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(f"•   {title} ")
        r1.font.name = "Times New Roman"; r1.font.bold = True
        r2 = p.add_run(desc)
        r2.font.name = "Times New Roman"

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: PROBLEM DEFINITION (Page 4)
    # =========================================================================
    add_ch_title("2", "PROBLEM DEFINITION")
    add_sec_heading("2.1", "EXISTING SYSTEM")
    ex_p1 = (
        "Presently, extracurricular governance in educational institutions is conducted through disconnected, ad-hoc mechanisms. "
        "Each club or cell operates as an isolated operational silo. When a student wishes to discover club recruitment or participate "
        "in an upcoming event, they must rely on informal information channels such as forwarded WhatsApp messages, printed notice-board "
        "posters, or personal word-of-mouth. Multiple independent Google Forms are distributed per event, leading to redundant data entry, "
        "lost registrations, and lack of real-time registration verification."
    )
    ex_p2 = (
        "Furthermore, taking attendance during workshops, hackathons, and guest lectures is conducted on physical paper roll sheets. "
        "Paper sign-in sheets are prone to proxy signatures, accidental physical damage, and data loss. Most critically, transferring "
        "these attendance logs into official On-Duty (OD) approval letters requires manual re-typing and physically routing paper documents "
        "through multiple administrative offices. When students participate in full-day symposiums, days often elapse before attendance "
        "is credited, resulting in students being marked absent erroneously in academic attendance databases. At the end of each academic "
        "year, preparing audit reports for NAAC or NBA requires faculty advisors to spend weeks manually collecting attendance lists, "
        "event photographs, and participant counts from personal drives."
    )
    add_para(ex_p1)
    add_para(ex_p2)

    add_sec_heading("2.2", "PROBLEM STATEMENT")
    prob_p = (
        "The complete absence of a centralized, auditable digital platform for campus clubs and cells results in severe information "
        "asymmetry, high administrative friction, inaccurate attendance tracking, and prolonged delays in academic On-Duty regularization. "
        "Manual record-keeping exposes institutional records to data loss and renders statutory accreditation compliance highly "
        "inefficient and prone to reporting discrepancies. Therefore, there is an urgent imperative to develop a secure, role-governed, "
        "and human-centered digital operating system that unifies club administration, event orchestration, attendance roll-calls, "
        "and achievement archiving into a single transparent platform."
    )
    add_para(prob_p)
    add_para(
        "This foundational challenge was crystallized into the primary design challenge guiding this investigation: "
        "“How might we design a centralized, accessible digital ecosystem for college clubs and cells that unifies student discovery, "
        "automates event attendance and On-Duty workflows, and provides verified records for institutional excellence?”",
        italic=True, space_before=4, space_after=8
    )

    add_sec_heading("2.3", "CONSTRAINTS")
    add_para("The design and development of the centralized platform were guided by four critical operational constraints:")
    constraints = [
        ("Institutional Role Hierarchy:", "The system must strictly mirror official academic governance with non-overlapping role permissions across Institutional Administrators, Faculty In-Charges, Student Coordinators, and Students."),
        ("Data Integrity & RLS:", "Student personal profiles, confidential attendance logs, and administrative audit trails must be protected by cryptographic authentication and database-level Row-Level Security (RLS)."),
        ("Zero-Friction Usability:", "The web interface must be intuitive, responsive across mobile phones and desktop computers, and exhibit high page-load speeds without requiring specialized user training."),
        ("Open-Source & Budgetary Limits:", "To ensure long-term sustainability and zero recurring licensing costs for academic institutions, the system must utilize open-source development stacks and free-tier cloud architectures.")
    ]
    for t, d in constraints:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    add_sec_heading("2.4", "PEOPLE AFFECTED")
    add_para("The key stakeholder groups directly affected by these operational inefficiencies include:")
    people = [
        ("Undergraduate & Postgraduate Students:", "Face fragmented information, missed event deadlines, manual paperwork, and stressful delays in academic OD approvals."),
        ("Student Club Coordinators & Office Bearers:", "Burdened by repetitive logistical overhead, manual Excel roster management, proxy attendance, and unorganized record keeping."),
        ("Faculty Advisors & Club In-Charges:", "Lack operational visibility into student activities, spend excessive time reviewing paper OD applications, and struggle to compile audit data."),
        ("Heads of Departments & Academic Administrators:", "Require verified, auditable student performance metrics and centralized documentation for institutional NAAC, NBA, and NIRF reviews.")
    ]
    for t, d in people:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    add_sec_heading("2.5", "DESIGN CHALLENGE")
    add_para("The core design challenge was articulated into seven actionable 'How Might We' questions addressed throughout the design phases:")
    hmw_qs = [
        "How might we create a single-source digital directory where students can explore all campus clubs and cells with full transparency?",
        "How might we streamline the membership application and recruitment interview workflow without manual paper forms?",
        "How might we design a reliable event scheduling mechanism that eliminates venue clashes and automates capacity quota management?",
        "How might we conduct tamper-proof roll-call attendance during events and instantly synchronize records for academic On-Duty (OD) regularization?",
        "How might we build a verified digital portfolio where students can store accredited achievement certificates authenticated by faculty?",
        "How might we enforce rigorous four-tier role-based access control (RBAC) to ensure security and institutional data governance?",
        "How might we aggregate institutional analytics into one-click exportable compliance dossiers for NAAC Criterion 5 and NBA audits?"
    ]
    for i, q in enumerate(hmw_qs, 1):
        p = add_para(f"{i}.   {q}", space_before=0, space_after=4)
        p.paragraph_format.left_indent = Inches(0.3)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: REQUIREMENTS AND ESTIMATES (Page 7)
    # =========================================================================
    add_ch_title("3", "REQUIREMENTS AND ESTIMATES")
    add_sec_heading("3.1", "HARDWARE REQUIREMENTS")
    add_para(
        "The system was engineered as a high-performance web platform accessible across consumer-grade hardware already owned by students "
        "and faculty. Table 3.1 delineates the minimum hardware specifications required for end-users and the development environment."
    )
    
    add_table_title("3.1", "Hardware requirements")
    h_table = doc.add_table(rows=4, cols=3)
    h_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(h_table)
    h_col_w = [Inches(1.8), Inches(1.8), Inches(2.6)]
    h_headers = ["Hardware", "Used by", "Purpose"]
    for j, h in enumerate(h_headers):
        c = h_table.rows[0].cells[j]; c.width = h_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    h_data = [
        ("Personal Smartphone / Tablet", "Students, Faculty, Coordinators", "Accessing mobile-responsive web portal, viewing notices, submitting RSVPs, taking roll-call."),
        ("Desktop Computer / Laptop", "Institutional Administrators, Faculty", "Administrative oversight, database auditing, managing club appointments, exporting NAAC reports."),
        ("Development Workstation (8GB RAM, Core i5/i7)", "Development Engineering Team", "Running Vite development server, compiling TypeScript modules, configuring Supabase RLS.")
    ]
    for i, row in enumerate(h_data):
        for j, val in enumerate(row):
            c = h_table.rows[i+1].cells[j]; c.width = h_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("3.2", "SOFTWARE REQUIREMENTS")
    add_para(
        "To ensure robust type safety, rapid UI rendering, and enterprise-grade data security, the software architecture "
        "was finalized as presented in Table 3.2."
    )
    
    add_table_title("3.2", "Software tools and platforms")
    s_table = doc.add_table(rows=7, cols=3)
    s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(s_table)
    s_col_w = [Inches(1.5), Inches(2.3), Inches(2.4)]
    s_headers = ["Layer", "Technology Used", "Role"]
    for j, h in enumerate(s_headers):
        c = s_table.rows[0].cells[j]; c.width = s_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    s_data = [
        ("Frontend Framework", "React 18 with TypeScript 5", "Component-driven single page application (SPA) with static type safety."),
        ("Styling & Theme", "Tailwind CSS 3", "Utility-first design engine configured with classic Wikipedia Vector theme."),
        ("Build Tool & Bundler", "Vite 5", "Lightning-fast ES modules development server and production tree-shaking."),
        ("Routing & Navigation", "React Router DOM v7", "Declarative client-side routing and role-based route guard protection."),
        ("Backend & Auth", "Supabase (BaaS) with JWT Auth", "Cloud API gateway, cryptographic authentication, and real-time database sync."),
        ("Database Engine", "PostgreSQL (with RLS Policies)", "ACID-compliant relational database enforcing Row-Level Security data protection.")
    ]
    for i, row in enumerate(s_data):
        for j, val in enumerate(row):
            c = s_table.rows[i+1].cells[j]; c.width = s_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("3.3", "SOFTWARE DESCRIPTION")
    add_subsec_heading("3.3.1", "React 18 and TypeScript")
    add_para(
        "React 18 provides a declarative, component-based virtual DOM engine that delivers instantaneous page transitions without full-page "
        "reloads. Coupled with TypeScript 5, every data entity—from membership status to event quotas—is strictly typed with compile-time "
        "contract guarantees, completely eliminating common runtime null-reference errors."
    )
    add_subsec_heading("3.3.2", "Tailwind CSS and Wikipedia Vector Styling")
    add_para(
        "Tailwind CSS offers high-performance utility classes that eliminate bloated CSS files. The user interface was specifically "
        "styled following a clean, academic Wikipedia Vector aesthetic—utilizing crisp borders (#a2a9b1), formal serif headings, "
        "rectangular functional buttons, and recognizable blue action links (#0645ad) to provide an authoritative, distraction-free environment."
    )
    add_subsec_heading("3.3.3", "Supabase and PostgreSQL Relational Engine")
    add_para(
        "Supabase serves as an open-source Backend-as-a-Service (BaaS) providing instant auto-generated REST APIs, secure user management, "
        "and real-time websockets. At its foundation is PostgreSQL, a world-class relational database executing complex relational joins, "
        "foreign-key constraints, and automated audit triggers."
    )
    add_subsec_heading("3.3.4", "Row-Level Security (RLS) Policies")
    add_para(
        "To ensure impenetrable multi-tier security, PostgreSQL Row-Level Security (RLS) policies were authored directly at the database level. "
        "Even if an unauthorized API call is attempted from the browser, database policies ensure that coordinators can only modify their "
        "assigned clubs, students can only view their own attendance, and faculty advisors hold sanction authority over authorized portfolios."
    )

    add_sec_heading("3.4", "ESTIMATES")
    add_para(
        "The project development utilized open-source tools and generous educational cloud tiers, resulting in zero initial capital expenditures. "
        "Human resource allocations involved a 5-member student engineering team working in specialized capacities: User Research & Design Thinking, "
        "Frontend Engineering, Database Schema & Security, UI/UX Design, and Accreditation Analytics Synthesis."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: DESIGN THINKING PROCESS (Pages 10-28)
    # =========================================================================
    add_ch_title("4", "DESIGN THINKING PROCESS")
    add_sec_heading("4.1", "OVERVIEW")
    add_para(
        "The project was executed through the rigorous 5-stage Design Thinking methodology mandated by the 24ITL34 laboratory course. "
        "Each laboratory exercise produced concrete analytical artifacts—including environmental trend scans, empathy maps, user journey "
        "diagrams, persona canvases, and storyboards—that directly informed the subsequent prototyping phase. Table 4.1 maps the laboratory "
        "exercises to their corresponding Design Thinking stages."
    )
    
    add_table_title("4.1", "Laboratory exercises mapped to design thinking phases")
    dt_table = doc.add_table(rows=8, cols=4)
    dt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(dt_table)
    dt_col_w = [Inches(0.8), Inches(2.2), Inches(1.3), Inches(1.9)]
    dt_hdrs = ["Ex. No.", "Exercise Name", "Phase", "Key Artifacts Produced"]
    for j, h in enumerate(dt_hdrs):
        c = dt_table.rows[0].cells[j]; c.width = dt_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    dt_data = [
        ("1", "Identify Problem & Project Scope", "Problem Framing", "Situation analysis, constraints, affected users, estimates, workflow."),
        ("2", "User Research using Explore Tools", "Explore", "STEEP trend analysis, activity system map, stakeholder matrices, project brief."),
        ("4", "Customer Interview & User Mapping", "Empathize", "Empathy map, journey map, interview field notes, post-interview synthesis."),
        ("5", "User Persona & Need Formulation", "Define", "SPICE framework analysis, need statements, core insight, persona canvas."),
        ("7", "User Scenario & Storytelling", "Ideate", "5-stage narrative storyboard canvas tracing student life before and after solution."),
        ("8", "Low-Fidelity Wireframe Prototyping", "Prototype", "Solution user journey flow, paper-style layout wireframes (3 screens)."),
        ("9", "Medium-Fidelity Web Implementation", "Prototype / Test", "Fully functional reactive web application across 11 modules with live Supabase.")
    ]
    for i, row in enumerate(dt_data):
        for j, val in enumerate(row):
            c = dt_table.rows[i+1].cells[j]; c.width = dt_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("4.2", "PROBLEM IDENTIFICATION")
    add_para(
        "The initial exercise framed the operational friction within the college campus. The workflow of the proposed system was "
        "synthesized into an end-to-end user sequence depicted in Figure 4.1. Students enter the portal, browse registered organizations, "
        "apply for membership, reserve seats for certified events, mark real-time attendance, and instantly receive authenticated On-Duty "
        "clearance letters, while administrators monitor institutional metrics from an interactive command dashboard."
    )
    add_figure_placeholder("4.1", "Workflow of Centralised Clubs and Cell Management System", height_inches=2.8)

    add_sec_heading("4.3", "EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)")
    add_subsec_heading("4.3.1", "STEEP Trends Analysis")
    add_para(
        "A comprehensive STEEP analysis (Social, Technological, Economic, Environmental, Political/Regulatory) was conducted to evaluate "
        "external pressures and institutional drivers governing extracurricular management, as illustrated in Figure 4.2."
    )
    add_figure_placeholder("4.2", "STEEP analysis for campus clubs and cells challenge", height_inches=2.6)
    
    steep_paras = [
        ("Social Trends:", "Undergraduate students increasingly demand transparent, on-demand digital services. They seek active peer networking, leadership opportunities, and verified co-curricular portfolios that boost corporate employability."),
        ("Technological Trends:", "Pervasive smartphone usage, high-speed campus Wi-Fi, modern cloud web applications, and real-time database synchronizations create the technical viability for an instant campus management portal."),
        ("Economic Trends:", "Eliminating physical paper sign-ups, printed certificates, and manual report compilation saves significant institutional printing and logistical expenditures, supporting frugal campus operations."),
        ("Environmental Trends:", "Transitioning from paper-intensive circulars, physical registration receipts, and printed attendance sheets to a paperless cloud system significantly curtails campus carbon footprints and paper waste."),
        ("Political & Regulatory Trends:", "Mandated accreditation requirements by NAAC (Criterion 5), National Board of Accreditation (NBA), and NIRF obligate colleges to produce verifiable, auditable student co-curricular participation data.")
    ]
    for t, d in steep_paras:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    add_subsec_heading("4.3.2", "STEEP Matrix and Prioritisation")
    add_para(
        "The identified trends were mapped on an Impact versus Likelihood matrix (Figure 4.3) and prioritized to guide architecture choices, "
        "summarized in Table 4.2."
    )
    add_figure_placeholder("4.3", "STEEP analysis matrix", height_inches=2.5)

    add_table_title("4.2", "Prioritised STEEP trends for club ecosystem")
    stp_table = doc.add_table(rows=5, cols=3)
    stp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(stp_table)
    stp_col_w = [Inches(1.8), Inches(1.8), Inches(2.6)]
    stp_hdrs = ["Quadrant", "Trend", "Implication for System Design"]
    for j, h in enumerate(stp_hdrs):
        c = stp_table.rows[0].cells[j]; c.width = stp_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    stp_data = [
        ("High Impact / Likely to Occur", "Paperless campus drive & digital convenience", "The portal must be 100% cloud-based and eliminate physical paperwork for registrations and On-Duty requests."),
        ("High Impact / Likely to Occur", "Stringent NAAC/NBA accreditation audits", "Database must log immutable audit timestamps and support 1-click Criterion 5 report generation."),
        ("High Impact / Uncertain", "Adoption across traditional faculty coordinators", "Interface must remain clean, minimal, and non-intimidating (Wikipedia Vector aesthetic) to ensure high faculty adoption."),
        ("Low Impact / Likely to Occur", "Mobile-first student browsing habits", "All interfaces must be fully responsive across mobile screens for instantaneous roll-calls.")
    ]
    for i, row in enumerate(stp_data):
        for j, val in enumerate(row):
            c = stp_table.rows[i+1].cells[j]; c.width = stp_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_subsec_heading("4.3.3", "Activity System Mapping")
    add_para(
        "The activity system map (Figure 4.4) defined the core institutional mission: “To deliver a unified, transparent digital ecosystem "
        "that empowers students to engage meaningfully in campus organizations while providing faculty and administrators with auditable co-curricular governance.” "
        "Four strategic pillars were defined: (1) Discover Clubs & Cells, (2) Orchestrate Events & RSVPs, (3) Automate Attendance & OD Clearances, "
        "and (4) Validate Achievements & Accreditations."
    )
    add_figure_placeholder("4.4", "Activity system map for Clubs and Cells Management System", height_inches=2.5)

    add_subsec_heading("4.3.4", "Stakeholder Mapping and Analysis")
    add_para(
        "Stakeholders were mapped systematically across an Interest versus Influence Matrix (Figure 4.5), relational linkages (Figure 4.6), "
        "and priority engagement matrices (Figure 4.7). Table 4.3 outlines the engagement protocol."
    )
    add_figure_placeholder("4.5", "Stakeholder mapping matrix", height_inches=2.4)
    add_figure_placeholder("4.6", "Stakeholder links and relationship mapping", height_inches=2.4)
    add_figure_placeholder("4.7", "Stakeholder priority mapping matrix", height_inches=2.4)

    add_table_title("4.3", "Stakeholder classification and engagement strategy")
    stk_table = doc.add_table(rows=5, cols=3)
    stk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(stk_table)
    stk_col_w = [Inches(1.8), Inches(2.0), Inches(2.4)]
    stk_hdrs = ["Interest / Influence", "Stakeholders", "Engagement Strategy"]
    for j, h in enumerate(stk_hdrs):
        c = stk_table.rows[0].cells[j]; c.width = stk_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    stk_data = [
        ("High Interest / High Influence", "Principal, HoDs, Institutional IQAC / NAAC Coordinators, Faculty Advisors", "Engage Closely: Involve in feature specification, security approval, and accreditation report format standardization."),
        ("High Interest / Low Influence", "General Students, Club Members, Event Attendees", "Keep Satisfied: Provide lightning-fast mobile portal, clear event notices, instant OD letters, and verified digital credentials."),
        ("Low Interest / High Influence", "College ERP & IT Systems Administrators", "Keep Informed: Establish standardized data export protocols and database synchronization schedules."),
        ("Low Interest / Low Influence", "External Auditors, Alumni Network, Industry Sponsors", "Monitor: Provide read-only verified event records and authenticated certification validation portals.")
    ]
    for i, row in enumerate(stk_data):
        for j, val in enumerate(row):
            c = stk_table.rows[i+1].cells[j]; c.width = stk_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_subsec_heading("4.3.5", "Project Brief and Reframing Opportunities")
    add_para(
        "By synthesizing agency context (NAAC compliance), process needs (event logistics & OD approval), and user desires (student engagement), "
        "the team reframed the opportunity as shown in Figure 4.8. The refined mission statement was finalized: "
        "“How might we engineer an intelligent, transparent web ecosystem that seamlessly connects college students with clubs and cells, "
        "eliminates administrative friction in attendance and On-Duty regularizations, and provides authenticated co-curricular records for institutional excellence?”"
    )
    add_figure_placeholder("4.8", "Reframing the opportunities", height_inches=2.5)

    add_sec_heading("4.4", "EMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)")
    add_para(
        "To ground the system in genuine human realities rather than assumptions, the team formulated an Empathy Map (Figure 4.9) and "
        "User Journey Map (Figure 4.10) to guide primary field investigations."
    )
    add_figure_placeholder("4.9", "Empathy map used to generate interview questions", height_inches=2.5)
    add_figure_placeholder("4.10", "Journey map of a student participating in club activities", height_inches=2.5)
    add_figure_placeholder("4.11", "Combined empathy map and user journey", height_inches=2.5)

    add_subsec_heading("4.4.1", "User Interview Documentation")
    add_para(
        "A formal semi-structured interview was conducted in the Department of Information Technology at Kongu Engineering College "
        "by team members Sahana S, Saran Karthik S, Sharan V, Vignesh M, and Murasoli B. Figure 4.12 provides the geo-tagged photographic "
        "evidence of the interaction, and Table 4.4 details the interviewee profile."
    )
    add_figure_placeholder("4.12", "Geo-tagged photograph of team with interviewee at KEC", height_inches=2.6)

    add_table_title("4.4", "Profile of the interviewee")
    int_table = doc.add_table(rows=7, cols=2)
    int_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(int_table)
    int_col_w = [Inches(2.0), Inches(4.2)]
    
    int_data = [
        ("Interviewee Name", "Dr. K. Sangeetha / Student In-Charge"),
        ("Designation / Role", "Faculty Advisor, Technical Coding Club & Assistant Professor (Dept. of IT)"),
        ("Institution", "Kongu Engineering College (Autonomous), Perundurai"),
        ("Experience", "8+ years in academic teaching and 4 years as Faculty Coordinator for co-curricular clubs"),
        ("Key Responsibilities", "Overseeing club budget, approving event proposals, endorsing On-Duty letters, conducting audits"),
        ("Interview Date & Venue", "22.10.2026; IT Department Seminar Hall & Staff Room, KEC")
    ]
    for i, (k, v) in enumerate(int_data):
        c0 = int_table.rows[i].cells[0]; c0.width = int_col_w[0]; set_cell_margins(c0)
        c0.paragraphs[0].add_run(k).font.bold = True
        c1 = int_table.rows[i].cells[1]; c1.width = int_col_w[1]; set_cell_margins(c1)
        c1.paragraphs[0].add_run(v)
        for c in [c0, c1]:
            for r in c.paragraphs[0].runs: r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_para("Two direct quotations from the interview underscored the critical bottlenecks:", bold=True, space_before=6, space_after=4)
    q1 = "“Every time our club hosts a symposium, students wait in long queues outside the staff room just to get physical signatures on their On-Duty slips. It is chaotic, stressful for students, and consumes hours of faculty time.”"
    q2 = "“When NAAC committee inspections occur, compiling participant counts, verified attendance sheets, and geotagged photographs across four years of events is an administrative nightmare because records are scattered in individual coordinators' laptops.”"
    add_para(q1, italic=True, space_before=0, space_after=4)
    add_para(q2, italic=True, space_before=0, space_after=8)

    add_subsec_heading("4.4.2", "Post-Interview Discussion & Synthesis")
    add_para(
        "A post-interview synthesis was performed to map the interviewee's motivations, pain points, and design implications, summarized in Table 4.5."
    )
    
    add_table_title("4.5", "Post-interview synthesis")
    syn_table = doc.add_table(rows=5, cols=3)
    syn_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(syn_table)
    syn_col_w = [Inches(1.8), Inches(2.2), Inches(2.2)]
    syn_hdrs = ["Aspect", "About the Interviewee", "Actionable Design Insight"]
    for j, h in enumerate(syn_hdrs):
        c = syn_table.rows[0].cells[j]; c.width = syn_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    syn_data = [
        ("Goals & Motivation", "Wants vibrant student engagement without paperwork chaos; aspires to transparent, verifiable event governance.", "Provide 1-click approvals for events and attendance roll-calls directly on mobile."),
        ("Current Pain Points", "Manual signature chasing for On-Duty; proxy attendance during large hall events; lost co-curricular certificates.", "Automate digital On-Duty generation synchronized with real-time roll-calls."),
        ("Accreditation Strain", "Spends weeks manually formatting attendance registers for NAAC Criterion 5 quality compliance.", "Build one-click exportable institutional compliance dossiers matching accreditation formats."),
        ("Key Human Insight", "Faculty and student coordinators are not opposed to accountability—they simply lack an integrated operational tool.", "Ensure clean, uncluttered user experience that requires zero specialized onboarding.")
    ]
    for i, row in enumerate(syn_data):
        for j, val in enumerate(row):
            c = syn_table.rows[i+1].cells[j]; c.width = syn_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("4.5", "DEFINE: NEEDS, INSIGHTS AND PERSONA")
    add_subsec_heading("4.5.1", "SPICE Framework Analysis")
    add_para(
        "The findings were deconstructed across the SPICE framework (Social, Physical, Identity, Communication, Emotional) "
        "as illustrated in Figure 4.13 and Table 4.6."
    )
    add_figure_placeholder("4.13", "SPICE framework for understanding deep user needs", height_inches=2.4)

    add_table_title("4.6", "SPICE analysis for Clubs and Cells Management System")
    spc_table = doc.add_table(rows=6, cols=2)
    spc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(spc_table)
    spc_col_w = [Inches(1.8), Inches(4.4)]
    spc_hdrs = ["Dimension", "Deep Human Need & Architectural Response"]
    for j, h in enumerate(spc_hdrs):
        c = spc_table.rows[0].cells[j]; c.width = spc_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    spc_data = [
        ("Social", "Belonging & Peer Collaboration: Need a seamless channel to discover technical societies, apply for leadership portfolios, and collaborate with like-minded peers across academic departments."),
        ("Physical", "Zero Physical Friction: Elimination of manual paper circulars, physical notice boards, paper sign-up sheets, and manual corridor queues for faculty signatures."),
        ("Identity", "Recognized Professional Persona: Students desire an accredited co-curricular identity showcasing certified club memberships, event achievements, and verified leadership roles."),
        ("Communication", "Instant & Transparent Updates: Real-time broadcast notifications for event schedules, application status changes, and On-Duty approval clearances."),
        ("Emotional", "Relief, Pride & Peace of Mind: Removing the persistent anxiety of being marked absent during hackathons, coupled with pride in holding authenticated college credentials.")
    ]
    for i, row in enumerate(spc_data):
        for j, val in enumerate(row):
            c = spc_table.rows[i+1].cells[j]; c.width = spc_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_subsec_heading("4.5.2", "Persona Canvas")
    add_para(
        "The synthesis led to the construction of a primary persona: Arun Kumar, an energetic undergraduate engineering student "
        "and aspiring club leader (Figure 4.14, Table 4.7)."
    )
    add_figure_placeholder("4.14", "Persona canvas", height_inches=2.6)

    add_table_title("4.7", "Persona summary: Active Student Leader & Campus Member")
    per_table = doc.add_table(rows=8, cols=2)
    per_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(per_table)
    per_col_w = [Inches(2.0), Inches(4.2)]
    
    per_data = [
        ("Demographics", "Age 19–21; 3rd Year B.Tech IT Student; Kongu Engineering College; Active campus member."),
        ("Core Goals", "Join premier technical coding clubs, participate in regional hackathons, and build a verified co-curricular portfolio."),
        ("Motivations", "Aspires to excel in campus placements, gain leadership experience, and earn verified achievement credentials."),
        ("Frustrations & Pains", "Misses club recruitment deadlines due to unread notice boards; experiences delays getting On-Duty signatures from faculty."),
        ("Digital Habits", "Uses smartphone constantly; checks college email; expects instant digital confirmation and zero manual paperwork."),
        ("Social Lifestyle", "Lives in campus hostel; collaborates in team hackathons; engages in peer technical forums."),
        ("Deep Unmet Need", "A unified digital portal where he can discover clubs, RSVP for hackathons in 1 click, and get automated On-Duty credit.")
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
        "To transform user insights into functional features, the team created a comprehensive storyboard canvas (Figure 4.15) "
        "tracing Arun's student journey before and after the ClubHub digital intervention, structured in Table 4.8."
    )
    add_figure_placeholder("4.15", "Storyboard canvas for the persona", height_inches=2.5)

    add_table_title("4.8", "Storyboard of the persona")
    sty_table = doc.add_table(rows=6, cols=2)
    sty_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sty_table)
    sty_col_w = [Inches(1.8), Inches(4.4)]
    sty_hdrs = ["Narrative Stage", "User Story Description"]
    for j, h in enumerate(sty_hdrs):
        c = sty_table.rows[0].cells[j]; c.width = sty_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    sty_data = [
        ("1. The Persona", "Arun, an enthusiastic 3rd-year engineering student eager to participate in campus technical hackathons and clubs."),
        ("2. The Setting", "A sprawling autonomous college campus with over 40 clubs and cells operating in departmental silos with paper notices."),
        ("3. The Problem", "Arun misses a flagship coding hackathon registration due to an unindexed circular, and when attending another workshop, loses attendance credit because his paper OD slip was misplaced."),
        ("4. The Solution (ClubHub)", "Arun logs into ClubHub, discovers all upcoming events on a centralized calendar, reserves a verified seat quota with 1 click, and receives a digital RSVP pass."),
        ("5. The Resolution", "At the event, the coordinator marks roll-call on a tablet; Arun's On-Duty approval is automatically generated and forwarded to the college ERP. Arun earns a verified digital achievement badge.")
    ]
    for i, row in enumerate(sty_data):
        for j, val in enumerate(row):
            c = sty_table.rows[i+1].cells[j]; c.width = sty_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: PROTOTYPE IMPLEMENTATION (Pages 29-33)
    # =========================================================================
    add_ch_title("5", "PROTOTYPE IMPLEMENTATION")
    add_sec_heading("5.1", "PROPOSED SYSTEM")
    add_para(
        "The proposed Centralised Clubs and Cell Management System (ClubHub) is a three-tier, responsive web platform engineered "
        "to manage the entire operational lifecycle of campus organizations. It provides dedicated role-based portals for four stakeholder groups: "
        "(1) Institutional Administrators, who manage the global directory, assign faculty advisors, and export accreditation dossiers; "
        "(2) Faculty Advisors, who sanction events, verify achievement portfolios, and approve official rosters; "
        "(3) Student Coordinators, who schedule events, take attendance roll-calls, and publish announcements; and "
        "(4) General Students, who discover clubs, submit applications, reserve event RSVPs, and track academic On-Duty clearances."
    )

    add_sec_heading("5.2", "LOW-FIDELITY PROTOTYPE (EXERCISE 8)")
    add_para(
        "Prior to software implementation, paper wireframes were designed to validate user journeys cheaply and iteratively. "
        "The low-fidelity prototype established three primary screens (Figure 5.1): (1) Unified Directory Screen with department filters; "
        "(2) Event RSVP screen with real-time seat quota badges; and (3) Digital On-Duty Tracker displaying verified attendance slips. "
        "Heuristic evaluation confirmed that single primary actions and rectangular button layouts maximized accessibility across all user cohorts."
    )
    add_figure_placeholder("5.1", "Low-fidelity screens: discovery, event RSVP and OD tracker", height_inches=2.7)

    add_sec_heading("5.3", "MEDIUM-FIDELITY PROTOTYPE")
    add_para(
        "The medium-fidelity prototype was developed as a production-grade single page application (SPA) using React 18, TypeScript, "
        "Tailwind CSS, and Supabase. Table 5.1 provides a detailed breakdown of the functional modules implemented."
    )
    
    add_table_title("5.1", "Screens and functional modules of the web prototype")
    mod_table = doc.add_table(rows=6, cols=3)
    mod_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(mod_table)
    mod_col_w = [Inches(1.8), Inches(2.2), Inches(2.2)]
    mod_hdrs = ["Screen / Module", "Main Functional Features", "Human Need Addressed"]
    for j, h in enumerate(mod_hdrs):
        c = mod_table.rows[0].cells[j]; c.width = mod_col_w[j]; set_cell_margins(c)
        r = c.paragraphs[0].add_run(h); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    mod_data = [
        ("Landing Page (Fig. 5.2)", "Executive serif header, college identity badge, single-click role demo logins (Student, Lead, Faculty, Admin), quick navigation.", "Simple, welcoming entry point with instant authentication access."),
        ("Executive Analytics Dashboard (Fig. 5.3)", "Real-time metrics: active clubs count, upcoming symposiums, total verified memberships, participation ratios, live activity streams.", "High-level institutional oversight and operational monitoring."),
        ("Clubs & Cells Directory (Fig. 5.4)", "Catalog of 18+ active technical societies & cells; category filtering; lead faculty display; 1-click membership recruitment application modal.", "Centralized discovery and transparent induction processing."),
        ("Event Management & RSVP Hub (Fig. 5.5)", "Calendar scheduling, venue clash detection, attendee capacity limits, instant RSVP reservation, downloadable PDF entry pass.", "Convenient event reservation without paper forms."),
        ("Real-Time Roll-Call & OD Generator", "Live checkbox attendance roster for coordinators; instant generation of verified On-Duty student attendance list for ERP synchronization.", "Eliminates corridor signature queues and proxy attendance.")
    ]
    for i, row in enumerate(mod_data):
        for j, val in enumerate(row):
            c = mod_table.rows[i+1].cells[j]; c.width = mod_col_w[j]; set_cell_margins(c)
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_figure_placeholder("5.2", "Landing page of the prototype", height_inches=2.5)
    add_figure_placeholder("5.3", "Administrator and coordinator analytics dashboard", height_inches=2.5)
    add_figure_placeholder("5.4", "Clubs and cells directory with active membership application", height_inches=2.5)
    add_figure_placeholder("5.5", "Event creation and real-time attendance roll-call interface", height_inches=2.5)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION (Pages 34-37)
    # =========================================================================
    add_ch_title("6", "RESULTS AND DISCUSSION")
    add_sec_heading("6.1", "OUTCOMES OF THE DESIGN PROCESS")
    add_para(
        "Each stage of the Design Thinking methodology yielded tangible analytical outcomes that directly governed technical decisions "
        "in the prototype, as summarized in Table 6.1."
    )
    
    add_table_title("6.1", "Results of each design thinking phase")
    res_table = doc.add_table(rows=7, cols=3)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(res_table)
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
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("6.2", "ASSESSMENT AGAINST THE SUCCESS CRITERIA")
    add_para(
        "The prototype was evaluated against the four foundational success criteria defined in the project brief (Table 6.2) "
        "and the seven core design challenge questions (Table 6.3)."
    )
    
    add_table_title("6.2", "Prototype assessment against success criteria")
    suc_table = doc.add_table(rows=5, cols=3)
    suc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(suc_table)
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
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_table_title("6.3", "Coverage of the design challenge questions")
    cov_table = doc.add_table(rows=8, cols=2)
    cov_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cov_table)
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
            r = c.paragraphs[0].add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(11)

    add_sec_heading("6.3", "DISCUSSION")
    add_subsec_heading("6.3.1", "Significance of Human-Centered Design")
    add_para(
        "By commencing with stakeholder interviews rather than writing code, the team avoided building a mere static website. "
        "User research uncovered that the greatest emotional stress experienced by students was not finding event dates, but the tedious "
        "process of obtaining On-Duty signatures from faculty rooms. Designing the automated roll-call to instant-OD pipeline converted a "
        "purely informational directory into an indispensable operational platform."
    )
    add_subsec_heading("6.3.2", "System Strengths and Limitations")
    add_para(
        "The system's foremost strengths lie in its zero-cost architecture, sub-second query performance via Supabase, bulletproof database "
        "security via Row-Level Security, and authentic Wikipedia Vector user interface that guarantees accessibility across age groups. "
        "Current limitations include reliance on demonstration user accounts for initial testing and the requirement for active internet connectivity."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE WORK (Page 38)
    # =========================================================================
    add_ch_title("7", "CONCLUSION AND FUTURE WORK")
    add_para(
        "This project successfully applied the human-centered Design Thinking methodology to solve the chronic administrative fragmentation "
        "surrounding college extracurricular governance. By systematically navigating through context exploration, stakeholder empathy interviews, "
        "need framing via SPICE, narrative storyboarding, and rapid prototyping, the team developed the Centralised Clubs and Cell Management System "
        "for Colleges (ClubHub)."
    )
    add_para(
        "The engineered web application effectively unifies all campus organizations into an interactive directory, automates membership inductions, "
        "orchestrates conflict-free event scheduling, conducts real-time roll-call attendance, and eliminates corridor signature queues through "
        "instant digital On-Duty generation. Furthermore, by archiving student achievements in an authenticated vault and aggregating participation "
        "metrics for NAAC Criterion 5 and NBA audits, the platform transforms co-curricular management from an administrative burden into an "
        "institutional asset."
    )
    add_para("Planned future enhancements include:", bold=True, space_before=6, space_after=4)
    future_work = [
        ("Direct College ERP Bi-Directional Synchronization:", "Establishing automated REST webhooks with the college's central ERP database to instantly update daily course attendance ledgers upon faculty OD approval."),
        ("QR-Code Ticket Validation:", "Integrating dynamic time-based QR codes on event entry passes scanned via coordinator smartphone cameras for instantaneous, fraud-proof roll-call check-in."),
        ("Automated Digital Certificate Generation:", "Deploying headless PDF canvas rendering engines that automatically stamp verified participant and winner certificates with unique cryptographic verification hashes."),
        ("Multi-College Multi-Tenant Deployment:", "Partitioning the Supabase cloud infrastructure to onboard external autonomous engineering institutions across the state under a unified inter-collegiate co-curricular network.")
    ]
    for t, d in future_work:
        p = add_para()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        p.add_run(f"•   {t} ").font.bold = True
        p.add_run(d)

    doc.add_page_break()

    # =========================================================================
    # BACK MATTER: APPENDIX - 1 (Page 39)
    # =========================================================================
    add_para("APPENDIX – 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=4, line_spacing=1.15)
    add_para("USER INTERVIEW DOCUMENTATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=16, line_spacing=1.15)
    
    add_para(
        "The record of the formal stakeholder interview conducted for Laboratory Exercise 4 is documented in Table A1.1. "
        "Questions were generated using the combined empathy map and journey map framework."
    )
    
    add_table_title("A1.1", "Interview record")
    app_table = doc.add_table(rows=8, cols=2)
    app_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(app_table)
    app_col_w = [Inches(2.0), Inches(4.2)]
    
    app_data = [
        ("Interviewers (Project Team)", "Sahana S (25ITR121), Saran Karthik S (25ITR128), Sharan V (25ITR134), Vignesh M (25ITR171), Murasoli B (25ITL188)"),
        ("Interviewee", "Dr. K. Sangeetha, Faculty In-Charge, Technical Coding Club & Assistant Professor, Department of IT, KEC"),
        ("Date and Venue", "22.10.2026; IT Staff Room & Laboratory Block, Kongu Engineering College"),
        ("Primary Observation 1", "Students spend excessive academic time obtaining sequential manual signatures on paper On-Duty forms across departments."),
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

    doc.add_page_break()

    # =========================================================================
    # BACK MATTER: REFERENCES (Page 40)
    # =========================================================================
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

    doc.add_page_break()

    # =========================================================================
    # BACK MATTER: MAPPING OF PROJECT GOALS TO SDG (Page 41)
    # =========================================================================
    add_para("MAPPING OF PROJECT GOALS TO SDG", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    sdg_intro = (
        "The 17 Sustainable Development Goals (SDGs) adopted by all United Nations Member States in 2015 provide a shared "
        "blueprint for peace and prosperity for people and the planet. The Centralised Clubs and Cell Management System for Colleges "
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

    # Save final document
    out_path = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM.docx"
    doc.save(out_path)
    print(f"Successfully generated complete report at: {out_path}")

if __name__ == "__main__":
    generate_report()
