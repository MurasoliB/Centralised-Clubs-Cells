with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. In Chapter 3: Add Figure 3.1
target_31 = 'add_subsec_heading("3.4.1", "Core Organizations and Governance Entity (organizations)")'
replacement_31 = '''# 5. Figure 3.1 Clean Area
    add_clean_figure_space("Figure 3.1", "Entity Relationship Diagram", empty_lines=14)

    add_subsec_heading("3.4.1", "Core Organizations and Governance Entity (organizations)")'''

text = text.replace(target_31, replacement_31, 1)

# 2. In Chapter 4: Remove duplicate Figure 1.2
target_dup = '''    # 2. Figure 1.2 Clean Area
    add_clean_figure_space("Figure 1.2", "Overall System Workflow", empty_lines=14)'''
text = text.replace(target_dup, '', 1)

# 3. In Chapter 5: Add Figure 4.1 and Figure 4.2
# Let's see what is in Chapter 5
ch5_start = text.find('add_sec_heading("5.1", "PROPOSED SYSTEM ARCHITECTURE")')
ch5_sub = '''add_sec_heading("5.1", "PROPOSED SYSTEM ARCHITECTURE")
    add_para(
        "The proposed system architecture is designed around a modern three-tier decoupled paradigm. "
        "The presentation tier consists of a reactive Single Page Application (SPA) built with React 18, Vite, and Tailwind CSS. "
        "The logic and data tier is powered by Supabase BaaS and a managed PostgreSQL relational database enforcing strict Row-Level Security."
    )

    add_sec_heading("5.2", "LOW-FIDELITY PROTOTYPE (EXERCISE 8)")
    add_para(
        "Initial low-fidelity wireframing explored student discovery flows, role navigation menus, and the mobile roll-call layout. "
        "Paper prototypes validated early information hierarchies before entering frontend implementation."
    )

    # 7. Figure 4.1 Clean Area
    add_clean_figure_space("Figure 4.1", "Admin Dashboard Interface", empty_lines=14)

    add_sec_heading("5.3", "MEDIUM-FIDELITY PROTOTYPE")
    add_para(
        "The medium-fidelity prototype implements responsive web interfaces providing complete multi-tier role access. "
        "Figure 4.2 illustrates the student discovery portal and faculty coordinator management consoles."
    )

    # 8. Figure 4.2 Clean Area
    add_clean_figure_space("Figure 4.2", "Student and Faculty Interface", empty_lines=14)
'''

# Find end of 5.1/5.2/5.3 in text
old_51_end = text.find('add_table_title("5.1",')
text = text[:ch5_start] + ch5_sub + "\n    " + text[old_51_end:]

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Patched all 8 figure locations in Chapter 1, 2, 3, 5!")
