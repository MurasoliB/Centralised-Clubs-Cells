import os
import subprocess
import shutil

DIAGRAMS_DIR = os.path.abspath("diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
TEMP_DIR = os.environ.get("TEMP", "C:\\temp")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content, output_png_name, width=1600, height=1100):
    html_path = os.path.join(DIAGRAMS_DIR, f"{output_png_name}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    temp_png_path = os.path.join(TEMP_DIR, f"{output_png_name}.png")
    final_png_path = os.path.join(DIAGRAMS_DIR, f"{output_png_name}.png")
    
    if os.path.exists(temp_png_path):
        os.remove(temp_png_path)
    
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={temp_png_path}",
        "--hide-scrollbars",
        file_url
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if os.path.exists(temp_png_path):
        shutil.copy2(temp_png_path, final_png_path)
        print(f"SUCCESS: Generated {final_png_path}")
        return True
    else:
        print(f"FAILED: Could not generate {final_png_path}")
        return False

# Common CSS styling for documentation diagrams
BASE_STYLE = """
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        background-color: #ffffff;
        color: #0f172a;
        padding: 40px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
    .diagram-container {
        width: 1520px;
        background: #ffffff;
        border: 2px solid #0f172a;
        padding: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header {
        text-align: center;
        border-bottom: 2px solid #0f172a;
        padding-bottom: 16px;
        margin-bottom: 25px;
    }
    .header h1 {
        font-size: 24px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #0f172a;
        margin-bottom: 6px;
    }
    .header p {
        font-size: 15px;
        color: #475569;
        font-weight: 500;
    }
    .diagram-body {
        width: 100%;
    }
    .box {
        background: #f8fafc;
        border: 1.5px solid #1e293b;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .box-title {
        font-size: 14px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .box-desc {
        font-size: 11px;
        color: #475569;
        line-height: 1.3;
    }
    .layer-card {
        border: 1.5px dashed #475569;
        border-radius: 8px;
        background: #f8fafc;
        padding: 16px 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .layer-badge {
        position: absolute;
        top: -12px;
        left: 24px;
        background: #0f172a;
        color: #ffffff;
        font-size: 12px;
        font-weight: 700;
        padding: 2px 14px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
</style>
"""

# ==============================================================================
# 1. System Architecture Diagram
# ==============================================================================
html_arch = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .tiers-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-top: 10px;
    }}
    .tier-box {{
        background: #ffffff;
        border: 1.5px solid #334155;
        border-radius: 6px;
        padding: 12px;
    }}
    .tier-box-header {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 6px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .tier-box-item {{
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 6px 8px;
        margin-bottom: 6px;
        font-size: 11px;
        color: #1e293b;
        font-weight: 600;
        text-align: left;
    }}
    .tier-box-item span {{
        display: block;
        font-size: 10px;
        color: #64748b;
        font-weight: 400;
    }}
    .connector-row {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 28px;
        color: #475569;
        font-size: 12px;
        font-weight: 700;
    }}
    .connector-row svg {{
        height: 24px;
        width: 100%;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 1.1: System Architecture Diagram</h1>
        <p>Four-Tier Centralised Management Ecosystem with Role-Based Access Control & Autonomous ERP Integration</p>
    </div>
    <div class="diagram-body">
        <!-- TIER 1 -->
        <div class="layer-card">
            <div class="layer-badge">Tier 1: Presentation & Client Interaction Layer</div>
            <div class="tiers-grid">
                <div class="tier-box">
                    <div class="tier-box-header">👨‍🎓 Student Portal <span>Web / Mobile</span></div>
                    <div class="tier-box-item">Central Clubs Discovery<span>Browse active clubs & cells</span></div>
                    <div class="tier-box-item">Online Recruitment Pass<span>Apply for club membership</span></div>
                    <div class="tier-box-item">Event RSVP & QR Passes<span>Instant digital seat reservation</span></div>
                    <div class="tier-box-item">Live OD Attendance Tracker<span>Real-time duty clearance log</span></div>
                </div>
                <div class="tier-box">
                    <div class="tier-box-header">👩‍🏫 Faculty Coordinator <span>Console</span></div>
                    <div class="tier-box-item">Event Proposal Workflow<span>Submit dates & venue requests</span></div>
                    <div class="tier-box-item">Mobile Roll-Call Interface<span>1-tap attendance marking</span></div>
                    <div class="tier-box-item">Instant On-Duty Roster<span>Automated letter drafting</span></div>
                    <div class="tier-box-item">Candidate Vetting Hub<span>Review applicant portfolios</span></div>
                </div>
                <div class="tier-box">
                    <div class="tier-box-header">🏛️ Institutional Admin <span>Executive</span></div>
                    <div class="tier-box-item">Clubs & Cells Directory<span>Charter approvals & quotas</span></div>
                    <div class="tier-box-item">RBAC Role Provisioning<span>Faculty & student permissioning</span></div>
                    <div class="tier-box-item">Venue Clash Algorithm<span>Automated conflict detection</span></div>
                    <div class="tier-box-item">NAAC / NBA Export Suite<span>Criterion 5 accreditation logs</span></div>
                </div>
                <div class="tier-box">
                    <div class="tier-box-header">🏢 Dean & Department HOD <span>Approvals</span></div>
                    <div class="tier-box-item">On-Duty Digital Endorse<span>Inter-departmental clearance</span></div>
                    <div class="tier-box-item">Student Activity Records<span>Co-curricular transcript log</span></div>
                    <div class="tier-box-item">Annual Milestone Dossier<span>Consolidated metrics reports</span></div>
                    <div class="tier-box-item">Policy Compliance Monitor<span>Extracurricular regulation</span></div>
                </div>
            </div>
        </div>

        <!-- CONNECTOR 1 -->
        <div class="connector-row">
            <svg viewBox="0 0 1000 24" preserveAspectRatio="none">
                <line x1="200" y1="0" x2="200" y2="24" stroke="#0f172a" stroke-width="2" stroke-dasharray="4"/>
                <line x1="500" y1="0" x2="500" y2="24" stroke="#0f172a" stroke-width="2" stroke-dasharray="4"/>
                <line x1="800" y1="0" x2="800" y2="24" stroke="#0f172a" stroke-width="2" stroke-dasharray="4"/>
                <text x="500" y="16" text-anchor="middle" font-size="11" fill="#0f172a" font-weight="700" background="#fff">HTTPS / TLS 1.3 Encrypted REST & WebSocket Traffic</text>
            </svg>
        </div>

        <!-- TIER 2 -->
        <div class="layer-card">
            <div class="layer-badge">Tier 2: Single Page Application (SPA) Frontend Engine</div>
            <div class="tiers-grid">
                <div class="tier-box">
                    <div class="tier-box-header">⚡ Core Framework</div>
                    <div class="tier-box-item">React 18.2 (Functional)<span>Component modular architecture</span></div>
                    <div class="tier-box-item">TypeScript 5.0 Strict<span>Static type checking & safety</span></div>
                </div>
                <div class="tier-box">
                    <div class="tier-box-header">🎨 Styling & Layout</div>
                    <div class="tier-box-item">Tailwind CSS Framework<span>Utility-first responsive styles</span></div>
                    <div class="tier-box-item">Wikipedia Vector Clean<span>High contrast academic UI design</span></div>
                </div>
                <div class="tier-box">
                    <div class="tier-box-header">🧭 State & Navigation</div>
                    <div class="tier-box-item">React Router v6 DOM<span>Protected route boundaries</span></div>
                    <div class="tier-box-item">Context API State<span>Session & auth global states</span></div>
                </div>
                <div class="tier-box">
                    <div class="tier-box-header">📦 Build & Assets</div>
                    <div class="tier-box-item">Vite 5 Lightning Bundler<span>Hot module replacement engine</span></div>
                    <div class="tier-box-item">Lucide Vector Icons<span>Accessible monochrome icon set</span></div>
                </div>
            </div>
        </div>

        <!-- CONNECTOR 2 -->
        <div class="connector-row">
            <svg viewBox="0 0 1000 24" preserveAspectRatio="none">
                <line x1="500" y1="0" x2="500" y2="24" stroke="#0f172a" stroke-width="2"/>
                <polygon points="500,24 494,14 506,14" fill="#0f172a"/>
                <text x="500" y="12" text-anchor="middle" font-size="11" fill="#0f172a" font-weight="700">Supabase JS Client SDK / JWT Bearer Tokens</text>
            </svg>
        </div>

        <!-- TIER 3 & 4 IN TWO COLUMNS -->
        <div style="display: grid; grid-template-columns: 2fr 1.2fr; gap: 20px;">
            <div class="layer-card" style="margin-bottom: 0;">
                <div class="layer-badge">Tier 3: Backend Services & Business Logic Gateway</div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                    <div class="tier-box">
                        <div class="tier-box-header">🔒 Auth & RBAC</div>
                        <div class="tier-box-item">Supabase Auth Gateway<span>JWT token validation</span></div>
                        <div class="tier-box-item">Role Interceptors<span>Student, Faculty, Admin guards</span></div>
                    </div>
                    <div class="tier-box">
                        <div class="tier-box-header">⚙️ Business Logic</div>
                        <div class="tier-box-item">Clash Detection Engine<span>Time & hall conflict checks</span></div>
                        <div class="tier-box-item">OD Compilation Worker<span>Auto-aggregates roll calls</span></div>
                    </div>
                    <div class="tier-box">
                        <div class="tier-box-header">🛡️ Security Gateway</div>
                        <div class="tier-box-item">PostgreSQL Row Security<span>Per-club tenant isolation</span></div>
                        <div class="tier-box-item">Audit Trail Triggers<span>Immutable administrative logs</span></div>
                    </div>
                </div>
            </div>

            <div class="layer-card" style="margin-bottom: 0;">
                <div class="layer-badge">Tier 4: Enterprise Integrations & Storage</div>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                    <div class="tier-box">
                        <div class="tier-box-header">🗄️ PostgreSQL DB</div>
                        <div class="tier-box-item">ACID Relational Core<span>Users, Orgs, Events, OD</span></div>
                        <div class="tier-box-item">Database Schemas<span>Foreign key integrity</span></div>
                    </div>
                    <div class="tier-box">
                        <div class="tier-box-header">🌐 Campus ERP API</div>
                        <div class="tier-box-item">ERP Attendance Sync<span>Direct attendance credit</span></div>
                        <div class="tier-box-item">SMTP Email Relay<span>Automated ticket dispatch</span></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 2. Overall System Workflow
# ==============================================================================
html_workflow = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .flow-steps {{
        display: flex;
        flex-direction: column;
        gap: 14px;
    }}
    .flow-step-row {{
        display: grid;
        grid-template-columns: 80px 220px 1fr 240px;
        background: #f8fafc;
        border: 1.5px solid #334155;
        border-radius: 6px;
        overflow: hidden;
        align-items: stretch;
    }}
    .step-num {{
        background: #0f172a;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 800;
    }}
    .step-role {{
        background: #e2e8f0;
        border-right: 1.5px solid #cbd5e1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 12px 16px;
    }}
    .step-role-title {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
    }}
    .step-role-badge {{
        font-size: 10px;
        color: #475569;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 2px;
    }}
    .step-desc {{
        padding: 12px 18px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-right: 1.5px solid #cbd5e1;
    }}
    .step-desc-title {{
        font-size: 14px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 2px;
    }}
    .step-desc-body {{
        font-size: 12px;
        color: #334155;
        line-height: 1.4;
    }}
    .step-artifact {{
        background: #ffffff;
        padding: 12px 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .step-artifact-title {{
        font-size: 11px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 2px;
    }}
    .step-artifact-badge {{
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: 600;
        color: #0f172a;
    }}
    .arrow-down {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 12px;
        color: #0f172a;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 1.2: Overall System Workflow</h1>
        <p>End-to-End Operational Lifecycle from Club Discovery to Automated On-Duty (OD) Academic Clearance</p>
    </div>
    <div class="diagram-body">
        <div class="flow-steps">
            <!-- STEP 1 -->
            <div class="flow-step-row">
                <div class="step-num">01</div>
                <div class="step-role">
                    <div class="step-role-title">College Admin</div>
                    <div class="step-role-badge">Institutional Setup</div>
                </div>
                <div class="step-desc">
                    <div class="step-desc-title">Club Charter Onboarding & Faculty Assigning</div>
                    <div class="step-desc-body">Admin configures central club entities, verifies founding mandates, assigns designated Faculty Advisors, and establishes departmental governance bounds.</div>
                </div>
                <div class="step-artifact">
                    <div class="step-artifact-title">Output Artifact</div>
                    <div class="step-artifact-badge">Active Club Charter & RLS Policy</div>
                </div>
            </div>

            <div class="arrow-down">▼</div>

            <!-- STEP 2 -->
            <div class="flow-step-row">
                <div class="step-num">02</div>
                <div class="step-role">
                    <div class="step-role-title">Student Applicant</div>
                    <div class="step-role-badge">Discovery & Join</div>
                </div>
                <div class="step-desc">
                    <div class="step-desc-title">Centralized Discovery & Membership Application</div>
                    <div class="step-desc-body">Student browses verified clubs and cells directory, examines past activities, selects target organization, and submits multi-question recruitment application.</div>
                </div>
                <div class="step-artifact">
                    <div class="step-artifact-title">Output Artifact</div>
                    <div class="step-artifact-badge">Pending Membership Application</div>
                </div>
            </div>

            <div class="arrow-down">▼</div>

            <!-- STEP 3 -->
            <div class="flow-step-row">
                <div class="step-num">03</div>
                <div class="step-role">
                    <div class="step-role-title">Faculty Advisor</div>
                    <div class="step-role-badge">Vetting & Induction</div>
                </div>
                <div class="step-desc">
                    <div class="step-desc-title">Application Review & Digital Induction</div>
                    <div class="step-desc-body">Faculty reviews submissions through the evaluation pipeline, marks interview feedback, and confirms inductees. Real-time notifications alert the student.</div>
                </div>
                <div class="step-artifact">
                    <div class="step-artifact-title">Output Artifact</div>
                    <div class="step-artifact-badge">Verified Member Profile & Role</div>
                </div>
            </div>

            <div class="arrow-down">▼</div>

            <!-- STEP 4 -->
            <div class="flow-step-row">
                <div class="step-num">04</div>
                <div class="step-role">
                    <div class="step-role-title">Club Coordinator</div>
                    <div class="step-role-badge">Event Creation</div>
                </div>
                <div class="step-desc">
                    <div class="step-desc-title">Event Scheduling & Clash-Free Publishing</div>
                    <div class="step-desc-body">Coordinator creates symposium/workshop proposal. The system executes automated venue clash detection before faculty approval and campus publication.</div>
                </div>
                <div class="step-artifact">
                    <div class="step-artifact-title">Output Artifact</div>
                    <div class="step-artifact-badge">Published Event & RSVP Hub</div>
                </div>
            </div>

            <div class="arrow-down">▼</div>

            <!-- STEP 5 -->
            <div class="flow-step-row">
                <div class="step-num">05</div>
                <div class="step-role">
                    <div class="step-role-title">Event Coordinator</div>
                    <div class="step-role-badge">Execution & Roll-Call</div>
                </div>
                <div class="step-desc">
                    <div class="step-desc-title">Real-Time Mobile Attendance Logging</div>
                    <div class="step-desc-body">During event execution, coordinators access the live mobile roll-call console to record attendee presence with instantaneous timestamping and fraud prevention.</div>
                </div>
                <div class="step-artifact">
                    <div class="step-artifact-title">Output Artifact</div>
                    <div class="step-artifact-badge">Verified Attendance Ledger</div>
                </div>
            </div>

            <div class="arrow-down">▼</div>

            <!-- STEP 6 -->
            <div class="flow-step-row">
                <div class="step-num">06</div>
                <div class="step-role">
                    <div class="step-role-title">System & Dean</div>
                    <div class="step-role-badge">OD Sync & Archival</div>
                </div>
                <div class="step-desc">
                    <div class="step-desc-title">Automated On-Duty (OD) Generation & ERP Sync</div>
                    <div class="step-desc-body">The system instantly drafts formal OD documentation sorted by roll number and department, transmits to Dean for digital sign-off, and syncs with ERP attendance.</div>
                </div>
                <div class="step-artifact">
                    <div class="step-artifact-title">Output Artifact</div>
                    <div class="step-artifact-badge">Official OD Clearance & ERP Credit</div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 3. Use Case Diagram
# ==============================================================================
html_usecase = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .usecase-layout {{
        display: grid;
        grid-template-columns: 200px 1fr 220px;
        gap: 30px;
        align-items: center;
    }}
    .actor-col {{
        display: flex;
        flex-direction: column;
        gap: 40px;
        align-items: center;
    }}
    .actor-card {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}
    .actor-icon {{
        width: 52px;
        height: 52px;
        background: #0f172a;
        color: #fff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    .actor-name {{
        font-size: 14px;
        font-weight: 700;
        color: #0f172a;
    }}
    .actor-type {{
        font-size: 11px;
        color: #64748b;
        font-weight: 600;
    }}
    .system-boundary {{
        border: 2px solid #0f172a;
        border-radius: 12px;
        padding: 24px 20px;
        background: #f8fafc;
        position: relative;
    }}
    .boundary-title {{
        position: absolute;
        top: -14px;
        left: 30px;
        background: #0f172a;
        color: #ffffff;
        font-size: 13px;
        font-weight: 700;
        padding: 3px 18px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }}
    .cases-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-top: 10px;
    }}
    .use-case-ellipse {{
        background: #ffffff;
        border: 1.5px solid #0f172a;
        border-radius: 24px;
        padding: 10px 14px;
        text-align: center;
        font-size: 12px;
        font-weight: 700;
        color: #1e293b;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 50px;
        line-height: 1.25;
    }}
    .use-case-ellipse span {{
        display: block;
        font-size: 9px;
        font-weight: 400;
        color: #64748b;
        margin-top: 2px;
    }}
    .sub-case {{
        border-style: dashed;
        border-color: #475569;
        background: #f1f5f9;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 2.1: Use Case Diagram</h1>
        <p>Unified Modeling Language (UML) Behavioral Specification for Stakeholder Roles & Autonomous Subsystems</p>
    </div>
    <div class="diagram-body">
        <div class="usecase-layout">
            <!-- ACTORS LEFT -->
            <div class="actor-col">
                <div class="actor-card">
                    <div class="actor-icon">👨‍🎓</div>
                    <div class="actor-name">Student User</div>
                    <div class="actor-type">Primary Actor</div>
                </div>
                <div class="actor-card">
                    <div class="actor-icon">👩‍🏫</div>
                    <div class="actor-name">Faculty Coordinator</div>
                    <div class="actor-type">Operational Actor</div>
                </div>
            </div>

            <!-- SYSTEM BOUNDARY -->
            <div class="system-boundary">
                <div class="boundary-title">System Boundary: Centralised Clubs and Cell Management System (ClubHub)</div>
                <div class="cases-grid">
                    <!-- Column 1: Student focused -->
                    <div class="use-case-ellipse">User Authentication & SSO<span>&laquo;include&raquo; by all</span></div>
                    <div class="use-case-ellipse">Browse Clubs & Cells Directory<span>Filter by category & tier</span></div>
                    <div class="use-case-ellipse">Submit Membership Application<span>Multi-stage candidate vetting</span></div>
                    <div class="use-case-ellipse">Register for Campus Events<span>RSVP with capacity checks</span></div>
                    <div class="use-case-ellipse">Access Digital Ticket Pass<span>QR-based entry voucher</span></div>

                    <!-- Column 2: Faculty & Ops focused -->
                    <div class="use-case-ellipse">Track Live On-Duty Status<span>Real-time academic log</span></div>
                    <div class="use-case-ellipse">Review Member Applications<span>Interview & induction actions</span></div>
                    <div class="use-case-ellipse">Schedule Event Proposals<span>Venue conflict checking</span></div>
                    <div class="use-case-ellipse">Execute Mobile Roll-Call<span>Real-time presence logging</span></div>
                    <div class="use-case-ellipse">Compile Official OD Roster<span>Automated letter compilation</span></div>

                    <!-- Column 3: Admin & ERP focused -->
                    <div class="use-case-ellipse">Manage User Accounts & Roles<span>RBAC credential assignment</span></div>
                    <div class="use-case-ellipse">Charter Club & Cell Governance<span>Quotas, budgets & advisors</span></div>
                    <div class="use-case-ellipse">Generate NAAC / NBA Dossiers<span>Criterion 5 accreditation</span></div>
                    <div class="use-case-ellipse sub-case">Synchronize with College ERP<span>&laquo;extend&raquo; automated API</span></div>
                    <div class="use-case-ellipse sub-case">Dispatch Email & System Alerts<span>&laquo;extend&raquo; notification bus</span></div>
                </div>
            </div>

            <!-- ACTORS RIGHT -->
            <div class="actor-col">
                <div class="actor-card">
                    <div class="actor-icon">🏛️</div>
                    <div class="actor-name">System Admin</div>
                    <div class="actor-type">Governance Actor</div>
                </div>
                <div class="actor-card">
                    <div class="actor-icon">🏢</div>
                    <div class="actor-name">Autonomous ERP</div>
                    <div class="actor-type">External System</div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 4. Data Flow Diagram
# ==============================================================================
html_dfd = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .dfd-grid {{
        display: grid;
        grid-template-columns: 220px 1fr 220px;
        gap: 20px;
        align-items: center;
    }}
    .entity-box {{
        background: #0f172a;
        color: #ffffff;
        border: 2px solid #0f172a;
        border-radius: 6px;
        padding: 16px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    .entity-title {{
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .entity-sub {{
        font-size: 11px;
        color: #94a3b8;
        margin-top: 2px;
    }}
    .process-cluster {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }}
    .process-circle {{
        background: #ffffff;
        border: 2px solid #1e293b;
        border-radius: 8px;
        padding: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .process-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1.5px solid #e2e8f0;
        padding-bottom: 6px;
        margin-bottom: 8px;
    }}
    .process-num {{
        background: #0f172a;
        color: #ffffff;
        font-size: 11px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
    }}
    .process-name {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
    }}
    .process-flows {{
        font-size: 11px;
        color: #475569;
        line-height: 1.4;
    }}
    .store-bar {{
        background: #f1f5f9;
        border-top: 2px solid #0f172a;
        border-bottom: 2px solid #0f172a;
        padding: 6px 12px;
        margin-top: 8px;
        font-size: 11px;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        justify-content: space-between;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 2.2: Data Flow Diagram (Level 1)</h1>
        <p>Transformation of Information across Core Functional Processes, External Entities, and Relational Data Stores</p>
    </div>
    <div class="diagram-body">
        <div class="dfd-grid">
            <!-- LEFT ENTITIES -->
            <div>
                <div class="entity-box">
                    <div class="entity-title">STUDENT</div>
                    <div class="entity-sub">External Entity [E1]</div>
                </div>
                <div class="entity-box" style="margin-bottom: 0;">
                    <div class="entity-title">FACULTY COORDINATOR</div>
                    <div class="entity-sub">External Entity [E2]</div>
                </div>
            </div>

            <!-- CENTRAL PROCESSES & DATA STORES -->
            <div>
                <div class="process-cluster">
                    <!-- P1 -->
                    <div class="process-circle">
                        <div class="process-header">
                            <span class="process-num">1.0</span>
                            <span class="process-name">Authentication & RBAC</span>
                        </div>
                        <div class="process-flows">
                            Inputs: Credentials, Roll Number<br>
                            Outputs: Session Token, Role Claims
                        </div>
                        <div class="store-bar">
                            <span>D1</span> <span>User Accounts & Roles</span>
                        </div>
                    </div>

                    <!-- P2 -->
                    <div class="process-circle">
                        <div class="process-header">
                            <span class="process-num">2.0</span>
                            <span class="process-name">Club & Recruitment</span>
                        </div>
                        <div class="process-flows">
                            Inputs: Application Profile, Status Vetting<br>
                            Outputs: Induction List, Membership Pass
                        </div>
                        <div class="store-bar">
                            <span>D2</span> <span>Clubs & Memberships Registry</span>
                        </div>
                    </div>

                    <!-- P3 -->
                    <div class="process-circle">
                        <div class="process-header">
                            <span class="process-num">3.0</span>
                            <span class="process-name">Event Scheduling & Clash</span>
                        </div>
                        <div class="process-flows">
                            Inputs: Date, Venue, Seating Cap<br>
                            Outputs: Approved Schedule, Public Listing
                        </div>
                        <div class="store-bar">
                            <span>D3</span> <span>Events & Schedule Store</span>
                        </div>
                    </div>

                    <!-- P4 -->
                    <div class="process-circle">
                        <div class="process-header">
                            <span class="process-num">4.0</span>
                            <span class="process-name">Registration & Passes</span>
                        </div>
                        <div class="process-flows">
                            Inputs: RSVP Request, Student Token<br>
                            Outputs: Digital Entry Pass, Headcount Cap
                        </div>
                        <div class="store-bar">
                            <span>D4</span> <span>Registrations & Tickets</span>
                        </div>
                    </div>

                    <!-- P5 -->
                    <div class="process-circle">
                        <div class="process-header">
                            <span class="process-num">5.0</span>
                            <span class="process-name">Real-Time Roll-Call</span>
                        </div>
                        <div class="process-flows">
                            Inputs: Coordinator Check-in, Geo-stamp<br>
                            Outputs: Verified Attendance Log, Non-Attendees
                        </div>
                        <div class="store-bar">
                            <span>D5</span> <span>Attendance & Audit Ledgers</span>
                        </div>
                    </div>

                    <!-- P6 -->
                    <div class="process-circle">
                        <div class="process-header">
                            <span class="process-num">6.0</span>
                            <span class="process-name">On-Duty & ERP Sync</span>
                        </div>
                        <div class="process-flows">
                            Inputs: Verified Presence, Faculty e-Sign<br>
                            Outputs: Formal OD Dossier, ERP Sync Credit
                        </div>
                        <div class="store-bar">
                            <span>D6</span> <span>On-Duty (OD) Archive</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- RIGHT ENTITIES -->
            <div>
                <div class="entity-box">
                    <div class="entity-title">COLLEGE ADMIN</div>
                    <div class="entity-sub">External Entity [E3]</div>
                </div>
                <div class="entity-box" style="margin-bottom: 0;">
                    <div class="entity-title">AUTONOMOUS ERP</div>
                    <div class="entity-sub">External System [E4]</div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 5. Entity Relationship Diagram
# ==============================================================================
html_erd = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .erd-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }}
    .entity-card {{
        background: #ffffff;
        border: 2px solid #0f172a;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}
    .entity-header {{
        background: #0f172a;
        color: #ffffff;
        padding: 8px 12px;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        justify-content: space-between;
    }}
    .entity-header span {{
        font-size: 10px;
        background: #334155;
        padding: 2px 6px;
        border-radius: 3px;
    }}
    .entity-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }}
    .entity-table td {{
        padding: 6px 10px;
        border-bottom: 1px solid #e2e8f0;
    }}
    .col-key {{
        font-weight: 700;
        width: 32px;
        text-align: center;
    }}
    .pk {{ color: #dc2626; }}
    .fk {{ color: #2563eb; }}
    .col-name {{
        font-weight: 600;
        color: #0f172a;
    }}
    .col-type {{
        color: #64748b;
        text-align: right;
        font-family: monospace;
        font-size: 10px;
    }}
    .rel-summary {{
        margin-top: 20px;
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 6px;
        padding: 12px 20px;
        display: flex;
        justify-content: space-around;
        font-size: 11px;
        font-weight: 600;
        color: #1e293b;
    }}
    .rel-badge {{
        background: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 4px;
        padding: 4px 10px;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 3.1: Entity Relationship Diagram (ERD)</h1>
        <p>PostgreSQL Relational Schema with Primary Keys, Foreign Keys, and Referential Constraints</p>
    </div>
    <div class="diagram-body">
        <div class="erd-grid">
            <!-- 1. USERS -->
            <div class="entity-card">
                <div class="entity-header">USERS <span>Primary Entity</span></div>
                <table class="entity-table">
                    <tr><td class="col-key pk">PK</td><td class="col-name">user_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">email</td><td class="col-type">VARCHAR(255)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">full_name</td><td class="col-type">VARCHAR(120)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">roll_number</td><td class="col-type">VARCHAR(20)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">role</td><td class="col-type">ENUM(Role)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">department</td><td class="col-type">VARCHAR(50)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">created_at</td><td class="col-type">TIMESTAMP</td></tr>
                </table>
            </div>

            <!-- 2. ORGANIZATIONS -->
            <div class="entity-card">
                <div class="entity-header">ORGANIZATIONS <span>Clubs & Cells</span></div>
                <table class="entity-table">
                    <tr><td class="col-key pk">PK</td><td class="col-name">org_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">name</td><td class="col-type">VARCHAR(150)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">category</td><td class="col-type">ENUM(Type)</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">faculty_advisor_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">description</td><td class="col-type">TEXT</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">status</td><td class="col-type">VARCHAR(20)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">created_at</td><td class="col-type">TIMESTAMP</td></tr>
                </table>
            </div>

            <!-- 3. MEMBERSHIPS -->
            <div class="entity-card">
                <div class="entity-header">MEMBERSHIPS <span>Associative</span></div>
                <table class="entity-table">
                    <tr><td class="col-key pk">PK</td><td class="col-name">membership_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">user_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">org_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">role_in_club</td><td class="col-type">VARCHAR(50)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">status</td><td class="col-type">ENUM(Status)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">applied_at</td><td class="col-type">TIMESTAMP</td></tr>
                </table>
            </div>

            <!-- 4. EVENTS -->
            <div class="entity-card">
                <div class="entity-header">EVENTS <span>Transactional</span></div>
                <table class="entity-table">
                    <tr><td class="col-key pk">PK</td><td class="col-name">event_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">org_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">title</td><td class="col-type">VARCHAR(200)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">venue</td><td class="col-type">VARCHAR(100)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">event_date</td><td class="col-type">TIMESTAMP</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">capacity</td><td class="col-type">INTEGER</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">status</td><td class="col-type">VARCHAR(20)</td></tr>
                </table>
            </div>

            <!-- 5. REGISTRATIONS -->
            <div class="entity-card">
                <div class="entity-header">REGISTRATIONS <span>RSVP Ledger</span></div>
                <table class="entity-table">
                    <tr><td class="col-key pk">PK</td><td class="col-name">registration_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">event_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">user_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">ticket_code</td><td class="col-type">VARCHAR(64)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">status</td><td class="col-type">VARCHAR(20)</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">registered_at</td><td class="col-type">TIMESTAMP</td></tr>
                </table>
            </div>

            <!-- 6. ATTENDANCE_RECORDS -->
            <div class="entity-card">
                <div class="entity-header">ATTENDANCE_RECORDS <span>Verification</span></div>
                <table class="entity-table">
                    <tr><td class="col-key pk">PK</td><td class="col-name">attendance_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">event_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">user_id</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key fk">FK</td><td class="col-name">marked_by</td><td class="col-type">UUID</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">marked_at</td><td class="col-type">TIMESTAMP</td></tr>
                    <tr><td class="col-key"></td><td class="col-name">od_eligible</td><td class="col-type">BOOLEAN</td></tr>
                </table>
            </div>
        </div>

        <div class="rel-summary">
            <div class="rel-badge">USERS (1) ────&lt; (M) MEMBERSHIPS</div>
            <div class="rel-badge">ORGANIZATIONS (1) ────&lt; (M) MEMBERSHIPS</div>
            <div class="rel-badge">ORGANIZATIONS (1) ────&lt; (M) EVENTS</div>
            <div class="rel-badge">EVENTS (1) ────&lt; (M) REGISTRATIONS</div>
            <div class="rel-badge">EVENTS (1) ────&lt; (M) ATTENDANCE_RECORDS</div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 6. Database Structure
# ==============================================================================
html_db_struct = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .schema-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 18px;
    }}
    .table-box {{
        background: #ffffff;
        border: 1.5px solid #0f172a;
        border-radius: 6px;
        overflow: hidden;
    }}
    .table-box-header {{
        background: #f1f5f9;
        border-bottom: 1.5px solid #0f172a;
        padding: 8px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .table-box-name {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
        font-family: monospace;
    }}
    .table-box-engine {{
        font-size: 10px;
        background: #0f172a;
        color: #fff;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: 600;
    }}
    .dict-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }}
    .dict-table th {{
        background: #e2e8f0;
        color: #0f172a;
        font-weight: 700;
        text-align: left;
        padding: 5px 8px;
        border-bottom: 1px solid #cbd5e1;
    }}
    .dict-table td {{
        padding: 5px 8px;
        border-bottom: 1px solid #f1f5f9;
        font-family: monospace;
    }}
    .dict-col {{ font-weight: 600; color: #0f172a; }}
    .dict-type {{ color: #475569; }}
    .dict-constraint {{ color: #dc2626; font-weight: 700; }}
    .dict-desc {{ font-family: sans-serif; font-size: 10px; color: #334155; }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 3.2: Database Structure & Data Dictionary</h1>
        <p>Physical Table Specifications, Data Types, Primary/Foreign Constraints, and Storage Engine Configurations</p>
    </div>
    <div class="diagram-body">
        <div class="schema-grid">
            <!-- TABLE 1 -->
            <div class="table-box">
                <div class="table-box-header">
                    <span class="table-box-name">public.users</span>
                    <span class="table-box-engine">PostgreSQL Relational Table</span>
                </div>
                <table class="dict-table">
                    <tr><th>Column</th><th>Data Type</th><th>Constraint</th><th>Description</th></tr>
                    <tr><td class="dict-col">user_id</td><td class="dict-type">UUID</td><td class="dict-constraint">PK, NOT NULL</td><td class="dict-desc">System unique user identifier</td></tr>
                    <tr><td class="dict-col">email</td><td class="dict-type">VARCHAR(255)</td><td class="dict-constraint">UNIQUE, NOT NULL</td><td class="dict-desc">Institutional college email</td></tr>
                    <tr><td class="dict-col">full_name</td><td class="dict-type">VARCHAR(120)</td><td class="dict-constraint">NOT NULL</td><td class="dict-desc">Student / Faculty legal name</td></tr>
                    <tr><td class="dict-col">roll_number</td><td class="dict-type">VARCHAR(20)</td><td class="dict-constraint">UNIQUE, INDEX</td><td class="dict-desc">Academic registration number</td></tr>
                    <tr><td class="dict-col">role</td><td class="dict-type">user_role_enum</td><td class="dict-constraint">NOT NULL</td><td class="dict-desc">student, faculty, coordinator, admin</td></tr>
                </table>
            </div>

            <!-- TABLE 2 -->
            <div class="table-box">
                <div class="table-box-header">
                    <span class="table-box-name">public.organizations</span>
                    <span class="table-box-engine">PostgreSQL Relational Table</span>
                </div>
                <table class="dict-table">
                    <tr><th>Column</th><th>Data Type</th><th>Constraint</th><th>Description</th></tr>
                    <tr><td class="dict-col">org_id</td><td class="dict-type">UUID</td><td class="dict-constraint">PK, NOT NULL</td><td class="dict-desc">Club or cell primary identifier</td></tr>
                    <tr><td class="dict-col">name</td><td class="dict-type">VARCHAR(150)</td><td class="dict-constraint">UNIQUE, NOT NULL</td><td class="dict-desc">Official society title</td></tr>
                    <tr><td class="dict-col">category</td><td class="dict-type">org_type_enum</td><td class="dict-constraint">NOT NULL</td><td class="dict-desc">technical_club, cell, society, nss</td></tr>
                    <tr><td class="dict-col">faculty_advisor_id</td><td class="dict-type">UUID</td><td class="dict-constraint">FK &rarr; users(user_id)</td><td class="dict-desc">Designated faculty advisor</td></tr>
                    <tr><td class="dict-col">status</td><td class="dict-type">VARCHAR(20)</td><td class="dict-constraint">DEFAULT 'active'</td><td class="dict-desc">active, suspended, archived</td></tr>
                </table>
            </div>

            <!-- TABLE 3 -->
            <div class="table-box">
                <div class="table-box-header">
                    <span class="table-box-name">public.events</span>
                    <span class="table-box-engine">PostgreSQL Relational Table</span>
                </div>
                <table class="dict-table">
                    <tr><th>Column</th><th>Data Type</th><th>Constraint</th><th>Description</th></tr>
                    <tr><td class="dict-col">event_id</td><td class="dict-type">UUID</td><td class="dict-constraint">PK, NOT NULL</td><td class="dict-desc">Symposium / workshop unique key</td></tr>
                    <tr><td class="dict-col">org_id</td><td class="dict-type">UUID</td><td class="dict-constraint">FK &rarr; organizations</td><td class="dict-desc">Hosting organization</td></tr>
                    <tr><td class="dict-col">title</td><td class="dict-type">VARCHAR(200)</td><td class="dict-constraint">NOT NULL</td><td class="dict-desc">Event public headline</td></tr>
                    <tr><td class="dict-col">venue</td><td class="dict-type">VARCHAR(100)</td><td class="dict-constraint">NOT NULL, INDEX</td><td class="dict-desc">Seminar hall / lab location</td></tr>
                    <tr><td class="dict-col">event_date</td><td class="dict-type">TIMESTAMP</td><td class="dict-constraint">NOT NULL, INDEX</td><td class="dict-desc">Scheduled start timestamp</td></tr>
                    <tr><td class="dict-col">capacity</td><td class="dict-type">INTEGER</td><td class="dict-constraint">CHECK (>0)</td><td class="dict-desc">Maximum attendee seating limit</td></tr>
                </table>
            </div>

            <!-- TABLE 4 -->
            <div class="table-box">
                <div class="table-box-header">
                    <span class="table-box-name">public.attendance_records</span>
                    <span class="table-box-engine">PostgreSQL Relational Table</span>
                </div>
                <table class="dict-table">
                    <tr><th>Column</th><th>Data Type</th><th>Constraint</th><th>Description</th></tr>
                    <tr><td class="dict-col">attendance_id</td><td class="dict-type">UUID</td><td class="dict-constraint">PK, NOT NULL</td><td class="dict-desc">Attendance row primary key</td></tr>
                    <tr><td class="dict-col">event_id</td><td class="dict-type">UUID</td><td class="dict-constraint">FK &rarr; events</td><td class="dict-desc">Associated event key</td></tr>
                    <tr><td class="dict-col">user_id</td><td class="dict-type">UUID</td><td class="dict-constraint">FK &rarr; users</td><td class="dict-desc">Student attendee key</td></tr>
                    <tr><td class="dict-col">marked_by</td><td class="dict-type">UUID</td><td class="dict-constraint">FK &rarr; users</td><td class="dict-desc">Coordinator who logged presence</td></tr>
                    <tr><td class="dict-col">marked_at</td><td class="dict-type">TIMESTAMP</td><td class="dict-constraint">DEFAULT now()</td><td class="dict-desc">Verified timestamp</td></tr>
                    <tr><td class="dict-col">od_status</td><td class="dict-type">VARCHAR(20)</td><td class="dict-constraint">DEFAULT 'pending'</td><td class="dict-desc">pending, endorsed, erp_synced</td></tr>
                </table>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 7. Admin Dashboard Interface Mockup
# ==============================================================================
html_ui_admin = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .ui-mock {{
        border: 2px solid #0f172a;
        border-radius: 8px;
        background: #f8fafc;
        overflow: hidden;
    }}
    .ui-topbar {{
        background: #0f172a;
        color: #ffffff;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .ui-brand {{
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .ui-badge {{
        background: #334155;
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 4px;
    }}
    .ui-body-grid {{
        display: grid;
        grid-template-columns: 200px 1fr;
        min-height: 540px;
    }}
    .ui-sidebar {{
        background: #ffffff;
        border-right: 1.5px solid #cbd5e1;
        padding: 16px 12px;
    }}
    .ui-nav-item {{
        padding: 10px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 4px;
    }}
    .ui-nav-item.active {{
        background: #0f172a;
        color: #ffffff;
    }}
    .ui-content {{
        padding: 24px;
        background: #f8fafc;
    }}
    .stat-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }}
    .stat-card {{
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        border-radius: 6px;
        padding: 16px;
    }}
    .stat-title {{
        font-size: 11px;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .stat-val {{
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }}
    .table-card {{
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        border-radius: 6px;
        padding: 16px;
    }}
    .table-title {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }}
    .mock-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }}
    .mock-table th {{
        background: #f1f5f9;
        padding: 8px;
        text-align: left;
        border-bottom: 1.5px solid #cbd5e1;
    }}
    .mock-table td {{
        padding: 8px;
        border-bottom: 1px solid #e2e8f0;
    }}
    .tag-active {{
        background: #dcfce7;
        color: #166534;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 10px;
    }}
    .tag-pending {{
        background: #fef9c3;
        color: #854d0e;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 10px;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 4.1: Admin Dashboard Interface</h1>
        <p>Institutional Executive Governance Console with Centralized Metrics, Role Assignments, and Audit Monitoring</p>
    </div>
    <div class="diagram-body">
        <div class="ui-mock">
            <div class="ui-topbar">
                <div class="ui-brand">ClubHub &bull; Centralised Administration Portal</div>
                <div class="ui-badge">Logged in: Principal / Dean Office &bull; Administrator Mode</div>
            </div>
            <div class="ui-body-grid">
                <div class="ui-sidebar">
                    <div class="ui-nav-item active">📊 Executive Overview</div>
                    <div class="ui-nav-item">🏛️ Manage Clubs & Cells</div>
                    <div class="ui-nav-item">👩‍🏫 Faculty Coordinators</div>
                    <div class="ui-nav-item">📅 Campus Calendar</div>
                    <div class="ui-nav-item">📝 On-Duty Approval Log</div>
                    <div class="ui-nav-item">📈 NAAC Criterion 5 Export</div>
                    <div class="ui-nav-item">⚙️ System Configuration</div>
                </div>
                <div class="ui-content">
                    <div class="stat-row">
                        <div class="stat-card">
                            <div class="stat-title">Active Clubs & Cells</div>
                            <div class="stat-val">28</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-title">Registered Students</div>
                            <div class="stat-val">3,450</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-title">Events Conducted</div>
                            <div class="stat-val">64</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-title">OD Regularizations</div>
                            <div class="stat-val">1,280</div>
                        </div>
                    </div>

                    <div class="table-card">
                        <div class="table-title">Recent Event Proposals & Venue Clash Clearance Queue</div>
                        <table class="mock-table">
                            <tr><th>Event Title</th><th>Hosting Club</th><th>Proposed Venue</th><th>Date & Time</th><th>Clash Status</th><th>Approval Action</th></tr>
                            <tr><td>HackSphere 2026</td><td>Coding Club</td><td>CC-3 Seminar Hall</td><td>2026-11-20 09:00 AM</td><td><span class="tag-active">CLEARED (0 Clashes)</span></td><td><span class="tag-active">SANCTIONED</span></td></tr>
                            <tr><td>DesignSprint Workshop</td><td>Design Tribe</td><td>Mech Audio Visual</td><td>2026-11-22 01:30 PM</td><td><span class="tag-active">CLEARED (0 Clashes)</span></td><td><span class="tag-pending">PENDING ADVISOR</span></td></tr>
                            <tr><td>Startup Pitch Challenge</td><td>EDC & IIC Cell</td><td>Convention Center</td><td>2026-11-25 10:00 AM</td><td><span class="tag-active">CLEARED (0 Clashes)</span></td><td><span class="tag-active">SANCTIONED</span></td></tr>
                            <tr><td>RoboWars Arena Setup</td><td>Robotics Club</td><td>Indoor Sports Hall</td><td>2026-11-28 09:00 AM</td><td><span class="tag-pending">CONFLICT DETECTED</span></td><td><span class="tag-pending">UNDER REVIEW</span></td></tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 8. Student and Faculty Interface Mockup
# ==============================================================================
html_ui_student = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_STYLE}
<style>
    .split-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }}
    .pane-card {{
        border: 2px solid #0f172a;
        border-radius: 8px;
        background: #ffffff;
        overflow: hidden;
    }}
    .pane-header {{
        background: #0f172a;
        color: #ffffff;
        padding: 10px 16px;
        font-size: 13px;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
    }}
    .pane-body {{
        padding: 18px;
        background: #f8fafc;
        min-height: 480px;
    }}
    .club-card {{
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 14px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .club-title {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
    }}
    .club-desc {{
        font-size: 11px;
        color: #475569;
        margin-top: 2px;
    }}
    .btn-apply {{
        background: #0f172a;
        color: #ffffff;
        border: none;
        padding: 6px 14px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
    }}
    .roll-item {{
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .roll-name {{
        font-size: 12px;
        font-weight: 700;
        color: #0f172a;
    }}
    .roll-reg {{
        font-size: 10px;
        color: #64748b;
        font-family: monospace;
    }}
    .btn-present {{
        background: #166534;
        color: #ffffff;
        border: none;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
    }}
</style>
</head>
<body>
<div class="diagram-container">
    <div class="header">
        <h1>Figure 4.2: Student and Faculty Interface</h1>
        <p>Operational Panels: (Left) Student Discovery & RSVP Portal &bull; (Right) Faculty Mobile Attendance Roll-Call</p>
    </div>
    <div class="diagram-body">
        <div class="split-grid">
            <!-- STUDENT PANEL -->
            <div class="pane-card">
                <div class="pane-header">
                    <span>👨‍🎓 Student Discovery & Membership Portal</span>
                    <span>Role: Student</span>
                </div>
                <div class="pane-body">
                    <div style="font-size: 12px; font-weight: 700; margin-bottom: 12px; color: #0f172a;">Active Campus Clubs & Cells Recruitment</div>
                    <div class="club-card">
                        <div>
                            <div class="club-title">Coding Club (KEC)</div>
                            <div class="club-desc">Competitive programming, hackathons & open source projects</div>
                        </div>
                        <button class="btn-apply">APPLIED (Pending)</button>
                    </div>
                    <div class="club-card">
                        <div>
                            <div class="club-title">Design Tribe</div>
                            <div class="club-desc">UI/UX prototyping, graphic design & design thinking sprints</div>
                        </div>
                        <button class="btn-apply" style="background: #2563eb;">JOIN NOW</button>
                    </div>
                    <div class="club-card">
                        <div>
                            <div class="club-title">Institution's Innovation Council (IIC)</div>
                            <div class="club-desc">Patenting, startup incubation & national innovation contests</div>
                        </div>
                        <button class="btn-apply" style="background: #2563eb;">JOIN NOW</button>
                    </div>

                    <div style="font-size: 12px; font-weight: 700; margin-top: 20px; margin-bottom: 10px; color: #0f172a;">My Registered Event Passes</div>
                    <div style="background: #eff6ff; border: 1.5px dashed #3b82f6; border-radius: 6px; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 12px; font-weight: 700; color: #1e3a8a;">Web3 & Cloud Computing Summit</div>
                            <div style="font-size: 10px; color: #3b82f6;">Date: Nov 18, 2026 &bull; CC-3 Hall &bull; Seat: A-42</div>
                        </div>
                        <div style="font-family: monospace; font-size: 11px; background: #fff; padding: 4px 8px; border-radius: 4px; font-weight: 700; border: 1px solid #93c5fd;">QR-PASS #8942</div>
                    </div>
                </div>
            </div>

            <!-- FACULTY ROLL-CALL PANEL -->
            <div class="pane-card">
                <div class="pane-header">
                    <span>👩‍🏫 Faculty Coordinator Live Roll-Call Console</span>
                    <span>Event: Web3 Summit</span>
                </div>
                <div class="pane-body">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                        <div>
                            <div style="font-size: 12px; font-weight: 700; color: #0f172a;">Live Attendee Check-In</div>
                            <div style="font-size: 10px; color: #64748b;">Marked: 48 / 50 Present &bull; Venue: CC-3</div>
                        </div>
                        <button style="background: #0f172a; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; font-size: 10px; font-weight: 700;">GENERATE OD DOSSIER</button>
                    </div>

                    <div class="roll-item">
                        <div>
                            <div class="roll-name">SAHANA S</div>
                            <div class="roll-reg">25ITR121 &bull; Department of IT</div>
                        </div>
                        <button class="btn-present">✓ PRESENT</button>
                    </div>
                    <div class="roll-item">
                        <div>
                            <div class="roll-name">SARAN KARTHIK S</div>
                            <div class="roll-reg">25ITR128 &bull; Department of IT</div>
                        </div>
                        <button class="btn-present">✓ PRESENT</button>
                    </div>
                    <div class="roll-item">
                        <div>
                            <div class="roll-name">SHARAN V</div>
                            <div class="roll-reg">25ITR134 &bull; Department of IT</div>
                        </div>
                        <button class="btn-present">✓ PRESENT</button>
                    </div>
                    <div class="roll-item">
                        <div>
                            <div class="roll-name">VIGNESH M</div>
                            <div class="roll-reg">25ITR171 &bull; Department of IT</div>
                        </div>
                        <button class="btn-present">✓ PRESENT</button>
                    </div>
                    <div class="roll-item">
                        <div>
                            <div class="roll-name">MURASOLI B</div>
                            <div class="roll-reg">25ITL188 &bull; Department of IT</div>
                        </div>
                        <button class="btn-present">✓ PRESENT</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# Render all diagrams
diagrams_list = [
    (html_arch, "Figure_1_1_System_Architecture"),
    (html_workflow, "Figure_1_2_Overall_Workflow"),
    (html_usecase, "Figure_2_1_Use_Case_Diagram"),
    (html_dfd, "Figure_2_2_Data_Flow_Diagram"),
    (html_erd, "Figure_3_1_Entity_Relationship_Diagram"),
    (html_db_struct, "Figure_3_2_Database_Structure"),
    (html_ui_admin, "Figure_4_1_Admin_Dashboard_Interface"),
    (html_ui_student, "Figure_4_2_Student_Faculty_Interface")
]

print("Starting generation of all 8 documentation diagram images...")
success_count = 0
for html_data, filename in diagrams_list:
    if render_html_to_png(html_data, filename):
        success_count += 1

print(f"\nCompleted: {success_count}/{len(diagrams_list)} diagrams generated successfully.")
