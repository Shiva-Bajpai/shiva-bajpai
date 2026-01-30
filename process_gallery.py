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

def add_vignette(im, opacity=180):
    # Create a gradient mask
    width, height = im.size
    # Create a radial gradient from center
    # This is a bit complex in pure PIL without numpy, so we'll approximate with a strong border overlay
    
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Base tint (overall darker)
    draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 100))
    
    # Vignette simulation: draw nested rectangles with increasing opacity towards edge? 
    # Or just use a simple radial gradient image
    
    # Let's create a radial gradient manually
    # Center (w/2, h/2) is transparent, edges are black
    
    # For simplicity and "premium" look, a strong uniform tint often works best with centered text, 
    # but user asked for "borders have black tint more".
    # Let's try a radial gradient approach using ImageChops
    
    gradient = Image.new('L', (width, height), 0)
    for y in range(height):
        for x in range(width):
            # Distance from center normalized
            dx = (x - width/2) / (width/2)
            dy = (y - height/2) / (height/2)
            dist = (dx*dx + dy*dy)**0.5
            # tint factor: 0 at center, 1 at edges. 
            # We want center to be somewhat dark (tint 100/255) and edges very dark (240/255)
            # intensity = base + (max - base) * dist
            intensity = int(80 + (175) * min(dist, 1.2)) # capped
            gradient.putpixel((x, y), intensity)
            
    # Apply this gradient as the alpha channel of a black image
    black_overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    black_overlay.putalpha(gradient)
    
    # Composite
    return Image.alpha_composite(im, black_overlay)

def process_gallery_image(image_path, output_path, text="Explore Now", font_path="/System/Library/Fonts/Supplemental/Didot.ttc"):
    try:
        # Open and convert
        base = Image.open(image_path).convert("RGBA")
        
        # 1. Add Vignette/Overlay
        base = add_vignette(base)
        
        # 2. Add Text
        draw = ImageDraw.Draw(base)
        try:
            # Font size: 4.5% of width - slightly bigger/bolder feel
            font_size = int(base.size[0] * 0.045)
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
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(255, 255, 255, 255))
        
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
