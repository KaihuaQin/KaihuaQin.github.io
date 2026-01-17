from PIL import Image
import os

def optimize_profile_pic():
    input_path = "prof_pic.jpg"
    output_path = "prof_pic.webp"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    # Open the image
    img = Image.open(input_path)
    print(f"Original size: {img.size}")
    
    # Calculate new size (max 400x400 for retina support of 160x160 display)
    max_size = (400, 400)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    print(f"New size: {img.size}")
    
    # Save as WebP
    img.save(output_path, "WEBP", quality=85)
    print(f"Saved optimized image to {output_path}")

    # Also save as optimized JPG for fallback or direct replacement if preferred
    img.save("prof_pic_optimized.jpg", "JPEG", quality=85, optimize=True)
    print(f"Saved optimized JPG to prof_pic_optimized.jpg")

if __name__ == "__main__":
    optimize_profile_pic()
