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

def process_gallery_image(image_path, output_path, text="Explore Now", font_path="/System/Library/Fonts/Supplemental/Didot.ttc"):
    try:
        # Open and convert
        base = Image.open(image_path).convert("RGBA")
        
        # 1. Add Overlay
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        # Semi-transparent black (approx 40% opacity for premium look)
        draw.rectangle([0, 0, base.size[0], base.size[1]], fill=(0, 0, 0, 100))
        base = Image.alpha_composite(base, overlay)
        
        # 2. Add Text
        draw = ImageDraw.Draw(base)
        try:
            # Font size: 4% of width for a subtle, premium look
            font_size = int(base.size[0] * 0.04)
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            print(f"Font not found at {font_path}, using default.")
            font = ImageFont.load_default()
            
        # Center text
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top
        x = (base.size[0] - text_width) / 2
        y = (base.size[1] - text_height) / 2
        
        # Draw text in White
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        # 3. Round Corners
        final_image = add_round_corners(base, 25)
        
        # Save
        final_image.save(output_path)
        print(f"Saved premium gallery image to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure source image exists, using the original clean screenshot
    source = "gallery_showcase_2.png" 
    output = "gallery_showcase_premium.png"
    process_gallery_image(source, output)
