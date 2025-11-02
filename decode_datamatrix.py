"""
Data Matrix Decoder - Complete Solution
Works on Windows 11
"""

from pylibdmtx.pylibdmtx import decode
from PIL import Image
import cv2
import os
import sys

def decode_datamatrix(image_path):
    """Decode Data Matrix barcode from image"""
    
    # Validate file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        return None
    
    print("="*70)
    print("DATA MATRIX BARCODE DECODER")
    print("="*70)
    print(f"Processing: {image_path}\n")
    
    try:
        # Decode using pylibdmtx
        pil_image = Image.open(image_path)
        results = decode(pil_image)
        
        if not results:
            print("❌ No Data Matrix barcode detected!")
            print("\nTips:")
            print("  - Ensure good image quality and lighting")
            print("  - Check if the Data Matrix is visible and undamaged")
            print("  - Try preprocessing the image (contrast, brightness)")
            return None
        
        # Load image for visualization
        cv_image = cv2.imread(image_path)
        
        print(f"✅ Found {len(results)} Data Matrix barcode(s)\n")
        
        decoded_data_list = []
        
        for i, result in enumerate(results, 1):
            # Extract data
            try:
                decoded_data = result.data.decode('utf-8')
            except:
                decoded_data = str(result.data)
            
            decoded_data_list.append(decoded_data)
            
            # Get dimensions
            rect = result.rect
            left, top = rect.left, rect.top
            width, height = rect.width, rect.height
            
            # Print details
            print(f"📊 Data Matrix #{i}")
            print(f"   Data: {decoded_data}")
            print(f"   Position: (x={left}, y={top})")
            print(f"   Size: {width}x{height} pixels")
            print(f"   Data Length: {len(decoded_data)} characters")
            print("-" * 70)
            
            # Visualize
            cv2.rectangle(cv_image, 
                         (left, top), 
                         (left + width, top + height), 
                         (0, 255, 0), 3)
            
            cv2.putText(cv_image, 
                       f"DM-{i}", 
                       (left, top - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.9, (0, 255, 0), 2)
        
        # Save annotated image
        output_path = "data-matrix.png"
        cv2.imwrite(output_path, cv_image)
        print(f"\n💾 Annotated image saved: {output_path}")
        
        # Display
        cv2.imshow("Data Matrix Detection", cv_image)
        print("\n👁️  Press any key to close the preview window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return decoded_data_list
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Change this to your image path
    image_file = "datamatrix.png"
    
    # Decode the Data Matrix
    results = decode_datamatrix(image_file)
    
    if results:
        print("\n" + "="*70)
        print("SUMMARY - ALL DECODED DATA")
        print("="*70)
        for i, data in enumerate(results, 1):
            print(f"{i}. {data}")

