import fitz

doc = fitz.open('CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.pdf')
print('Total pages in PDF:', len(doc))

search_terms = [
    # Front matter
    "BONAFIDE CERTIFICATE",
    "DECLARATION",
    "ACKNOWLEDGEMENT",
    "ABSTRACT",
    "TABLE OF CONTENTS",
    "LIST OF TABLES",
    "LIST OF FIGURES",
    "LIST OF ABBREVIATIONS",
    # Chapters
    "1. INTRODUCTION",
    "1.1 INTRODUCTION",
    "1.2 OBJECTIVE",
    "1.3 SCOPE",
    "2. PROBLEM DEFINITION",
    "2.1 EXISTING SYSTEM",
    "2.2 PROBLEM STATEMENT",
    "2.3 CONSTRAINTS",
    "2.4 PEOPLE AFFECTED",
    "2.5 DESIGN CHALLENGE",
    "3. REQUIREMENTS AND ESTIMATES",
    "3.1 HARDWARE REQUIREMENTS",
    "3.2 SOFTWARE REQUIREMENTS",
    "3.3 SOFTWARE DESCRIPTION",
    "3.4 DATABASE DESIGN",
    "3.5 ESTIMATES",
    "4. DESIGN THINKING PROCESS",
    "4.1 OVERVIEW",
    "4.2 PROBLEM IDENTIFICATION",
    "4.3 EXPLORE",
    "4.4 EMPATHIZE",
    "4.5 DEFINE",
    "4.6 IDEATE",
    "5. PROTOTYPE IMPLEMENTATION",
    "5.1 PROPOSED SYSTEM",
    "5.2 LOW-FIDELITY",
    "5.3 MEDIUM-FIDELITY",
    "5.4 DETAILED MODULE",
    "6. RESULTS AND DISCUSSION",
    "6.1 OUTCOMES",
    "6.2 ASSESSMENT",
    "6.3 SOFTWARE TESTING",
    "6.4 DISCUSSION",
    "7. CONCLUSION AND FUTURE WORK",
    "7.1 CONCLUSION",
    "7.2 FUTURE ENHANCEMENTS",
    "APPENDIX – 1",
    "REFERENCES",
    "MAPPING OF PROJECT GOALS TO SDG",
    # Tables
    "Table 3.1",
    "Table 3.2",
    "Table 4.1",
    "Table 4.2",
    "Table 4.3",
    "Table 4.4",
    "Table 4.5",
    "Table 5.1",
    # Figures
    "Figure 1.1",
    "Figure 1.2",
    "Figure 2.1",
    "Figure 2.2",
    "Figure 3.1",
    "Figure 3.2",
    "Figure 4.1",
    "Figure 4.2"
]

found = {}
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    for term in search_terms:
        if term not in found:
            # Check if term is in text (case insensitive)
            if term.lower() in text.lower():
                found[term] = page_num + 1

print("\n--- EXACT PAGE OCCURRENCES IN RENDERED PDF ---")
for term, page_no in found.items():
    print(f"{term:<35} : Page {page_no}")

missing = [t for t in search_terms if t not in found]
if missing:
    print("\nMissing search terms:", missing)
