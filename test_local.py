import cv2
import numpy as np
import os

def validate_cover_local(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot read image - {image_path}")
        return
    
    height, width = image.shape[:2]
    
    print("\n" + "="*50)
    print("COVER VALIDATION RESULTS")
    print("="*50)
    print(f"Image dimensions: {width} x {height} pixels")
    
    dpi_estimate = width / 5
    print(f"Estimated DPI: {dpi_estimate:.0f}")
    
    if width >= 1200 and height >= 1800:
        print("✓ Resolution: PASS (Good quality)")
        resolution_ok = True
    else:
        print("✗ Resolution: FAIL (Too low)")
        resolution_ok = False
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    magnitude = np.sqrt(sobelx**2)
    text_density = np.mean(magnitude) / 10
    
    if text_density > 5:
        print(f"✓ Text detected: Yes (density: {text_density:.1f})")
        text_ok = True
    else:
        print(f"✗ Text detected: Low (density: {text_density:.1f})")
        text_ok = False
    
    mm_to_px = dpi_estimate / 25.4
    badge_height_px = int(9 * mm_to_px)
    badge_zone_y = height - badge_height_px
    
    print(f"Badge zone: Bottom {badge_height_px} pixels")
    
    bottom_region = image[badge_zone_y:height, 0:width]
    bottom_brightness = np.mean(bottom_region) / 255 * 100
    
    if bottom_brightness > 70:
        print(f"✓ Badge area clear: Yes (brightness: {bottom_brightness:.0f}%)")
        badge_ok = True
    else:
        print(f"⚠ Badge area occupied: Possible overlap (brightness: {bottom_brightness:.0f}%)")
        badge_ok = False
    
    confidence = 100
    issues = []
    
    if not resolution_ok:
        confidence -= 30
        issues.append("Low resolution")
    
    if not text_ok:
        confidence -= 20
        issues.append("Low text visibility")
    
    if not badge_ok:
        confidence -= 30
        issues.append("Potential overlap with badge area")
    
    if confidence >= 70:
        status = "PASS"
    else:
        status = "REVIEW NEEDED"
    
    print("\n" + "-"*50)
    print(f"STATUS: {status}")
    print(f"CONFIDENCE: {confidence}%")
    print(f"ISSUES: {', '.join(issues) if issues else 'None'}")
    print("-"*50)
    
    return {'status': status, 'confidence': confidence, 'issues': issues}

if __name__ == "__main__":
    print("\nBOOK COVER VALIDATOR (Offline Mode)")
    print("-"*50)
    image_path = input("Enter image path: ").strip()
    validate_cover_local(image_path)