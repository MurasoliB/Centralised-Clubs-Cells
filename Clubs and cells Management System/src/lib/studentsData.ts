export interface RealStudent {
  id: string;
  name: string;
  email: string;
  department: string;
  register_number: string;
  year: number;
  section: string;
  role: 'student';
  is_active: boolean;
}

// 8 Official Departments x 40 Students (10 students per year) = 320 Real Students
export const REAL_STUDENTS_ROSTER: RealStudent[] = [
  // ==========================================
  // 1. INFORMATION TECHNOLOGY (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24itr001', name: 'Murasoli B', email: 'murasolib.24itr001@kongu.edu', department: 'Information Technology', register_number: '24ITR001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24itr002', name: 'Aadhiran K', email: 'aadhiran.24itr002@kongu.edu', department: 'Information Technology', register_number: '24ITR002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24itr003', name: 'Ananya S', email: 'ananya.24itr003@kongu.edu', department: 'Information Technology', register_number: '24ITR003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24itr004', name: 'Balaji P', email: 'balaji.24itr004@kongu.edu', department: 'Information Technology', register_number: '24ITR004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24itr005', name: 'Charumathi V', email: 'charumathi.24itr005@kongu.edu', department: 'Information Technology', register_number: '24ITR005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24itr006', name: 'Deepak Raja M', email: 'deepakraja.24itr006@kongu.edu', department: 'Information Technology', register_number: '24ITR006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24itr007', name: 'Dharshini R', email: 'dharshini.24itr007@kongu.edu', department: 'Information Technology', register_number: '24ITR007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24itr008', name: 'Gokul Nath S', email: 'gokulnath.24itr008@kongu.edu', department: 'Information Technology', register_number: '24ITR008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24itr009', name: 'Harini K', email: 'harini.24itr009@kongu.edu', department: 'Information Technology', register_number: '24ITR009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24itr010', name: 'Ishwarya M', email: 'ishwarya.24itr010@kongu.edu', department: 'Information Technology', register_number: '24ITR010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23itr001', name: 'Jeevanandham P', email: 'jeevanandham.23itr001@kongu.edu', department: 'Information Technology', register_number: '23ITR001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23itr002', name: 'Kabilan V', email: 'kabilan.23itr002@kongu.edu', department: 'Information Technology', register_number: '23ITR002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23itr003', name: 'Kavya Dharshini S', email: 'kavya.23itr003@kongu.edu', department: 'Information Technology', register_number: '23ITR003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23itr004', name: 'Keerthana R', email: 'keerthana.23itr004@kongu.edu', department: 'Information Technology', register_number: '23ITR004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23itr005', name: 'Logeshwaran M', email: 'logeshwaran.23itr005@kongu.edu', department: 'Information Technology', register_number: '23ITR005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23itr006', name: 'Madhavan S', email: 'madhavan.23itr006@kongu.edu', department: 'Information Technology', register_number: '23ITR006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23itr007', name: 'Manoj Kumar P', email: 'manoj.23itr007@kongu.edu', department: 'Information Technology', register_number: '23ITR007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23itr008', name: 'Monisha M', email: 'monisha.23itr008@kongu.edu', department: 'Information Technology', register_number: '23ITR008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23itr009', name: 'Nandhini S', email: 'nandhini.23itr009@kongu.edu', department: 'Information Technology', register_number: '23ITR009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23itr010', name: 'Naveen Prasath K', email: 'naveen.23itr010@kongu.edu', department: 'Information Technology', register_number: '23ITR010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22itr001', name: 'Nithish Kumar S', email: 'nithish.22itr001@kongu.edu', department: 'Information Technology', register_number: '22ITR001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22itr002', name: 'Pavithra M', email: 'pavithra.22itr002@kongu.edu', department: 'Information Technology', register_number: '22ITR002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22itr003', name: 'Pranesh R', email: 'pranesh.22itr003@kongu.edu', department: 'Information Technology', register_number: '22ITR003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22itr004', name: 'Priya Dharshini V', email: 'priyadharshini.22itr004@kongu.edu', department: 'Information Technology', register_number: '22ITR004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22itr005', name: 'Rahul M', email: 'rahul.22itr005@kongu.edu', department: 'Information Technology', register_number: '22ITR005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22itr006', name: 'Rithika S', email: 'rithika.22itr006@kongu.edu', department: 'Information Technology', register_number: '22ITR006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22itr007', name: 'Rohith Kumar P', email: 'rohith.22itr007@kongu.edu', department: 'Information Technology', register_number: '22ITR007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22itr008', name: 'Sandhiya R', email: 'sandhiya.22itr008@kongu.edu', department: 'Information Technology', register_number: '22ITR008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22itr009', name: 'Sanjay Ram S', email: 'sanjayram.22itr009@kongu.edu', department: 'Information Technology', register_number: '22ITR009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22itr010', name: 'Saranya P', email: 'saranya.22itr010@kongu.edu', department: 'Information Technology', register_number: '22ITR010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21itr001', name: 'Sathish Kumar R', email: 'sathish.21itr001@kongu.edu', department: 'Information Technology', register_number: '21ITR001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21itr002', name: 'Shobana M', email: 'shobana.21itr002@kongu.edu', department: 'Information Technology', register_number: '21ITR002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21itr003', name: 'Sneha Latha R', email: 'sneha.21itr003@kongu.edu', department: 'Information Technology', register_number: '21ITR003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21itr004', name: 'Sri Hari M', email: 'srihari.21itr004@kongu.edu', department: 'Information Technology', register_number: '21ITR004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21itr005', name: 'Subash Bose R', email: 'subash.21itr005@kongu.edu', department: 'Information Technology', register_number: '21ITR005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21itr006', name: 'Suresh Kumar R', email: 'suresh.21itr006@kongu.edu', department: 'Information Technology', register_number: '21ITR006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21itr007', name: 'Surya Prakash M', email: 'surya.21itr007@kongu.edu', department: 'Information Technology', register_number: '21ITR007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21itr008', name: 'Swetha M', email: 'swetha.21itr008@kongu.edu', department: 'Information Technology', register_number: '21ITR008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21itr009', name: 'Tharun Kumar S', email: 'tharun.21itr009@kongu.edu', department: 'Information Technology', register_number: '21ITR009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21itr010', name: 'Vigneshwaran K', email: 'vignesh.21itr010@kongu.edu', department: 'Information Technology', register_number: '21ITR010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 2. COMPUTER SCIENCE (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24csr001', name: 'Abishek R', email: 'abishek.24csr001@kongu.edu', department: 'Computer Science', register_number: '24CSR001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24csr002', name: 'Akshaya M', email: 'akshaya.24csr002@kongu.edu', department: 'Computer Science', register_number: '24CSR002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24csr003', name: 'Arvind Kumar S', email: 'arvind.24csr003@kongu.edu', department: 'Computer Science', register_number: '24CSR003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24csr004', name: 'Bhavadharani K', email: 'bhavadharani.24csr004@kongu.edu', department: 'Computer Science', register_number: '24CSR004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24csr005', name: 'Chandra Mohan V', email: 'chandramohan.24csr005@kongu.edu', department: 'Computer Science', register_number: '24CSR005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24csr006', name: 'Dhanush S', email: 'dhanush.24csr006@kongu.edu', department: 'Computer Science', register_number: '24CSR006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24csr007', name: 'Divya Bharathi N', email: 'divya.24csr007@kongu.edu', department: 'Computer Science', register_number: '24CSR007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24csr008', name: 'Gowtham Raj P', email: 'gowtham.24csr008@kongu.edu', department: 'Computer Science', register_number: '24CSR008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24csr009', name: 'Hariharan S', email: 'hariharan.24csr009@kongu.edu', department: 'Computer Science', register_number: '24CSR009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24csr010', name: 'Janani P', email: 'janani.24csr010@kongu.edu', department: 'Computer Science', register_number: '24CSR010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23csr001', name: 'Jayanth Kumar S', email: 'jayanth.23csr001@kongu.edu', department: 'Computer Science', register_number: '23CSR001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23csr002', name: 'Kamalesh R', email: 'kamalesh.23csr002@kongu.edu', department: 'Computer Science', register_number: '23CSR002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23csr003', name: 'Kanishka M', email: 'kanishka.23csr003@kongu.edu', department: 'Computer Science', register_number: '23CSR003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23csr004', name: 'Karthick Raja S', email: 'karthick.23csr004@kongu.edu', department: 'Computer Science', register_number: '23CSR004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23csr005', name: 'Kavin Kumar M', email: 'kavin.23csr005@kongu.edu', department: 'Computer Science', register_number: '23CSR005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23csr006', name: 'Kishore Kumar S', email: 'kishore.23csr006@kongu.edu', department: 'Computer Science', register_number: '23CSR006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23csr007', name: 'Madhumitha K', email: 'madhumitha.23csr007@kongu.edu', department: 'Computer Science', register_number: '23CSR007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23csr008', name: 'Mithun R', email: 'mithun.23csr008@kongu.edu', department: 'Computer Science', register_number: '23CSR008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23csr009', name: 'Moulishwaran S', email: 'moulishwaran.23csr009@kongu.edu', department: 'Computer Science', register_number: '23CSR009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23csr010', name: 'Mukilan P', email: 'mukilan.23csr010@kongu.edu', department: 'Computer Science', register_number: '23CSR010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22csr001', name: 'Murali Dharan S', email: 'muralidharan.22csr001@kongu.edu', department: 'Computer Science', register_number: '22CSR001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22csr002', name: 'Muthu Kumar R', email: 'muthukumar.22csr002@kongu.edu', department: 'Computer Science', register_number: '22CSR002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22csr003', name: 'Nithya Shree R', email: 'nithyashree.22csr003@kongu.edu', department: 'Computer Science', register_number: '22CSR003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22csr004', name: 'Pradeepa K', email: 'pradeepa.22csr004@kongu.edu', department: 'Computer Science', register_number: '22CSR004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22csr005', name: 'Prasanna Kumar M', email: 'prasanna.22csr005@kongu.edu', department: 'Computer Science', register_number: '22CSR005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22csr006', name: 'Praveen Raj S', email: 'praveen.22csr006@kongu.edu', department: 'Computer Science', register_number: '22CSR006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22csr007', name: 'Preethi V', email: 'preethi.22csr007@kongu.edu', department: 'Computer Science', register_number: '22CSR007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22csr008', name: 'Ragul S', email: 'ragul.22csr008@kongu.edu', department: 'Computer Science', register_number: '22CSR008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22csr009', name: 'Rajesh Kannan P', email: 'rajesh.22csr009@kongu.edu', department: 'Computer Science', register_number: '22CSR009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22csr010', name: 'Rakshitha S', email: 'rakshitha.22csr010@kongu.edu', department: 'Computer Science', register_number: '22CSR010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21csr001', name: 'Ram Prasath K', email: 'ramprasath.21csr001@kongu.edu', department: 'Computer Science', register_number: '21CSR001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21csr002', name: 'Ramya N', email: 'ramya.21csr002@kongu.edu', department: 'Computer Science', register_number: '21CSR002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21csr003', name: 'Ranjith Kumar M', email: 'ranjith.21csr003@kongu.edu', department: 'Computer Science', register_number: '21CSR003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21csr004', name: 'Sabari Nathan S', email: 'sabari.21csr004@kongu.edu', department: 'Computer Science', register_number: '21CSR004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21csr005', name: 'Sakthi Vel M', email: 'sakthivel.21csr005@kongu.edu', department: 'Computer Science', register_number: '21CSR005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21csr006', name: 'Santhosh Kumar K', email: 'santhosh.21csr006@kongu.edu', department: 'Computer Science', register_number: '21CSR006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21csr007', name: 'Saravanan M', email: 'saravanan.21csr007@kongu.edu', department: 'Computer Science', register_number: '21CSR007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21csr008', name: 'Sasikumar S', email: 'sasikumar.21csr008@kongu.edu', department: 'Computer Science', register_number: '21CSR008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21csr009', name: 'Senthamizh Selvan P', email: 'senthamizh.21csr009@kongu.edu', department: 'Computer Science', register_number: '21CSR009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21csr010', name: 'Sivakumar K', email: 'sivakumar.21csr010@kongu.edu', department: 'Computer Science', register_number: '21CSR010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 3. ELECTRONICS (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24ecr001', name: 'Aadhira P', email: 'aadhira.24ecr001@kongu.edu', department: 'Electronics', register_number: '24ECR001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24ecr002', name: 'Abinaya R', email: 'abinaya.24ecr002@kongu.edu', department: 'Electronics', register_number: '24ECR002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24ecr003', name: 'Ajay Kumar M', email: 'ajay.24ecr003@kongu.edu', department: 'Electronics', register_number: '24ECR003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24ecr004', name: 'Anbarasan T', email: 'anbarasan.24ecr004@kongu.edu', department: 'Electronics', register_number: '24ECR004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24ecr005', name: 'Archana N', email: 'archana.24ecr005@kongu.edu', department: 'Electronics', register_number: '24ECR005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24ecr006', name: 'Boopathi K', email: 'boopathi.24ecr006@kongu.edu', department: 'Electronics', register_number: '24ECR006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24ecr007', name: 'Devanathan S', email: 'devanathan.24ecr007@kongu.edu', department: 'Electronics', register_number: '24ECR007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24ecr008', name: 'Dharani P', email: 'dharani.24ecr008@kongu.edu', department: 'Electronics', register_number: '24ECR008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24ecr009', name: 'Eswaran P', email: 'eswaran.24ecr009@kongu.edu', department: 'Electronics', register_number: '24ECR009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24ecr010', name: 'Gokula Krishnan M', email: 'gokulakrishnan.24ecr010@kongu.edu', department: 'Electronics', register_number: '24ECR010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23ecr001', name: 'Gopika R', email: 'gopika.23ecr001@kongu.edu', department: 'Electronics', register_number: '23ECR001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23ecr002', name: 'Gowri Shankar S', email: 'gowrishankar.23ecr002@kongu.edu', department: 'Electronics', register_number: '23ECR002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23ecr003', name: 'Hari Prasath M', email: 'hariprasath.23ecr003@kongu.edu', department: 'Electronics', register_number: '23ECR003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23ecr004', name: 'Harish Kumar V', email: 'harish.23ecr004@kongu.edu', department: 'Electronics', register_number: '23ECR004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23ecr005', name: 'Hema Malini S', email: 'hemamalini.23ecr005@kongu.edu', department: 'Electronics', register_number: '23ECR005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23ecr006', name: 'Ilango K', email: 'ilango.23ecr006@kongu.edu', department: 'Electronics', register_number: '23ECR006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23ecr007', name: 'Indhumathi R', email: 'indhumathi.23ecr007@kongu.edu', department: 'Electronics', register_number: '23ECR007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23ecr008', name: 'Jagadeesh S', email: 'jagadeesh.23ecr008@kongu.edu', department: 'Electronics', register_number: '23ECR008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23ecr009', name: 'Kalaiarasi S', email: 'kalaiarasi.23ecr009@kongu.edu', department: 'Electronics', register_number: '23ECR009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23ecr010', name: 'Karthiga N', email: 'karthiga.23ecr010@kongu.edu', department: 'Electronics', register_number: '23ECR010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22ecr001', name: 'Kavitha P', email: 'kavitha.22ecr001@kongu.edu', department: 'Electronics', register_number: '22ECR001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22ecr002', name: 'Mahendran R', email: 'mahendran.22ecr002@kongu.edu', department: 'Electronics', register_number: '22ECR002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22ecr003', name: 'Malini V', email: 'malini.22ecr003@kongu.edu', department: 'Electronics', register_number: '22ECR003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22ecr004', name: 'Manicka Vasagam S', email: 'manickavasagam.22ecr004@kongu.edu', department: 'Electronics', register_number: '22ECR004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22ecr005', name: 'Meenakshi S', email: 'meenakshi.22ecr005@kongu.edu', department: 'Electronics', register_number: '22ECR005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22ecr006', name: 'Mohan Raj K', email: 'mohanraj.22ecr006@kongu.edu', department: 'Electronics', register_number: '22ECR006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22ecr007', name: 'Prabu S', email: 'prabu.22ecr007@kongu.edu', department: 'Electronics', register_number: '22ECR007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22ecr008', name: 'Selva Ganapathy M', email: 'selvaganapathy.22ecr008@kongu.edu', department: 'Electronics', register_number: '22ECR008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22ecr009', name: 'Sharmila R', email: 'sharmila.22ecr009@kongu.edu', department: 'Electronics', register_number: '22ECR009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22ecr010', name: 'Shivani S', email: 'shivani.22ecr010@kongu.edu', department: 'Electronics', register_number: '22ECR010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21ecr001', name: 'Soundarya S', email: 'soundarya.21ecr001@kongu.edu', department: 'Electronics', register_number: '21ECR001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21ecr002', name: 'Sreeja P', email: 'sreeja.21ecr002@kongu.edu', department: 'Electronics', register_number: '21ECR002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21ecr003', name: 'Sri Ram S', email: 'sriram.21ecr003@kongu.edu', department: 'Electronics', register_number: '21ECR003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21ecr004', name: 'Sudhakar M', email: 'sudhakar.21ecr004@kongu.edu', department: 'Electronics', register_number: '21ECR004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21ecr005', name: 'Suganya K', email: 'suganya.21ecr005@kongu.edu', department: 'Electronics', register_number: '21ECR005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21ecr006', name: 'Sujith Kumar S', email: 'sujith.21ecr006@kongu.edu', department: 'Electronics', register_number: '21ECR006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21ecr007', name: 'Sumathi P', email: 'sumathi.21ecr007@kongu.edu', department: 'Electronics', register_number: '21ECR007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21ecr008', name: 'Sundar Raj M', email: 'sundarraj.21ecr008@kongu.edu', department: 'Electronics', register_number: '21ECR008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21ecr009', name: 'Surendran S', email: 'surendran.21ecr009@kongu.edu', department: 'Electronics', register_number: '21ECR009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21ecr010', name: 'Tamilarasan P', email: 'tamilarasan.21ecr010@kongu.edu', department: 'Electronics', register_number: '21ECR010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 4. ELECTRICAL (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24eer001', name: 'Aadhavan M', email: 'aadhavan.24eer001@kongu.edu', department: 'Electrical', register_number: '24EER001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24eer002', name: 'Akilan K', email: 'akilan.24eer002@kongu.edu', department: 'Electrical', register_number: '24EER002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24eer003', name: 'Anusuya S', email: 'anusuya.24eer003@kongu.edu', department: 'Electrical', register_number: '24EER003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24eer004', name: 'Balamurugan R', email: 'balamurugan.24eer004@kongu.edu', department: 'Electrical', register_number: '24EER004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24eer005', name: 'Bhuvanesh P', email: 'bhuvanesh.24eer005@kongu.edu', department: 'Electrical', register_number: '24EER005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24eer006', name: 'Chidambaram S', email: 'chidambaram.24eer006@kongu.edu', department: 'Electrical', register_number: '24EER006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24eer007', name: 'Deepan V', email: 'deepan.24eer007@kongu.edu', department: 'Electrical', register_number: '24EER007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24eer008', name: 'Gayathri Devi M', email: 'gayathri.24eer008@kongu.edu', department: 'Electrical', register_number: '24EER008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24eer009', name: 'Gunaseelan P', email: 'gunaseelan.24eer009@kongu.edu', department: 'Electrical', register_number: '24EER009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24eer010', name: 'Hemachandran S', email: 'hemachandran.24eer010@kongu.edu', department: 'Electrical', register_number: '24EER010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23eer001', name: 'Iniyan R', email: 'iniyan.23eer001@kongu.edu', department: 'Electrical', register_number: '23EER001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23eer002', name: 'Jayasurya K', email: 'jayasurya.23eer002@kongu.edu', department: 'Electrical', register_number: '23EER002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23eer003', name: 'Jeevitha S', email: 'jeevitha.23eer003@kongu.edu', department: 'Electrical', register_number: '23EER003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23eer004', name: 'Kalidass M', email: 'kalidass.23eer004@kongu.edu', department: 'Electrical', register_number: '23EER004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23eer005', name: 'Karthi Keyan P', email: 'karthikeyan.23eer005@kongu.edu', department: 'Electrical', register_number: '23EER005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23eer006', name: 'Lavanya R', email: 'lavanya.23eer006@kongu.edu', department: 'Electrical', register_number: '23EER006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23eer007', name: 'Mani Kandan S', email: 'manikandan.23eer007@kongu.edu', department: 'Electrical', register_number: '23EER007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23eer008', name: 'Muruganandam K', email: 'muruganandam.23eer008@kongu.edu', department: 'Electrical', register_number: '23EER008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23eer009', name: 'Nithila P', email: 'nithila.23eer009@kongu.edu', department: 'Electrical', register_number: '23EER009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23eer010', name: 'Palanisamy M', email: 'palanisamy.23eer010@kongu.edu', department: 'Electrical', register_number: '23EER010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22eer001', name: 'Parthiban S', email: 'parthiban.22eer001@kongu.edu', department: 'Electrical', register_number: '22EER001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22eer002', name: 'Poornima R', email: 'poornima.22eer002@kongu.edu', department: 'Electrical', register_number: '22EER002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22eer003', name: 'Prasanth Kumar K', email: 'prasanth.22eer003@kongu.edu', department: 'Electrical', register_number: '22EER003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22eer004', name: 'Rajkumar M', email: 'rajkumar.22eer004@kongu.edu', department: 'Electrical', register_number: '22EER004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22eer005', name: 'Revathi S', email: 'revathi.22eer005@kongu.edu', department: 'Electrical', register_number: '22EER005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22eer006', name: 'Sakthivelan P', email: 'sakthivelan.22eer006@kongu.edu', department: 'Electrical', register_number: '22EER006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22eer007', name: 'Sampath Kumar S', email: 'sampath.22eer007@kongu.edu', department: 'Electrical', register_number: '22EER007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22eer008', name: 'Sangeetha R', email: 'sangeetha.22eer008@kongu.edu', department: 'Electrical', register_number: '22EER008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22eer009', name: 'Senthil Nathan M', email: 'senthilnathan.22eer009@kongu.edu', department: 'Electrical', register_number: '22EER009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22eer010', name: 'Sivaguru K', email: 'sivaguru.22eer010@kongu.edu', department: 'Electrical', register_number: '22EER010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21eer001', name: 'Sridevi P', email: 'sridevi.21eer001@kongu.edu', department: 'Electrical', register_number: '21EER001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21eer002', name: 'Subbiah M', email: 'subbiah.21eer002@kongu.edu', department: 'Electrical', register_number: '21EER002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21eer003', name: 'Thangavel S', email: 'thangavel.21eer003@kongu.edu', department: 'Electrical', register_number: '21EER003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21eer004', name: 'Thennarasu R', email: 'thennarasu.21eer004@kongu.edu', department: 'Electrical', register_number: '21EER004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21eer005', name: 'Umashankar K', email: 'umashankar.21eer005@kongu.edu', department: 'Electrical', register_number: '21EER005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21eer006', name: 'Vadivelan P', email: 'vadivelan.21eer006@kongu.edu', department: 'Electrical', register_number: '21EER006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21eer007', name: 'Varadharajan S', email: 'varadharajan.21eer007@kongu.edu', department: 'Electrical', register_number: '21EER007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21eer008', name: 'Velmurugan M', email: 'velmurugan.21eer008@kongu.edu', department: 'Electrical', register_number: '21EER008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21eer009', name: 'Vijayakumar R', email: 'vijayakumar.21eer009@kongu.edu', department: 'Electrical', register_number: '21EER009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21eer010', name: 'Yogarajan S', email: 'yogarajan.21eer010@kongu.edu', department: 'Electrical', register_number: '21EER010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 5. MECHANICAL (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24mer001', name: 'Aravindhan K', email: 'aravindhan.24mer001@kongu.edu', department: 'Mechanical', register_number: '24MER001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24mer002', name: 'Balamurali S', email: 'balamurali.24mer002@kongu.edu', department: 'Mechanical', register_number: '24MER002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24mer003', name: 'Chandru P', email: 'chandru.24mer003@kongu.edu', department: 'Mechanical', register_number: '24MER003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24mer004', name: 'Deva Raj M', email: 'devaraj.24mer004@kongu.edu', department: 'Mechanical', register_number: '24MER004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24mer005', name: 'Elayaraja R', email: 'elayaraja.24mer005@kongu.edu', department: 'Mechanical', register_number: '24MER005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24mer006', name: 'Gnanasekaran S', email: 'gnanasekaran.24mer006@kongu.edu', department: 'Mechanical', register_number: '24MER006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24mer007', name: 'Guru Prasath K', email: 'guru.24mer007@kongu.edu', department: 'Mechanical', register_number: '24MER007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24mer008', name: 'Harikrishnan M', email: 'harikrishnan.24mer008@kongu.edu', department: 'Mechanical', register_number: '24MER008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24mer009', name: 'Jayaprakash P', email: 'jayaprakash.24mer009@kongu.edu', department: 'Mechanical', register_number: '24MER009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24mer010', name: 'Kamalakannan S', email: 'kamalakannan.24mer010@kongu.edu', department: 'Mechanical', register_number: '24MER010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23mer001', name: 'Karthikeyan R', email: 'karthikeyan.23mer001@kongu.edu', department: 'Mechanical', register_number: '23MER001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23mer002', name: 'Kirubakaran M', email: 'kirubakaran.23mer002@kongu.edu', department: 'Mechanical', register_number: '23MER002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23mer003', name: 'Loganathan K', email: 'loganathan.23mer003@kongu.edu', department: 'Mechanical', register_number: '23MER003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23mer004', name: 'Manikandan P', email: 'manikandan.23mer004@kongu.edu', department: 'Mechanical', register_number: '23MER004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23mer005', name: 'Marimuthu S', email: 'marimuthu.23mer005@kongu.edu', department: 'Mechanical', register_number: '23MER005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23mer006', name: 'Mohanraj R', email: 'mohanraj.23mer006@kongu.edu', department: 'Mechanical', register_number: '23MER006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23mer007', name: 'Murugesan K', email: 'murugesan.23mer007@kongu.edu', department: 'Mechanical', register_number: '23MER007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23mer008', name: 'Nagarajan M', email: 'nagarajan.23mer008@kongu.edu', department: 'Mechanical', register_number: '23MER008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23mer009', name: 'Natarajan P', email: 'natarajan.23mer009@kongu.edu', department: 'Mechanical', register_number: '23MER009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23mer010', name: 'Pandian S', email: 'pandian.23mer010@kongu.edu', department: 'Mechanical', register_number: '23MER010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22mer001', name: 'Perumal R', email: 'perumal.22mer001@kongu.edu', department: 'Mechanical', register_number: '22MER001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22mer002', name: 'Ponnusamy K', email: 'ponnusamy.22mer002@kongu.edu', department: 'Mechanical', register_number: '22MER002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22mer003', name: 'Prakashraj M', email: 'prakashraj.22mer003@kongu.edu', department: 'Mechanical', register_number: '22MER003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22mer004', name: 'Radhakrishnan S', email: 'radhakrishnan.22mer004@kongu.edu', department: 'Mechanical', register_number: '22MER004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22mer005', name: 'Rajadurai P', email: 'rajadurai.22mer005@kongu.edu', department: 'Mechanical', register_number: '22MER005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22mer006', name: 'Ramachandran R', email: 'ramachandran.22mer006@kongu.edu', department: 'Mechanical', register_number: '22MER006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22mer007', name: 'Ramesh Kumar S', email: 'ramesh.22mer007@kongu.edu', department: 'Mechanical', register_number: '22MER007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22mer008', name: 'Rathinavel K', email: 'rathinavel.22mer008@kongu.edu', department: 'Mechanical', register_number: '22MER008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22mer009', name: 'Sakthikumar M', email: 'sakthikumar.22mer009@kongu.edu', department: 'Mechanical', register_number: '22MER009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22mer010', name: 'Saravanakumar P', email: 'saravanakumar.22mer010@kongu.edu', department: 'Mechanical', register_number: '22MER010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21mer001', name: 'Selvakumar S', email: 'selvakumar.21mer001@kongu.edu', department: 'Mechanical', register_number: '21MER001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21mer002', name: 'Senthilkumar R', email: 'senthilkumar.21mer002@kongu.edu', department: 'Mechanical', register_number: '21MER002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21mer003', name: 'Shanmugam K', email: 'shanmugam.21mer003@kongu.edu', department: 'Mechanical', register_number: '21MER003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21mer004', name: 'Silambarasan M', email: 'silambarasan.21mer004@kongu.edu', department: 'Mechanical', register_number: '21MER004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21mer005', name: 'Sivasankaran P', email: 'sivasankaran.21mer005@kongu.edu', department: 'Mechanical', register_number: '21MER005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21mer006', name: 'Subramanian S', email: 'subramanian.21mer006@kongu.edu', department: 'Mechanical', register_number: '21MER006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21mer007', name: 'Thangadurai R', email: 'thangadurai.21mer007@kongu.edu', department: 'Mechanical', register_number: '21MER007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21mer008', name: 'Thirunavukkarasu K', email: 'thirunavukkarasu.21mer008@kongu.edu', department: 'Mechanical', register_number: '21MER008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21mer009', name: 'Vasanthakumar M', email: 'vasanthakumar.21mer009@kongu.edu', department: 'Mechanical', register_number: '21MER009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21mer010', name: 'Vetrivel P', email: 'vetrivel.21mer010@kongu.edu', department: 'Mechanical', register_number: '21MER010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 6. CIVIL (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24cer001', name: 'Anandha Kumar R', email: 'anandhakumar.24cer001@kongu.edu', department: 'Civil', register_number: '24CER001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24cer002', name: 'Ayyappan S', email: 'ayyappan.24cer002@kongu.edu', department: 'Civil', register_number: '24CER002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24cer003', name: 'Bhuvaneswaran K', email: 'bhuvaneswaran.24cer003@kongu.edu', department: 'Civil', register_number: '24CER003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24cer004', name: 'Chelladurai M', email: 'chelladurai.24cer004@kongu.edu', department: 'Civil', register_number: '24CER004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24cer005', name: 'Dhilip Kumar P', email: 'dhilip.24cer005@kongu.edu', department: 'Civil', register_number: '24CER005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24cer006', name: 'Gowrisankar S', email: 'gowrisankar.24cer006@kongu.edu', department: 'Civil', register_number: '24CER006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24cer007', name: 'Hemalatha R', email: 'hemalatha.24cer007@kongu.edu', department: 'Civil', register_number: '24CER007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24cer008', name: 'Ilamporai K', email: 'ilamporai.24cer008@kongu.edu', department: 'Civil', register_number: '24CER008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24cer009', name: 'Jothika M', email: 'jothika.24cer009@kongu.edu', department: 'Civil', register_number: '24CER009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24cer010', name: 'Kalpana P', email: 'kalpana.24cer010@kongu.edu', department: 'Civil', register_number: '24CER010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23cer001', name: 'Kannan S', email: 'kannan.23cer001@kongu.edu', department: 'Civil', register_number: '23CER001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23cer002', name: 'Kowsalya R', email: 'kowsalya.23cer002@kongu.edu', department: 'Civil', register_number: '23CER002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23cer003', name: 'Madheswaran K', email: 'madheswaran.23cer003@kongu.edu', department: 'Civil', register_number: '23CER003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23cer004', name: 'Mohanapriya M', email: 'mohanapriya.23cer004@kongu.edu', department: 'Civil', register_number: '23CER004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23cer005', name: 'Muthulakshmi P', email: 'muthulakshmi.23cer005@kongu.edu', department: 'Civil', register_number: '23CER005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23cer006', name: 'Nagalakshmi S', email: 'nagalakshmi.23cer006@kongu.edu', department: 'Civil', register_number: '23CER006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23cer007', name: 'Narendran R', email: 'narendran.23cer007@kongu.edu', department: 'Civil', register_number: '23CER007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23cer008', name: 'Nithyakalyani K', email: 'nithyakalyani.23cer008@kongu.edu', department: 'Civil', register_number: '23CER008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23cer009', name: 'Palanivel M', email: 'palanivel.23cer009@kongu.edu', department: 'Civil', register_number: '23CER009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23cer010', name: 'Poongodi P', email: 'poongodi.23cer010@kongu.edu', department: 'Civil', register_number: '23CER010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22cer001', name: 'Prabhu Doss S', email: 'prabhudoss.22cer001@kongu.edu', department: 'Civil', register_number: '22CER001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22cer002', name: 'Premnath R', email: 'premnath.22cer002@kongu.edu', department: 'Civil', register_number: '22CER002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22cer003', name: 'Priyanga K', email: 'priyanga.22cer003@kongu.edu', department: 'Civil', register_number: '22CER003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22cer004', name: 'Rajasekar M', email: 'rajasekar.22cer004@kongu.edu', department: 'Civil', register_number: '22CER004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22cer005', name: 'Ranjitham P', email: 'ranjitham.22cer005@kongu.edu', department: 'Civil', register_number: '22CER005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22cer006', name: 'Revathi Devi S', email: 'revathidevi.22cer006@kongu.edu', department: 'Civil', register_number: '22CER006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22cer007', name: 'Sathiyamoorthy R', email: 'sathiyamoorthy.22cer007@kongu.edu', department: 'Civil', register_number: '22CER007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22cer008', name: 'Selvalakshmi K', email: 'selvalakshmi.22cer008@kongu.edu', department: 'Civil', register_number: '22CER008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22cer009', name: 'Sivaranjani M', email: 'sivaranjani.22cer009@kongu.edu', department: 'Civil', register_number: '22CER009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22cer010', name: 'Sornalatha P', email: 'sornalatha.22cer010@kongu.edu', department: 'Civil', register_number: '22CER010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21cer001', name: 'Srinivasan S', email: 'srinivasan.21cer001@kongu.edu', department: 'Civil', register_number: '21CER001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21cer002', name: 'Subashini R', email: 'subashini.21cer002@kongu.edu', department: 'Civil', register_number: '21CER002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21cer003', name: 'Sudha K', email: 'sudha.21cer003@kongu.edu', department: 'Civil', register_number: '21CER003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21cer004', name: 'Sundaresan M', email: 'sundaresan.21cer004@kongu.edu', department: 'Civil', register_number: '21CER004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21cer005', name: 'Tamilarasi P', email: 'tamilarasi.21cer005@kongu.edu', department: 'Civil', register_number: '21CER005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21cer006', name: 'Thilagavathi S', email: 'thilagavathi.21cer006@kongu.edu', department: 'Civil', register_number: '21CER006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21cer007', name: 'Uma Devi R', email: 'umadevi.21cer007@kongu.edu', department: 'Civil', register_number: '21CER007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21cer008', name: 'Vasanthi K', email: 'vasanthi.21cer008@kongu.edu', department: 'Civil', register_number: '21CER008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21cer009', name: 'Vijayalakshmi M', email: 'vijayalakshmi.21cer009@kongu.edu', department: 'Civil', register_number: '21CER009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21cer010', name: 'Vinothini P', email: 'vinothini.21cer010@kongu.edu', department: 'Civil', register_number: '21CER010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 7. CHEMICAL (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24chr001', name: 'Aarthi S', email: 'aarthi.24chr001@kongu.edu', department: 'Chemical', register_number: '24CHR001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24chr002', name: 'Bharathi Raja K', email: 'bharathiraja.24chr002@kongu.edu', department: 'Chemical', register_number: '24CHR002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24chr003', name: 'Chitra Devi M', email: 'chitradevi.24chr003@kongu.edu', department: 'Chemical', register_number: '24CHR003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24chr004', name: 'Dharuman P', email: 'dharuman.24chr004@kongu.edu', department: 'Chemical', register_number: '24CHR004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24chr005', name: 'Geethanjali R', email: 'geethanjali.24chr005@kongu.edu', department: 'Chemical', register_number: '24CHR005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24chr006', name: 'Haripriya S', email: 'haripriya.24chr006@kongu.edu', department: 'Chemical', register_number: '24CHR006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24chr007', name: 'Indhira K', email: 'indhira.24chr007@kongu.edu', department: 'Chemical', register_number: '24CHR007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24chr008', name: 'Janarthanan M', email: 'janarthanan.24chr008@kongu.edu', department: 'Chemical', register_number: '24CHR008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24chr009', name: 'Kiruthika P', email: 'kiruthika.24chr009@kongu.edu', department: 'Chemical', register_number: '24CHR009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24chr010', name: 'Lavanyashree R', email: 'lavanyashree.24chr010@kongu.edu', department: 'Chemical', register_number: '24CHR010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23chr001', name: 'Mahesh Kumar S', email: 'mahesh.23chr001@kongu.edu', department: 'Chemical', register_number: '23CHR001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23chr002', name: 'Nandhagopal K', email: 'nandhagopal.23chr002@kongu.edu', department: 'Chemical', register_number: '23CHR002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23chr003', name: 'Pavithran M', email: 'pavithran.23chr003@kongu.edu', department: 'Chemical', register_number: '23CHR003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23chr004', name: 'Radhakumari P', email: 'radhakumari.23chr004@kongu.edu', department: 'Chemical', register_number: '23CHR004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23chr005', name: 'Rajendran S', email: 'rajendran.23chr005@kongu.edu', department: 'Chemical', register_number: '23CHR005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23chr006', name: 'Reshma R', email: 'reshma.23chr006@kongu.edu', department: 'Chemical', register_number: '23CHR006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23chr007', name: 'Sabareesh K', email: 'sabareesh.23chr007@kongu.edu', department: 'Chemical', register_number: '23CHR007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23chr008', name: 'Sakthidevi M', email: 'sakthidevi.23chr008@kongu.edu', department: 'Chemical', register_number: '23CHR008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23chr009', name: 'Sangeeth Kumar P', email: 'sangeeth.23chr009@kongu.edu', department: 'Chemical', register_number: '23CHR009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23chr010', name: 'Saraswathi S', email: 'saraswathi.23chr010@kongu.edu', department: 'Chemical', register_number: '23CHR010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22chr001', name: 'Sasirekha R', email: 'sasirekha.22chr001@kongu.edu', department: 'Chemical', register_number: '22CHR001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22chr002', name: 'Sathyanarayanan K', email: 'sathyanarayanan.22chr002@kongu.edu', department: 'Chemical', register_number: '22CHR002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22chr003', name: 'Shanmugapriya M', email: 'shanmugapriya.22chr003@kongu.edu', department: 'Chemical', register_number: '22CHR003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22chr004', name: 'Sivakumar P', email: 'sivakumar.22chr004@kongu.edu', department: 'Chemical', register_number: '22CHR004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22chr005', name: 'Sowmiya S', email: 'sowmiya.22chr005@kongu.edu', department: 'Chemical', register_number: '22CHR005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22chr006', name: 'Subathra R', email: 'subathra.22chr006@kongu.edu', department: 'Chemical', register_number: '22CHR006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22chr007', name: 'Sudharshan K', email: 'sudharshan.22chr007@kongu.edu', department: 'Chemical', register_number: '22CHR007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22chr008', name: 'Suganthi M', email: 'suganthi.22chr008@kongu.edu', department: 'Chemical', register_number: '22CHR008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22chr009', name: 'Sundaram P', email: 'sundaram.22chr009@kongu.edu', department: 'Chemical', register_number: '22CHR009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22chr010', name: 'Swarnalatha S', email: 'swarnalatha.22chr010@kongu.edu', department: 'Chemical', register_number: '22CHR010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21chr001', name: 'Thangamariappan R', email: 'thangamariappan.21chr001@kongu.edu', department: 'Chemical', register_number: '21CHR001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21chr002', name: 'Thenral K', email: 'thenral.21chr002@kongu.edu', department: 'Chemical', register_number: '21CHR002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21chr003', name: 'Usharani M', email: 'usharani.21chr003@kongu.edu', department: 'Chemical', register_number: '21CHR003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21chr004', name: 'Vanathi P', email: 'vanathi.21chr004@kongu.edu', department: 'Chemical', register_number: '21CHR004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21chr005', name: 'Vasanthakumar S', email: 'vasanthakumar.21chr005@kongu.edu', department: 'Chemical', register_number: '21CHR005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21chr006', name: 'Vengatachalapathy R', email: 'vengatachalapathy.21chr006@kongu.edu', department: 'Chemical', register_number: '21CHR006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21chr007', name: 'Vigneswaran K', email: 'vigneswaran.21chr007@kongu.edu', department: 'Chemical', register_number: '21CHR007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21chr008', name: 'Vinithra M', email: 'vinithra.21chr008@kongu.edu', department: 'Chemical', register_number: '21CHR008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21chr009', name: 'Viswanathan P', email: 'viswanathan.21chr009@kongu.edu', department: 'Chemical', register_number: '21CHR009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21chr010', name: 'Yuvarani S', email: 'yuvarani.21chr010@kongu.edu', department: 'Chemical', register_number: '21CHR010', year: 4, section: 'B', role: 'student', is_active: true },

  // ==========================================
  // 8. BIOTECHNOLOGY (40 Students)
  // ==========================================
  // Year 1 (10 Students)
  { id: 'std-24btr001', name: 'Anbumozhi S', email: 'anbumozhi.24btr001@kongu.edu', department: 'Biotechnology', register_number: '24BTR001', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24btr002', name: 'Balamurugan K', email: 'balamurugan.24btr002@kongu.edu', department: 'Biotechnology', register_number: '24BTR002', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24btr003', name: 'Chandralekha M', email: 'chandralekha.24btr003@kongu.edu', department: 'Biotechnology', register_number: '24BTR003', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24btr004', name: 'Deivayanai P', email: 'deivayanai.24btr004@kongu.edu', department: 'Biotechnology', register_number: '24BTR004', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24btr005', name: 'Gokila R', email: 'gokila.24btr005@kongu.edu', department: 'Biotechnology', register_number: '24BTR005', year: 1, section: 'A', role: 'student', is_active: true },
  { id: 'std-24btr006', name: 'Hemavathy S', email: 'hemavathy.24btr006@kongu.edu', department: 'Biotechnology', register_number: '24BTR006', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24btr007', name: 'Jayashree K', email: 'jayashree.24btr007@kongu.edu', department: 'Biotechnology', register_number: '24BTR007', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24btr008', name: 'Kanimozhi M', email: 'kanimozhi.24btr008@kongu.edu', department: 'Biotechnology', register_number: '24BTR008', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24btr009', name: 'Logapriya P', email: 'logapriya.24btr009@kongu.edu', department: 'Biotechnology', register_number: '24BTR009', year: 1, section: 'B', role: 'student', is_active: true },
  { id: 'std-24btr010', name: 'Madhumalar R', email: 'madhumalar.24btr010@kongu.edu', department: 'Biotechnology', register_number: '24BTR010', year: 1, section: 'B', role: 'student', is_active: true },
  // Year 2 (10 Students)
  { id: 'std-23btr001', name: 'Malarvizhi S', email: 'malarvizhi.23btr001@kongu.edu', department: 'Biotechnology', register_number: '23BTR001', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23btr002', name: 'Menaka K', email: 'menaka.23btr002@kongu.edu', department: 'Biotechnology', register_number: '23BTR002', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23btr003', name: 'Nithyashree M', email: 'nithyashree.23btr003@kongu.edu', department: 'Biotechnology', register_number: '23BTR003', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23btr004', name: 'Pavalakodi P', email: 'pavalakodi.23btr004@kongu.edu', department: 'Biotechnology', register_number: '23BTR004', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23btr005', name: 'Priyadharshini R', email: 'priyadharshini.23btr005@kongu.edu', department: 'Biotechnology', register_number: '23BTR005', year: 2, section: 'A', role: 'student', is_active: true },
  { id: 'std-23btr006', name: 'Rajakumari S', email: 'rajakumari.23btr006@kongu.edu', department: 'Biotechnology', register_number: '23BTR006', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23btr007', name: 'Revathisri K', email: 'revathisri.23btr007@kongu.edu', department: 'Biotechnology', register_number: '23BTR007', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23btr008', name: 'Sakthipriya M', email: 'sakthipriya.23btr008@kongu.edu', department: 'Biotechnology', register_number: '23BTR008', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23btr009', name: 'Sathiyapriya P', email: 'sathiyapriya.23btr009@kongu.edu', department: 'Biotechnology', register_number: '23BTR009', year: 2, section: 'B', role: 'student', is_active: true },
  { id: 'std-23btr010', name: 'Selvapriya S', email: 'selvapriya.23btr010@kongu.edu', department: 'Biotechnology', register_number: '23BTR010', year: 2, section: 'B', role: 'student', is_active: true },
  // Year 3 (10 Students)
  { id: 'std-22btr001', name: 'Sharmiladevi R', email: 'sharmiladevi.22btr001@kongu.edu', department: 'Biotechnology', register_number: '22BTR001', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22btr002', name: 'Sivapriya K', email: 'sivapriya.22btr002@kongu.edu', department: 'Biotechnology', register_number: '22BTR002', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22btr003', name: 'Soundharavalli M', email: 'soundharavalli.22btr003@kongu.edu', department: 'Biotechnology', register_number: '22BTR003', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22btr004', name: 'Sripriya P', email: 'sripriya.22btr004@kongu.edu', department: 'Biotechnology', register_number: '22BTR004', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22btr005', name: 'Subhasri S', email: 'subhasri.22btr005@kongu.edu', department: 'Biotechnology', register_number: '22BTR005', year: 3, section: 'A', role: 'student', is_active: true },
  { id: 'std-22btr006', name: 'Sudharsana R', email: 'sudharsana.22btr006@kongu.edu', department: 'Biotechnology', register_number: '22BTR006', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22btr007', name: 'Sugashini K', email: 'sugashini.22btr007@kongu.edu', department: 'Biotechnology', register_number: '22BTR007', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22btr008', name: 'Tamilselvi M', email: 'tamilselvi.22btr008@kongu.edu', department: 'Biotechnology', register_number: '22BTR008', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22btr009', name: 'Thenmozhi P', email: 'thenmozhi.22btr009@kongu.edu', department: 'Biotechnology', register_number: '22BTR009', year: 3, section: 'B', role: 'student', is_active: true },
  { id: 'std-22btr010', name: 'Udhayapriya S', email: 'udhayapriya.22btr010@kongu.edu', department: 'Biotechnology', register_number: '22BTR010', year: 3, section: 'B', role: 'student', is_active: true },
  // Year 4 (10 Students)
  { id: 'std-21btr001', name: 'Valliammai R', email: 'valliammai.21btr001@kongu.edu', department: 'Biotechnology', register_number: '21BTR001', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21btr002', name: 'Vanishree K', email: 'vanishree.21btr002@kongu.edu', department: 'Biotechnology', register_number: '21BTR002', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21btr003', name: 'Vasundhara M', email: 'vasundhara.21btr003@kongu.edu', department: 'Biotechnology', register_number: '21BTR003', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21btr004', name: 'Vennila P', email: 'vennila.21btr004@kongu.edu', department: 'Biotechnology', register_number: '21BTR004', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21btr005', name: 'Vidhyasri S', email: 'vidhyasri.21btr005@kongu.edu', department: 'Biotechnology', register_number: '21BTR005', year: 4, section: 'A', role: 'student', is_active: true },
  { id: 'std-21btr006', name: 'Vijayapriya R', email: 'vijayapriya.21btr006@kongu.edu', department: 'Biotechnology', register_number: '21BTR006', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21btr007', name: 'Vimalasri K', email: 'vimalasri.21btr007@kongu.edu', department: 'Biotechnology', register_number: '21BTR007', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21btr008', name: 'Vinodhaprabha M', email: 'vinodhaprabha.21btr008@kongu.edu', department: 'Biotechnology', register_number: '21BTR008', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21btr009', name: 'Yamunadevi P', email: 'yamunadevi.21btr009@kongu.edu', department: 'Biotechnology', register_number: '21BTR009', year: 4, section: 'B', role: 'student', is_active: true },
  { id: 'std-21btr010', name: 'Yuvasri S', email: 'yuvasri.21btr010@kongu.edu', department: 'Biotechnology', register_number: '21BTR010', year: 4, section: 'B', role: 'student', is_active: true },
];

