from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, output_path="text_image.png", image_size=(500, 300), font_size=30):
    # Create an image with a white background
    img = Image.new('RGB', image_size, "white")
    draw = ImageDraw.Draw(img)

    # Load a font (adjust path if necessary)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Use a system font
    except IOError:
        font = ImageFont.load_default()

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate text position to center it
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    # Draw text on the image
    draw.text(position, text, fill="black", font=font)

    # Save the image
    img.save(output_path)
    print(f"Image saved as {output_path}")

# Example usage
create_text_image("Hello, World!")
