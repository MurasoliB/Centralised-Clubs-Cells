import fitz, re

doc = fitz.open('CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.pdf')

for pdf_idx in range(10, len(doc)):
    page = doc[pdf_idx]
    body_page = pdf_idx - 9
    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    headings = []
    for l in lines:
        if re.match(r'^(CHAPTER \d|\d\.\d|Figure \d\.\d|Table \d\.\d|APPENDIX|REFERENCES|MAPPING)', l):
            headings.append(l)
    print(f"Page {body_page:02d} (PDF {pdf_idx+1:02d}): {headings}")
