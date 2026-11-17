import docx
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()
doc.add_paragraph("Front matter page 1")
doc.add_page_break()
doc.add_paragraph("Front matter page 2")

s2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
s2.header.is_linked_to_previous = False
s2.footer.is_linked_to_previous = False

sectPr = s2._sectPr
pgNumType = sectPr.find(qn('w:pgNumType'))
if pgNumType is not None:
    sectPr.remove(pgNumType)
sectPr.append(parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1"/>'))

footer = s2.footer
f_p = footer.paragraphs[0]
f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_p._p.append(parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>'))

doc.add_paragraph("Chapter 1 starts on page 1")
doc.add_page_break()
doc.add_paragraph("Chapter 1 continues on page 2")

doc.save("test_restart.docx")
print("test_restart.docx created successfully!")
