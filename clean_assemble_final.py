import os, re, subprocess, docx, fitz

with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Truncate everything after line 1494 (the accidental syntax error append)
main_run_idx = code.find('if __name__ == "__main__":')
if main_run_idx != -1:
    code = code[:main_run_idx] + 'if __name__ == "__main__":\n    generate_master_final_report()\n'

# 2. In Chapter 3: Ensure Figure 3.1 is present
if 'Figure 3.1' not in code:
    target_31 = 'add_subsec_heading("3.4.1", "Core Organizations and Governance Entity (organizations)")'
    rep_31 = '''# 5. Figure 3.1 Clean Area
    add_clean_figure_space("Figure 3.1", "Entity Relationship Diagram", empty_lines=14)

    add_subsec_heading("3.4.1", "Core Organizations and Governance Entity (organizations)")'''
    code = code.replace(target_31, rep_31, 1)

# 3. In Chapter 4: Remove any duplicate Figure 1.2
dup_fig = '''    # 2. Figure 1.2 Clean Area
    add_clean_figure_space("Figure 1.2", "Overall System Workflow", empty_lines=14)'''
if code.count(dup_fig) > 1:
    # replace only the second occurrence
    first = code.find(dup_fig)
    second = code.find(dup_fig, first + len(dup_fig))
    code = code[:second] + code[second + len(dup_fig):]

# 4. In Chapter 5: Insert Chapter 5 Title, 5.1, 5.2, Figure 4.1, 5.3, Figure 4.2 before Table 5.1
ch5_block = '''    # =========================================================================
    # CHAPTER 5: PROTOTYPE IMPLEMENTATION
    # =========================================================================
    doc.add_page_break()
    add_ch_title("5", "PROTOTYPE IMPLEMENTATION")

    add_sec_heading("5.1", "PROPOSED SYSTEM ARCHITECTURE")
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

t51_target = 'add_table_title("5.1", "Screens and functional modules of the web prototype")'
if 'add_ch_title("5", "PROTOTYPE IMPLEMENTATION")' not in code:
    code = code.replace(t51_target, ch5_block + t51_target, 1)

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Cleaned and assembled generate_final_report_v2.py successfully!")
