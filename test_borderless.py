import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os, sys, shutil

def create_borderless_table(doc, num_rows, num_cols, col_widths, tbl_ind_dxa=101):
    table = doc.add_table(rows=num_rows, cols=num_cols)
    tblPr = table._tbl.tblPr
    
    # 1. tblBorders -> none
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
    
    # 2. tblInd
    tblInd = tblPr.find(qn('w:tblInd'))
    if tblInd is not None:
        tblPr.remove(tblInd)
    tblPr.append(parse_xml(f'<w:tblInd {nsdecls("w")} w:w="{tbl_ind_dxa}" w:type="dxa"/>'))
    
    # 3. tblCellMar
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
    
    # 4. Set column widths on every cell
    for row in table.rows:
        for c_idx, width in enumerate(col_widths):
            row.cells[c_idx].width = width
            tcPr = row.cells[c_idx]._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is not None:
                tcPr.remove(tcW)
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width.pt * 20)}" w:type="dxa"/>'))
            
    return table

def apply_row_cell_widths(row, col_widths):
    for c_idx, width in enumerate(col_widths):
        row.cells[c_idx].width = width
        tcPr = row.cells[c_idx]._tc.get_or_add_tcPr()
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is not None:
            tcPr.remove(tcW)
        tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(width.pt * 20)}" w:type="dxa"/>'))

print("Helper verified!")
