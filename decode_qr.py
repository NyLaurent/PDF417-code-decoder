"""
QR Code Decoder using pyzbar
Best for complex QR codes and multiple QR detection
"""

import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import os

def decode_qr_code(image_path):
    """Decode QR code from image using pyzbar"""
    
    # Validate file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return None
    
    print("="*70)
    print("QR CODE DECODER (pyzbar)")
    print("="*70)
    print(f"Processing: {image_path}\n")
    
    try:
        # Load image
        image = cv2.imread(image_path)
        
        # Decode specifically QR codes
        qr_codes = decode(image, symbols=[ZBarSymbol.QRCODE])
        
        if not qr_codes:
            print("❌ No QR code detected!")
            print("\nTips:")
            print("  - Ensure the QR code is clear and well-lit")
            print("  - Check if all corner markers are visible")
            print("  - Try different angles or distances")
            return None
        
        print(f"✅ Found {len(qr_codes)} QR code(s)\n")
        
        decoded_data_list = []
        
        for i, qr in enumerate(qr_codes, 1):
            # Extract data
            qr_data = qr.data.decode('utf-8')
            qr_type = qr.type
            (x, y, w, h) = qr.rect
            
            decoded_data_list.append(qr_data)
            
            # Print details
            print(f"📱 QR Code #{i}")
            print(f"   Data: {qr_data}")
            print(f"   Type: {qr_type}")
            print(f"   Position: (x={x}, y={y})")
            print(f"   Size: {w}x{h} pixels")
            print(f"   Data Length: {len(qr_data)} characters")
            
            # Detect data type
            if qr_data.startswith('http://') or qr_data.startswith('https://'):
                print(f"   Content Type: 🌐 URL/Website")
            elif qr_data.startswith('mailto:'):
                print(f"   Content Type: 📧 Email")
            elif qr_data.startswith('tel:'):
                print(f"   Content Type: 📞 Phone Number")
            elif qr_data.startswith('WIFI:'):
                print(f"   Content Type: 📶 WiFi Credentials")
            else:
                print(f"   Content Type: 📝 Text/Other")
            
            print("-" * 70)
            
            # Draw rectangle around QR code
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Draw corner points
            points = qr.polygon
            if len(points) == 4:
                pts = [(int(p.x), int(p.y)) for p in points]
                for j in range(4):
                    cv2.line(image, pts[j], pts[(j+1) % 4], (255, 0, 0), 3)
            
            # Add text label
            label = f"QR-{i}"
            cv2.putText(image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Save annotated image
        output_path = "qr_code_decoded.png"
        cv2.imwrite(output_path, image)
        print(f"\n💾 Annotated image saved: {output_path}")
        
        # Display
        cv2.imshow("QR Code Detection", image)
        print("\n👁️  Press any key to close the window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return decoded_data_list
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Change this to your image path
    image_file = "qr_code.png"
    
    # Decode the QR code
    results = decode_qr_code(image_file)
    
    if results:
        print("\n" + "="*70)
        print("SUMMARY - ALL DECODED DATA")
        print("="*70)
        for i, data in enumerate(results, 1):
            print(f"{i}. {data}")

