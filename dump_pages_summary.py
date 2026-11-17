import fitz

doc = fitz.open('CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.pdf')
print("Total pages:", len(doc))

# Let's inspect pages from page 1 to 42
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    first_few = ' | '.join(lines[:4])
    print(f"Page {page_num+1:02d}: {first_few[:90]}")
