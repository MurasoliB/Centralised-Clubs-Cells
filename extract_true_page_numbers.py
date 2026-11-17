import fitz, re

doc = fitz.open('CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.pdf')
print("Total PDF pages:", len(doc))

# Find the exact PDF page index where Chapter 1 starts
ch1_pdf_idx = None
for idx in range(len(doc)):
    text = doc[idx].get_text()
    if "CHAPTER 1" in text and "INTRODUCTION" in text:
        ch1_pdf_idx = idx
        break

print(f"Chapter 1 starts at PDF page index {ch1_pdf_idx} (Page {ch1_pdf_idx+1} of PDF)")

# Body page numbering starts at 1 from ch1_pdf_idx
def get_body_page(pdf_idx):
    return (pdf_idx - ch1_pdf_idx) + 1

# Targets to locate
targets = [
    # TOC Sections
    ("1.\tINTRODUCTION", "CHAPTER 1"),
    ("1.1\tINTRODUCTION", "1.1   INTRODUCTION"),
    ("1.2\tOBJECTIVE", "1.2   OBJECTIVE"),
    ("1.3\tSCOPE", "1.3   SCOPE"),
    ("2.\tPROBLEM DEFINITION", "CHAPTER 2"),
    ("2.1\tEXISTING SYSTEM", "2.1   EXISTING SYSTEM"),
    ("2.2\tPROBLEM STATEMENT", "2.2   PROBLEM STATEMENT"),
    ("2.3\tCONSTRAINTS", "2.3   CONSTRAINTS"),
    ("2.4\tPEOPLE AFFECTED", "2.4   PEOPLE AFFECTED"),
    ("2.5\tDESIGN CHALLENGE", "2.5   DESIGN CHALLENGE"),
    ("3.\tREQUIREMENTS AND ESTIMATES", "CHAPTER 3"),
    ("3.1\tHARDWARE REQUIREMENTS", "3.1   HARDWARE REQUIREMENTS"),
    ("3.2\tSOFTWARE REQUIREMENTS", "3.2   SOFTWARE REQUIREMENTS"),
    ("3.3\tSOFTWARE DESCRIPTION", "3.3   SOFTWARE DESCRIPTION"),
    ("3.4\tDATABASE DESIGN & SCHEMA SPECIFICATIONS", "3.4   DATABASE DESIGN"),
    ("3.5\tESTIMATES", "3.5   ESTIMATES"),
    ("4.\tDESIGN THINKING PROCESS", "CHAPTER 4"),
    ("4.1\tOVERVIEW", "4.1   OVERVIEW"),
    ("4.2\tPROBLEM IDENTIFICATION", "4.2   PROBLEM IDENTIFICATION"),
    ("4.3\tEXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "4.3   EXPLORE"),
    ("4.4\tEMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "4.4   EMPATHIZE"),
    ("4.5\tDEFINE: NEEDS, INSIGHTS AND PERSONA", "4.5   DEFINE"),
    ("4.6\tIDEATE: STORYTELLING", "4.6   IDEATE"),
    ("5.\tPROTOTYPE IMPLEMENTATION", "CHAPTER 5"),
    ("5.1\tPROPOSED SYSTEM ARCHITECTURE", "5.1   PROPOSED SYSTEM ARCHITECTURE"),
    ("5.2\tLOW-FIDELITY PROTOTYPE (EXERCISE 8)", "5.2   LOW-FIDELITY PROTOTYPE"),
    ("5.3\tMEDIUM-FIDELITY PROTOTYPE", "5.3   MEDIUM-FIDELITY PROTOTYPE"),
    ("5.4\tDETAILED MODULE SPECIFICATIONS", "5.4   DETAILED MODULE SPECIFICATIONS"),
    ("6.\tRESULTS AND DISCUSSION", "CHAPTER 6"),
    ("6.1\tOUTCOMES OF THE DESIGN PROCESS", "6.1   OUTCOMES OF THE DESIGN PROCESS"),
    ("6.2\tASSESSMENT AGAINST THE SUCCESS CRITERIA", "6.2   ASSESSMENT AGAINST THE SUCCESS CRITERIA"),
    ("6.3\tSOFTWARE TESTING PROCEDURES AND TEST CASES", "6.3   SOFTWARE TESTING PROCEDURES"),
    ("6.4\tDISCUSSION", "6.4   DISCUSSION"),
    ("7.\tCONCLUSION AND FUTURE WORK", "CHAPTER 7"),
    ("APPENDIX – 1: USER INTERVIEW DOCUMENTATION", "APPENDIX – 1"),
    ("REFERENCES", "REFERENCES"),
    ("MAPPING OF PROJECT GOALS TO SDG", "MAPPING OF PROJECT GOALS TO SDG"),
    # Tables
    ("Table 3.1", "Table 3.1"),
    ("Table 3.2", "Table 3.2"),
    ("Table 4.1", "Table 4.1"),
    ("Table 4.2", "Table 4.2"),
    ("Table 4.3", "Table 4.3"),
    ("Table 4.4", "Table 4.4"),
    ("Table 4.5", "Table 4.5"),
    ("Table 5.1", "Table 5.1"),
    # Figures
    ("Figure 1.1", "Figure 1.1"),
    ("Figure 1.2", "Figure 1.2"),
    ("Figure 2.1", "Figure 2.1"),
    ("Figure 2.2", "Figure 2.2"),
    ("Figure 3.1", "Figure 3.1"),
    ("Figure 3.2", "Figure 3.2"),
    ("Figure 4.1", "Figure 4.1"),
    ("Figure 4.2", "Figure 4.2")
]

results = {}
for label, query in targets:
    found_page = None
    for pdf_idx in range(ch1_pdf_idx, len(doc)):
        text = doc[pdf_idx].get_text()
        if query.lower() in text.lower():
            found_page = get_body_page(pdf_idx)
            break
    results[label] = found_page
    print(f"{label:<55} -> Page {found_page}")
