from PIL import Image, ImageDraw, ImageFont
import os

def add_overlay_and_text(image_path, output_path, text="Explore Now"):
    try:
        # Open the image
        base = Image.open(image_path).convert("RGBA")
        
        # Create a transparent overlay
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Add a semi-transparent black rectangle (tint)
        # Alpha 128 (approx 50% opacity)
        draw.rectangle([0, 0, base.size[0], base.size[1]], fill=(0, 0, 0, 100))
        
        # Composite the overlay onto the base
        base = Image.alpha_composite(base, overlay)
        
        # Prepare to draw text
        draw = ImageDraw.Draw(base)
        
        # Font setup - try to find a nice system font
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        if not os.path.exists(font_path):
             font_path = "/Library/Fonts/Arial.ttf"
        
        try:
            # Calculate font size relative to image width (e.g., 5% of width)
            font_size = int(base.size[0] * 0.05)
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            print("System font not found, using default.")
            font = ImageFont.load_default()
            
        # Calculate text position to center it
        # Get bounding box of text
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top
        
        x = (base.size[0] - text_width) / 2
        y = (base.size[1] - text_height) / 2
        
        # Draw text (White)
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        # Save
        base.save(output_path)
        print(f"Successfully saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

# Run the function
add_overlay_and_text("gallery_showcase_2.png", "gallery_showcase_overlay.png", "Explore Now")
