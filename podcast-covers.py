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

## Notes
- This script does not automatically wrap text. Ensure that your titles in the CSV are formatted to fit the image dimensions.
- The font size and pla

"""
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Load CSV file
csv_file = '/python/scotus.csv'
data = pd.read_csv(csv_file)

# Path to your predefined graphic
graphic_path = '/python/Blank.png'

# Font settings
font_path = '/python/fonts/MonaspaceArgon-Bold.otf'
font_size = 100
font = ImageFont.truetype(font_path, font_size)

for index, row in data.iterrows():
    # Open the image
    img = Image.open(graphic_path)
    draw = ImageDraw.Draw(img)

    # Coordinates for text insertion
    x = 38
    y = 1833

    # Inserting text from the 'Title' column of the CSV
    # Expecting that the text in the CSV is manually formatted with line breaks
    text = row['Title']
    lines = text.split('\n')  # Splitting text into lines

    # Draw each line of the text
    for line in lines:
        draw.text((x, y), line, fill="white", font=font)
        y += font_size  # Adjust the line spacing based on your font size

    # Save the new image, naming it based on the title
    safe_title = ''.join(e for e in text if e.isalnum())  # Remove non-alphanumeric characters
    new_image_path = f'/python/covers/{safe_title}_{index}.png'
    img.save(new_image_path)

    # Save the new image, naming it based on the title
    safe_title = ''.join(e for e in text if e.isalnum())  # Remove non-alphanumeric characters
    new_image_path = f'/python/covers/{safe_title}_{index}.png'
    img.save(new_image_path)


