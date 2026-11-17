import fitz

doc = fitz.open('CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.pdf')

# Section 2 starts at PDF page index 10 (which is Page 11 of PDF, but labeled '1' in footer)
# Let's map each PDF page index (0 to 40) to its displayed page number:
# PDF page 0 -> Cover (no number)
# PDF page 1 -> ii (or no number)
# PDF page 2 -> iii
# PDF page 3 -> iv (ABSTRACT)
# PDF page 4 -> v (ACKNOWLEDGEMENT)
# PDF page 5 -> vi (TOC page 1)
# PDF page 6 -> vii (TOC page 2)
# PDF page 7 -> viii (LIST OF TABLES)
# PDF page 8 -> ix (LIST OF FIGURES)
# PDF page 9 -> x (LIST OF ABBREVIATIONS)
# PDF page 10 onwards -> Body page = (PDF page - 9) -> 10 - 9 = 1!

items_to_find = [
    # TOC items
    ("1. INTRODUCTION", "CHAPTER 1"),
    ("1.1 INTRODUCTION", "1.1   INTRODUCTION"),
    ("1.2 OBJECTIVE", "1.2   OBJECTIVE"),
    ("1.3 SCOPE", "1.3   SCOPE"),
    ("2. PROBLEM DEFINITION", "CHAPTER 2"),
    ("2.1 EXISTING SYSTEM", "2.1   EXISTING SYSTEM"),
    ("2.2 PROBLEM STATEMENT", "2.2   PROBLEM STATEMENT"),
    ("2.3 CONSTRAINTS", "2.3   CONSTRAINTS"),
    ("2.4 PEOPLE AFFECTED", "2.4   PEOPLE AFFECTED"),
    ("2.5 DESIGN CHALLENGE", "2.5   DESIGN CHALLENGE"),
    ("3. REQUIREMENTS AND ESTIMATES", "CHAPTER 3"),
    ("3.1 HARDWARE REQUIREMENTS", "3.1   HARDWARE REQUIREMENTS"),
    ("3.2 SOFTWARE REQUIREMENTS", "3.2   SOFTWARE REQUIREMENTS"),
    ("3.3 SOFTWARE DESCRIPTION", "3.3   SOFTWARE DESCRIPTION"),
    ("3.4 DATABASE DESIGN & SCHEMA SPECIFICATIONS", "3.4   DATABASE DESIGN"),
    ("3.5 ESTIMATES", "3.5   ESTIMATES"),
    ("4. DESIGN THINKING PROCESS", "CHAPTER 4"),
    ("4.1 OVERVIEW", "4.1   OVERVIEW"),
    ("4.2 PROBLEM IDENTIFICATION", "4.2   PROBLEM IDENTIFICATION"),
    ("4.3 EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)", "4.3   EXPLORE"),
    ("4.4 EMPATHIZE: UNDERSTANDING THE USER (EXERCISE 4)", "4.4   EMPATHIZE"),
    ("4.5 DEFINE: NEEDS, INSIGHTS AND PERSONA", "4.5   DEFINE"),
    ("4.6 IDEATE: STORYTELLING", "4.6   IDEATE"),
    ("5. PROTOTYPE IMPLEMENTATION", "CHAPTER 5"),
    ("5.1 PROPOSED SYSTEM ARCHITECTURE", "5.1   PROPOSED SYSTEM"),
    ("5.2 LOW-FIDELITY PROTOTYPE (EXERCISE 8)", "5.2   LOW-FIDELITY"),
    ("5.3 MEDIUM-FIDELITY PROTOTYPE", "5.3   MEDIUM-FIDELITY"),
    ("5.4 DETAILED MODULE SPECIFICATIONS", "5.4   DETAILED MODULE"),
    ("6. RESULTS AND DISCUSSION", "CHAPTER 6"),
    ("6.1 OUTCOMES OF THE DESIGN PROCESS", "6.1   OUTCOMES"),
    ("6.2 ASSESSMENT AGAINST THE SUCCESS CRITERIA", "6.2   ASSESSMENT"),
    ("6.3 SOFTWARE TESTING PROCEDURES AND TEST CASES", "6.3   SOFTWARE TESTING"),
    ("6.4 DISCUSSION", "6.4   DISCUSSION"),
    ("7. CONCLUSION AND FUTURE WORK", "CHAPTER 7"),
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
    ("Figure 4.2", "Figure 4.2"),
]

print("=== EXACT BODY PAGE NUMBERS (STARTING AT CHAPTER 1 = PAGE 1) ===")
# Search from PDF page 10 onwards (body section)
results = {}
for label, query in items_to_find:
    found_page = None
    for pdf_idx in range(10, len(doc)):
        text = doc[pdf_idx].get_text()
        if query.lower() in text.lower():
            body_page = pdf_idx - 9  # pdf_idx 10 -> body page 1
            found_page = body_page
            break
    results[label] = found_page
    print(f"{label:<50} -> Page {found_page}")
