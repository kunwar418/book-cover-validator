import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    def __init__(self):
        self.text_detector = None
        
    def load_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Cannot load image: {image_path}")
        return image
    
    def get_image_dimensions(self, image):
        height, width = image.shape[:2]
        return width, height
    
    def calculate_safe_zone(self, width, height, dpi=300):
        mm_to_px = dpi / 25.4
        
        safe_margin_px = int(3 * mm_to_px)
        badge_height_px = int(9 * mm_to_px)
        
        safe_zone = {
            'x_min': safe_margin_px,
            'x_max': width - safe_margin_px,
            'y_min': safe_margin_px,
            'y_max': height - safe_margin_px - badge_height_px
        }
        
        badge_zone = {
            'x_min': safe_margin_px,
            'x_max': width - safe_margin_px,
            'y_min': height - badge_height_px,
            'y_max': height - safe_margin_px
        }
        
        return safe_zone, badge_zone
    
    def detect_text_regions(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        magnitude = np.uint8(255 * magnitude / np.max(magnitude))
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(magnitude, kernel, iterations=2)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            if area > 500 and h > 10 and w > 20:
                text_regions.append({'x': x, 'y': y, 'w': w, 'h': h})
        
        return text_regions
    
    def check_overlap(self, text_region, badge_zone):
        text_left = text_region['x']
        text_right = text_region['x'] + text_region['w']
        text_top = text_region['y']
        text_bottom = text_region['y'] + text_region['h']
        
        badge_left = badge_zone['x_min']
        badge_right = badge_zone['x_max']
        badge_top = badge_zone['y_min']
        badge_bottom = badge_zone['y_max']
        
        overlap = not (text_right < badge_left or 
                      text_left > badge_right or 
                      text_bottom < badge_top or 
                      text_top > badge_bottom)
        
        return overlap
    
    def check_resolution(self, image, min_dpi=150):
        height, width = image.shape[:2]
        if width < 1200 or height < 1800:
            return False, "Low resolution cover"
        return True, "Resolution OK"
    
    def get_author_name_region(self, text_regions):
        bottom_regions = sorted(text_regions, key=lambda x: x['y'] + x['h'], reverse=True)
        
        for region in bottom_regions[:5]:
            region_bottom = region['y'] + region['h']
            if region_bottom > 0:
                return region
        return None
    
    def validate_cover(self, image_path):
        image = self.load_image(image_path)
        height, width = image.shape[:2]
        
        safe_zone, badge_zone = self.calculate_safe_zone(width, height)
        
        resolution_ok, resolution_msg = self.check_resolution(image)
        
        text_regions = self.detect_text_regions(image)
        
        author_region = self.get_author_name_region(text_regions)
        
        badge_overlap = False
        if author_region:
            badge_overlap = self.check_overlap(author_region, badge_zone)
        
        issues = []
        confidence = 100
        
        if badge_overlap:
            issues.append("Author name overlaps with award badge area")
            confidence -= 30
        
        if not resolution_ok:
            issues.append(resolution_msg)
            confidence -= 20
        
        if len(text_regions) == 0:
            issues.append("No text detected on cover")
            confidence -= 50
        
        if len(issues) == 0:
            status = "PASS"
        elif confidence >= CONFIDENCE_THRESHOLD:
            status = "PASS"
        else:
            status = "REVIEW NEEDED"
        
        return {
            'status': status,
            'confidence': max(0, confidence),
            'issues': issues,
            'badge_overlap': badge_overlap,
            'resolution_ok': resolution_ok,
            'text_regions_count': len(text_regions)
        }