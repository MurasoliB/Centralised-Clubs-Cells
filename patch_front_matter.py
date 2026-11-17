import re

with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace FRONT MATTER sections 6, 7, 8, 9 with exact borderless table format matching ref doc
new_front_matter = '''    # =========================================================================
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
    add_toc_row(toc_table, "ABSTRACT", "iv", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "ACKNOWLEDGEMENT", "v", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "LIST OF TABLES", "viii", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "LIST OF FIGURES", "ix", is_bold=True, left_indent_pt=26.5)
    add_toc_row(toc_table, "LIST OF ABBREVIATIONS", "x", is_bold=True, left_indent_pt=26.5)

    # Chapter 1
    add_toc_row(toc_table, "1.\\tINTRODUCTION", "1", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "1.1\\tINTRODUCTION", "1", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "1.2\\tOBJECTIVE", "3", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "1.3\\tSCOPE", "4", is_bold=False, left_indent_pt=30.8)

    # Chapter 2
    add_toc_row(toc_table, "2.\\tPROBLEM DEFINITION", "6", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "2.1\\tEXISTING SYSTEM", "6", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.2\\tPROBLEM STATEMENT", "8", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.3\\tCONSTRAINTS", "9", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.4\\tPEOPLE AFFECTED", "10", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.5\\tDESIGN CHALLENGE", "11", is_bold=False, left_indent_pt=30.8)

    # Chapter 3
    add_toc_row(toc_table, "3.\\tREQUIREMENTS AND ESTIMATES", "13", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "3.1\\tHARDWARE REQUIREMENTS", "13", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.2\\tSOFTWARE REQUIREMENTS", "14", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.3\\tSOFTWARE DESCRIPTION", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.4\\tDATABASE DESIGN & SCHEMA SPECIFICATIONS", "18", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.5\\tESTIMATES", "21", is_bold=False, left_indent_pt=30.8)

    # Chapter 4
    add_toc_row(toc_table, "4.\\tDESIGN THINKING PROCESS", "22", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "4.1\\tOVERVIEW", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.2\\tPROBLEM IDENTIFICATION", "23", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.3\\tEXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "25", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.4\\tEMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "30", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.5\\tDEFINE: NEEDS, INSIGHTS AND PERSONA", "34", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.6\\tIDEATE: STORYTELLING", "37", is_bold=False, left_indent_pt=30.8)

    # Chapter 5
    add_toc_row(toc_table, "5.\\tPROTOTYPE IMPLEMENTATION", "39", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "5.1\\tPROPOSED SYSTEM ARCHITECTURE", "39", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.2\\tLOW-FIDELITY PROTOTYPE (EXERCISE 8)", "41", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.3\\tMEDIUM-FIDELITY PROTOTYPE", "42", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.4\\tDETAILED MODULE SPECIFICATIONS", "44", is_bold=False, left_indent_pt=30.8)

    # Chapter 6
    add_toc_row(toc_table, "6.\\tRESULTS AND DISCUSSION", "47", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "6.1\\tOUTCOMES OF THE DESIGN PROCESS", "47", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.2\\tASSESSMENT AGAINST THE SUCCESS CRITERIA", "48", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.3\\tSOFTWARE TESTING PROCEDURES AND TEST CASES", "50", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.4\\tDISCUSSION", "53", is_bold=False, left_indent_pt=30.8)

    # Chapter 7
    add_toc_row(toc_table, "7.\\tCONCLUSION AND FUTURE WORK", "55", is_bold=True, left_indent_pt=2.5)

    # Back matter
    add_toc_row(toc_table, "APPENDIX – 1: USER INTERVIEW DOCUMENTATION", "57", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "REFERENCES", "58", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "MAPPING OF PROJECT GOALS TO SDG", "59", is_bold=True, left_indent_pt=2.5)

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
        ("1.1", "System Architecture Diagram", "3"),
        ("1.2", "Overall System Workflow", "5"),
        ("2.1", "Use Case Diagram", "8"),
        ("2.2", "Data Flow Diagram", "11"),
        ("3.1", "Entity Relationship Diagram", "17"),
        ("3.2", "Database Structure", "20"),
        ("4.1", "Admin Dashboard Interface", "42"),
        ("4.2", "Student and Faculty Interface", "45")
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
'''

# Find start of FRONT MATTER 6 and end of FRONT MATTER 9
start_idx = code.find("# FRONT MATTER: 6. TABLE OF CONTENTS")
# Find start of CHAPTER 1
end_idx = code.find("# =========================================================================", code.find("CHAPTER 1: INTRODUCTION", start_idx) - 200)

print("start_idx:", start_idx)
print("end_idx:", end_idx)

if start_idx != -1 and end_idx != -1:
    updated_code = code[:start_idx] + new_front_matter + "\n\n    " + code[end_idx:]
    with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
        f.write(updated_code)
    print("Successfully replaced FRONT MATTER in generate_final_report_v2.py!")
else:
    print("Could not find start or end index!")
