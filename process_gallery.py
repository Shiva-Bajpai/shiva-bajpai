from PIL import Image, ImageDraw, ImageFont, ImageChops
import os

def add_round_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def add_tint(im, opacity=100):
    # Create a uniform black overlay
    overlay = Image.new("RGBA", im.size, (0, 0, 0, opacity))
    # Composite
    base = im.convert("RGBA")
    return Image.alpha_composite(base, overlay)

def process_gallery_image(image_path, output_path, text="Explore Now", font_path="/System/Library/Fonts/Supplemental/Didot.ttc"):
    try:
        # Open and convert
        base = Image.open(image_path).convert("RGBA")
        
        # 1. Add Tint
        base = add_tint(base, opacity=90) # Adjust opacity for "black tint" feel
        
        # 2. Add Text
        draw = ImageDraw.Draw(base)
        try:
            # Font size: 8% of width - significantly larger as requested
            font_size = int(base.size[0] * 0.08)
            font = ImageFont.truetype(font_path, font_size)
            
            # Simulate Bold by drawing multiple times with offset if bold font not found
            # Or just rely on size and contrast. Didot is naturally thin. 
            # Let's try to find a bolder font or stroke it.
            # actually stroke_width param exists in newer pillow
            
        except OSError:
            print(f"Font not found at {font_path}, using default.")
            font = ImageFont.load_default()
            
        # Center text
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top
        x = (base.size[0] - text_width) / 2
        y = (base.size[1] - text_height) / 2
        
        # Draw text in Pure White with stroke for "Bold" effect
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(255, 255, 255, 255))
        
        # 3. Round Corners
        final_image = add_round_corners(base, 25)
        
        # Save
        final_image.save(output_path)
        print(f"Saved premium gallery image to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    tasks = [
        ("raw_code.png", "grid_code_large.png", "Code"),
        ("raw_design.png", "grid_design_large.png", "Design"),
        ("gallery_showcase_2.png", "grid_gallery_large.png", "Gallery"),
        ("raw_writing.png", "grid_writing_large.png", "Writing")
    ]
    
    for source, output, label in tasks:
        if os.path.exists(source):
            process_gallery_image(source, output, text=label)
        else:
            print(f"Warning: Source image {source} not found.")
