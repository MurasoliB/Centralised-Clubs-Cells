import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Page setup: A4, 1-inch margins (left 1.25)
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
r_title = p_title.add_run("LIST OF ABBREVIATIONS")
r_title.font.name = "Times New Roman"
r_title.font.size = Pt(14)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(0, 0, 0)

# 16 Core/Main abbreviations directly matching the sample's length & layout
main_abbreviations = [
    ("API", "Application Programming Interface"),
    ("CSS", "Cascading Style Sheets"),
    ("DB", "Database"),
    ("DSP", "Design Thinking and Systems Project"),
    ("EDC", "Entrepreneurship Development Cell"),
    ("HMW", "How Might We"),
    ("HTML", "HyperText Markup Language"),
    ("IIC", "Institution's Innovation Council"),
    ("JS", "JavaScript"),
    ("JWT", "JSON Web Token"),
    ("KEC", "Kongu Engineering College"),
    ("OD", "On-Duty"),
    ("RLS", "Row-Level Security"),
    ("SDG", "Sustainable Development Goal"),
    ("SQL", "Structured Query Language"),
    ("UI / UX", "User Interface / User Experience")
]

table = doc.add_table(rows=0, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False

col_widths = [Inches(1.5), Inches(4.7)]

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

for abbr, desc in main_abbreviations:
    row_cells = table.add_row().cells
    row_cells[0].width = col_widths[0]
    row_cells[1].width = col_widths[1]
    
    # Left: Abbreviation (Bold)
    p0 = row_cells[0].paragraphs[0]
    p0.paragraph_format.space_before = Pt(3)
    p0.paragraph_format.space_after = Pt(3)
    p0.paragraph_format.line_spacing = 1.2
    r0 = p0.add_run(abbr)
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(12)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(0, 0, 0)
    
    # Right: Description (Regular)
    p1 = row_cells[1].paragraphs[0]
    p1.paragraph_format.space_before = Pt(3)
    p1.paragraph_format.space_after = Pt(3)
    p1.paragraph_format.line_spacing = 1.2
    r1 = p1.add_run(desc)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.font.bold = False
    r1.font.color.rgb = RGBColor(0, 0, 0)

out_docx = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/List_of_Abbreviations_Main.docx"
doc.save(out_docx)
print("Saved main abbreviations to:", out_docx)
