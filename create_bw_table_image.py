import os
from PIL import Image, ImageDraw, ImageFont

def create_bw_table_image(output_path):
    # Dimensions
    width = 1200
    height = 680
    
    # Pure white background
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Fonts - Academic Times New Roman or Arial
    font_serif = "C:/Windows/Fonts/times.ttf" if os.path.exists("C:/Windows/Fonts/times.ttf") else "C:/Windows/Fonts/arial.ttf"
    font_serif_b = "C:/Windows/Fonts/timesbd.ttf" if os.path.exists("C:/Windows/Fonts/timesbd.ttf") else "C:/Windows/Fonts/arialbd.ttf"
    
    font_caption = ImageFont.truetype(font_serif_b, 22)
    font_subcaption = ImageFont.truetype(font_serif, 15)
    font_th = ImageFont.truetype(font_serif_b, 20)
    font_td_title = ImageFont.truetype(font_serif_b, 18)
    font_td_sub = ImageFont.truetype(font_serif, 15)
    
    # Table layout
    table_x = 100
    table_w = width - (table_x * 2) # 1000
    col_w = table_w // 2 # 500 each
    
    start_y = 110
    th_h = 55
    row_h = 85
    
    # Caption (Academic table style)
    draw.text((table_x, 45), "Table 1: System Technology Stack Specification", fill=(0, 0, 0), font=font_caption)
    draw.text((table_x, 75), "Clubs and Cells Management System (ClubHub) — Architecture Components", fill=(60, 60, 60), font=font_subcaption)
    
    # Table Header Row
    # Top rule (thick 2.5px)
    draw.line([(table_x, start_y), (table_x + table_w, start_y)], fill=(0, 0, 0), width=3)
    
    # Light gray header background
    draw.rectangle([(table_x, start_y + 3), (table_x + table_w, start_y + th_h)], fill=(245, 245, 245))
    
    # Header vertical divider
    draw.line([(table_x + col_w, start_y), (table_x + col_w, start_y + th_h)], fill=(0, 0, 0), width=1)
    # Header outer vertical borders
    draw.line([(table_x, start_y), (table_x, start_y + th_h)], fill=(0, 0, 0), width=2)
    draw.line([(table_x + table_w, start_y), (table_x + table_w, start_y + th_h)], fill=(0, 0, 0), width=2)
    
    # Header texts
    draw.text((table_x + 30, start_y + 16), "Frontend (Client-Side)", fill=(0, 0, 0), font=font_th)
    draw.text((table_x + col_w + 30, start_y + 16), "Backend & Infrastructure", fill=(0, 0, 0), font=font_th)
    
    # Mid rule below header
    mid_y = start_y + th_h
    draw.line([(table_x, mid_y), (table_x + table_w, mid_y)], fill=(0, 0, 0), width=2)
    
    # 5 Data rows
    rows_data = [
        (("1. React 18", "Component-driven single page application"),
         ("1. Supabase (BaaS)", "Managed cloud backend suite & REST APIs")),
        
        (("2. TypeScript 5", "Static type-safety & compile-time verification"),
         ("2. PostgreSQL", "Relational database with Row-Level Security (RLS)")),
         
        (("3. Tailwind CSS 3", "Utility-first design with Wikipedia theme layout"),
         ("3. Supabase Auth (JWT)", "Role-based access (Admin, Faculty, Lead, Student)")),
         
        (("4. Vite 5", "High-speed bundling & development build engine"),
         ("4. Supabase Storage", "Cloud object storage for user avatars & certificates")),
         
        (("5. React Router & Recharts", "Client routing & interactive participation charts"),
         ("5. Node.js & Batch CLI", "Offline terminal administration console & launcher"))
    ]
    
    for i, (f_data, b_data) in enumerate(rows_data):
        curr_y = mid_y + (i * row_h)
        next_y = curr_y + row_h
        
        # Row alternate subtle fill or pure white
        # Pure academic: white with clean borders
        draw.rectangle([(table_x, curr_y), (table_x + table_w, next_y)], fill=(255, 255, 255))
        
        # Vertical borders
        draw.line([(table_x, curr_y), (table_x, next_y)], fill=(0, 0, 0), width=2)
        draw.line([(table_x + col_w, curr_y), (table_x + col_w, next_y)], fill=(0, 0, 0), width=1)
        draw.line([(table_x + table_w, curr_y), (table_x + table_w, next_y)], fill=(0, 0, 0), width=2)
        
        # Horizontal row divider (1px)
        if i < 4:
            draw.line([(table_x, next_y), (table_x + table_w, next_y)], fill=(180, 180, 180), width=1)
            
        # Left (Frontend) cell content
        draw.text((table_x + 30, curr_y + 18), f_data[0], fill=(0, 0, 0), font=font_td_title)
        draw.text((table_x + 30, curr_y + 46), f_data[1], fill=(70, 70, 70), font=font_td_sub)
        
        # Right (Backend) cell content
        draw.text((table_x + col_w + 30, curr_y + 18), b_data[0], fill=(0, 0, 0), font=font_td_title)
        draw.text((table_x + col_w + 30, curr_y + 46), b_data[1], fill=(70, 70, 70), font=font_td_sub)

    # Bottom rule (thick 2.5px)
    bottom_y = mid_y + (5 * row_h)
    draw.line([(table_x, bottom_y), (table_x + table_w, bottom_y)], fill=(0, 0, 0), width=3)
    
    # Footer note
    draw.text((table_x, bottom_y + 18), "Note: Designed for Kongu Engineering College (Autonomous) — IT Department DSP Project.", fill=(90, 90, 90), font=font_subcaption)

    # Save
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", quality=100)
    print(f"B&W Table generated: {output_path}")

if __name__ == "__main__":
    out1 = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/Clubs and cells Management System/assets/tech_stack_table_bw.png"
    out2 = "C:/Users/ELCOT/.gemini/antigravity/brain/5847d047-8608-4f3f-8443-8cf060e261e2/tech_stack_table_bw.png"
    create_bw_table_image(out1)
    create_bw_table_image(out2)

