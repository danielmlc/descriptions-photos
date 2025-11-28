from PIL import Image
import os

def analyze_style_v2():
    try:
        img = Image.open("样本图片.png")
        width, height = img.size
        
        # Crop bottom 20%
        crop_h = int(height * 0.2)
        region = img.crop((0, height - crop_h, width, height))
        pixels = region.load()
        
        # Check corners of the region to guess background
        # Top-left of region
        tl = pixels[0, 0]
        # Bottom-left of region
        bl = pixels[0, crop_h - 1]
        # Center
        center = pixels[width//2, crop_h//2]
        
        print(f"Region Top-Left Color: {tl}")
        print(f"Region Bottom-Left Color: {bl}")
        print(f"Region Center Color: {center}")
        
        # Check if it's a solid block
        # If corners are white/bright, it's likely a white footer.
        is_bright_bg = (sum(tl) > 600) # > 200*3
        
        print(f"Is bright background? {is_bright_bg}")
        
        # If bright background, look for dark text
        text_pixels = []
        if is_bright_bg:
            print("Looking for dark text...")
            for y in range(crop_h):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    if r < 100 and g < 100 and b < 100: # Dark
                        text_pixels.append((x, y))
        else:
            print("Looking for bright text...")
            for y in range(crop_h):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    if r > 200 and g > 200 and b > 200: # Bright
                        text_pixels.append((x, y))
                        
        if not text_pixels:
            print("No text pixels found.")
            return
            
        ys = [p[1] for p in text_pixels]
        min_y, max_y = min(ys), max(ys)
        
        # Project to Y to find lines again
        row_counts = [0] * crop_h
        for x, y in text_pixels:
            row_counts[y] += 1
            
        # Print row counts simplified
        print("Line analysis:")
        current_line_height = 0
        gap_height = 0
        lines = []
        
        for y in range(min_y, max_y + 1):
            if row_counts[y] > 2: # Threshold
                if current_line_height == 0:
                    # Start of line
                    if gap_height > 2: # Gap between lines
                        pass
                current_line_height += 1
                gap_height = 0
            else:
                if current_line_height > 0:
                    gap_height += 1
                    if gap_height > 2: # End of line
                        lines.append(current_line_height)
                        current_line_height = 0
        
        if current_line_height > 0:
            lines.append(current_line_height)
            
        print(f"Detected {len(lines)} lines with heights: {lines}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_style_v2()
