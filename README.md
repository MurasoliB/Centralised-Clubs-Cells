# Centralised-Clubs-Cells (ClubHub)
> **Kongu Engineering College (Autonomous) &bull; Department of Information Technology**  
> Centralised Extracurricular Affairs, Student Charters, Events, and Cell Governance Platform

[![React](https://img.shields.io/badge/React-18.3.1-blue.svg?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue.svg?logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4.8-646CFF.svg?logo=vite)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E.svg?logo=supabase)](https://supabase.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-336791.svg?logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Executive Summary

**ClubHub** is an enterprise-grade extracurricular management portal specifically designed for collegiate institutions. Built with human-centered design principles for Kongu Engineering College (KEC), it bridges the communication and governance divide across campus clubs, technical research cells, faculty coordinators, and student bodies.

Traditionally, extracurricular operations depend on disparate chat groups, manual paperwork, disconnected spreadsheets, and fragmented attendance sheets. **ClubHub** centralizes all charters, memberships, hackathon registrations, achievement verifications, event budgeting, and compliance logs into a single institutional repository.

---

## 🚀 Key System Features

### 1. 🛡️ Institutional Role-Based Access Control (RBAC)
Dedicated user workspaces tailored to institutional hierarchy:
- **College Administrator (Dean / Principal):** Complete collegiate oversight, audit compliance logs, charter approvals, and faculty coordinator appointments.
- **Faculty Coordinator (Staff Advisor):** Governance over assigned club/cell, event sanctioning, certificate endorsements, and budget validation.
- **Club Coordinator (Student Lead):** Operational dashboard to publish events, authenticate member registrations, verify attendance, and announce circulars.
- **Student Body:** Discover clubs and cells, 1-click apply for memberships, RSVP for campus hackathons and workshops, track personal attendance, and build an extracurricular portfolio.

### 2. ⚡ Zero-Latency Instant Demo Mode
- **1-Click Institutional Access:** One-click role buttons on the login screen (`Student`, `Lead`, `Faculty`, `Admin`) allow instant system evaluation without requiring manual credential entry.
- **Deterministic RFC-Compliant UUID Architecture:** Session generation ensures seamless foreign key integrity across both local and live PostgreSQL cloud environments.

### 3. 📅 Real-Time Campus Events & RSVP Hub
- Published events display countdown timers, venue tags, participant capacity quotas, and downloadable agendas.
- Students can register and cancel registrations with immediate UI feedback and local persistence fallback.

### 4. 📝 Club & Cell Charter Management
- Real-time directory categorizing **Technical Clubs** (Coding Club, Design Tribe, Robotics Club) and **Specialized Cells** (Institution's Innovation Council, Entrepreneurship Cell, Women Development Cell).
- In-depth organization profile pages featuring faculty advisor bios, student leader contacts, active charter rosters, and past achievements.

### 5. 👥 Membership Applications & Approvals
- Frictionless 1-click **`[ Apply ]`** directly from the directory table or detailed profile views.
- Coordinators and Administrators receive pending submissions with real-time **Approve** and **Reject** authentication controls.

### 6. 🏆 Student Academic & Activity Portfolio
- Dynamic student profiles tracking skills, interests, registration numbers, departments, and approved club affiliations.
- Client-side canvas image optimization for high-resolution academic avatar uploads.

### 7. 🔒 Resilient Dual-Layer Architecture
- **Supabase Cloud Native:** Real-time PostgreSQL database with relational constraints and storage triggers.
- **Offline / Fault-Tolerant Engine:** Automatic browser cache fallback prevents any page freezes or UI lockups even if the remote database is offline, rate-limited, or pending migration.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend Framework** | React 18.3.1 with TypeScript 5.5.3 |
| **Bundler & Build Tool** | Vite 5.4.8 (Rollup-optimized ESM) |
| **Styling & UI Design** | Tailwind CSS 3.4.1, Lucide React (Vector Icons), Wikipedia Vector Skin aesthetics |
| **State & Navigation** | React Router DOM v7, React Context API, Custom Hooks |
| **Backend & Database** | Supabase Cloud (PostgreSQL 15), Row Level Security (RLS) |
| **Forms & Validation** | React Hook Form, Zod Schema Validation |
| **Data Visualization** | Recharts (Campus Participation & Attendance Trends) |
| **Desktop Automation** | Windows Command & Batch Scripts (`ClubHub.bat`) |

---

## 📋 System Requirements

- **Node.js:** v18.0.0 or higher (Node v20+ recommended)
- **NPM:** v9.0.0 or higher
- **Web Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari
- **Operating System:** Windows, macOS, or Linux

---

## ⚙️ Quick Installation Guide

### Option A: 1-Click Launch (Windows)
If you are on Windows, simply double-click the included batch launcher:
```bat
ClubHub.bat
```
This script automatically detects project paths, prompts you with launch options, boots the Vite development server, and opens your browser directly to `http://localhost:5173/`.

---

### Option B: Step-by-Step Manual Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/MurasoliB/Centralised-Clubs-Cells.git
cd Centralised-Clubs-Cells
```

#### 2. Install Dependencies
Install dependencies in both the root workspace and inner application directory:
```bash
npm install
npm --prefix "Clubs and cells Management System" install
```

#### 3. Configure Environment Variables
Copy the `.env.example` template to `.env`:
```bash
cp .env.example .env
cp .env.example "Clubs and cells Management System/.env"
```

Open `.env` in any text editor:
```env
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-publishable-key-here
```
> **Note:** If you run without configuring `.env`, ClubHub automatically engages its built-in institutional offline mode with pre-populated demo clubs, events, and rosters!

#### 4. (Optional) Run Supabase Database Migration & Dummy Data
If connecting to your own live Supabase project:
1. Open your project on [Supabase Dashboard](https://supabase.com/dashboard).
2. Navigate to the **SQL Editor**.
3. Copy and run the contents of [`fix_rls_and_dummy_data.sql`](./fix_rls_and_dummy_data.sql).
4. All tables, organizations, events, demo profiles, and memberships will be initialized instantly.

#### 5. Start the Development Server
```bash
npm run dev
```
Navigate to **`http://localhost:5173/`** in your browser.

#### 6. Build for Production
To create an optimized production build:
```bash
npm run build
```
Compiled output is generated in `Clubs and cells Management System/dist/`.

---

## 🔑 Pre-Configured Demo Accounts

For instant evaluation, you can use the **1-Click Demo** buttons on the Login page (`/login`) or sign in using these pre-configured accounts:

| Role | Email | Password | Department |
|---|---|---|---|
| **Student** | `student@college.edu` | `Student@KEC2026` | Information Technology |
| **Club Coordinator** | `coordinator@college.edu` | `coord123456` | Information Technology |
| **Faculty Coordinator** | `faculty@college.edu` | `faculty123456` | Information Technology |
| **Administrator** | `admin@college.edu` | `admin123456` | Administration |
| **Student (Custom)** | `vigneshM@gmail.com` | `AnyPassword` | Information Technology |
| **Student (Custom)** | `balajimurasoli@gmail.com`| `AnyPassword` | Information Technology |

---

## 📂 Project Structure

```
Centralised-Clubs-Cells/
├── .env.example                      # Environment variables template
├── .gitignore                        # Git exclusion rules (sensitive tokens protected)
├── ClubHub.bat                       # 1-Click Windows execution script
├── Database_Showcase.html            # Standalone visual offline database viewer
├── fix_rls_and_dummy_data.sql        # Master database sync & RLS configuration script
├── seed_dummy_data.sql               # Seed data for campus organizations & events
├── package.json                      # Workspace orchestrator package configuration
├── README.md                         # Project documentation and setup guide
└── Clubs and cells Management System/ # Core React + Vite application
    ├── .env.example                  # Nested environment template
    ├── package.json                  # Application dependencies and scripts
    ├── vite.config.ts                # Vite build and path alias configurations
    ├── tailwind.config.js            # Tailwind CSS styling tokens
    ├── src/
    │   ├── App.tsx                   # Main route tree with ProtectedRoute guards
    │   ├── main.tsx                  # React entry point
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── AppLayout.tsx     # Institutional top navbar and skin header
    │   │   │   ├── PageHeader.tsx    # Standardized section header
    │   │   │   └── ProtectedRoute.tsx# Role-based route guard
    │   │   └── ui/                   # Reusable UI component library (Cards, Buttons, Modals, Tables)
    │   ├── context/
    │   │   ├── AuthContext.tsx       # Authentication, session recovery, and demo fallback
    │   │   ├── ThemeContext.tsx      # Dark / Light theme provider
    │   │   └── ToastContext.tsx      # Global notification toasts
    │   ├── lib/
    │   │   ├── constants.ts          # Institutional constants and nav configurations
    │   │   ├── eventsData.ts         # Pre-loaded campus hackathons and workshops
    │   │   ├── organizationsData.ts  # Pre-loaded technical clubs and cells catalog
    │   │   ├── orgScope.ts           # Work portfolio and club assignment resolver
    │   │   ├── supabase.ts           # Supabase client instantiation
    │   │   └── utils.ts              # UUID helpers, date formatters, CSV exporters
    │   ├── pages/
    │   │   ├── auth/
    │   │   │   ├── LoginPage.tsx     # Authentication portal with 1-click fill
    │   │   │   └── SignupPage.tsx    # Student account registration
    │   │   ├── AchievementsPage.tsx  # Student laurels and certificate records
    │   │   ├── AnnouncementsPage.tsx # Official circulars and notifications
    │   │   ├── AttendancePage.tsx    # Event attendance rosters and scanning
    │   │   ├── AuditLogsPage.tsx     # Compliance activity audit log (Admin only)
    │   │   ├── DashboardPage.tsx     # Executive analytics and quick action hub
    │   │   ├── EventDetailsPage.tsx  # Event agenda, location map, and RSVP actions
    │   │   ├── EventsPage.tsx        # Collegiate events calendar
    │   │   ├── MembershipsPage.tsx   # Enrolled charters and approval workflows
    │   │   ├── OrganizationDetailsPage.tsx # Club/Cell infobox, roster, and applications
    │   │   ├── OrganizationsPage.tsx # Campus directory with 1-click [ Apply ]
    │   │   ├── ProfilePage.tsx       # Institutional credentials and avatar studio
    │   │   ├── ReportsPage.tsx       # Performance analytics and CSV export
    │   │   └── StaffManagementPage.tsx # Faculty advisor assignment (Admin only)
    │   └── types/
    │       └── database.ts           # TypeScript interfaces for database schema
    └── supabase/
        └── migrations/
            └── 20260822085230_create_clubs_management_schema.sql # 11 relational tables
```

---

## 🔍 Major Feature Workflows

### 1. Student Membership Application
1. Sign in as a **Student** (`student@college.edu` or custom email).
2. Navigate to **Clubs & Cells** from the top navigation bar.
3. Click **`[ Apply ]`** directly on any organization row, or click **`[ View Profile ]`** &rarr; **`Apply for Membership`**.
4. Application status immediately transitions to `[ Pending ]`.
5. Switch to **My Memberships** to view all your enrolled and pending charters.

### 2. Coordinator Review & Approval
1. Sign in as a **Club Coordinator** (`coordinator@college.edu`).
2. Navigate to **Memberships**.
3. Under **Pending Applications**, inspect incoming student applicant details (Name, Register Number, Department).
4. Click **`Approve`** or **`Reject`**. Approved students are immediately moved to the **Active Member Roll**.

### 3. Event RSVP & Attendance
1. Browse upcoming campus competitions in **Events** (e.g. *Kongu ByteCraft 24-Hour Hackathon*).
2. Click **`View Details`** &rarr; **`Register for Event`**.
3. System verifies participant quotas and reserves the student's seat with a `✓ Registered` badge.

---

## ❓ Troubleshooting Guide

<details>
<summary><strong>1. "ReferenceError: Shield is not defined" or icon error</strong></summary>

- **Resolution:** This has been fully resolved by ensuring all Lucide vector icon imports in `ProfilePage.tsx` and UI components are explicitly declared. Run `npm run build` to verify clean compilation.
</details>

<details>
<summary><strong>2. "invalid input syntax for type uuid" error when opening details</strong></summary>

- **Resolution:** ClubHub implements `isUUID()` sanitization across `OrganizationDetailsPage.tsx` and `EventDetailsPage.tsx`. Non-UUID slugs automatically resolve to local charters without triggering PostgreSQL abort errors.
</details>

<details>
<summary><strong>3. "Failed to submit application: violates row-level security policy"</strong></summary>

- **Resolution:** Run [`fix_rls_and_dummy_data.sql`](./fix_rls_and_dummy_data.sql) in your Supabase SQL editor. Additionally, ClubHub features automatic local fallback storage so operations always succeed immediately.
</details>

<details>
<summary><strong>4. Port 5173 is already in use</strong></summary>

- **Resolution:** Stop other running dev servers, or specify a custom port:
  ```bash
  npm run dev -- --port 3000
  ```
</details>

---

## 👥 Contributors & Acknowledgements

Developed by the Department of Information Technology, **Kongu Engineering College (Autonomous)**, Perundurai, Erode, Tamil Nadu, India.

- **Murasoli B** ([@MurasoliB](https://github.com/MurasoliB))
- **Sahana S**
- **Saran Karthik S**
- **Sharan V**
- **Vignesh M**

---

## 📄 License
This project is distributed under the **MIT License**. Feel free to use, modify, and distribute with proper attribution.
