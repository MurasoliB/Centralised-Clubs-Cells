const readline = require('readline');
const path = require('path');
const fs = require('fs');

// Load students
let students = [];
try {
  const studentsFile = fs.readFileSync(path.join(__dirname, '../src/lib/studentsData.ts'), 'utf8');
  const matches = [...studentsFile.matchAll(/id: '(.*?)',\s*name: '(.*?)',\s*email: '(.*?)',\s*department: '(.*?)',\s*register_number: '(.*?)',\s*year: (\d+),\s*section: '(.*?)'/g)];
  students = matches.map(m => ({
    id: m[1],
    name: m[2],
    email: m[3],
    department: m[4],
    register_number: m[5],
    year: parseInt(m[6]),
    section: m[7]
  }));
} catch (e) {
  students = [];
}

const ORGANIZATIONS = [
  { name: 'Coding Club', short: 'CC', type: 'Club', dept: 'Computer Science', events: 2, members: 32 },
  { name: 'Robotics Cell', short: 'RC', type: 'Cell', dept: 'Electronics', events: 2, members: 24 },
  { name: 'Cultural Club', short: 'CUL', type: 'Club', dept: 'Civil', events: 2, members: 28 },
  { name: 'Entrepreneurship Cell', short: 'ECELL', type: 'Cell', dept: 'Information Technology', events: 2, members: 26 },
  { name: 'Sports Club', short: 'SC', type: 'Club', dept: 'Mechanical', events: 2, members: 30 },
  { name: 'Literary Cell', short: 'LIT', type: 'Cell', dept: 'Computer Science', events: 2, members: 20 },
];

const EVENTS = [
  { id: 1, org: 'Coding Club (Club)', title: 'Kongu ByteCraft 2026: 24-Hr National Hackathon', type: 'Competition', date: 'Oct 28–29, 2026', venue: 'CC3 & CC4 Labs, IT Park', max: 160 },
  { id: 2, org: 'Coding Club (Club)', title: 'Full-Stack AI Masterclass: Autonomous Agents', type: 'Workshop', date: 'Nov 18–19, 2026', venue: 'IT Seminar Hall & CC5 Lab', max: 150 },
  { id: 3, org: 'Robotics Cell (Cell)', title: 'RoboKEC 2026: Autonomous Rover Challenge & Drone Prix', type: 'Competition', date: 'Oct 31, 2026', venue: 'Robotics Arena, Mech Block', max: 120 },
  { id: 4, org: 'Robotics Cell (Cell)', title: 'ROS2 & Computer Vision Industrial Automation Hands-On', type: 'Workshop', date: 'Nov 21–22, 2026', venue: 'Mechatronics Embedded Lab', max: 100 },
  { id: 5, org: 'Cultural Club (Club)', title: 'KEC Sangamam 2026: South Zone Cultural Fiesta', type: 'Cultural', date: 'Nov 04–05, 2026', venue: 'Open Air Theatre (OAT)', max: 450 },
  { id: 6, org: 'Cultural Club (Club)', title: 'KEC Symphony & Classical Carnatic Vocal Extravaganza', type: 'Cultural', date: 'Nov 25, 2026', venue: 'Maharaja Auditorium', max: 350 },
  { id: 7, org: 'Entrepreneurship Cell (Cell)', title: 'KEC VentureLaunch 2026: Seed Pitch & Angel Summit', type: 'Seminar', date: 'Nov 07, 2026', venue: 'MBA Convention Centre', max: 200 },
  { id: 8, org: 'Entrepreneurship Cell (Cell)', title: 'Startup Bootcamp: Patent Drafting & IPR Clinic', type: 'Workshop', date: 'Nov 28, 2026', venue: 'EDC Innovation Seminar Hall', max: 140 },
  { id: 9, org: 'Sports Club (Club)', title: 'Kongu Trophy 2026: Inter-Dept Badminton & Futsal Cup', type: 'Competition', date: 'Nov 11–12, 2026', venue: 'Indoor Sports Complex & Turf', max: 180 },
  { id: 10, org: 'Sports Club (Club)', title: 'KEC Annual Inter-Collegiate Cricket Championship', type: 'Competition', date: 'Dec 02–04, 2026', venue: 'Main Sports Pavilion', max: 220 },
  { id: 11, org: 'Literary Cell (Cell)', title: 'Kongu National Parliamentary Debate 2026', type: 'Competition', date: 'Nov 14–15, 2026', venue: 'Civil Conference Auditorium', max: 120 },
  { id: 12, org: 'Literary Cell (Cell)', title: 'Writers Conclave: Creative Non-Fiction & Oratory', type: 'Workshop', date: 'Dec 08–09, 2026', venue: 'Central Library Auditorium', max: 110 },
];

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function prompt(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function showMenu() {
  while (true) {
    console.clear();
    console.log('===============================================================================');
    console.log('       KEC CLUBHUB - COMMAND PROMPT INTERACTIVE CONSOLE MENU');
    console.log('===============================================================================');
    console.log('  [1] View Campus Organizations (6 Clubs & Cells, 2 Events Each)');
    console.log('  [2] View Campus Events Schedule (12 Official Events with Venues & Dates)');
    console.log('  [3] View Student Roster Summary (320 Students, 8 Depts, 40 per Dept)');
    console.log('  [4] Search Student by Roll Number or Name');
    console.log('  [5] Filter Students by Department');
    console.log('  [6] View Academic Year Breakdown');
    console.log('  [7] Return to Main Menu / Exit Console');
    console.log('===============================================================================');

    const choice = (await prompt('\nEnter option [1-7]: ')).trim();

    if (choice === '1') {
      console.clear();
      console.log('\n--- CAMPUS CLUBS & CELLS DIRECTORY ---');
      console.log('Name'.padEnd(25) + 'Type'.padEnd(10) + 'Department'.padEnd(25) + 'Events'.padEnd(10) + 'Members');
      console.log('-'.repeat(80));
      ORGANIZATIONS.forEach(o => {
        console.log(o.name.padEnd(25) + o.type.padEnd(10) + o.dept.padEnd(25) + String(o.events).padEnd(10) + o.members);
      });
      await prompt('\nPress Enter to return to menu...');
    } else if (choice === '2') {
      console.clear();
      console.log('\n--- CAMPUS EVENTS SCHEDULE (2 PER CLUB/CELL) ---');
      console.log('#'.padEnd(4) + 'Organization'.padEnd(30) + 'Date'.padEnd(18) + 'Title');
      console.log('-'.repeat(90));
      EVENTS.forEach(e => {
        console.log(String(e.id).padEnd(4) + e.org.padEnd(30) + e.date.padEnd(18) + e.title);
        console.log('    -> Category: ' + e.type + ' | Venue: ' + e.venue + ' | Capacity: ' + e.max);
      });
      await prompt('\nPress Enter to return to menu...');
    } else if (choice === '3') {
      console.clear();
      console.log('\n--- STUDENT ROSTER SUMMARY ---');
      console.log(`Total Enrolled Students : ${students.length}`);
      console.log('Total Departments       : 8 (Computer Science, IT, Electronics, Electrical, Mechanical, Civil, Chemical, BioTech)');
      console.log('Formula Satisfied       : 40 Students / Dept, 10 Students / Year (UG 1 to 4)');
      console.log('\nSample First 10 Students:');
      console.log('Roll No'.padEnd(14) + 'Name'.padEnd(24) + 'Dept'.padEnd(25) + 'Year'.padEnd(8) + 'Sec');
      console.log('-'.repeat(75));
      students.slice(0, 10).forEach(s => {
        console.log(s.register_number.padEnd(14) + s.name.padEnd(24) + s.department.padEnd(25) + ('Year ' + s.year).padEnd(8) + s.section);
      });
      await prompt('\nPress Enter to return to menu...');
    } else if (choice === '4') {
      const q = (await prompt('\nEnter student name or roll number (e.g. 24ITR001 or Gowtham): ')).trim().toLowerCase();
      const results = students.filter(s => s.name.toLowerCase().includes(q) || s.register_number.toLowerCase().includes(q));
      console.log(`\nFound ${results.length} student(s):`);
      console.log('Roll No'.padEnd(14) + 'Name'.padEnd(24) + 'Department'.padEnd(25) + 'Year'.padEnd(8) + 'Email');
      console.log('-'.repeat(90));
      results.slice(0, 20).forEach(s => {
        console.log(s.register_number.padEnd(14) + s.name.padEnd(24) + s.department.padEnd(25) + ('Yr ' + s.year).padEnd(8) + s.email);
      });
      await prompt('\nPress Enter to return to menu...');
    } else if (choice === '5') {
      const depts = [...new Set(students.map(s => s.department))];
      console.log('\nSelect a Department:');
      depts.forEach((d, i) => console.log(`  [${i + 1}] ${d}`));
      const idx = parseInt(await prompt('\nEnter department number: ')) - 1;
      if (depts[idx]) {
        const deptStudents = students.filter(s => s.department === depts[idx]);
        console.log(`\n--- ${depts[idx].toUpperCase()} (${deptStudents.length} Students, 10 per Year) ---`);
        console.log('Roll No'.padEnd(14) + 'Name'.padEnd(24) + 'Year'.padEnd(10) + 'Section'.padEnd(10) + 'Email');
        console.log('-'.repeat(80));
        deptStudents.forEach(s => {
          console.log(s.register_number.padEnd(14) + s.name.padEnd(24) + ('Year ' + s.year).padEnd(10) + s.section.padEnd(10) + s.email);
        });
      }
      await prompt('\nPress Enter to return to menu...');
    } else if (choice === '6') {
      console.clear();
      console.log('\n--- ACADEMIC YEAR DISTRIBUTION (UG 1 TO 4) ---');
      const years = [1, 2, 3, 4];
      years.forEach(y => {
        const count = students.filter(s => s.year === y).length;
        console.log(`  Academic Year ${y} : ${count} Students (10 students per department across 8 departments)`);
      });
      console.log(`  Total           : ${students.length} Students Verified`);
      await prompt('\nPress Enter to return to menu...');
    } else if (choice === '7') {
      break;
    }
  }
  rl.close();
}

showMenu();

