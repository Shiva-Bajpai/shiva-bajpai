from PIL import Image
from collections import Counter

def get_dominant_color(image_path):
    try:
        im = Image.open(image_path).convert("RGB")
        # Resize to speed up processing
        im = im.resize((100, 100))
        pixels = list(im.getdata())
        # Filter out blacks/dark grays only
        filtered_pixels = [p for p in pixels if not (p[0] < 50 and p[1] < 50 and p[2] < 50)]
        
        if not filtered_pixels:
            print("Only dark pixels found.")
            return
            
        counts = Counter(filtered_pixels)
        most_common = counts.most_common(5)
        
        print("Dominant light colors:")
        for color, count in most_common:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            print(f"Color: {color}, Hex: {hex_color}, Count: {count}")

    except Exception as e:
        print(f"Error: {e}")

get_dominant_color('BG')
