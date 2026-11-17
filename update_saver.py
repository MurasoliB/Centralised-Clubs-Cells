with open('generate_final_report_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    out_final = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL_V2.docx"
    doc.save(out_final)
    print(f"SUCCESS: Fully completed master document at: {out_final}")'''

replacement = '''    targets = [
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL_UPDATED.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL_V2.docx"
    ]
    for t in targets:
        try:
            doc.save(t)
            print("SUCCESS: Saved to", t)
        except Exception as e:
            print("Could not save to", t, ":", e)'''

text = text.replace(target, replacement, 1)

with open('generate_final_report_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated save logic!")
