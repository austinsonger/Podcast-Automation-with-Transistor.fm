use std::error::Error;
use std::fs;
use std::path::Path;
use textwrap::fill;
use rusttype::{Font, Scale, FontCollection, FontFamily, PositionedGlyph};
use image::{ImageBuffer, Rgb};
use imageproc::drawing::draw_text_mut;

const FONT_PATH: &str = "./config/MonaspaceArgon-Bold.otf"; // Update with the actual path to your font
const FONT_SIZE: f32 = 100.0; // Adjust font size as needed

fn load_font() -> Result<Font, Box<dyn Error>> {
    if let Ok(font_data) = include_bytes!(FONT_PATH) {
        return Font::from_bytes(font_data as &[u8]);
    }
    
    // If the font file is not found or cannot be loaded, use a default font
    let default_font = FontCollection::new()
        .into_font() // only necessary if you want to convert the collection into a Font
        .unwrap_or(FontFamily::SERIF);

    Ok(default_font)
}

fn main() -> Result<(), Box<dyn Error>> {
    // Path to CSV file
    let csv_file = "./config/scotus.csv";

    // Base directory for the year
    let base_dir = "../2023/";

    // Path to your predefined graphic
    let graphic_path = "./config/Blank.png";

    // Read CSV file
    let mut rdr = csv::Reader::from_path(csv_file)?;

    // Load the font, falling back to a default font if necessary
    let font = load_font()?;

    for result in rdr.records() {
        let record = result?;
        let title = record.get(0).ok_or("Missing 'Title' column")?.trim();
        let case_id = record.get(1).ok_or("Missing 'Case ID' column")?.trim();

        // Full path for the case directory
        let case_dir = Path::new(&base_dir).join(case_id);

        // Create directory for the case if it doesn't exist
        fs::create_dir_all(&case_dir)?;

        // Directory for images
        let images_dir = case_dir.join("images");
        fs::create_dir_all(&images_dir)?;

        // Define the new image path in 'images' subdirectory
        let new_image_path = images_dir.join(format!("{}_cover.png", case_id));

        // Check if the image already exists
        if !new_image_path.exists() {
            // Open the image
            let mut img = ImageBuffer::new(1920, 1080); // Adjust image dimensions as needed
            let draw = img.as_mut();

            // Coordinates for text insertion
            let mut x = 500;
            let mut y = 1500;

            // Wrap text using textwrap (fixed number of characters per line)
            let wrapped_text = fill(title, 30); // Adjust width as needed
            let lines: Vec<&str> = wrapped_text.lines().collect();

            // Draw each line of the text
            for line in lines {
                draw_text_mut(draw, Rgb([255, 255, 255]), x, y, Scale::uniform(FONT_SIZE), &font, line);
                y += FONT_SIZE as i32 + 10; // Adjust line spacing
            }

            // Save the new image in the created directory
            img.save(&new_image_path)?;
        }
    }

    Ok(())
}
