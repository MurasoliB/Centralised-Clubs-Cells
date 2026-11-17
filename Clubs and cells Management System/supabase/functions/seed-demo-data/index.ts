import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    // Only admin, faculty coordinator, and club coordinator — no students
    const users = [
      { email: "admin@college.edu", password: "admin123456", name: "Dr. Rajesh Kumar", role: "admin", department: "Administration", phone: "+919999900001" },
      { email: "faculty@college.edu", password: "faculty123456", name: "Prof. Suresh Menon", role: "faculty_coordinator", department: "Computer Science", phone: "+919999900002" },
      { email: "coordinator@college.edu", password: "coord123456", name: "Ananya Sharma", role: "club_coordinator", department: "Information Technology", phone: "+919999900003" },
    ];

    const createdUsers: { id: string; email: string; role: string; name: string; department: string }[] = [];

    for (const u of users) {
      const { data: existing } = await supabase.auth.admin.listUsers();
      const found = existing.users.find((eu: any) => eu.email === u.email);
      let userId = found?.id;

      if (!userId) {
        const { data: newUser, error } = await supabase.auth.admin.createUser({
          email: u.email,
          password: u.password,
          email_confirm: true,
          user_metadata: { name: u.name, role: u.role },
        });
        if (error) continue;
        userId = newUser.user.id;
      }

      await supabase.from("profiles").upsert({
        id: userId,
        name: u.name,
        email: u.email,
        role: u.role,
        department: u.department,
        phone: u.phone,
        is_active: true,
      });

      createdUsers.push({ id: userId!, email: u.email, role: u.role, name: u.name, department: u.department });
    }

    const faculty = createdUsers.find((u) => u.role === "faculty_coordinator");
    const clubCoord = createdUsers.find((u) => u.role === "club_coordinator");

    const orgs = [
      { name: "Coding Club", short_name: "CC", type: "club", description: "A community for programming enthusiasts to learn and build projects.", category: "Technical", department: "Computer Science", faculty_coord: faculty?.id, student_coord: clubCoord?.id, contact_email: "coding@college.edu" },
      { name: "Robotics Cell", short_name: "RC", type: "cell", description: "Building autonomous robots and competing nationally.", category: "Technical", department: "Electronics", faculty_coord: faculty?.id, student_coord: null, contact_email: "robotics@college.edu" },
      { name: "Cultural Club", short_name: "CUL", type: "club", description: "Celebrating diversity through music, dance, and drama.", category: "Cultural", department: "Civil", faculty_coord: null, student_coord: clubCoord?.id, contact_email: "cultural@college.edu" },
      { name: "Entrepreneurship Cell", short_name: "ECELL", type: "cell", description: "Fostering innovation and startup culture on campus.", category: "Professional", department: "Information Technology", faculty_coord: faculty?.id, student_coord: null, contact_email: "ecell@college.edu" },
      { name: "Sports Club", short_name: "SC", type: "club", description: "Promoting fitness and competitive sports.", category: "Sports", department: "Mechanical", faculty_coord: null, student_coord: null, contact_email: "sports@college.edu" },
      { name: "Literary Cell", short_name: "LIT", type: "cell", description: "A space for writers, poets, and debaters.", category: "Literary", department: "Computer Science", faculty_coord: null, student_coord: null, contact_email: "literary@college.edu" },
    ];

    const createdOrgs: { id: string; name: string; type: string }[] = [];
    for (const o of orgs) {
      const { data: existing } = await supabase.from("organizations").select("id, name, type").eq("name", o.name).maybeSingle();
      if (existing) { createdOrgs.push(existing); continue; }
      const { data, error } = await supabase.from("organizations").insert({
        name: o.name,
        short_name: o.short_name,
        type: o.type,
        description: o.description,
        category: o.category,
        department: o.department,
        faculty_coordinator_id: o.faculty_coord,
        student_coordinator_id: o.student_coord,
        contact_email: o.contact_email,
        status: "active",
      }).select("id, name, type").single();
      if (!error && data) createdOrgs.push(data);
    }

    // Events
    const events = [
      { title: "Hackathon 2026", type: "competition", location: "Main Auditorium", max: 100, days: 7 },
      { title: "Robotics Workshop", type: "workshop", location: "Electronics Lab", max: 50, days: 3 },
      { title: "Cultural Night", type: "cultural", location: "Open Ground", max: 200, days: 10 },
      { title: "Startup Pitch Day", type: "seminar", location: "Seminar Hall", max: 80, days: 5 },
      { title: "Inter-college Debate", type: "competition", location: "Conference Room", max: 40, days: 14 },
      { title: "AI Seminar", type: "seminar", location: "CS Seminar Hall", max: 120, days: 2 },
    ];

    const createdEvents: { id: string }[] = [];
    for (let i = 0; i < events.length; i++) {
      const e = events[i];
      const org = createdOrgs[i % createdOrgs.length];
      if (!org) continue;
      const startDate = new Date(Date.now() + e.days * 86400000);
      const { data, error } = await supabase.from("events").insert({
        organization_id: org.id,
        title: e.title,
        description: `${e.title} - a great opportunity to learn and network.`,
        event_type: e.type,
        location: e.location,
        start_date: startDate.toISOString(),
        end_date: new Date(startDate.getTime() + 4 * 3600000).toISOString(),
        registration_deadline: new Date(startDate.getTime() - 86400000).toISOString(),
        maximum_participants: e.max,
        status: "upcoming",
        created_by: faculty?.id,
      }).select("id").single();
      if (!error && data) createdEvents.push(data);
    }

    // Announcements
    for (let i = 0; i < createdOrgs.length; i++) {
      const org = createdOrgs[i];
      await supabase.from("announcements").insert({
        organization_id: org.id,
        title: `Welcome to ${org.name}!`,
        content: `Greetings from ${org.name}. Stay tuned for upcoming events and activities.`,
        created_by: faculty?.id,
        target_audience: "all",
      });
    }

    // Notifications for all users
    for (const u of createdUsers) {
      await supabase.from("notifications").insert({
        user_id: u.id,
        title: "Welcome to ClubHub",
        message: `Hello ${u.name}, welcome to the Centralized Clubs & Cells Management System!`,
        type: "info",
      });
    }

    return new Response(JSON.stringify({ success: true, users: createdUsers.length, orgs: createdOrgs.length, events: createdEvents.length }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
