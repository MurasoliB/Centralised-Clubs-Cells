import os
from PIL import Image, ImageDraw, ImageFont

def create_tech_stack_infographic(output_path):
    # Canvas dimensions
    width = 1600
    height = 1080
    
    # Create image with high-quality background
    img = Image.new("RGBA", (width, height), (248, 250, 252, 255)) # slate-50
    draw = ImageDraw.Draw(img)
    
    # Fonts
    font_path_regular = "C:/Windows/Fonts/segoeui.ttf" if os.path.exists("C:/Windows/Fonts/segoeui.ttf") else "C:/Windows/Fonts/arial.ttf"
    font_path_bold = "C:/Windows/Fonts/segoeuib.ttf" if os.path.exists("C:/Windows/Fonts/segoeuib.ttf") else "C:/Windows/Fonts/arialbd.ttf"
    font_path_semibold = "C:/Windows/Fonts/seguisb.ttf" if os.path.exists("C:/Windows/Fonts/seguisb.ttf") else font_path_bold
    
    font_sup = ImageFont.truetype(font_path_bold, 18)
    font_title = ImageFont.truetype(font_path_bold, 40)
    font_subtitle = ImageFont.truetype(font_path_regular, 20)
    
    font_col_header = ImageFont.truetype(font_path_bold, 24)
    font_col_badge = ImageFont.truetype(font_path_bold, 14)
    
    font_item_num = ImageFont.truetype(font_path_bold, 18)
    font_item_title = ImageFont.truetype(font_path_bold, 22)
    font_item_tag = ImageFont.truetype(font_path_semibold, 13)
    font_item_desc = ImageFont.truetype(font_path_regular, 16)
    font_footer = ImageFont.truetype(font_path_semibold, 15)
    
    # 1. Header Background Banner
    draw.rectangle([(0, 0), (width, 170)], fill=(15, 23, 42, 255)) # slate-900
    draw.line([(0, 170), (width, 170)], fill=(30, 41, 59, 255), width=2)
    
    # Accent top border
    draw.rectangle([(0, 0), (width, 6)], fill=(37, 99, 235, 255)) # blue-600
    
    # Header Text
    draw.text((80, 28), "KONGU ENGINEERING COLLEGE (AUTONOMOUS)  •  DEPARTMENT OF IT", fill=(148, 163, 184, 255), font=font_sup)
    draw.text((80, 58), "ClubHub — Technology Stack Architecture", fill=(255, 255, 255, 255), font=font_title)
    draw.text((80, 115), "Modern 2-Tier Extracurricular Management & Verified Certification Ecosystem", fill=(203, 213, 225, 255), font=font_subtitle)
    
    # College Badge on Header Right
    badge_w, badge_h = 240, 48
    badge_x = width - 80 - badge_w
    badge_y = 62
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=6, fill=(30, 41, 59, 255), outline=(51, 65, 85, 255), width=1)
    draw.text((badge_x + 22, badge_y + 14), "AY 2026–2027  •  PORTAL", fill=(56, 189, 248, 255), font=font_sup)
    
    # Column configuration
    col_w = 690
    gap = 60
    left_x = 80
    right_x = left_x + col_w + gap
    start_y = 205
    
    # 2. Left Column Header (Frontend)
    # Header card
    draw.rounded_rectangle([(left_x, start_y), (left_x + col_w, start_y + 60)], radius=8, fill=(239, 246, 255, 255), outline=(191, 219, 254, 255), width=2)
    draw.rectangle([(left_x, start_y), (left_x + 8, start_y + 60)], fill=(37, 99, 235, 255)) # blue strip
    draw.text((left_x + 25, start_y + 16), "1. FRONTEND ARCHITECTURE", fill=(30, 58, 138, 255), font=font_col_header)
    # Badge
    fb_w = 110
    draw.rounded_rectangle([(left_x + col_w - fb_w - 20, start_y + 16), (left_x + col_w - 20, start_y + 44)], radius=4, fill=(219, 234, 254, 255))
    draw.text((left_x + col_w - fb_w - 10, start_y + 22), "5 COMPONENTS", fill=(29, 78, 216, 255), font=font_col_badge)
    
    # 3. Right Column Header (Backend)
    draw.rounded_rectangle([(right_x, start_y), (right_x + col_w, start_y + 60)], radius=8, fill=(240, 253, 244, 255), outline=(187, 247, 208, 255), width=2)
    draw.rectangle([(right_x, start_y), (right_x + 8, start_y + 60)], fill=(16, 185, 129, 255)) # emerald strip
    draw.text((right_x + 25, start_y + 16), "2. BACKEND & INFRASTRUCTURE", fill=(6, 78, 59, 255), font=font_col_header)
    # Badge
    bb_w = 110
    draw.rounded_rectangle([(right_x + col_w - bb_w - 20, start_y + 16), (right_x + col_w - 20, start_y + 44)], radius=4, fill=(220, 252, 231, 255))
    draw.text((right_x + col_w - bb_w - 10, start_y + 22), "5 COMPONENTS", fill=(4, 120, 87, 255), font=font_col_badge)
    
    # 4. Frontend 5 Items
    frontend_items = [
        ("React 18", "UI Library", "Component-driven reactive single-page architecture & virtual DOM updates", (37, 99, 235)),
        ("TypeScript 5", "Language", "Statically typed safety, strict contracts, and zero-runtime type errors", (14, 116, 144)),
        ("Tailwind CSS 3", "Styling & Theme", "Utility-first design engine styled with classic Wikipedia Vector theme", (2, 132, 199)),
        ("Vite 5", "Build Tool", "Lightning-fast ES modules development server & optimized production rollup", (124, 58, 237)),
        ("React Router & Recharts", "Navigation & Analytics", "Client-side declarative routing and interactive attendance/roster metrics", (79, 70, 229))
    ]
    
    # 5. Backend 5 Items
    backend_items = [
        ("Supabase (BaaS)", "Cloud Platform", "Managed backend suite providing auto-generated REST APIs & real-time sync", (5, 150, 105)),
        ("PostgreSQL", "Database", "ACID-compliant relational database protected by Row-Level Security (RLS)", (13, 148, 136)),
        ("Supabase Auth (JWT)", "Security & RBAC", "Token authentication enforcing 4 distinct roles: Admin, Faculty, Lead, Student", (16, 185, 129)),
        ("Supabase Storage", "Object Storage", "High-throughput cloud storage buckets for student avatars & certificates", (22, 163, 74)),
        ("Node.js & Batch CLI", "Tooling & Shell", "Interactive offline terminal management console and 1-click portal launcher", (71, 85, 105))
    ]
    
    row_y = start_y + 80
    row_h = 135
    row_gap = 14
    
    for i in range(5):
        curr_y = row_y + i * (row_h + row_gap)
        
        # --- Draw Frontend Card ---
        draw.rounded_rectangle([(left_x, curr_y), (left_x + col_w, curr_y + row_h)], radius=8, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        # Left accent pip
        draw.rounded_rectangle([(left_x + 16, curr_y + 18), (left_x + 50, curr_y + 52)], radius=6, fill=(239, 246, 255, 255), outline=(191, 219, 254, 255), width=1)
        draw.text((left_x + 28, curr_y + 24), str(i + 1), fill=(37, 99, 235, 255), font=font_item_num)
        
        # Title
        f_title, f_tag, f_desc, f_color = frontend_items[i]
        draw.text((left_x + 65, curr_y + 22), f_title, fill=(15, 23, 42, 255), font=font_item_title)
        
        # Tag pill
        tag_bbox = draw.textbbox((0, 0), f_tag, font=font_item_tag)
        tag_w = tag_bbox[2] - tag_bbox[0] + 16
        draw.rounded_rectangle([(left_x + col_w - tag_w - 20, curr_y + 22), (left_x + col_w - 20, curr_y + 46)], radius=4, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=1)
        draw.text((left_x + col_w - tag_w - 12, curr_y + 26), f_tag, fill=(71, 85, 105, 255), font=font_item_tag)
        
        # Separator line
        draw.line([(left_x + 65, curr_y + 62), (left_x + col_w - 20, curr_y + 62)], fill=(241, 245, 249, 255), width=1)
        
        # Description
        draw.text((left_x + 65, curr_y + 76), f_desc, fill=(100, 116, 139, 255), font=font_item_desc)
        
        
        # --- Draw Backend Card ---
        draw.rounded_rectangle([(right_x, curr_y), (right_x + col_w, curr_y + row_h)], radius=8, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        # Left accent pip
        draw.rounded_rectangle([(right_x + 16, curr_y + 18), (right_x + 50, curr_y + 52)], radius=6, fill=(240, 253, 244, 255), outline=(187, 247, 208, 255), width=1)
        draw.text((right_x + 28, curr_y + 24), str(i + 1), fill=(16, 185, 129, 255), font=font_item_num)
        
        # Title
        b_title, b_tag, b_desc, b_color = backend_items[i]
        draw.text((right_x + 65, curr_y + 22), b_title, fill=(15, 23, 42, 255), font=font_item_title)
        
        # Tag pill
        btag_bbox = draw.textbbox((0, 0), b_tag, font=font_item_tag)
        btag_w = btag_bbox[2] - btag_bbox[0] + 16
        draw.rounded_rectangle([(right_x + col_w - btag_w - 20, curr_y + 22), (right_x + col_w - 20, curr_y + 46)], radius=4, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=1)
        draw.text((right_x + col_w - btag_w - 12, curr_y + 26), b_tag, fill=(71, 85, 105, 255), font=font_item_tag)
        
        # Separator line
        draw.line([(right_x + 65, curr_y + 62), (right_x + col_w - 20, curr_y + 62)], fill=(241, 245, 249, 255), width=1)
        
        # Description
        draw.text((right_x + 65, curr_y + 76), b_desc, fill=(100, 116, 139, 255), font=font_item_desc)

    # 6. Bottom Information Bar
    foot_y = height - 55
    draw.rectangle([(0, foot_y), (width, height)], fill=(241, 245, 249, 255))
    draw.line([(0, foot_y), (width, foot_y)], fill=(226, 232, 240, 255), width=1)
    
    draw.text((80, foot_y + 18), "Kongu Engineering College  •  Design Thinking & Systems Project (DSP)", fill=(71, 85, 105, 255), font=font_footer)
    draw.text((width - 430, foot_y + 18), "Full-Stack Web Architecture  •  Production Ready", fill=(100, 116, 139, 255), font=font_footer)

    # Save to disk
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out1 = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/Clubs and cells Management System/assets/tech_stack.png"
    out2 = "C:/Users/ELCOT/.gemini/antigravity/brain/5847d047-8608-4f3f-8443-8cf060e261e2/tech_stack.png"
    create_tech_stack_infographic(out1)
    create_tech_stack_infographic(out2)

