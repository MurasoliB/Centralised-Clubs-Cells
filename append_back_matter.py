with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    text = f.read()

back_matter_and_save = '''

    # =========================================================================
    # BACK MATTER: REFERENCES
    # =========================================================================
    doc.add_page_break()
    add_para("REFERENCES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    refs = [
        "[1]   T. Brown, “Design Thinking,” Harvard Business Review, vol. 86, no. 6, pp. 84–92, Jun. 2008.",
        "[2]   R. Razzouk and V. Shute, “What is design thinking and why is it important?,” Review of Educational Research, vol. 82, no. 3, pp. 330–348, Sep. 2012.",
        "[3]   National Assessment and Accreditation Council (NAAC), “Institutional Accreditation Manual for Autonomous Colleges: Criterion V – Student Support and Progression,” NAAC Guidelines, Bengaluru, India, 2024.",
        "[4]   National Board of Accreditation (NBA), “Manual for Accreditation of Undergraduate Engineering Programmes: Outcome Based Education Parameters,” New Delhi, India, 2023.",
        "[5]   A. Cooper, R. Reimann, D. Cronin, and C. Noessel, About Face: The Essentials of Interaction Design, 4th ed., Indianapolis, IN: John Wiley & Sons, 2014.",
        "[6]   E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns: Elements of Reusable Object-Oriented Software, Reading, MA: Addison-Wesley, 1994.",
        "[7]   M. Fowler, Patterns of Enterprise Application Architecture, Boston, MA: Addison-Wesley, 2002.",
        "[8]   Supabase Inc., “Supabase Documentation: Database Architecture and Row-Level Security Policies in PostgreSQL,” 2026. [Online]. Available: https://supabase.com/docs.",
        "[9]   React Core Team, “React 18 Documentation: Concurrent Features and Component Architecture,” Meta Platforms Inc., 2024. [Online]. Available: https://react.dev.",
        "[10]  Vite Core Team, “Vite: Next Generation Frontend Tooling,” 2024. [Online]. Available: https://vitejs.dev."
    ]
    for r_text in refs:
        p = add_para(r_text, space_before=0, space_after=6)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)

    # =========================================================================
    # BACK MATTER: MAPPING OF PROJECT GOALS TO SDG
    # =========================================================================
    doc.add_page_break()
    add_para("MAPPING OF PROJECT GOALS TO SDG", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=16, line_spacing=1.15)
    
    sdg_intro = (
        "The 17 Sustainable Development Goals (SDGs) adopted by all United Nations Member States in 2015 provide a shared "
        "blueprint for peace, prosperity, and institutional accountability. The Centralised Clubs and Cell Management System for Colleges "
        "(ClubHub) directly maps to and advances three critical Sustainable Development Goals:"
    )
    add_para(sdg_intro, space_before=0, space_after=12)

    sdgs = [
        ("SDG 4: Quality Education", [
            "Target 4.4 (Relevant Skills for Employment): Provides students with transparent access to technical societies, hackathons, and certified co-curricular events that foster coding, engineering innovation, and leadership skills essential for employment.",
            "Target 4.7 (Holistic Education): Encourages wide student participation across cultural clubs, environmental forums, and statutory cells (EDC, WDC, NSS), ensuring rounded character building and social responsibility."
        ]),
        ("SDG 9: Industry, Innovation and Infrastructure", [
            "Target 9.b (Domestic Technology Innovation): Demonstrates how frugal, open-source digital technologies (React, TypeScript, Supabase BaaS) can modernize campus administrative infrastructure with zero recurring software licensing fees.",
            "Target 9.c (Information & Communication Technology Access): Delivers a high-performance, mobile-responsive web platform ensuring all students—regardless of device ownership—enjoy equal access to campus co-curricular opportunities."
        ]),
        ("SDG 16: Peace, Justice and Strong Institutions", [
            "Target 16.6 (Effective, Accountable and Transparent Institutions): Replaces paper sign-up forms and closed-door approvals with an auditable, role-governed digital record, completely eliminating proxy attendance and ensuring transparent co-curricular governance.",
            "Target 16.10 (Public Access to Information): Guarantees that club recruitment criteria, leadership appointments, and event participation records are openly accessible and verifiable across the entire college community."
        ])
    ]

    for sdg_title, subpoints in sdgs:
        add_para(sdg_title, bold=True, size=13, space_before=8, space_after=4)
        for sp in subpoints:
            p = add_para(f"•   {sp}", space_before=0, space_after=4)
            p.paragraph_format.left_indent = Inches(0.3)

    targets = [
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_FINAL.docx",
        "CENTRALISED_CLUBS_AND_CELL_MANAGEMENT_SYSTEM_8_TABLES.docx"
    ]
    for t in targets:
        try:
            doc.save(t)
            print("SUCCESS: Saved to", t)
        except Exception as e:
            print("Could not save to", t, ":", e)

if __name__ == "__main__":
    generate_master_final_report()
'''

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(text.rstrip() + back_matter_and_save)

print("Appended back matter and save targets successfully!")
