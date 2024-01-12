

import pandas as pd
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

"""
    Generate cover images for each episode based on the data in a CSV file.

    Args:
        csv_file (str): Path to the CSV file containing episode data.
        base_dir (str): Base directory for the year.
        graphic_path (str): Path to the predefined graphic.
        font_path (str): Path to the font file.
        font_size (int): Font size for the text on the cover image.

    Returns:
        None
"""

# Load CSV file
csv_file = './config/scotus.csv'
data = pd.read_csv(csv_file)

# Base directory for the year
base_dir = './2024/'

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




