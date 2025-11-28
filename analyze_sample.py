from PIL import Image
import os

def analyze_sample():
    try:
        img = Image.open("样本图片.png")
        print(f"Size: {img.size}")
        
        width, height = img.size
        # Crop bottom left corner (e.g., bottom 20% and left 50%)
        crop_h = int(height * 0.2)
        crop_w = int(width * 0.5)
        
        region = img.crop((0, height - crop_h, crop_w, height))
        
        # Convert to grayscale to find content
        gray = region.convert("L")
        
        # Find rows with high brightness (assuming white text)
        # We'll look for rows that have significant number of bright pixels
        
        bright_rows = []
        for y in range(crop_h):
            row_pixels = [gray.getpixel((x, y)) for x in range(crop_w)]
            # If any pixel is very bright (> 200), we count it
            if any(p > 200 for p in row_pixels):
                bright_rows.append(y)
        
        if not bright_rows:
            print("No bright text detected in bottom left.")
            return

        min_y = min(bright_rows)
        max_y = max(bright_rows)
        
        print(f"Text area detected from relative y={min_y} to {max_y} in the bottom 20% region.")
        print(f"Text height: {max_y - min_y} pixels.")
        
        # Check for gaps to guess number of lines
        # If there is a gap of > 5 pixels of dark rows, it might be multiple lines
        
        gaps = 0
        in_text = False
        gap_size = 0
        lines = 0
        
        for y in range(min_y, max_y + 1):
            row_pixels = [gray.getpixel((x, y - min_y)) for x in range(crop_w)] # Wait, y is relative to crop
            # actually I should re-read pixels from region
            row_pixels = [gray.getpixel((x, y)) for x in range(crop_w)]
            
            is_text_row = any(p > 200 for p in row_pixels)
            
            if is_text_row:
                if not in_text:
                    in_text = True
                    lines += 1
                gap_size = 0
            else:
                if in_text:
                    gap_size += 1
                    if gap_size > 5: # arbitrary threshold for line gap
                        in_text = False
        
        print(f"Estimated number of lines: {lines}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_sample()
