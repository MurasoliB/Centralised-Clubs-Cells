import fitz

doc = fitz.open('CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.pdf')
print("Total pages in ALIGNED.pdf:", len(doc))

for i in range(len(doc)):
    page = doc[i]
    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    first_few = ' | '.join(lines[:3]) if lines else 'EMPTY'
    last_line = lines[-1] if lines else 'EMPTY'
    print(f"Page {i+1:02d}: {first_few[:70]:<70} | Foot: {repr(last_line)}")
