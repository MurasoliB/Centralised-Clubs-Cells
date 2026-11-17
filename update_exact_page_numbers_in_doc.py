with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    text = f.read()

# Exact TOC Block with the true, verified page numbers:
exact_toc = '''    # Front matter items (indent = 26.5 pt, bold)
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
    add_toc_row(toc_table, "2.2\\tPROBLEM STATEMENT", "7", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.3\\tCONSTRAINTS", "8", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.4\\tPEOPLE AFFECTED", "8", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "2.5\\tDESIGN CHALLENGE", "9", is_bold=False, left_indent_pt=30.8)

    # Chapter 3
    add_toc_row(toc_table, "3.\\tREQUIREMENTS AND ESTIMATES", "11", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "3.1\\tHARDWARE REQUIREMENTS", "11", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.2\\tSOFTWARE REQUIREMENTS", "11", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.3\\tSOFTWARE DESCRIPTION", "12", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.4\\tDATABASE DESIGN & SCHEMA SPECIFICATIONS", "13", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "3.5\\tESTIMATES", "15", is_bold=False, left_indent_pt=30.8)

    # Chapter 4
    add_toc_row(toc_table, "4.\\tDESIGN THINKING PROCESS", "16", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "4.1\\tOVERVIEW", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.2\\tPROBLEM IDENTIFICATION", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.3\\tEXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "16", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.4\\tEMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "17", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.5\\tDEFINE: NEEDS, INSIGHTS AND PERSONA", "19", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "4.6\\tIDEATE: STORYTELLING", "20", is_bold=False, left_indent_pt=30.8)

    # Chapter 5
    add_toc_row(toc_table, "5.\\tPROTOTYPE IMPLEMENTATION", "22", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "5.1\\tPROPOSED SYSTEM ARCHITECTURE", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.2\\tLOW-FIDELITY PROTOTYPE (EXERCISE 8)", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.3\\tMEDIUM-FIDELITY PROTOTYPE", "22", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "5.4\\tDETAILED MODULE SPECIFICATIONS", "23", is_bold=False, left_indent_pt=30.8)

    # Chapter 6
    add_toc_row(toc_table, "6.\\tRESULTS AND DISCUSSION", "25", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "6.1\\tOUTCOMES OF THE DESIGN PROCESS", "25", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.2\\tASSESSMENT AGAINST THE SUCCESS CRITERIA", "25", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.3\\tSOFTWARE TESTING PROCEDURES AND TEST CASES", "26", is_bold=False, left_indent_pt=30.8)
    add_toc_row(toc_table, "6.4\\tDISCUSSION", "27", is_bold=False, left_indent_pt=30.8)

    # Chapter 7
    add_toc_row(toc_table, "7.\\tCONCLUSION AND FUTURE WORK", "30", is_bold=True, left_indent_pt=2.5)

    # Back matter
    add_toc_row(toc_table, "APPENDIX – 1: USER INTERVIEW DOCUMENTATION", "31", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "REFERENCES", "32", is_bold=True, left_indent_pt=2.5)
    add_toc_row(toc_table, "MAPPING OF PROJECT GOALS TO SDG", "33", is_bold=True, left_indent_pt=2.5)'''

toc_start = text.find('add_toc_row(toc_table, "ABSTRACT"')
toc_end = text.find('doc.add_page_break()', toc_start)
text = text[:toc_start] + exact_toc + "\n\n    " + text[toc_end:]

# Exact List of Tables:
exact_lot = '''tables_catalog = [
        ("3.1", "Hardware requirements for clients and development environment", "11"),
        ("3.2", "Software tools, frameworks and cloud services", "11"),
        ("4.1", "Laboratory exercises mapped to design thinking phases", "16"),
        ("4.2", "Prioritised STEEP trends for club ecosystem", "17"),
        ("4.3", "Stakeholder classification and engagement strategy", "17"),
        ("4.4", "Active Student Leader & Campus Member Persona Summary", "18"),
        ("4.5", "Storyboard of the persona narrative", "20"),
        ("5.1", "Screens and functional modules of the web prototype", "23")
    ]'''

lot_start = text.find('tables_catalog = [')
lot_end = text.find(']', lot_start) + 1
text = text[:lot_start] + exact_lot + text[lot_end:]

# Exact List of Figures:
exact_lof = '''figures_8_entries = [
        ("1.1", "System Architecture Diagram", "2"),
        ("1.2", "Overall System Workflow", "4"),
        ("2.1", "Use Case Diagram", "7"),
        ("2.2", "Data Flow Diagram", "9"),
        ("3.1", "Entity Relationship Diagram", "13"),
        ("3.2", "Database Structure", "15"),
        ("4.1", "Admin Dashboard Interface", "22"),
        ("4.2", "Student and Faculty Interface", "22")
    ]'''

lof_start = text.find('figures_8_entries = [')
lof_end = text.find(']', lof_start) + 1
text = text[:lof_start] + exact_lof + text[lof_end:]

# Add output targets
target_list = '''    targets = [
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_CORRECT_PAGES.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_8_TABLES.docx"
    ]'''

cur_target_start = text.find('targets = [')
cur_target_end = text.find(']', cur_target_start) + 1
text = text[:cur_target_start] + target_list + text[cur_target_end:]

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated Table of Contents, List of Tables, and List of Figures with exact true page numbers!")
