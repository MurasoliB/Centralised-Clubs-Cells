export interface OrgWithStats {
  id: string;
  name: string;
  short_name: string | null;
  type: string;
  description: string | null;
  category: string | null;
  department: string | null;
  status: string;
  memberCount: number;
  eventCount: number;
}

export const DEFAULT_ORGANIZATIONS: OrgWithStats[] = [
  {
    id: '45283f33-e7a2-4938-bfc6-08ea848e0d61',
    name: 'Coding Club',
    short_name: 'CC',
    type: 'club',
    description: 'A community for programming enthusiasts to learn, build projects, and compete in hackathons.',
    category: 'Technical',
    department: 'Computer Science',
    status: 'active',
    memberCount: 32,
    eventCount: 2,
  },
  {
    id: '32cfeb41-1570-4151-8725-191f4e48b983',
    name: 'Robotics Cell',
    short_name: 'RC',
    type: 'cell',
    description: 'Building autonomous rovers, drones, and competing in national hardware robotics competitions.',
    category: 'Technical',
    department: 'Electronics',
    status: 'active',
    memberCount: 24,
    eventCount: 2,
  },
  {
    id: '21ad11f0-1dda-4cbe-a10f-683dbe0d417e',
    name: 'Cultural Club',
    short_name: 'CUL',
    type: 'club',
    description: 'Celebrating diversity through traditional South Indian music, folk dance, classical arts, and theatre.',
    category: 'Cultural',
    department: 'Civil',
    status: 'active',
    memberCount: 28,
    eventCount: 2,
  },
  {
    id: 'c07fb697-55d1-4167-abb6-78f653542c85',
    name: 'Entrepreneurship Cell',
    short_name: 'ECELL',
    type: 'cell',
    description: 'Fostering innovation, IPR patents, seed venture funding, and student startup acceleration on campus.',
    category: 'Professional',
    department: 'Information Technology',
    status: 'active',
    memberCount: 26,
    eventCount: 2,
  },
  {
    id: '3253a0c6-a0aa-4610-85ab-b29997900f89',
    name: 'Sports Club',
    short_name: 'SC',
    type: 'club',
    description: 'Promoting athletic fitness, inter-collegiate tournaments, cricket, futsal, and badminton leagues.',
    category: 'Sports',
    department: 'Mechanical',
    status: 'active',
    memberCount: 30,
    eventCount: 2,
  },
  {
    id: 'd9d6ee32-2af3-40a2-a55d-2ea74eefcb21',
    name: 'Literary Cell',
    short_name: 'LIT',
    type: 'cell',
    description: 'A platform for aspiring writers, parliamentary debaters, essayists, and creative orators.',
    category: 'Literary',
    department: 'Computer Science',
    status: 'active',
    memberCount: 20,
    eventCount: 2,
  },
];

