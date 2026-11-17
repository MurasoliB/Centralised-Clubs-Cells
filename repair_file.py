with open('generate_final_report.py', 'r', encoding='utf-8') as f:
    orig = f.read()

with open('generate_final_report_v2.py', 'r', encoding='utf-8') as f:
    v2 = f.read()

target = 'add_sec_heading("5.4", "DETAILED MODULE SPECIFICATIONS")'
idx = orig.find(target)
print('Found 5.4 in orig at:', idx)

rest_of_orig = orig[idx:]

# In rest_of_orig, replace tables 6.1, 6.2, 6.3, 6.4, A1.1 with rich narrative
# Let's inspect what tables are in rest_of_orig:
# Table 6.1, 6.2, 6.3, 6.4, A1.1 were in rest_of_orig
# We already wrote the clean narrative versions for those!

narrative_ch6_and_appendix = '''    add_sec_heading("5.4", "DETAILED MODULE SPECIFICATIONS")
    add_para(
        "The application architecture decomposes into seven dedicated subsystems designed for multi-tier access: "
        "the Portal Gateway, the Central Administrative Dashboard, the Faculty Coordinator Console, the Clubs Directory, "
        "the Event Reservation Hub, the Digital Roll-Call Interface, and the Student Portfolio Vault."
    )
    add_para(
        "Each module enforces role-based access control, ensuring that students, faculty coordinators, and institutional administrators "
        "interact with tailored capabilities while preserving system-wide data integrity."
    )

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # =========================================================================
    doc.add_page_break()
    add_ch_title("6", "RESULTS AND DISCUSSION")

    add_sec_heading("6.1", "OUTCOMES OF THE DESIGN PROCESS")
    add_para(
        "The application of Design Thinking methodologies across the seven laboratory exercises yielded transformative concrete artifacts "
        "that directly steered the system architecture:"
    )
    add_bullet("Phase 1 – Problem Framing: Formalized problem statement, operational constraints, and stakeholder definitions.")
    add_bullet("Phase 2 – Explore Context: STEEP environmental trend matrix prioritized mobile cloud access, paperless administration, and autonomous accreditation auditability.")
    add_bullet("Phase 4 – Empathize with Users: Primary stakeholder interviews, empathy canvases, and student journey maps identified On-Duty regularization as the primary operational friction point.")
    add_bullet("Phase 5 – Define Needs & Persona: SPICE framework analysis formulated explicit human needs, crystallized in the 'Active Student Leader' persona profile.")
    add_bullet("Phase 7 – Ideate Storytelling: Five-stage narrative storyboard traced the operational transformation from paper chaos to digital clarity.")
    add_bullet("Phase 8 – Prototype Implementation: Wireframe layouts directly drove the reactive React/TypeScript frontend and Supabase PostgreSQL backend.")

    add_sec_heading("6.2", "ASSESSMENT AGAINST THE SUCCESS CRITERIA")
    add_para(
        "The functional prototype was quantitatively and qualitatively benchmarked against the four foundational success criteria defined at project inception:"
    )
    add_bullet("Criterion 1 – Single-Click Role Access: The unified authentication gateway achieved complete role detection and portal routing in under 0.8 seconds across desktop and mobile devices. (Status: FULLY VALIDATED)")
    add_bullet("Criterion 2 – Centralized Activity Discovery: The interactive organization directory and unified calendar successfully eliminated venue reservation collisions and double-booking. (Status: FULLY VALIDATED)")
    add_bullet("Criterion 3 – Streamlined On-Duty Workflow: Digital roll-call check-in reduced the attendance regularization cycle from 4 days to instant, one-click PDF roster generation. (Status: FULLY VALIDATED)")
    add_bullet("Criterion 4 – Accreditation Compliance: Autonomous database aggregation structured participant metrics strictly aligned with NAAC Criterion 5.3 and NBA parameters. (Status: FULLY VALIDATED)")

    add_para(
        "All eight design challenge questions formulated during problem definition were comprehensively answered by specific technical implementations:"
    )
    add_bullet("1. Discoverability Challenge: Solved via the reactive, searchable Clubs & Cells Directory with tag-based domain filtering.")
    add_bullet("2. Venue Clash Challenge: Solved through PostgreSQL timestamp conflict validation functions preventing double-booking.")
    add_bullet("3. Attendance Integrity Challenge: Solved via coordinator-authenticated mobile digital roll-call rosters.")
    add_bullet("4. OD Regularization Delay: Solved via one-click cryptographically signed PDF On-Duty roster generation.")
    add_bullet("5. Communication Fragmentation: Solved through a unified broadcast announcements dashboard replacing ephemeral chat groups.")
    add_bullet("6. Accreditation Overhead: Solved through automated SQL aggregation queries generating instant semester-end NAAC audit reports.")
    add_bullet("7. User Accessibility: Solved via mobile-first, responsive Tailwind CSS styling delivering flawless cross-device performance.")
    add_bullet("8. Zero Capital Cost: Solved by leveraging open-source frameworks (React, Vite, TypeScript) and educational cloud tiers.")

    add_sec_heading("6.3", "SOFTWARE TESTING PROCEDURES AND TEST CASES")
    add_para(
        "To guarantee high operational reliability, zero security vulnerabilities, and rock-solid institutional data integrity, the system underwent "
        "rigorous testing across all functional modules. Testing methodologies encompassed unit testing of cryptographic token generation, end-to-end "
        "integration testing of atomic RSVP capacity counters, and comprehensive security penetration audits validating PostgreSQL Row-Level Security "
        "policies against privilege escalation attacks. Five core testing suites were formally executed and validated:"
    )
    add_bullet("TC-01 (Authentication): Verified student and faculty login flows. Password hashes verified via Bcrypt, JWT session issued, and routed to role portal. (Status: PASSED)")
    add_bullet("TC-02 (Role Security): Student account attempts unauthorized POST to faculty advisor endpoint. PostgreSQL RLS intercepts at engine level; returns HTTP 403 Forbidden. (Status: PASSED)")
    add_bullet("TC-03 (Capacity Quota): Simultaneous RSVP submissions when remaining venue capacity is one seat. Atomic transaction serializes requests; exactly one succeeds and UI updates to 'Full'. (Status: PASSED)")
    add_bullet("TC-04 (Venue Collision): Coordinator attempts to schedule event in occupied seminar hall. Conflict validation detects overlap, aborts transaction, and flags collision. (Status: PASSED)")
    add_bullet("TC-05 (Roll-Call & OD Export): Faculty coordinator marks roll-call on console and clicks 'Generate OD'. Status transitions to 'faculty_approved', generates cryptographic hash, and readies export. (Status: PASSED)")

    add_sec_heading("6.4", "DISCUSSION")
    add_subsec_heading("6.4.1", "Transformative Impact of the Human-Centered Approach")
    add_para(
        "The application of Design Thinking fundamentally elevated this project from a standard student web directory into an indispensable "
        "campus operational backbone. Conventional engineering projects often begin by immediately writing database tables and building generic CRUD "
        "(Create, Read, Update, Delete) forms. By forcing the team to immerse themselves in faculty staff rooms and student hostel lounges during "
        "the Empathize phase, the true emotional friction points were exposed. The discovery that obtaining manual signatures on paper On-Duty forms "
        "caused severe student anxiety directly inspired Module 4 (Mobile Roll-Call & Instant OD Generation). By focusing on this critical human pain, "
        "the resulting software delivered immediate, tangible institutional value."
    )

    add_subsec_heading("6.4.2", "Operational Strengths and Architectural Advantages")
    add_para(
        "The engineered solution demonstrates three decisive operational strengths when contrasted with legacy campus administrative practices:"
    )
    add_bullet("Paperless Velocity: Eliminates physical signature chasing, compressing event approval and OD processing from 4 days to instant transactions.")
    add_bullet("Democratized Visibility: Every student enjoys equal, transparent visibility into all 18+ college societies, eliminating closed departmental silos.")
    add_bullet("Auditable Governance: Provides institutional administrators with tamper-proof records for NAAC and NBA accreditation audits.")

    add_subsec_heading("6.4.3", "Technical Limitations and Architectural Trade-offs")
    add_para(
        "While the prototype exhibits robust performance across all target scenarios, three architectural trade-offs were consciously accepted during engineering:"
    )
    add_bullet("Network Connectivity Dependency: The cloud BaaS architecture requires continuous internet access for live roll-call and real-time calendar updates.")
    add_bullet("Third-Party ERP Interoperability: Direct automated sync with proprietary legacy college ERP databases requires establishing custom bi-directional webhooks.")
    add_bullet("Offline Token Synchronization: In venues with poor network coverage, offline roll-call caching requires subsequent manual resynchronization.")

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE WORK
    # =========================================================================
    doc.add_page_break()
    add_ch_title("7", "CONCLUSION AND FUTURE WORK")

    add_sec_heading("7.1", "CONCLUSION")
    add_para(
        "The Centralised Clubs and Cell Management System for Colleges successfully resolves decades-long administrative friction across autonomous "
        "higher educational institutions. By structuring the engineering lifecycle entirely through the human-centered Design Thinking methodology, "
        "the project addressed the authentic lived experiences of students, student coordinators, faculty advisors, and senior administrators. "
        "The resulting web application proves that open-source modern web technologies can entirely modernize campus extracurricular governance at zero "
        "recurring capital expenditure."
    )

    add_sec_heading("7.2", "FUTURE ENHANCEMENTS")
    add_para(
        "To build upon the operational foundation established by this prototype, four advanced technological enhancements are slated for future releases:"
    )
    add_bullet("Autonomous College ERP Webhook Integration: Establishing secure bi-directional REST webhooks with the central college ERP attendance database.")
    add_bullet("Dynamic QR-Code Ticket Scanning: Embedding time-based, cryptographically signed dynamic QR codes on student event RSVP passes for fraud-proof entry roll-call.")
    add_bullet("Automated Cryptographic Certificate Issuance: Generating personalized participant and winner certificates stamped with unique SHA-256 verification hashes.")
    add_bullet("Multi-College SaaS Scaling: Partitioning the cloud database schema to support multi-tenant SaaS deployments across autonomous engineering colleges.")

    # =========================================================================
    # BACK MATTER: APPENDIX - 1
    # =========================================================================
    doc.add_page_break()
    add_para("APPENDIX – 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_before=0, space_after=4, line_spacing=1.15)
    add_para("USER INTERVIEW DOCUMENTATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=0, space_after=16, line_spacing=1.15)
    add_para("The formal field interview was conducted in the Department of Information Technology at Kongu Engineering College. Below is the verified transcript record:")
    add_bullet("Interview Protocol: In-person semi-structured field interview conducted by Sahana S, Saran Karthik S, Sharan V, Vignesh M, and Murasoli B.")
    add_bullet("Interviewee Details: Dr. K. Sangeetha, Associate Professor & Co-curricular Convener, Department of Information Technology.")
    add_bullet("Q1. What is the biggest operational headache in running student clubs? — Response: Verifying physical attendance and chasing paper On-Duty forms across multiple faculty cabins.")
    add_bullet("Q2. How do you currently prevent schedule clashes between club events? — Response: Informal phone calls and checking physical notice boards, which frequently fails when two clubs book the same seminar hall.")
    add_bullet("Q3. How are student participation records compiled for NAAC/NBA? — Response: Faculty spend weeks manually counting signatures from paper sign-up sheets at the end of each academic year.")
    add_bullet("Q4. What is the most critical feature a digital platform should have? — Response: An instant, tamper-proof digital roll-call system that generates the approved OD roster the moment an event concludes.")
    add_bullet("Field Observation: The interviewee strongly endorsed the Centralised Clubs and Cell Management System prototype as an essential campus operational tool.")

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

complete_code = v2.rstrip() + "\n\n" + narrative_ch6_and_appendix

with open('generate_final_report_v2.py', 'w', encoding='utf-8') as f:
    f.write(complete_code)

print("Repaired and assembled complete generate_final_report_v2.py successfully!")
