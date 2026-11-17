export interface RealCampusEvent {
  id: string;
  organization_id: string;
  title: string;
  description: string;
  event_type: 'competition' | 'workshop' | 'seminar' | 'cultural' | 'technical';
  location: string;
  start_date: string;
  end_date: string;
  registration_deadline: string;
  maximum_participants: number;
  banner: string;
  status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled';
  instructions: string;
  organization: {
    id: string;
    name: string;
    short_name: string;
    type: 'club' | 'cell';
    department?: string;
  };
}

/**
 * 12 Fresh Official Campus Events
 * Exactly 2 Events per Club or Cell (6 Organizations total)
 * All dates are upcoming (late October, November, and December 2026)
 */
export const REAL_CAMPUS_EVENTS: RealCampusEvent[] = [
  // 1. Coding Club (Club) - Event 1
  {
    id: 'evt-cc-01',
    organization_id: '45283f33-e7a2-4938-bfc6-08ea848e0d61',
    title: 'Kongu ByteCraft 2026: 24-Hour National Hackathon',
    description: 'Annual 24-hour collegiate hackathon solving core problem statements in AI, Blockchain, and Edge IoT with industry mentorship and seed grants.',
    event_type: 'competition',
    location: 'CC3 & CC4 Advanced Computing Labs, IT Park',
    start_date: '2026-10-28T09:00:00+05:30',
    end_date: '2026-10-29T17:00:00+05:30',
    registration_deadline: '2026-10-27T18:00:00+05:30',
    maximum_participants: 160,
    banner: 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Bring your laptops, chargers, and college ID card. High-speed LAN and refreshments will be provided throughout the 24 hours.',
    organization: {
      id: '45283f33-e7a2-4938-bfc6-08ea848e0d61',
      name: 'Coding Club',
      short_name: 'CC',
      type: 'club',
      department: 'Computer Science',
    },
  },
  // 2. Coding Club (Club) - Event 2
  {
    id: 'evt-cc-02',
    organization_id: '45283f33-e7a2-4938-bfc6-08ea848e0d61',
    title: 'Full-Stack AI Masterclass: Autonomous Agents & Vector Architectures',
    description: 'Hands-on intensive two-day masterclass on building multi-agent architectures, function-calling workflows, and RAG vector search pipelines.',
    event_type: 'workshop',
    location: 'IT Seminar Hall & CC5 High-Performance Lab',
    start_date: '2026-11-18T09:00:00+05:30',
    end_date: '2026-11-19T16:30:00+05:30',
    registration_deadline: '2026-11-16T18:00:00+05:30',
    maximum_participants: 150,
    banner: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Ensure Python 3.11+, Node.js, and VS Code are preinstalled on your laptops. Starter repositories will be distributed at 9:00 AM.',
    organization: {
      id: '45283f33-e7a2-4938-bfc6-08ea848e0d61',
      name: 'Coding Club',
      short_name: 'CC',
      type: 'club',
      department: 'Computer Science',
    },
  },

  // 3. Robotics Cell (Cell) - Event 1
  {
    id: 'evt-rc-01',
    organization_id: '32cfeb41-1570-4151-8725-191f4e48b983',
    title: 'RoboKEC 2026: Autonomous Rover Challenge & Drone Prix',
    description: 'State-level robotics confrontation featuring custom line-follower rovers, obstacle avoidance mazes, and high-speed FPV micro-drone obstacle navigation.',
    event_type: 'competition',
    location: 'Robotics Arena, Mechanical & Mechatronics Block',
    start_date: '2026-10-31T09:30:00+05:30',
    end_date: '2026-10-31T17:30:00+05:30',
    registration_deadline: '2026-10-29T20:00:00+05:30',
    maximum_participants: 120,
    banner: 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Bots must strictly adhere to weight specifications (max 3kg for ground rovers). LiPo battery charging is strictly confined to safety stations.',
    organization: {
      id: '32cfeb41-1570-4151-8725-191f4e48b983',
      name: 'Robotics Cell',
      short_name: 'RC',
      type: 'cell',
      department: 'Electronics',
    },
  },
  // 4. Robotics Cell (Cell) - Event 2
  {
    id: 'evt-rc-02',
    organization_id: '32cfeb41-1570-4151-8725-191f4e48b983',
    title: 'ROS2 & Computer Vision Workshop: Industrial Automation Hands-On',
    description: 'Practical training on Robot Operating System 2 (ROS2), LiDAR point clouds, and OpenCV object identification for smart factory manipulators.',
    event_type: 'workshop',
    location: 'Mechatronics Embedded Systems Laboratory',
    start_date: '2026-11-21T09:30:00+05:30',
    end_date: '2026-11-22T17:00:00+05:30',
    registration_deadline: '2026-11-19T18:00:00+05:30',
    maximum_participants: 100,
    banner: 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Linux/Ubuntu environment or WSL2 recommended. Hardware microcontroller kits will be loaned during lab sessions.',
    organization: {
      id: '32cfeb41-1570-4151-8725-191f4e48b983',
      name: 'Robotics Cell',
      short_name: 'RC',
      type: 'cell',
      department: 'Electronics',
    },
  },

  // 5. Cultural Club (Club) - Event 1
  {
    id: 'evt-cul-01',
    organization_id: '21ad11f0-1dda-4cbe-a10f-683dbe0d417e',
    title: 'KEC Sangamam 2026: South Zone Cultural & Folk Arts Fiesta',
    description: 'Inter-collegiate cultural extravaganza featuring traditional folk dance, theatrical battle of bands, fusion choreography, and street mime art.',
    event_type: 'cultural',
    location: 'Open Air Theatre (OAT) & Convention Centre',
    start_date: '2026-11-04T10:00:00+05:30',
    end_date: '2026-11-05T20:00:00+05:30',
    registration_deadline: '2026-11-02T18:00:00+05:30',
    maximum_participants: 450,
    banner: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'All music audio tracks must be submitted to the stage crew 2 hours prior to performance slots. Traditional dress code encouraged.',
    organization: {
      id: '21ad11f0-1dda-4cbe-a10f-683dbe0d417e',
      name: 'Cultural Club',
      short_name: 'CUL',
      type: 'club',
      department: 'Civil',
    },
  },
  // 6. Cultural Club (Club) - Event 2
  {
    id: 'evt-cul-02',
    organization_id: '21ad11f0-1dda-4cbe-a10f-683dbe0d417e',
    title: 'KEC Symphony & Classical Carnatic Vocal Extravaganza',
    description: 'Evening of acoustic Carnatic jugalbandi, violin ensembles, and Western classical instrumentals featuring talent across all 8 departments.',
    event_type: 'cultural',
    location: 'Maharaja Auditorium, Main Campus',
    start_date: '2026-11-25T16:00:00+05:30',
    end_date: '2026-11-25T21:00:00+05:30',
    registration_deadline: '2026-11-23T18:00:00+05:30',
    maximum_participants: 350,
    banner: 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Reserved auditorium seating. Doors close 15 minutes before the opening curtain at 4:00 PM.',
    organization: {
      id: '21ad11f0-1dda-4cbe-a10f-683dbe0d417e',
      name: 'Cultural Club',
      short_name: 'CUL',
      type: 'club',
      department: 'Civil',
    },
  },

  // 7. Entrepreneurship Cell (Cell) - Event 1
  {
    id: 'evt-ec-01',
    organization_id: 'c07fb697-55d1-4167-abb6-78f653542c85',
    title: 'KEC VentureLaunch 2026: Seed Pitch & Angel Summit',
    description: 'Campus startup showcase where student founders pitch viable business models to certified venture capital investors and Tamil Nadu angel networks.',
    event_type: 'seminar',
    location: 'MBA Convention Centre & Incubation Centre',
    start_date: '2026-11-07T09:30:00+05:30',
    end_date: '2026-11-07T17:00:00+05:30',
    registration_deadline: '2026-11-05T18:00:00+05:30',
    maximum_participants: 200,
    banner: 'https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: '10-minute slide deck pitch followed by 5 minutes of Q&A. Executive summaries must be uploaded prior to the deadline.',
    organization: {
      id: 'c07fb697-55d1-4167-abb6-78f653542c85',
      name: 'Entrepreneurship Cell',
      short_name: 'ECELL',
      type: 'cell',
      department: 'Information Technology',
    },
  },
  // 8. Entrepreneurship Cell (Cell) - Event 2
  {
    id: 'evt-ec-02',
    organization_id: 'c07fb697-55d1-4167-abb6-78f653542c85',
    title: 'Startup Bootcamp: Patent Drafting, IPR & Product-Market Fit',
    description: 'Interactive clinic led by IP attorneys on patent filing, provisional claims, trademark registration, and building sustainable revenue funnels.',
    event_type: 'workshop',
    location: 'EDC Innovation Seminar Hall',
    start_date: '2026-11-28T09:30:00+05:30',
    end_date: '2026-11-28T16:30:00+05:30',
    registration_deadline: '2026-11-26T18:00:00+05:30',
    maximum_participants: 140,
    banner: 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Bring draft architecture diagrams or project descriptions for live patent novelty screening.',
    organization: {
      id: 'c07fb697-55d1-4167-abb6-78f653542c85',
      name: 'Entrepreneurship Cell',
      short_name: 'ECELL',
      type: 'cell',
      department: 'Information Technology',
    },
  },

  // 9. Sports Club (Club) - Event 1
  {
    id: 'evt-sc-01',
    organization_id: '3253a0c6-a0aa-4610-85ab-b29997900f89',
    title: 'Kongu Trophy 2026: Inter-Departmental Badminton & Futsal Cup',
    description: 'Premier floodlit sports tournament featuring men and women badminton singles/doubles and 5-a-side knockout futsal tournament.',
    event_type: 'competition',
    location: 'KEC Indoor Sports Complex & Turf Ground',
    start_date: '2026-11-11T08:30:00+05:30',
    end_date: '2026-11-12T18:00:00+05:30',
    registration_deadline: '2026-11-09T18:00:00+05:30',
    maximum_participants: 180,
    banner: 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Non-marking badminton court shoes and shin guards for futsal are strictly mandatory. Official department sports jerseys required.',
    organization: {
      id: '3253a0c6-a0aa-4610-85ab-b29997900f89',
      name: 'Sports Club',
      short_name: 'SC',
      type: 'club',
      department: 'Mechanical',
    },
  },
  // 10. Sports Club (Club) - Event 2
  {
    id: 'evt-sc-02',
    organization_id: '3253a0c6-a0aa-4610-85ab-b29997900f89',
    title: 'KEC Annual Inter-Collegiate Cricket & Basketball Championship',
    description: '3-day collegiate championship hosting 16 regional college teams across T20 leather-ball cricket and outdoor FIBA-rules basketball.',
    event_type: 'competition',
    location: 'KEC Main Sports Pavilion & Cricket Ground',
    start_date: '2026-12-02T08:00:00+05:30',
    end_date: '2026-12-04T18:00:00+05:30',
    registration_deadline: '2026-11-30T18:00:00+05:30',
    maximum_participants: 220,
    banner: 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Team rosters must be verified with physical student ID cards at the tournament registration desk at 7:30 AM.',
    organization: {
      id: '3253a0c6-a0aa-4610-85ab-b29997900f89',
      name: 'Sports Club',
      short_name: 'SC',
      type: 'club',
      department: 'Mechanical',
    },
  },

  // 11. Literary Cell (Cell) - Event 1
  {
    id: 'evt-lit-01',
    organization_id: 'd9d6ee32-2af3-40a2-a55d-2ea74eefcb21',
    title: 'Kongu National Parliamentary Debate & Youth Mock Parliament 2026',
    description: 'Flagship British Parliamentary debating championship debating contemporary technology policy, green economy, and AI ethics.',
    event_type: 'competition',
    location: 'Civil Conference Auditorium & Smart Seminar Hall',
    start_date: '2026-11-14T09:30:00+05:30',
    end_date: '2026-11-15T16:30:00+05:30',
    registration_deadline: '2026-11-12T18:00:00+05:30',
    maximum_participants: 120,
    banner: 'https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Debates follow Oxford/BP rules. Adjudicator briefings start promptly at 9:15 AM on day 1.',
    organization: {
      id: 'd9d6ee32-2af3-40a2-a55d-2ea74eefcb21',
      name: 'Literary Cell',
      short_name: 'LIT',
      type: 'cell',
      department: 'Computer Science',
    },
  },
  // 12. Literary Cell (Cell) - Event 2
  {
    id: 'evt-lit-02',
    organization_id: 'd9d6ee32-2af3-40a2-a55d-2ea74eefcb21',
    title: 'Writers Conclave: Creative Non-Fiction, Poetry & Technical Oratory',
    description: 'Intensive workshop on narrative non-fiction, spoken word poetry, essay publishing, and effective technical presentation skills.',
    event_type: 'workshop',
    location: 'Central Library Digital Auditorium',
    start_date: '2026-12-08T10:00:00+05:30',
    end_date: '2026-12-09T16:00:00+05:30',
    registration_deadline: '2026-12-06T18:00:00+05:30',
    maximum_participants: 110,
    banner: 'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80',
    status: 'upcoming',
    instructions: 'Participants may bring one original manuscript or poetry piece for peer-critique circle and editorial review.',
    organization: {
      id: 'd9d6ee32-2af3-40a2-a55d-2ea74eefcb21',
      name: 'Literary Cell',
      short_name: 'LIT',
      type: 'cell',
      department: 'Computer Science',
    },
  },
];

