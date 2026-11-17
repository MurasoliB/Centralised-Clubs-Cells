import re

with open("generate_final_report_v2.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update add_table_title to always have keep_with_next = True
old_add_table_title = code[code.find("def add_table_title"):code.find("def add_clean_figure_space")]
new_add_table_title = '''def add_table_title(tbl_num, tbl_name):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r1 = p.add_run(f"Table {tbl_num}   ")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.font.bold = True
        r2 = p.add_run(tbl_name)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        return p

    def format_single_page_table(table, col_widths=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_full_visible_borders(table, border_sz="4")
        num_rows = len(table.rows)
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            cantSplit = trPr.find(qn('w:cantSplit'))
            if cantSplit is None:
                trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            for c_idx, cell in enumerate(row.cells):
                if col_widths and c_idx < len(col_widths):
                    cell.width = col_widths[c_idx]
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.0
                    if r_idx < num_rows - 1:
                        p.paragraph_format.keep_with_next = True

    '''

code = code.replace(old_add_table_title, new_add_table_title, 1)

# 2. Replace Table 3.1 & 3.2
t31_old_start = code.find('add_table_title("3.1",')
t32_old_end = code.find('add_sec_heading("3.3",', t31_old_start)

new_t31_t32 = '''add_table_title("3.1", "Hardware requirements for clients and development environment")
    h_table = doc.add_table(rows=4, cols=3)
    h_col_w = [Inches(2.2), Inches(1.8), Inches(2.5)]
    h_data = [
        ("Hardware Component", "Target User Group", "Functional Purpose"),
        ("Smartphone / Tablet", "Students & Coordinators", "Access web portal, event RSVP, live OD tracking"),
        ("Desktop PC / Laptop", "Faculty & Administrators", "Approve events, schedule venues, audit attendance"),
        ("Development Workstation", "Engineering Team", "Build, test, and host the web application")
    ]
    for i, row in enumerate(h_data):
        for j, val in enumerate(row):
            c = h_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(h_table, h_col_w)

    add_para(
        "Modern progressive web design minimizes hardware dependencies by executing business logic in the cloud. "
        "The web application relies on lightweight responsive frontends that run seamlessly on standard mobile browsers, "
        "requiring zero specialized client hardware installations."
    )

    add_table_title("3.2", "Software tools, frameworks and cloud services")
    s_table = doc.add_table(rows=7, cols=3)
    s_col_w = [Inches(1.8), Inches(2.2), Inches(2.5)]
    s_data = [
        ("Layer", "Technology Platform", "Functional Responsibility"),
        ("Frontend UI", "React 18 & TypeScript", "Component-based reactive single-page app"),
        ("Styling Engine", "Tailwind CSS 3", "Utility-first responsive layouts and dark mode"),
        ("Build Tool", "Vite 5", "Fast native ES module bundling & dev server"),
        ("Client Routing", "React Router DOM", "Role-based client navigation & protection"),
        ("Cloud Backend", "Supabase BaaS", "Auto-generated REST APIs & authentication"),
        ("Database", "PostgreSQL (RLS)", "Relational storage with row-level security")
    ]
    for i, row in enumerate(s_data):
        for j, val in enumerate(row):
            c = s_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(s_table, s_col_w)

    '''

code = code[:t31_old_start] + new_t31_t32 + code[t32_old_end:]

# 3. Replace Table 4.1, 4.2, 4.3
t41_old_start = code.find('add_table_title("4.1",')
t43_old_end = code.find('add_sec_heading("4.4",', t41_old_start)

new_t41_t42_t43 = '''add_table_title("4.1", "Laboratory exercises mapped to design thinking phases")
    dt_table = doc.add_table(rows=8, cols=4)
    dt_col_w = [Inches(0.8), Inches(2.2), Inches(1.5), Inches(2.0)]
    dt_data = [
        ("Ex. No.", "Exercise Name", "Design Phase", "Key Artifacts Produced"),
        ("1", "Identify Problem & Project Scope", "Problem Framing", "Problem statement & constraints"),
        ("2", "User Research using Explore Tools", "Explore", "STEEP trends & stakeholder map"),
        ("4", "Customer Interview & User Mapping", "Empathize", "Empathy map & student journey map"),
        ("5", "User Persona & Need Formulation", "Define", "SPICE framework & persona profile"),
        ("7", "User Scenario & Storytelling", "Ideate", "5-stage narrative storyboard"),
        ("8", "Low-Fidelity Prototyping", "Prototype", "Paper-style UI wireframe layouts"),
        ("9", "Medium-Fidelity Web Implementation", "Prototype / Test", "Working multi-role web prototype")
    ]
    for i, row in enumerate(dt_data):
        for j, val in enumerate(row):
            c = dt_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(dt_table, dt_col_w)

    add_para(
        "Each laboratory exercise generated tangible design artifacts that progressively uncovered root challenges and shaped system behavior. "
        "The explore phase began with environmental scanning of institutional extracurricular dynamics."
    )

    add_sec_heading("4.3", "EXPLORE: UNDERSTANDING THE CONTEXT (EXERCISE 2)")
    add_para(
        "To understand macro-environmental factors influencing college extracurriculars, a comprehensive STEEP (Social, Technological, Economic, "
        "Environmental, Political) analysis was conducted. Trends were evaluated based on their institutional impact and likelihood."
    )

    # 2. Figure 1.2 Clean Area
    add_clean_figure_space("Figure 1.2", "Overall System Workflow", empty_lines=14)

    add_table_title("4.2", "Prioritised STEEP trends for club ecosystem")
    stp_table = doc.add_table(rows=5, cols=3)
    stp_col_w = [Inches(2.0), Inches(2.2), Inches(2.3)]
    stp_data = [
        ("Quadrant", "Prioritized Trend", "Strategic Design Implication"),
        ("High Impact / High Likelihood", "Paperless campus governance", "Digital workflows for approvals and OD tracking"),
        ("High Impact / High Likelihood", "Stricter NAAC/NBA audit rules", "Automated report generation for accreditation"),
        ("High Impact / Medium Likelihood", "Faculty digital adoption rate", "Intuitive UI requiring zero formal training"),
        ("Medium Impact / High Likelihood", "Mobile-first student browsing", "Fully responsive layouts on smartphones")
    ]
    for i, row in enumerate(stp_data):
        for j, val in enumerate(row):
            c = stp_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(stp_table, stp_col_w)

    add_para(
        "Stakeholder mapping identified diverse constituent groups with varying degrees of institutional influence and operational interest. "
        "Table 4.3 outlines engagement protocols tailored to each quadrant."
    )

    add_table_title("4.3", "Stakeholder classification and engagement strategy")
    stk_table = doc.add_table(rows=5, cols=3)
    stk_col_w = [Inches(1.8), Inches(2.2), Inches(2.5)]
    stk_data = [
        ("Influence / Interest", "Stakeholder Group", "Engagement Strategy"),
        ("High Power / High Interest", "Principal & Department Heads", "Manage Closely: Policy reviews & milestone demos"),
        ("Low Power / High Interest", "Students & Club Members", "Keep Satisfied: Fast mobile discovery & instant OD"),
        ("High Power / Low Interest", "Campus IT & ERP Admin", "Keep Informed: System compatibility & data security"),
        ("Low Power / Low Interest", "External Auditors & Alumni", "Monitor: Verified event credentials & audit logs")
    ]
    for i, row in enumerate(stk_data):
        for j, val in enumerate(row):
            c = stk_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(stk_table, stk_col_w)

    '''

code = code[:t41_old_start] + new_t41_t42_t43 + code[t43_old_end:]

# 4. Replace Table 4.4 & 4.5 (Persona & Storyboard)
t44_old_start = code.find('add_table_title("4.4", "Active Student Leader & Campus Member Persona Summary")')
t45_old_end = code.find('add_ch_title("5. PROTOTYPE IMPLEMENTATION")', t44_old_start)

new_t44_t45 = '''add_table_title("4.4", "Active Student Leader & Campus Member Persona Summary")
    per_table = doc.add_table(rows=6, cols=2)
    per_col_w = [Inches(2.2), Inches(4.3)]
    per_data = [
        ("Persona Attribute", "Details & Behavioral Characteristics"),
        ("Name & Demographics", "Arun Kumar; 20 Years Old; 3rd Year B.Tech IT Student"),
        ("Core Goals", "Join premier technical societies, lead hackathons, build portfolio"),
        ("Key Pain Points", "Misses event notices on WhatsApp; 4-day delays for paper OD forms"),
        ("Tech Behavior", "Active mobile user; expects instant push notifications & one-click RSVP"),
        ("Emotional Need", "Assurance that co-curricular attendance is officially regularized by faculty")
    ]
    for i, row in enumerate(per_data):
        for j, val in enumerate(row):
            c = per_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(per_table, per_col_w)

    add_sec_heading("4.6", "IDEATE: STORYTELLING")
    add_para(
        "A five-stage narrative storyboard was composed to visualize the transformative impact of the proposed system "
        "on the daily life and co-curricular journey of the primary persona."
    )

    add_table_title("4.5", "Storyboard of the persona narrative")
    sty_table = doc.add_table(rows=6, cols=2)
    sty_col_w = [Inches(2.0), Inches(4.5)]
    sty_data = [
        ("Narrative Stage", "User Journey Storyline & Touchpoint"),
        ("1. The Persona", "Arun wants to actively participate in campus technical clubs."),
        ("2. The Setting", "A busy autonomous college campus with 18+ independent clubs."),
        ("3. The Conflict", "Arun misses a hackathon registration due to scattered paper circulars."),
        ("4. The Solution", "Arun opens ClubHub, discovers events, and reserves a seat in one click."),
        ("5. The Resolution", "Coordinator scans his attendance; signed On-Duty roster is generated instantly.")
    ]
    for i, row in enumerate(sty_data):
        for j, val in enumerate(row):
            c = sty_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(sty_table, sty_col_w)

    '''

code = code[:t44_old_start] + new_t44_t45 + code[t45_old_end:]

# 5. Replace Table 5.1 (Modules)
t51_old_start = code.find('add_table_title("5.1",')
t51_old_end = code.find('add_sec_heading("5.4",', t51_old_start)

new_t51 = '''add_table_title("5.1", "Screens and functional modules of the web prototype")
    mod_table = doc.add_table(rows=8, cols=3)
    mod_col_w = [Inches(1.8), Inches(2.3), Inches(2.4)]
    mod_data = [
        ("Interface / Module", "Core Technical Feature", "Operational Benefit"),
        ("Portal Landing Page", "Single-click role gateway", "Fast, welcoming entry for students & faculty"),
        ("Admin Dashboard", "Campus-wide live metrics", "Executive oversight of club health & events"),
        ("Faculty Console", "Event approval & scheduling", "Eliminates venue clashes & paper delays"),
        ("Clubs Directory", "Categorized club search", "Central discovery across all campus domains"),
        ("Event RSVP Hub", "Real-time seat counter", "Prevents overcrowding with atomic booking"),
        ("Roll-Call Console", "Mobile digital roll-call", "Instant verified On-Duty roster export"),
        ("Student Portfolio", "Digital credentials vault", "Accreditation-ready extracurricular records")
    ]
    for i, row in enumerate(mod_data):
        for j, val in enumerate(row):
            c = mod_table.rows[i].cells[j]
            r = c.paragraphs[0].add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if i == 0:
                r.font.bold = True
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_single_page_table(mod_table, mod_col_w)

    '''

code = code[:t51_old_start] + new_t51 + code[t51_old_end:]

with open("generate_final_report_v2.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully updated all 8 tables to simple, compact, single-page format!")
