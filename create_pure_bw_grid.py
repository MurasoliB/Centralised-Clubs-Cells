import os
from PIL import Image, ImageDraw, ImageFont

def create_pure_bw_grid(output_path):
    width = 1100
    height = 560
    
    # Pure white canvas
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_serif = "C:/Windows/Fonts/times.ttf" if os.path.exists("C:/Windows/Fonts/times.ttf") else "C:/Windows/Fonts/arial.ttf"
    font_serif_b = "C:/Windows/Fonts/timesbd.ttf" if os.path.exists("C:/Windows/Fonts/timesbd.ttf") else "C:/Windows/Fonts/arialbd.ttf"
    
    font_title = ImageFont.truetype(font_serif_b, 20)
    font_th = ImageFont.truetype(font_serif_b, 19)
    font_td_name = ImageFont.truetype(font_serif_b, 17)
    font_td_detail = ImageFont.truetype(font_serif, 14)
    
    # Table bounds
    tx = 60
    tw = width - (tx * 2) # 980
    cw = tw // 2 # 490
    ty = 60
    th_h = 50
    row_h = 75
    
    # Title
    draw.text((tx, 25), "TECH STACK SPECIFICATION (FRONTEND & BACKEND)", fill=(0, 0, 0), font=font_title)
    
    # Outer rectangle
    total_h = th_h + (5 * row_h)
    draw.rectangle([(tx, ty), (tx + tw, ty + total_h)], outline=(0, 0, 0), width=2)
    
    # Header bottom divider
    draw.line([(tx, ty + th_h), (tx + tw, ty + th_h)], fill=(0, 0, 0), width=2)
    
    # Middle vertical line
    draw.line([(tx + cw, ty), (tx + cw, ty + total_h)], fill=(0, 0, 0), width=2)
    
    # Header text
    draw.text((tx + 25, ty + 15), "FRONTEND", fill=(0, 0, 0), font=font_th)
    draw.text((tx + cw + 25, ty + 15), "BACKEND", fill=(0, 0, 0), font=font_th)
    
    rows = [
        (("1. React 18", "Component-based single-page UI architecture"),
         ("1. Supabase (BaaS)", "Managed cloud backend suite & real-time APIs")),
        
        (("2. TypeScript 5", "Static type-safety and compile-time verification"),
         ("2. PostgreSQL", "Relational database with Row-Level Security")),
        
        (("3. Tailwind CSS 3", "Utility-first styling & responsive layouts"),
         ("3. Supabase Auth", "JWT token authentication & role management")),
        
        (("4. Vite 5", "High-speed bundling & development build engine"),
         ("4. Supabase Storage", "Cloud storage buckets for avatars & certificates")),
        
        (("5. React Router & Recharts", "Client-side routing & interactive analytics charts"),
         ("5. Node.js & Batch Script", "Offline CLI terminal console & 1-click launcher"))
    ]
    
    for i, (f, b) in enumerate(rows):
        cy = ty + th_h + (i * row_h)
        ny = cy + row_h
        
        # Horizontal row line
        if i > 0:
            draw.line([(tx, cy), (tx + tw, cy)], fill=(0, 0, 0), width=1)
            
        # Left cell
        draw.text((tx + 25, cy + 16), f[0], fill=(0, 0, 0), font=font_td_name)
        draw.text((tx + 25, cy + 42), f[1], fill=(40, 40, 40), font=font_td_detail)
        
        # Right cell
        draw.text((tx + cw + 25, cy + 16), b[0], fill=(0, 0, 0), font=font_td_name)
        draw.text((tx + cw + 25, cy + 42), b[1], fill=(40, 40, 40), font=font_td_detail)
        
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG", quality=100)
    print(f"Pure B&W Grid generated: {output_path}")

if __name__ == "__main__":
    out1 = "c:/MY DRIVE/15/KEC IT/Subjects/Lab Experiments/Design Thinking Lab/DSP/Clubs and cells Management System/Clubs and cells Management System/assets/tech_stack_bw_grid.png"
    out2 = "C:/Users/ELCOT/.gemini/antigravity/brain/5847d047-8608-4f3f-8443-8cf060e261e2/tech_stack_bw_grid.png"
    create_pure_bw_grid(out1)
    create_pure_bw_grid(out2)

