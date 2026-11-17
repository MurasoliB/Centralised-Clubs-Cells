import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Page setup: A4, 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1)

# Heading
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(24)
r_title = p_title.add_run("TABLE OF CONTENTS")
r_title.font.name = "Times New Roman"
r_title.font.size = Pt(14)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(0, 0, 0)

# Table data: (ch_no, title, page_no, is_bold, indent_level)
data = [
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

table = doc.add_table(rows=1, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False

# Column widths: 0.5 in, 4.7 in, 1.0 in
col_widths = [Inches(0.55), Inches(4.7), Inches(1.0)]

# Set borders to NONE (invisible table)
tblPr = table._tbl.tblPr
tblBorders = parse_xml(r'''
    <w:tblBorders %s>
        <w:top w:val="none"/>
        <w:left w:val="none"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>
''' % nsdecls('w'))
tblPr.append(tblBorders)

# Header row
hdr_cells = table.rows[0].cells
for idx, width in enumerate(col_widths):
    hdr_cells[idx].width = width

p0 = hdr_cells[0].paragraphs[0]
p0.paragraph_format.space_before = Pt(0)
p0.paragraph_format.space_after = Pt(8)

p1 = hdr_cells[1].paragraphs[0]
p1.paragraph_format.space_before = Pt(0)
p1.paragraph_format.space_after = Pt(8)
r1 = p1.add_run("TITLE")
r1.font.name = "Times New Roman"
r1.font.size = Pt(12)
r1.font.bold = True
r1.font.color.rgb = RGBColor(0, 0, 0)

p2 = hdr_cells[2].paragraphs[0]
p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p2.paragraph_format.space_before = Pt(0)
p2.paragraph_format.space_after = Pt(8)
r2 = p2.add_run("PAGE NO.")
r2.font.name = "Times New Roman"
r2.font.size = Pt(12)
r2.font.bold = True
r2.font.color.rgb = RGBColor(0, 0, 0)

# Add data rows
for ch, title, pg, is_bold, indent in data:
    row_cells = table.add_row().cells
    for idx, width in enumerate(col_widths):
        row_cells[idx].width = width
    
    # Cell 0: Chapter number
    p = row_cells[0].paragraphs[0]
    p.paragraph_format.space_before = Pt(3 if is_bold and ch else 1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(ch)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = is_bold
    r.font.color.rgb = RGBColor(0, 0, 0)
    
    # Cell 1: Title
    p = row_cells[1].paragraphs[0]
    p.paragraph_format.space_before = Pt(3 if is_bold and ch else 1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if indent > 0:
        p.paragraph_format.left_indent = Inches(0.2)
    r = p.add_run(title)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = is_bold
    r.font.color.rgb = RGBColor(0, 0, 0)
    
    # Cell 2: Page number
    p = row_cells[2].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(3 if is_bold and ch else 1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(pg)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = is_bold
    r.font.color.rgb = RGBColor(0, 0, 0)

out_docx = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/Table_of_Contents.docx"
doc.save(out_docx)
print("Saved docx to:", out_docx)
