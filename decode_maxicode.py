"""
MaxiCode Decoder using pyzbar
MaxiCode is used primarily by UPS for package tracking and logistics
"""

import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import os

def decode_maxicode(image_path):
    """Decode MaxiCode from image"""
    
    # Validate file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return None
    
    print("="*70)
    print("MAXICODE DECODER")
    print("="*70)
    print(f"Processing: {image_path}\n")
    
    try:
        # Load image
        image = cv2.imread(image_path)
        
        # Decode specifically MaxiCode symbols
        maxicodes = decode(image, symbols=[ZBarSymbol.MAXICODE])
        
        if not maxicodes:
            print("❌ No MaxiCode detected!")
            print("\nTips:")
            print("  - Ensure the bull's-eye center pattern is visible")
            print("  - Check image quality and resolution")
            print("  - MaxiCode requires good contrast and lighting")
            print("  - Ensure all hexagonal modules are clear")
            return None
        
        print(f"✅ Found {len(maxicodes)} MaxiCode(s)\n")
        
        decoded_data_list = []
        
        for i, maxicode in enumerate(maxicodes, 1):
            # Extract data
            try:
                maxicode_data = maxicode.data.decode('utf-8')
            except:
                maxicode_data = str(maxicode.data)
            
            maxicode_type = maxicode.type
            (x, y, w, h) = maxicode.rect
            
            decoded_data_list.append(maxicode_data)
            
            # Print details
            print(f"📦 MaxiCode #{i}")
            print(f"   Data: {maxicode_data}")
            print(f"   Type: {maxicode_type}")
            print(f"   Position: (x={x}, y={y})")
            print(f"   Size: {w}x{h} pixels")
            print(f"   Data Length: {len(maxicode_data)} characters")
            
            # Parse structured data (UPS format)
            if len(maxicode_data) > 20:
                print(f"\n   📊 MaxiCode Structure:")
                print(f"      Raw Data: {maxicode_data[:50]}...")
                # MaxiCode often contains structured shipping data
                print(f"      (Shipping/Tracking Information)")
            
            print("-" * 70)
            
            # Draw rectangle around MaxiCode
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Draw polygon outline if available
            points = maxicode.polygon
            if len(points) >= 4:
                pts = [(int(p.x), int(p.y)) for p in points]
                for j in range(len(pts)):
                    cv2.line(image, pts[j], pts[(j+1) % len(pts)], (255, 0, 0), 2)
            
            # Add text label
            label = f"MAXICODE-{i}"
            cv2.putText(image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Save annotated image
        output_path = "maxicode_decoded.png"
        cv2.imwrite(output_path, image)
        print(f"\n💾 Annotated image saved: {output_path}")
        
        # Display
        cv2.imshow("MaxiCode Detection", image)
        print("\n👁️  Press any key to close the window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return decoded_data_list
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Change this to your image path
    image_file = "maxicode.png"
    
    # Decode the MaxiCode
    results = decode_maxicode(image_file)
    
    if results:
        print("\n" + "="*70)
        print("SUMMARY - ALL DECODED DATA")
        print("="*70)
        for i, data in enumerate(results, 1):
            print(f"{i}. {data}")

