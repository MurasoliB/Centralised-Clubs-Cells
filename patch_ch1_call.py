with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    text = f.read()

# Update targets
old_targets = '''    targets = [
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_8_TABLES.docx"
    ]'''

new_targets = '''    targets = [
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_ALIGNED.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_8_TABLES.docx"
    ]'''

text = text.replace(old_targets, new_targets, 1)

# Ensure Chapter 1 does not add an extra page break after section break
old_ch1_call = 'add_ch_title("1", "INTRODUCTION")'
new_ch1_call = 'add_ch_title("1", "INTRODUCTION", add_break=False)'
text = text.replace(old_ch1_call, new_ch1_call, 1)

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated save targets and Chapter 1 call!")
