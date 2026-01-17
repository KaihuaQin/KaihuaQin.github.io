import os
from PIL import Image, ImageDraw, ImageFont

# Brand Color (Deep Slate Blue)
COLOR = "#2c3e50"
BG_COLOR = (255, 255, 255, 0) # Transparent
ICON_CHAR = "KQ"

def create_image(size, font_size_ratio=0.8):
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Load a font (try default, then fallbacks if needed)
    try:
        # Try to find a nice serif or sans-serif font
        # Mac standard location
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        if not os.path.exists(font_path):
             font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        
        font = ImageFont.truetype(font_path, int(size * font_size_ratio))
    except:
        font = ImageFont.load_default()

    # Calculate text position to center it
    # getbbox returns left, top, right, bottom
    left, top, right, bottom = font.getbbox(ICON_CHAR)
    text_width = right - left
    text_height = bottom - top
    
    # Center position
    # Adjust y slightly because fonts often have baseline offset
    x = (size - text_width) / 2 - left
    y = (size - text_height) / 2 - top
    
    draw.text((x, y), ICON_CHAR, font=font, fill=COLOR)
    
    return img

def create_apple_touch_icon(size=180):
    # Apple touch icons typically have a white background, not transparent
    img = Image.new('RGB', (size, size), "white")
    draw = ImageDraw.Draw(img)
    
    # Similar font logic
    try:
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        if not os.path.exists(font_path):
             font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        font = ImageFont.truetype(font_path, int(size * 0.7))
    except:
        font = ImageFont.load_default()

    left, top, right, bottom = font.getbbox(ICON_CHAR)
    text_width = right - left
    text_height = bottom - top
    
    x = (size - text_width) / 2 - left
    y = (size - text_height) / 2 - top
    
    draw.text((x, y), ICON_CHAR, font=font, fill=COLOR)
    return img

def create_svg():
    # Simple SVG creation
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-weight="bold" font-size="80" fill="{COLOR}">{ICON_CHAR}</text>
</svg>"""
    return svg_content

def main():
    print("Generating favicons...")
    
    # 1. favicon.svg
    with open("favicon.svg", "w") as f:
        f.write(create_svg())
    print("Created favicon.svg")
    
    # 2. PNGs
    sizes = [16, 32]
    images = []
    
    for size in sizes:
        img = create_image(size)
        filename = f"favicon-{size}x{size}.png"
        img.save(filename)
        images.append(img)
        print(f"Created {filename}")
        
    # 3. favicon.ico (includes 16, 32, 48)
    # create a 48x48 version for the ico as well
    img48 = create_image(48)
    img48.save("favicon.ico", format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print("Created favicon.ico")
    
    # 4. apple-touch-icon.png
    apple_img = create_apple_touch_icon()
    apple_img.save("apple-touch-icon.png")
    print("Created apple-touch-icon.png")

if __name__ == "__main__":
    main()
