"""
Universal Barcode Decoder
Decodes all barcode types including EAN-13
"""

import cv2
from pyzbar.pyzbar import decode
import os

def decode_all_barcodes(image_path):
    """Decode all types of barcodes from image"""
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return None
    
    print("="*70)
    print("UNIVERSAL BARCODE DECODER")
    print("="*70)
    print(f"Processing: {image_path}\n")
    
    try:
        # Load image
        image = cv2.imread(image_path)
        
        # Decode all barcodes
        barcodes = decode(image)
        
        if not barcodes:
            print("❌ No barcodes detected!")
            return None
        
        print(f"✅ Found {len(barcodes)} barcode(s)\n")
        
        results = []
        
        for i, barcode in enumerate(barcodes, 1):
            # Extract data
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            (x, y, w, h) = barcode.rect
            
            results.append({
                'type': barcode_type,
                'data': barcode_data
            })
            
            # Print details
            print(f"🔍 Barcode #{i}")
            print(f"   Type: {barcode_type}")
            print(f"   Data: {barcode_data}")
            print(f"   Position: (x={x}, y={y})")
            print(f"   Size: {w}x{h} pixels")
            
            # Special handling for EAN-13
            if barcode_type == 'EAN13' and len(barcode_data) == 13:
                print(f"\n   📊 EAN-13 Structure:")
                print(f"      Prefix: {barcode_data[:3]}")
                print(f"      Manufacturer: {barcode_data[3:7]}")
                print(f"      Product: {barcode_data[7:12]}")
                print(f"      Check: {barcode_data[12]}")
            
            print("-" * 70)
            
            # Visualize
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            label = f"{barcode_type}: {barcode_data}"
            cv2.putText(image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Save and display
        output_path = "barcodes_decoded.png"
        cv2.imwrite(output_path, image)
        print(f"\n💾 Saved: {output_path}")
        
        cv2.imshow("Barcode Detection", image)
        print("\n👁️  Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Change this to your image path
    image_file = "barcode.png"
    
    # Decode all barcodes
    results = decode_all_barcodes(image_file)
    
    if results:
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        for i, item in enumerate(results, 1):
            print(f"{i}. [{item['type']}] {item['data']}")

