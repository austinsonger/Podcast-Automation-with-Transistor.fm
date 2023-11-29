"""
# Image Text Overlay Script

## Overview
This Python script is designed to automate the process of overlaying text onto a predefined image template. It reads titles from a CSV file and places them onto an image, creating a series of new images with the text embedded. This script is particularly useful for generating customized images in bulk, such as podcast covers, event posters, or social media graphics.

## Functionality
- **CSV Reading**: The script reads data from a specified CSV file. Each row in the CSV should contain a title in the 'Title' column.
- **Image Processing**: The script uses a predefined image as a template and overlays text onto this image.
- **Text Placement and Formatting**: Text from the CSV file is placed at specified coordinates on the image. The font style, size, and color can be customized.
- **Manual Text Wrapping**: The script expects that the text in the CSV file is pre-formatted with line breaks for proper text wrapping on the image.
- **Image Output**: Each row from the CSV results in a new image file, saved with a name based on the corresponding title.

## Requirements
- Python 3
- Pandas Library
- Pillow (PIL) Library

## Setup and Usage
1. **Install Required Libraries**: Ensure Pandas and Pillow are installed in your Python environment.
2. **CSV File**: Prepare your CSV file with titles. Ensure each title is appropriately formatted with line breaks (`\n`) where needed.
3. **Image and Font Setup**: Place your image template and desired font file in the script's directory or specify their paths in the script.
4. **Customization**: Adjust the script to set the font size and the coordinates for text placement on the image.
5. **Execution**: Run the script. It will process each title from your CSV file and create new images in the specified output directory.

"""

import pandas as pd
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Load CSV file
csv_file = 'scotus.csv'
data = pd.read_csv(csv_file)

# Base directory for the year
base_dir = '../2023/'

# Path to your predefined graphic
graphic_path = './config/Blank.png'

# Font settings
font_path = './config/MonaspaceArgon-Bold.otf'  # Update with the actual path to your font
font_size = 100
font = ImageFont.truetype(font_path, font_size)

for index, row in data.iterrows():
    title = row['Title'].strip()
    case_id = row['Case ID'].strip()

    # Full path for the case directory
    case_dir = os.path.join(base_dir, case_id)

    # Create directory for the case if it doesn't exist
    os.makedirs(case_dir, exist_ok=True)

    # Directory for images
    images_dir = os.path.join(case_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)  # Create 'images' subdirectory

    # Define the new image path in 'images' subdirectory
    new_image_path = os.path.join(images_dir, f"{case_id}_cover.png")
    # Check if the image already exists
    if not os.path.exists(new_image_path):
        # Open the image
        img = Image.open(graphic_path)
        draw = ImageDraw.Draw(img)

        # Coordinates for text insertion
        x = 500
        y = 1500

        # Wrap text using textwrap (fixed number of characters per line)
        text = row['Title']
        wrapped_text = textwrap.fill(text, width=30)  # Adjust width as needed
        lines = wrapped_text.split('\n')

        # Draw each line of the text
        for line in lines:
            draw.text((x, y), line, fill="white", font=font)
            y += font_size + 10  # Adjust line spacing

        # Save the new image in the created directory
        img.save(new_image_path)
