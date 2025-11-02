"""
Aztec Code Decoder using pyzbar
Aztec codes are 2D barcodes used in transport, ticketing, and identification
"""

import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import os

def decode_aztec_code(image_path):
    """Decode Aztec code from image"""
    
    # Validate file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return None
    
    print("="*70)
    print("AZTEC CODE DECODER")
    print("="*70)
    print(f"Processing: {image_path}\n")
    
    try:
        # Load image
        image = cv2.imread(image_path)
        
        # Decode specifically Aztec codes
        aztec_codes = decode(image, symbols=[ZBarSymbol.AZTEC])
        
        if not aztec_codes:
            print("❌ No Aztec code detected!")
            print("\nTips:")
            print("  - Ensure the bulls-eye center is clearly visible")
            print("  - Check if the image has good contrast")
            print("  - Try improving image quality/resolution")
            print("  - Ensure proper lighting and focus")
            return None
        
        print(f"✅ Found {len(aztec_codes)} Aztec code(s)\n")
        
        decoded_data_list = []
        
        for i, aztec in enumerate(aztec_codes, 1):
            # Extract data
            try:
                aztec_data = aztec.data.decode('utf-8')
            except:
                aztec_data = str(aztec.data)
            
            aztec_type = aztec.type
            (x, y, w, h) = aztec.rect
            
            decoded_data_list.append(aztec_data)
            
            # Print details
            print(f"🎯 Aztec Code #{i}")
            print(f"   Data: {aztec_data}")
            print(f"   Type: {aztec_type}")
            print(f"   Position: (x={x}, y={y})")
            print(f"   Size: {w}x{h} pixels")
            print(f"   Data Length: {len(aztec_data)} characters")
            
            # Detect content type
            if aztec_data.startswith('http://') or aztec_data.startswith('https://'):
                print(f"   Content Type: 🌐 URL")
            elif '@' in aztec_data and '.' in aztec_data:
                print(f"   Content Type: 📧 Email/Contact")
            elif aztec_data.isdigit():
                print(f"   Content Type: 🔢 Numeric ID")
            else:
                print(f"   Content Type: 📝 Text/Data")
            
            print("-" * 70)
            
            # Draw rectangle around Aztec code
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Draw polygon outline if available
            points = aztec.polygon
            if len(points) >= 4:
                pts = [(int(p.x), int(p.y)) for p in points]
                for j in range(len(pts)):
                    cv2.line(image, pts[j], pts[(j+1) % len(pts)], (255, 0, 0), 2)
            
            # Add text label
            label = f"AZTEC-{i}"
            cv2.putText(image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Save annotated image
        output_path = "aztec_code_decoded.png"
        cv2.imwrite(output_path, image)
        print(f"\n💾 Annotated image saved: {output_path}")
        
        # Display
        cv2.imshow("Aztec Code Detection", image)
        print("\n👁️  Press any key to close the window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return decoded_data_list
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Change this to your image path
    image_file = "aztec-code.png"
    
    # Decode the Aztec code
    results = decode_aztec_code(image_file)
    
    if results:
        print("\n" + "="*70)
        print("SUMMARY - ALL DECODED DATA")
        print("="*70)
        for i, data in enumerate(results, 1):
            print(f"{i}. {data}")

