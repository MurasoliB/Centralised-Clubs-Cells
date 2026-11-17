import os
import subprocess
import shutil

DIAGRAMS_DIR = os.path.abspath("diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
TEMP_DIR = os.environ.get("TEMP", "C:\\temp")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content, output_png_name, width=1600, height=1150):
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

# Base CSS with rich presentation styling matching the reference report
BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f8fafc;
        color: #0f172a;
        padding: 30px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    .canvas-container {
        width: 1540px;
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        position: relative;
    }
    .top-banner {
        border-radius: 12px;
        padding: 16px 24px;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .top-banner h1 {
        font-size: 23px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .top-banner p {
        font-size: 13px;
        font-weight: 500;
        opacity: 0.95;
    }
    .tag-chip {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(4px);
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .card {
        border-radius: 10px;
        padding: 16px;
        border: 1.5px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        position: relative;
    }
    .card-title {
        font-size: 14px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }
    .card-item {
        background: #ffffff;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(0,0,0,0.08);
        font-size: 12px;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .card-item span {
        display: block;
        font-size: 10.5px;
        color: #64748b;
        font-weight: 400;
        margin-top: 2px;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
    }
</style>
"""

# ==============================================================================
# 1. System Architecture Diagram (Vibrant 4-Tier Presentation Canvas)
# ==============================================================================
html_arch = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_CSS}
<style>
    .banner-arch {{
        background: linear-gradient(135deg, #059669 0%, #0d9488 50%, #0284c7 100%);
    }}
    .tiers-wrap {{
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}
    .tier-row {{
        border-radius: 12px;
        padding: 16px 20px;
        border: 1.5px solid;
        position: relative;
    }}
    .tier-header-badge {{
        position: absolute;
        top: -12px;
        left: 24px;
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        color: #ffffff;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.12);
    }}
    .tier-grid-4 {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-top: 6px;
    }}
    .tier-grid-3 {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-top: 6px;
    }}
    .tier-blue {{ background: #f0f7ff; border-color: #93c5fd; }}
    .tier-blue .tier-header-badge {{ background: #2563eb; }}
    .tier-green {{ background: #f0fdf4; border-color: #86efac; }}
    .tier-green .tier-header-badge {{ background: #059669; }}
    .tier-amber {{ background: #fffbeb; border-color: #fde68a; }}
    .tier-amber .tier-header-badge {{ background: #d97706; }}
    .tier-purple {{ background: #faf5ff; border-color: #d8b4fe; }}
    .tier-purple .tier-header-badge {{ background: #7c3aed; }}
    .subcard {{
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .subcard-head {{
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .subcard-item {{
        background: #f8fafc;
        border-radius: 4px;
        padding: 6px 10px;
        margin-bottom: 6px;
        font-size: 11px;
        font-weight: 600;
        color: #1e293b;
        border-left: 3px solid;
    }}
    .subcard-item span {{
        display: block;
        font-size: 10px;
        color: #64748b;
        font-weight: 400;
    }}
    .border-blue {{ border-left-color: #2563eb; }}
    .border-green {{ border-left-color: #059669; }}
    .border-amber {{ border-left-color: #d97706; }}
    .border-purple {{ border-left-color: #7c3aed; }}
    .arrow-banner {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        font-size: 11px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .arrow-line {{
        flex: 1;
        height: 2px;
        background: #cbd5e1;
    }}
</style>
</head>
<body>
<div class="canvas-container">
    <div class="top-banner banner-arch">
        <div>
            <h1>Figure 1.1: System Architecture Diagram</h1>
            <p>Four-Tier Enterprise Management Ecosystem with Role-Based Access Control & Autonomous Campus ERP Sync</p>
        </div>
        <div class="tag-chip">ClubHub System Architecture</div>
    </div>

    <div class="tiers-wrap">
        <!-- TIER 1 -->
        <div class="tier-row tier-blue">
            <div class="tier-header-badge">Tier 1: Client & Presentation Layer (Multi-Stakeholder Experience)</div>
            <div class="tier-grid-4">
                <div class="subcard">
                    <div class="subcard-head">👨‍🎓 Student Portal (PWA)</div>
                    <div class="subcard-item border-blue">Clubs & Cells Discovery<span>Single-source campus directory</span></div>
                    <div class="subcard-item border-blue">Online Recruitment Pass<span>Portfolio & application vetting</span></div>
                    <div class="subcard-item border-blue">Event RSVP & QR Passes<span>Instant ticket seat allocation</span></div>
                    <div class="subcard-item border-blue">Live OD Attendance Log<span>Real-time academic duty tracker</span></div>
                </div>
                <div class="subcard">
                    <div class="subcard-head">👩‍🏫 Faculty Coordinator</div>
                    <div class="subcard-item border-blue">Event Proposal Console<span>Venue booking & clash check</span></div>
                    <div class="subcard-item border-blue">Mobile Roll-Call Interface<span>1-tap live attendance check-in</span></div>
                    <div class="subcard-item border-blue">Instant OD Documentation<span>Automated roster generation</span></div>
                    <div class="subcard-item border-blue">Candidate Screening Hub<span>Induction decision workflow</span></div>
                </div>
                <div class="subcard">
                    <div class="subcard-head">🏛️ Institutional Admin</div>
                    <div class="subcard-item border-blue">Club Charter Governance<span>Mandate & budget approvals</span></div>
                    <div class="subcard-item border-blue">RBAC Role Provisioning<span>Faculty & coordinator rights</span></div>
                    <div class="subcard-item border-blue">Venue Conflict Arbiter<span>Central scheduling calendar</span></div>
                    <div class="subcard-item border-blue">NAAC Criterion 5 Export<span>Accreditation-ready dossiers</span></div>
                </div>
                <div class="subcard">
                    <div class="subcard-head">🏢 Dean & Department HOD</div>
                    <div class="subcard-item border-blue">Digital OD Sign-Off<span>Departmental clearance bus</span></div>
                    <div class="subcard-item border-blue">Transcript Verification<span>Co-curricular credential audits</span></div>
                    <div class="subcard-item border-blue">Annual Milestone Reports<span>Participation analytics</span></div>
                    <div class="subcard-item border-blue">Policy Compliance<span>Attendance minimum monitoring</span></div>
                </div>
            </div>
        </div>

        <div class="arrow-banner">
            <div class="arrow-line"></div>
            <span>▼ HTTPS / TLS 1.3 Encrypted REST & Realtime WebSocket Channels ▼</span>
            <div class="arrow-line"></div>
        </div>

        <!-- TIER 2 -->
        <div class="tier-row tier-green">
            <div class="tier-header-badge">Tier 2: Frontend Engineering Architecture (Single Page Application)</div>
            <div class="tier-grid-4">
                <div class="subcard">
                    <div class="subcard-head">⚛️ React 18 Engine</div>
                    <div class="subcard-item border-green">Modular Architecture<span>Componentized reusable blocks</span></div>
                    <div class="subcard-item border-green">Concurrent Mode<span>Smooth interactive rendering</span></div>
                </div>
                <div class="subcard">
                    <div class="subcard-head">📘 TypeScript 5.0</div>
                    <div class="subcard-item border-green">Strict Type Safety<span>End-to-end interface contracts</span></div>
                    <div class="subcard-item border-green">Zero Runtime Errors<span>Static validation at build-time</span></div>
                </div>
                <div class="subcard">
                    <div class="subcard-head">🎨 Tailwind CSS Design</div>
                    <div class="subcard-item border-green">Wikipedia Aesthetic<span>Crisp academic typography</span></div>
                    <div class="subcard-item border-green">Fully Responsive<span>Mobile, tablet & desktop ready</span></div>
                </div>
                <div class="subcard">
                    <div class="subcard-head">⚡ Vite & Navigation</div>
                    <div class="subcard-item border-green">Lightning Bundler<span>Sub-second hot-reload</span></div>
                    <div class="subcard-item border-green">React Router v6<span>Protected role guard boundaries</span></div>
                </div>
            </div>
        </div>

        <div class="arrow-banner">
            <div class="arrow-line"></div>
            <span>▼ Supabase Client SDK / Bearer JWT Token Interceptors ▼</span>
            <div class="arrow-line"></div>
        </div>

        <!-- TIER 3 & 4 SIDE BY SIDE -->
        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px;">
            <div class="tier-row tier-amber" style="margin-bottom: 0;">
                <div class="tier-header-badge">Tier 3: Backend Services & Business Logic</div>
                <div class="tier-grid-3">
                    <div class="subcard">
                        <div class="subcard-head">🔒 Auth & RBAC</div>
                        <div class="subcard-item border-amber">Supabase Auth<span>JWT claims & sessions</span></div>
                        <div class="subcard-item border-amber">Role Interceptors<span>Guards per endpoint</span></div>
                    </div>
                    <div class="subcard">
                        <div class="subcard-head">⚙️ Business Logic</div>
                        <div class="subcard-item border-amber">Clash Detection<span>Venue conflict worker</span></div>
                        <div class="subcard-item border-amber">OD Compiler<span>Roll-call aggregation</span></div>
                    </div>
                    <div class="subcard">
                        <div class="subcard-head">🛡️ Row Security</div>
                        <div class="subcard-item border-amber">PostgreSQL RLS<span>Club-tenant data isolation</span></div>
                        <div class="subcard-item border-amber">Audit Triggers<span>Tamper-proof event logs</span></div>
                    </div>
                </div>
            </div>

            <div class="tier-row tier-purple" style="margin-bottom: 0;">
                <div class="tier-header-badge">Tier 4: Enterprise Database & External Integrations</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 6px;">
                    <div class="subcard">
                        <div class="subcard-head">🗄️ PostgreSQL DB</div>
                        <div class="subcard-item border-purple">ACID Relational Core<span>Users, Orgs, Events, OD</span></div>
                        <div class="subcard-item border-purple">Foreign Key Integrity<span>Cascading referential rules</span></div>
                    </div>
                    <div class="subcard">
                        <div class="subcard-head">🏫 Campus ERP Sync</div>
                        <div class="subcard-item border-purple">ERP REST API Gateway<span>Direct attendance credit</span></div>
                        <div class="subcard-item border-purple">SMTP Mail Dispatch<span>QR tickets & notifications</span></div>
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
# 2. Overall System Workflow (Flowchart style of Fig 4.1 in reference)
# ==============================================================================
html_workflow = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_CSS}
<style>
    .banner-flow {{
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #06b6d4 100%);
    }}
    .flow-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 12px;
        margin-top: 10px;
        align-items: stretch;
    }}
    .flow-col {{
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 12px;
        padding: 16px 12px;
        position: relative;
        text-align: center;
    }}
    .flow-num {{
        width: 38px;
        height: 38px;
        background: #2563eb;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 10px;
        box-shadow: 0 3px 6px rgba(37, 99, 235, 0.3);
    }}
    .flow-role {{
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        color: #2563eb;
        background: #dbeafe;
        padding: 2px 8px;
        border-radius: 12px;
        margin-bottom: 8px;
    }}
    .flow-title {{
        font-size: 13px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        line-height: 1.3;
    }}
    .flow-box {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 8px;
        font-size: 11px;
        color: #334155;
        line-height: 1.4;
        margin-bottom: 12px;
        flex: 1;
        text-align: left;
    }}
    .flow-box b {{
        color: #0f172a;
        display: block;
        margin-bottom: 3px;
    }}
    .flow-output {{
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 6px;
        padding: 6px 8px;
        font-size: 10px;
        font-weight: 700;
        color: #065f46;
        width: 100%;
        text-align: center;
    }}
    .connector-arrow {{
        position: absolute;
        right: -16px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        background: #2563eb;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 900;
        z-index: 10;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    .summary-bar {{
        margin-top: 20px;
        background: #eff6ff;
        border: 1.5px solid #bfdbfe;
        border-radius: 10px;
        padding: 14px 20px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }}
    .summary-item {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 12px;
        font-weight: 700;
        color: #1e40af;
    }}
    .summary-item span {{
        font-size: 18px;
    }}
</style>
</head>
<body>
<div class="canvas-container">
    <div class="top-banner banner-flow">
        <div>
            <h1>Figure 1.2: Overall System Workflow</h1>
            <p>End-to-End Operational Lifecycle from Club Discovery to Automated On-Duty (OD) Academic Clearance</p>
        </div>
        <div class="tag-chip">End-to-End Workflow Process</div>
    </div>

    <div class="flow-grid">
        <!-- 1 -->
        <div class="flow-col">
            <div class="flow-num">1</div>
            <div class="flow-role">Admin Setup</div>
            <div class="flow-title">Charter & Advisor Assigning</div>
            <div class="flow-box">
                <b>Club Onboarding:</b>
                Admin creates club profiles, sets mandates, defines student membership quotas, and assigns faculty mentors.
            </div>
            <div class="flow-output">Active Club Charter</div>
            <div class="connector-arrow">➔</div>
        </div>

        <!-- 2 -->
        <div class="flow-col">
            <div class="flow-num">2</div>
            <div class="flow-role">Student</div>
            <div class="flow-title">Discovery & Application</div>
            <div class="flow-box">
                <b>Unified Portal:</b>
                Student browses active clubs, inspects activities, fills induction questionnaire, and submits application.
            </div>
            <div class="flow-output">Candidate Application</div>
            <div class="connector-arrow">➔</div>
        </div>

        <!-- 3 -->
        <div class="flow-col">
            <div class="flow-num">3</div>
            <div class="flow-role">Faculty</div>
            <div class="flow-title">Screening & Induction</div>
            <div class="flow-box">
                <b>Portfolio Review:</b>
                Faculty evaluates applicants through multi-stage vetting (Review ➔ Shortlist ➔ Induct) with live alerts.
            </div>
            <div class="flow-output">Verified Membership</div>
            <div class="connector-arrow">➔</div>
        </div>

        <!-- 4 -->
        <div class="flow-col">
            <div class="flow-num">4</div>
            <div class="flow-role">Coordinator</div>
            <div class="flow-title">Event Proposal & Clash Check</div>
            <div class="flow-box">
                <b>Intelligent Scheduling:</b>
                Coordinator drafts workshop proposal; system validates hall availability & prevents timetable clashes.
            </div>
            <div class="flow-output">Sanctioned Event & RSVP</div>
            <div class="connector-arrow">➔</div>
        </div>

        <!-- 5 -->
        <div class="flow-col">
            <div class="flow-num">5</div>
            <div class="flow-role">Student</div>
            <div class="flow-title">1-Click RSVP & Entry Pass</div>
            <div class="flow-box">
                <b>Seat Reservation:</b>
                Students reserve spots within attendee caps; instant personalized QR ticket pass is generated for entry.
            </div>
            <div class="flow-output">Digital QR Pass #</div>
            <div class="connector-arrow">➔</div>
        </div>

        <!-- 6 -->
        <div class="flow-col">
            <div class="flow-num">6</div>
            <div class="flow-role">Event Day</div>
            <div class="flow-title">Mobile Roll-Call Check-in</div>
            <div class="flow-box">
                <b>Live Roll-Call:</b>
                Coordinators mark presence via 1-tap mobile checklist; timestamps prevent proxy sign-ins during sessions.
            </div>
            <div class="flow-output">Verified Attendance Log</div>
            <div class="connector-arrow">➔</div>
        </div>

        <!-- 7 -->
        <div class="flow-col">
            <div class="flow-num">7</div>
            <div class="flow-role">Dean & ERP</div>
            <div class="flow-title">Automated OD & ERP Sync</div>
            <div class="flow-box">
                <b>Instant Regularization:</b>
                System drafts official OD letters sorted by department; digital Dean sign-off directly updates ERP registers.
            </div>
            <div class="flow-output">Zero Paperwork OD Credit</div>
        </div>
    </div>

    <div class="summary-bar">
        <div class="summary-item"><span>⏱️</span> Bureaucratic Delay Reduced from 5 Days to Instant Real-Time</div>
        <div class="summary-item"><span>📋</span> 100% Elimination of Physical Paperwork & Lost Registers</div>
        <div class="summary-item"><span>📊</span> Automated Compliance for NAAC Criterion 5 Accreditation</div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 3. Use Case Diagram (UML Behavioral Model matching Stakeholder Style)
# ==============================================================================
html_usecase = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_CSS}
<style>
    .banner-uc {{
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #c026d3 100%);
    }}
    .uc-canvas {{
        display: grid;
        grid-template-columns: 240px 1fr 240px;
        gap: 20px;
        align-items: center;
    }}
    .actor-box {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    .actor-avatar {{
        width: 58px;
        height: 58px;
        border-radius: 50%;
        margin: 0 auto 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: #ffffff;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }}
    .avatar-student {{ background: linear-gradient(135deg, #0284c7, #2563eb); }}
    .avatar-faculty {{ background: linear-gradient(135deg, #059669, #10b981); }}
    .avatar-admin {{ background: linear-gradient(135deg, #7c3aed, #9333ea); }}
    .avatar-erp {{ background: linear-gradient(135deg, #ea580c, #f59e0b); }}
    .actor-title {{
        font-size: 14px;
        font-weight: 800;
        color: #0f172a;
    }}
    .actor-role {{
        font-size: 11px;
        color: #64748b;
        font-weight: 600;
        margin-top: 2px;
    }}
    .boundary-card {{
        background: #f8fafc;
        border: 2.5px solid #4f46e5;
        border-radius: 16px;
        padding: 24px;
        position: relative;
    }}
    .boundary-tag {{
        position: absolute;
        top: -14px;
        left: 28px;
        background: #4f46e5;
        color: #ffffff;
        font-size: 12px;
        font-weight: 800;
        padding: 3px 18px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }}
    .uc-modules {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-top: 10px;
    }}
    .uc-module-box {{
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        border-radius: 10px;
        padding: 14px;
    }}
    .uc-module-head {{
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        color: #4f46e5;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 6px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }}
    .uc-pill {{
        background: #f1f5f9;
        border: 1.5px solid #94a3b8;
        border-radius: 20px;
        padding: 7px 12px;
        margin-bottom: 8px;
        font-size: 11.5px;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .uc-pill span {{
        font-size: 9.5px;
        color: #64748b;
        font-weight: 500;
    }}
    .pill-student {{ border-color: #38bdf8; background: #f0f9ff; }}
    .pill-faculty {{ border-color: #4ade80; background: #f0fdf4; }}
    .pill-admin {{ border-color: #c084fc; background: #faf5ff; }}
    .pill-include {{ border-color: #cbd5e1; border-style: dashed; background: #ffffff; }}
</style>
</head>
<body>
<div class="canvas-container">
    <div class="top-banner banner-uc">
        <div>
            <h1>Figure 2.1: Use Case Diagram</h1>
            <p>Unified Modeling Language (UML) Behavioral Specification for Multi-Tier Stakeholders & Campus ERP</p>
        </div>
        <div class="tag-chip">Stakeholder Use Case Specifications</div>
    </div>

    <div class="uc-canvas">
        <!-- ACTORS LEFT -->
        <div>
            <div class="actor-box">
                <div class="actor-avatar avatar-student">👨‍🎓</div>
                <div class="actor-title">Student User</div>
                <div class="actor-role">Primary Campus Participant</div>
            </div>
            <div class="actor-box" style="margin-bottom: 0;">
                <div class="actor-avatar avatar-faculty">👩‍🏫</div>
                <div class="actor-title">Faculty Coordinator</div>
                <div class="actor-role">Operational & Event Mentor</div>
            </div>
        </div>

        <!-- BOUNDARY -->
        <div class="boundary-card">
            <div class="boundary-tag">System Boundary: Centralised Clubs & Cells Management System</div>
            <div class="uc-modules">
                <!-- MOD 1 -->
                <div class="uc-module-box">
                    <div class="uc-module-head">Membership & Induction <span>Student & Faculty</span></div>
                    <div class="uc-pill pill-include">User Authentication & SSO <span>&laquo;include&raquo;</span></div>
                    <div class="uc-pill pill-student">Browse Central Clubs Directory <span>All active units</span></div>
                    <div class="uc-pill pill-student">Submit Membership Application <span>Induction form</span></div>
                    <div class="uc-pill pill-faculty">Review & Induct Candidates <span>Shortlist & confirm</span></div>
                </div>

                <!-- MOD 2 -->
                <div class="uc-module-box">
                    <div class="uc-module-head">Event Orchestration <span>Faculty & Student</span></div>
                    <div class="uc-pill pill-faculty">Propose Event & Check Clashes <span>Venue conflict</span></div>
                    <div class="uc-pill pill-student">Register for Campus Events <span>Capacity capped</span></div>
                    <div class="uc-pill pill-student">Access Digital Entry Pass <span>QR code voucher</span></div>
                    <div class="uc-pill pill-include">Notify Student via Email/SMS <span>&laquo;extend&raquo;</span></div>
                </div>

                <!-- MOD 3 -->
                <div class="uc-module-box">
                    <div class="uc-module-head">Attendance & On-Duty <span>Faculty & Dean</span></div>
                    <div class="uc-pill pill-faculty">Execute Live Mobile Roll-Call <span>Real-time presence</span></div>
                    <div class="uc-pill pill-faculty">Compile Standardized OD Dossier <span>Auto-generated</span></div>
                    <div class="uc-pill pill-student">Track Academic OD Status <span>Duty clearance log</span></div>
                    <div class="uc-pill pill-include">Sync with College ERP <span>&laquo;extend&raquo; automated</span></div>
                </div>

                <!-- MOD 4 -->
                <div class="uc-module-box">
                    <div class="uc-module-head">Governance & Audits <span>Admin & Accreditation</span></div>
                    <div class="uc-pill pill-admin">Manage User Accounts & RBAC <span>Rights provisioning</span></div>
                    <div class="uc-pill pill-admin">Charter Club Mandates & Quotas <span>Society governance</span></div>
                    <div class="uc-pill pill-admin">Export NAAC Criterion 5 Dossiers <span>Accreditation data</span></div>
                    <div class="uc-pill pill-admin">Maintain Tamper-Proof Audit Logs <span>Activity security</span></div>
                </div>
            </div>
        </div>

        <!-- ACTORS RIGHT -->
        <div>
            <div class="actor-box">
                <div class="actor-avatar avatar-admin">🏛️</div>
                <div class="actor-title">College Admin</div>
                <div class="actor-role">Governance & Accreditation</div>
            </div>
            <div class="actor-box" style="margin-bottom: 0;">
                <div class="actor-avatar avatar-erp">🏫</div>
                <div class="actor-title">Autonomous ERP</div>
                <div class="actor-role">External Academic System</div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 4. Data Flow Diagram (Level 1)
# ==============================================================================
html_dfd = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_CSS}
<style>
    .banner-dfd {{
        background: linear-gradient(135deg, #0f766e 0%, #0d9488 50%, #14b8a6 100%);
    }}
    .dfd-canvas {{
        display: grid;
        grid-template-columns: 220px 1fr 220px;
        gap: 24px;
        align-items: center;
    }}
    .entity-node {{
        background: #0f172a;
        color: #ffffff;
        border-radius: 12px;
        padding: 20px 14px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        margin-bottom: 24px;
        border: 2px solid #334155;
    }}
    .entity-tag {{
        font-size: 10px;
        color: #2dd4bf;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .entity-name {{
        font-size: 15px;
        font-weight: 800;
    }}
    .process-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }}
    .process-card {{
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }}
    .process-head {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        padding-bottom: 6px;
        border-bottom: 1.5px solid #f1f5f9;
    }}
    .process-circle-num {{
        width: 32px;
        height: 32px;
        background: #0d9488;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 800;
    }}
    .process-card-title {{
        font-size: 13px;
        font-weight: 800;
        color: #0f172a;
    }}
    .flow-pill {{
        background: #f8fafc;
        border-left: 3px solid #0d9488;
        border-radius: 4px;
        padding: 6px 8px;
        font-size: 10.5px;
        color: #334155;
        margin-bottom: 6px;
    }}
    .store-bar-dfd {{
        background: #eff6ff;
        border-top: 2px solid #2563eb;
        border-bottom: 2px solid #2563eb;
        padding: 5px 10px;
        border-radius: 2px;
        font-size: 10.5px;
        font-weight: 700;
        color: #1e40af;
        display: flex;
        justify-content: space-between;
        margin-top: 6px;
    }}
</style>
</head>
<body>
<div class="canvas-container">
    <div class="top-banner banner-dfd">
        <div>
            <h1>Figure 2.2: Data Flow Diagram (Level 1)</h1>
            <p>Transformation of Information across Core Functional Processes, External Stakeholders, and Data Stores</p>
        </div>
        <div class="tag-chip">Information Flow Architecture</div>
    </div>

    <div class="dfd-canvas">
        <!-- LEFT ENTITIES -->
        <div>
            <div class="entity-node">
                <div class="entity-tag">[Entity 1]</div>
                <div class="entity-name">👨‍🎓 STUDENT</div>
            </div>
            <div class="entity-node" style="margin-bottom: 0;">
                <div class="entity-tag">[Entity 2]</div>
                <div class="entity-name">👩‍🏫 FACULTY COORDINATOR</div>
            </div>
        </div>

        <!-- PROCESSES & STORES -->
        <div class="process-grid">
            <!-- P1 -->
            <div class="process-card">
                <div class="process-head">
                    <div class="process-circle-num">1.0</div>
                    <div class="process-card-title">Authentication & RBAC</div>
                </div>
                <div class="flow-pill">In: Credentials, Roll No ➔ Out: JWT Token</div>
                <div class="store-bar-dfd"><span>D1</span> <span>User Accounts & Roles Store</span></div>
            </div>

            <!-- P2 -->
            <div class="process-card">
                <div class="process-head">
                    <div class="process-circle-num">2.0</div>
                    <div class="process-card-title">Club & Recruitment</div>
                </div>
                <div class="flow-pill">In: Candidate Profile ➔ Out: Induction Decision</div>
                <div class="store-bar-dfd"><span>D2</span> <span>Clubs & Memberships Registry</span></div>
            </div>

            <!-- P3 -->
            <div class="process-card">
                <div class="process-head">
                    <div class="process-circle-num">3.0</div>
                    <div class="process-card-title">Event Scheduling & Clash</div>
                </div>
                <div class="flow-pill">In: Date, Hall ➔ Out: Verified Sanction</div>
                <div class="store-bar-dfd"><span>D3</span> <span>Events & Schedule Store</span></div>
            </div>

            <!-- P4 -->
            <div class="process-card">
                <div class="process-head">
                    <div class="process-circle-num">4.0</div>
                    <div class="process-card-title">Registration & Passes</div>
                </div>
                <div class="flow-pill">In: RSVP Request ➔ Out: Digital QR Pass #</div>
                <div class="store-bar-dfd"><span>D4</span> <span>Registrations & Tickets Store</span></div>
            </div>

            <!-- P5 -->
            <div class="process-card">
                <div class="process-head">
                    <div class="process-circle-num">5.0</div>
                    <div class="process-card-title">Real-Time Roll-Call</div>
                </div>
                <div class="flow-pill">In: 1-Tap Attendance ➔ Out: Verified Presence</div>
                <div class="store-bar-dfd"><span>D5</span> <span>Attendance & Audit Ledgers</span></div>
            </div>

            <!-- P6 -->
            <div class="process-card">
                <div class="process-head">
                    <div class="process-circle-num">6.0</div>
                    <div class="process-card-title">On-Duty & ERP Sync</div>
                </div>
                <div class="flow-pill">In: Verified Roster ➔ Out: Automatic ERP Credit</div>
                <div class="store-bar-dfd"><span>D6</span> <span>On-Duty (OD) Archive & Logs</span></div>
            </div>
        </div>

        <!-- RIGHT ENTITIES -->
        <div>
            <div class="entity-node">
                <div class="entity-tag">[Entity 3]</div>
                <div class="entity-name">🏛️ COLLEGE ADMIN</div>
            </div>
            <div class="entity-node" style="margin-bottom: 0;">
                <div class="entity-tag">[Entity 4]</div>
                <div class="entity-name">🏫 AUTONOMOUS ERP</div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 5. Entity Relationship Diagram (ERD)
# ==============================================================================
html_erd = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_CSS}
<style>
    .banner-erd {{
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #ea580c 100%);
    }}
    .erd-grid-3 {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }}
    .table-card-erd {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
    }}
    .table-head-erd {{
        padding: 8px 12px;
        color: #ffffff;
        font-size: 13px;
        font-weight: 800;
        display: flex;
        justify-content: space-between;
        align-items: center;
        letter-spacing: 0.5px;
    }}
    .head-blue {{ background: #2563eb; }}
    .head-green {{ background: #059669; }}
    .head-amber {{ background: #d97706; }}
    .head-purple {{ background: #7c3aed; }}
    .head-teal {{ background: #0d9488; }}
    .head-rose {{ background: #e11d48; }}
    .table-head-erd span {{
        font-size: 9.5px;
        background: rgba(255,255,255,0.25);
        padding: 2px 6px;
        border-radius: 3px;
    }}
    .erd-fields {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }}
    .erd-fields td {{
        padding: 6px 10px;
        border-bottom: 1px solid #f1f5f9;
    }}
    .key-badge {{
        font-size: 9px;
        font-weight: 800;
        padding: 2px 5px;
        border-radius: 3px;
    }}
    .pk-badge {{ background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }}
    .fk-badge {{ background: #e0e7ff; color: #4338ca; border: 1px solid #a5b4fc; }}
    .f-name {{ font-weight: 700; color: #0f172a; }}
    .f-type {{ text-align: right; color: #64748b; font-family: monospace; font-size: 10px; }}
    .rel-summary-bar {{
        margin-top: 18px;
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 10px;
        padding: 12px 20px;
        display: flex;
        justify-content: space-around;
        font-size: 11.5px;
        font-weight: 700;
        color: #1e293b;
    }}
    .rel-chip {{
        background: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 6px;
        padding: 4px 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }}
</style>
</head>
<body>
<div class="canvas-container">
    <div class="top-banner banner-erd">
        <div>
            <h1>Figure 3.1: Entity Relationship Diagram (ERD)</h1>
            <p>PostgreSQL Relational Schema with Primary Keys, Foreign Keys, and Cardinality Constraints</p>
        </div>
        <div class="tag-chip">Relational Data Model</div>
    </div>

    <div class="erd-grid-3">
        <!-- 1. USERS -->
        <div class="table-card-erd">
            <div class="table-head-erd head-blue">USERS <span>Primary Actor</span></div>
            <table class="erd-fields">
                <tr><td><span class="key-badge pk-badge">PK</span></td><td class="f-name">user_id</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">email</td><td class="f-type">VARCHAR(255)</td></tr>
                <tr><td></td><td class="f-name">full_name</td><td class="f-type">VARCHAR(120)</td></tr>
                <tr><td></td><td class="f-name">roll_number</td><td class="f-type">VARCHAR(20)</td></tr>
                <tr><td></td><td class="f-name">role</td><td class="f-type">user_role_enum</td></tr>
                <tr><td></td><td class="f-name">department</td><td class="f-type">VARCHAR(50)</td></tr>
                <tr><td></td><td class="f-name">created_at</td><td class="f-type">TIMESTAMP</td></tr>
            </table>
        </div>

        <!-- 2. ORGANIZATIONS -->
        <div class="table-card-erd">
            <div class="table-head-erd head-green">ORGANIZATIONS <span>Clubs & Cells</span></div>
            <table class="erd-fields">
                <tr><td><span class="key-badge pk-badge">PK</span></td><td class="f-name">org_id</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">name</td><td class="f-type">VARCHAR(150)</td></tr>
                <tr><td></td><td class="f-name">category</td><td class="f-type">org_type_enum</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">faculty_advisor_id</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">description</td><td class="f-type">TEXT</td></tr>
                <tr><td></td><td class="f-name">status</td><td class="f-type">VARCHAR(20)</td></tr>
                <tr><td></td><td class="f-name">created_at</td><td class="f-type">TIMESTAMP</td></tr>
            </table>
        </div>

        <!-- 3. MEMBERSHIPS -->
        <div class="table-card-erd">
            <div class="table-head-erd head-amber">MEMBERSHIPS <span>Associative</span></div>
            <table class="erd-fields">
                <tr><td><span class="key-badge pk-badge">PK</span></td><td class="f-name">membership_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">user_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">org_id</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">role_in_club</td><td class="f-type">VARCHAR(50)</td></tr>
                <tr><td></td><td class="f-name">status</td><td class="f-type">member_status</td></tr>
                <tr><td></td><td class="f-name">applied_at</td><td class="f-type">TIMESTAMP</td></tr>
            </table>
        </div>

        <!-- 4. EVENTS -->
        <div class="table-card-erd">
            <div class="table-head-erd head-purple">EVENTS <span>Transactional</span></div>
            <table class="erd-fields">
                <tr><td><span class="key-badge pk-badge">PK</span></td><td class="f-name">event_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">org_id</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">title</td><td class="f-type">VARCHAR(200)</td></tr>
                <tr><td></td><td class="f-name">venue</td><td class="f-type">VARCHAR(100)</td></tr>
                <tr><td></td><td class="f-name">event_date</td><td class="f-type">TIMESTAMP</td></tr>
                <tr><td></td><td class="f-name">capacity</td><td class="f-type">INTEGER</td></tr>
                <tr><td></td><td class="f-name">status</td><td class="f-type">VARCHAR(20)</td></tr>
            </table>
        </div>

        <!-- 5. REGISTRATIONS -->
        <div class="table-card-erd">
            <div class="table-head-erd head-teal">REGISTRATIONS <span>RSVP Ledger</span></div>
            <table class="erd-fields">
                <tr><td><span class="key-badge pk-badge">PK</span></td><td class="f-name">registration_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">event_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">user_id</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">ticket_code</td><td class="f-type">VARCHAR(64)</td></tr>
                <tr><td></td><td class="f-name">status</td><td class="f-type">VARCHAR(20)</td></tr>
                <tr><td></td><td class="f-name">registered_at</td><td class="f-type">TIMESTAMP</td></tr>
            </table>
        </div>

        <!-- 6. ATTENDANCE_RECORDS -->
        <div class="table-card-erd">
            <div class="table-head-erd head-rose">ATTENDANCE <span>Audit Ledger</span></div>
            <table class="erd-fields">
                <tr><td><span class="key-badge pk-badge">PK</span></td><td class="f-name">attendance_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">event_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">user_id</td><td class="f-type">UUID</td></tr>
                <tr><td><span class="key-badge fk-badge">FK</span></td><td class="f-name">marked_by</td><td class="f-type">UUID</td></tr>
                <tr><td></td><td class="f-name">marked_at</td><td class="f-type">TIMESTAMP</td></tr>
                <tr><td></td><td class="f-name">od_status</td><td class="f-type">VARCHAR(20)</td></tr>
            </table>
        </div>
    </div>

    <div class="rel-summary-bar">
        <div class="rel-chip">USERS (1) ────&lt; (M) MEMBERSHIPS</div>
        <div class="rel-chip">ORGANIZATIONS (1) ────&lt; (M) MEMBERSHIPS</div>
        <div class="rel-chip">ORGANIZATIONS (1) ────&lt; (M) EVENTS</div>
        <div class="rel-chip">EVENTS (1) ────&lt; (M) REGISTRATIONS</div>
        <div class="rel-chip">EVENTS (1) ────&lt; (M) ATTENDANCE</div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 6. Database Structure & Data Dictionary
# ==============================================================================
html_db_struct = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{BASE_CSS}
<style>
    .banner-db {{
        background: linear-gradient(135deg, #047857 0%, #059669 50%, #10b981 100%);
    }}
    .db-grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }}
    .dict-box {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .dict-header {{
        background: #0f172a;
        color: #ffffff;
        padding: 9px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .dict-table-name {{
        font-family: monospace;
        font-size: 13.5px;
        font-weight: 700;
        color: #38bdf8;
    }}
    .dict-badge {{
        font-size: 10px;
        background: #334155;
        padding: 2px 8px;
        border-radius: 4px;
        color: #e2e8f0;
    }}
    .spec-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }}
    .spec-table th {{
        background: #f1f5f9;
        color: #334155;
        font-weight: 800;
        padding: 6px 10px;
        text-align: left;
        border-bottom: 1.5px solid #cbd5e1;
        font-size: 10.5px;
        text-transform: uppercase;
    }}
    .spec-table td {{
        padding: 6px 10px;
        border-bottom: 1px solid #f8fafc;
    }}
    .c-name {{ font-family: monospace; font-weight: 700; color: #0f172a; }}
    .c-type {{ font-family: monospace; color: #0284c7; font-weight: 600; font-size: 10.5px; }}
    .c-rule {{ color: #dc2626; font-weight: 700; font-size: 10px; }}
    .c-desc {{ color: #475569; font-size: 10.5px; }}
</style>
</head>
<body>
<div class="canvas-container">
    <div class="top-banner banner-db">
        <div>
            <h1>Figure 3.2: Database Structure & Data Dictionary</h1>
            <p>Physical Table Specifications, Data Types, Primary/Foreign Constraints, and Storage Engine Configurations</p>
        </div>
        <div class="tag-chip">Physical Storage Specifications</div>
    </div>

    <div class="db-grid-2">
        <!-- TABLE 1 -->
        <div class="dict-box">
            <div class="dict-header">
                <span class="dict-table-name">public.users</span>
                <span class="dict-badge">PostgreSQL Engine</span>
            </div>
            <table class="spec-table">
                <tr><th>Column</th><th>Type</th><th>Constraint</th><th>Description</th></tr>
                <tr><td class="c-name">user_id</td><td class="c-type">UUID</td><td class="c-rule">PK, NOT NULL</td><td class="c-desc">Unique identifier</td></tr>
                <tr><td class="c-name">email</td><td class="c-type">VARCHAR(255)</td><td class="c-rule">UNIQUE, NOT NULL</td><td class="c-desc">College email ID</td></tr>
                <tr><td class="c-name">full_name</td><td class="c-type">VARCHAR(120)</td><td class="c-rule">NOT NULL</td><td class="c-desc">Student / Faculty name</td></tr>
                <tr><td class="c-name">roll_number</td><td class="c-type">VARCHAR(20)</td><td class="c-rule">UNIQUE, INDEX</td><td class="c-desc">Academic reg number</td></tr>
                <tr><td class="c-name">role</td><td class="c-type">role_enum</td><td class="c-rule">NOT NULL</td><td class="c-desc">student, faculty, admin</td></tr>
            </table>
        </div>

        <!-- TABLE 2 -->
        <div class="dict-box">
            <div class="dict-header">
                <span class="dict-table-name">public.organizations</span>
                <span class="dict-badge">PostgreSQL Engine</span>
            </div>
            <table class="spec-table">
                <tr><th>Column</th><th>Type</th><th>Constraint</th><th>Description</th></tr>
                <tr><td class="c-name">org_id</td><td class="c-type">UUID</td><td class="c-rule">PK, NOT NULL</td><td class="c-desc">Club unique identifier</td></tr>
                <tr><td class="c-name">name</td><td class="c-type">VARCHAR(150)</td><td class="c-rule">UNIQUE, NOT NULL</td><td class="c-desc">Official club name</td></tr>
                <tr><td class="c-name">category</td><td class="c-type">org_enum</td><td class="c-rule">NOT NULL</td><td class="c-desc">technical, cell, society</td></tr>
                <tr><td class="c-name">faculty_advisor_id</td><td class="c-type">UUID</td><td class="c-rule">FK &rarr; users(user_id)</td><td class="c-desc">Designated faculty advisor</td></tr>
                <tr><td class="c-name">status</td><td class="c-type">VARCHAR(20)</td><td class="c-rule">DEFAULT 'active'</td><td class="c-desc">active, archived</td></tr>
            </table>
        </div>

        <!-- TABLE 3 -->
        <div class="dict-box">
            <div class="dict-header">
                <span class="dict-table-name">public.events</span>
                <span class="dict-badge">PostgreSQL Engine</span>
            </div>
            <table class="spec-table">
                <tr><th>Column</th><th>Type</th><th>Constraint</th><th>Description</th></tr>
                <tr><td class="c-name">event_id</td><td class="c-type">UUID</td><td class="c-rule">PK, NOT NULL</td><td class="c-desc">Symposium / event ID</td></tr>
                <tr><td class="c-name">org_id</td><td class="c-type">UUID</td><td class="c-rule">FK &rarr; organizations</td><td class="c-desc">Hosting club ID</td></tr>
                <tr><td class="c-name">title</td><td class="c-type">VARCHAR(200)</td><td class="c-rule">NOT NULL</td><td class="c-desc">Event headline</td></tr>
                <tr><td class="c-name">venue</td><td class="c-type">VARCHAR(100)</td><td class="c-rule">NOT NULL, INDEX</td><td class="c-desc">Seminar hall / lab</td></tr>
                <tr><td class="c-name">capacity</td><td class="c-type">INTEGER</td><td class="c-rule">CHECK (>0)</td><td class="c-desc">Seat cap limit</td></tr>
            </table>
        </div>

        <!-- TABLE 4 -->
        <div class="dict-box">
            <div class="dict-header">
                <span class="dict-table-name">public.attendance_records</span>
                <span class="dict-badge">PostgreSQL Engine</span>
            </div>
            <table class="spec-table">
                <tr><th>Column</th><th>Type</th><th>Constraint</th><th>Description</th></tr>
                <tr><td class="c-name">attendance_id</td><td class="c-type">UUID</td><td class="c-rule">PK, NOT NULL</td><td class="c-desc">Attendance row key</td></tr>
                <tr><td class="c-name">event_id</td><td class="c-type">UUID</td><td class="c-rule">FK &rarr; events</td><td class="c-desc">Associated event</td></tr>
                <tr><td class="c-name">user_id</td><td class="c-type">UUID</td><td class="c-rule">FK &rarr; users</td><td class="c-desc">Student attendee</td></tr>
                <tr><td class="c-name">marked_by</td><td class="c-type">UUID</td><td class="c-rule">FK &rarr; users</td><td class="c-desc">Coordinator ID</td></tr>
                <tr><td class="c-name">od_status</td><td class="c-type">VARCHAR(20)</td><td class="c-rule">DEFAULT 'pending'</td><td class="c-desc">pending, endorsed, synced</td></tr>
            </table>
        </div>
    </div>
</div>
</body>
</html>
"""

diagrams_list = [
    (html_arch, "Figure_1_1_System_Architecture"),
    (html_workflow, "Figure_1_2_Overall_Workflow"),
    (html_usecase, "Figure_2_1_Use_Case_Diagram"),
    (html_dfd, "Figure_2_2_Data_Flow_Diagram"),
    (html_erd, "Figure_3_1_Entity_Relationship_Diagram"),
    (html_db_struct, "Figure_3_2_Database_Structure")
]

print("Rendering all 6 diagrams in Design Thinking Reference Document Canvas Style...")
for html_data, name in diagrams_list:
    render_html_to_png(html_data, name)

print("Done rendering all 6 reference-styled diagrams!")
