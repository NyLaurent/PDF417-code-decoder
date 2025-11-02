# Barcode Decoder

A Python-based barcode decoder that uses ZXing library via Docker to decode barcodes from images and visualizes the detected barcode location with a bounding polygon overlay.

## Overview

This project decodes barcodes from image files using the ZXing (Zebra Crossing) barcode scanning library. It runs ZXing inside a Docker container to avoid local Java installation requirements, then uses OpenCV to draw a bounding polygon around the detected barcode and save an annotated image.

## Features

- 🎯 **Barcode Detection**: Detects and decodes various barcode formats supported by ZXing (PDF417, QR Code, UPC, EAN, Code 128, etc.)
- 📦 **Containerized Execution**: Uses Docker to run ZXing Java library without requiring local Java installation
- 📊 **Visual Annotation**: Automatically draws a green bounding polygon around detected barcodes
- 💾 **Image Export**: Saves annotated images with barcode boundaries highlighted
- 🔍 **Coordinate Extraction**: Parses and displays barcode corner coordinates

## Prerequisites

- **Python 3.x** with the following packages:
  - `opencv-python` (cv2)
  - `numpy`
- **Docker** installed and running
- The required ZXing JAR files (included in the repository):
  - `core-3.5.0.jar`
  - `javase-3.5.0.jar`
  - `jcommander-1.82.jar`

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd decoder
```

2. Install Python dependencies:

```bash
pip install opencv-python numpy
```

3. Ensure Docker is installed and running:

```bash
docker --version
```

4. Place your barcode image file as `image.png` in the project directory, or modify the `barcode_image` variable in `decode_barcode.py` to point to your image file.

## Usage

1. Place your barcode image in the project directory (default: `image.png`)
2. Run the decoder script:

```bash
python decode_barcode.py
```

3. The script will:
   - Decode the barcode and print the result to the console
   - Draw a green bounding polygon around the detected barcode
   - Save an annotated image as `annotated_barcode.png`
   - Display the annotated image in a window (press any key to close)

## How It Works

1. **Validation**: Checks that all required files (JAR files and image) exist
2. **Docker Execution**: Runs ZXing's CommandLineRunner inside an OpenJDK Docker container
3. **Output Parsing**: Extracts barcode data and corner point coordinates from ZXing output
4. **Visualization**: Uses OpenCV to:
   - Load the original image
   - Draw a green polygon connecting the barcode corner points
   - Save the annotated image
   - Display the result

## File Structure

```
decoder/
├── decode_barcode.py       # Main Python script
├── image.png               # Input barcode image (replace with your image)
├── core-3.5.0.jar         # ZXing core library
├── javase-3.5.0.jar       # ZXing Java SE library
├── jcommander-1.82.jar    # Command-line argument parser for Java
└── README.md              # This file
```

## Output

- **Console Output**: Displays the decoded barcode data and corner coordinates
- **Annotated Image**: Saves `annotated_barcode.png` with the barcode boundary highlighted in green

## Customization

To decode a different image file, modify the `barcode_image` variable in `decode_barcode.py`:

```python
barcode_image = "your_image.png"  # Change this to your image filename
```

## Troubleshooting

- **"Error: [file] not found!"**: Ensure all JAR files and the image file are in the project directory
- **Docker errors**: Make sure Docker is running and can pull the `openjdk:17` image
- **"No bounding box points detected"**: The barcode might not be detectable, or the image quality may be insufficient
- **OpenCV display issues**: If running on a headless server, the `cv2.imshow()` call may fail. Consider removing or modifying the display code

## Dependencies

- **Python Libraries**:

  - `opencv-python`: Image processing and visualization
  - `numpy`: Array operations for polygon drawing

- **Java Libraries** (provided as JAR files):

  - ZXing Core 3.5.0
  - ZXing JavaSE 3.5.0
  - JCommander 1.82

- **Docker Image**:
  - `openjdk:17`: Java runtime environment for executing ZXing

## License

This project uses ZXing library which is licensed under Apache License 2.0.
