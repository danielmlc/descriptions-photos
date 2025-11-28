from PIL import Image, ImageStat
import os

def analyze_style():
    try:
        img = Image.open("样本图片.png")
        width, height = img.size
        print(f"Sample Image Size: {width}x{height}")
        
        # Crop bottom 20%
        crop_h = int(height * 0.2)
        region = img.crop((0, height - crop_h, width, height))
        
        # Find bright pixels to detect text
        pixels = region.load()
        text_pixels = []
        
        for y in range(crop_h):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Assuming text is bright
                if r > 200 and g > 200 and b > 200:
                    text_pixels.append((x, y, (r, g, b)))
        
        if not text_pixels:
            print("No bright text found.")
            return

        # Calculate bounding box of text in the region
        xs = [p[0] for p in text_pixels]
        ys = [p[1] for p in text_pixels]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        print(f"Text Bounding Box (relative to bottom 20%): x={min_x}-{max_x}, y={min_y}-{max_y}")
        print(f"Margins: Left={min_x}, Bottom={crop_h - max_y}")
        
        # Analyze color more precisely
        # Get average color of text pixels
        avg_r = sum(p[2][0] for p in text_pixels) / len(text_pixels)
        avg_g = sum(p[2][1] for p in text_pixels) / len(text_pixels)
        avg_b = sum(p[2][2] for p in text_pixels) / len(text_pixels)
        print(f"Average Text Color: R={avg_r:.1f}, G={avg_g:.1f}, B={avg_b:.1f}")
        
        # Check for multiple lines by looking at horizontal projection
        # Count bright pixels per row
        row_counts = [0] * crop_h
        for y in range(min_y, max_y + 1):
            count = 0
            for x in range(min_x, max_x + 1):
                r, g, b = pixels[x, y]
                if r > 200 and g > 200 and b > 200:
                    count += 1
            row_counts[y] = count
            
        # Print row counts to see gaps
        print("Row projection (non-zero):")
        gap_found = False
        lines_found = 0
        in_line = False
        for y in range(min_y, max_y + 1):
            if row_counts[y] > 5: # Threshold
                if not in_line:
                    in_line = True
                    lines_found += 1
            else:
                if in_line:
                    in_line = False
        
        print(f"Detected Lines of text: {lines_found}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_style()
