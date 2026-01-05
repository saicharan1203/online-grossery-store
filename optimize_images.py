"""Script to optimize large images for better performance."""

import os
from PIL import Image
import io

IMAGE_DIR = "static/images"
MAX_SIZE = (400, 400)  # Maximum dimensions for product images
QUALITY = 85  # JPEG/WebP quality

def get_file_size_kb(path):
    return os.path.getsize(path) / 1024

def optimize_image(filepath):
    """Optimize a single image file."""
    original_size = get_file_size_kb(filepath)
    
    # Skip if already small (less than 50KB)
    if original_size < 50:
        return None
    
    try:
        with Image.open(filepath) as img:
            # Convert to RGB if necessary (for PNG with transparency, use RGBA)
            if img.mode == 'RGBA':
                # Keep as RGBA for transparency
                pass
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if larger than max size
            if img.size[0] > MAX_SIZE[0] or img.size[1] > MAX_SIZE[1]:
                img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
            
            # Determine output format
            ext = os.path.splitext(filepath)[1].lower()
            output_path = filepath
            
            if ext == '.png':
                # Convert large PNGs to WebP for better compression
                output_path = filepath.replace('.png', '.webp')
                img.save(output_path, 'WEBP', quality=QUALITY, optimize=True)
                # Remove original PNG if converted
                if output_path != filepath and os.path.exists(output_path):
                    os.remove(filepath)
                    return (filepath, output_path, original_size, get_file_size_kb(output_path))
            elif ext == '.webp':
                img.save(output_path, 'WEBP', quality=QUALITY, optimize=True)
            elif ext in ['.jpg', '.jpeg']:
                img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
            
            new_size = get_file_size_kb(output_path)
            return (filepath, output_path, original_size, new_size)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def main():
    print("🔧 Optimizing product images for better performance...\n")
    
    total_saved = 0
    optimized_files = []
    converted_files = []
    
    for filename in os.listdir(IMAGE_DIR):
        filepath = os.path.join(IMAGE_DIR, filename)
        
        if not os.path.isfile(filepath):
            continue
            
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.png', '.jpg', '.jpeg', '.webp']:
            continue
        
        result = optimize_image(filepath)
        if result:
            old_path, new_path, old_size, new_size = result
            saved = old_size - new_size
            total_saved += saved
            
            if old_path != new_path:
                converted_files.append((old_path, new_path, old_size, new_size))
                print(f"✅ Converted: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
                print(f"   {old_size:.1f}KB -> {new_size:.1f}KB (saved {saved:.1f}KB)")
            else:
                optimized_files.append((old_path, old_size, new_size))
                print(f"✅ Optimized: {os.path.basename(old_path)}")
                print(f"   {old_size:.1f}KB -> {new_size:.1f}KB (saved {saved:.1f}KB)")
    
    print(f"\n{'='*50}")
    print(f"📊 SUMMARY")
    print(f"{'='*50}")
    print(f"Optimized files: {len(optimized_files)}")
    print(f"Converted files: {len(converted_files)}")
    print(f"Total space saved: {total_saved/1024:.2f}MB")
    
    # Return list of converted files for database update
    return converted_files

if __name__ == "__main__":
    converted = main()
    
    if converted:
        print("\n⚠️  Some PNG files were converted to WebP.")
        print("You may need to update image paths in the database.")
