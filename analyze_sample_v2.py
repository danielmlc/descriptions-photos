from PIL import Image, ImageStat
import os

def analyze():
    # Check target image size
    try:
        img1 = Image.open("1.jpg")
        print(f"Target Image 1.jpg Size: {img1.size}")
    except:
        print("Could not open 1.jpg")

    try:
        img = Image.open("样本图片.png")
        print(f"Sample Image Size: {img.size}")
        
        width, height = img.size
        crop_h = int(height * 0.15) # Check bottom 15%
        crop_w = width
        
        region = img.crop((0, height - crop_h, width, height))
        stat = ImageStat.Stat(region)
        avg_brightness = sum(stat.mean) / len(stat.mean)
        print(f"Bottom 15% Average Brightness: {avg_brightness:.2f}")
        
        # Analyze center of the bottom region to guess text color
        # We'll take a histogram of the bottom region
        # If it's mostly white, text is likely black.
        # If it's mostly dark, text is likely white.
        
        if avg_brightness > 200:
            print("Bottom region is very bright. Likely white footer with black text.")
        elif avg_brightness < 50:
            print("Bottom region is very dark. Likely dark footer or photo with white text.")
        else:
            print("Bottom region is mid-tone.")
            
    except Exception as e:
        print(f"Error analyzing sample: {e}")

if __name__ == "__main__":
    analyze()
