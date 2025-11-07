"""
Generate a cool app icon with lightning bolt
Creates app_icon.ico for ScraperG1000
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Generate a modern app icon with lightning bolt"""

    # Create 256x256 image (standard icon size)
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw gradient background circle
    for i in range(100):
        alpha = int(255 * (1 - i/100))
        radius = int(size/2 - i)
        color = (
            int(50 + i * 2),      # Red
            int(150 + i),          # Green
            int(255),              # Blue (electric blue)
            alpha
        )
        draw.ellipse([size/2 - radius, size/2 - radius,
                     size/2 + radius, size/2 + radius],
                    fill=color)

    # Draw solid background circle
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin],
                fill=(30, 40, 60, 255))

    # Draw electric blue outer ring
    ring_width = 8
    draw.ellipse([margin, margin, size-margin, size-margin],
                outline=(0, 200, 255, 255), width=ring_width)

    # Draw lightning bolt (cool angular design)
    lightning_color = (255, 220, 0, 255)  # Electric yellow

    # Lightning bolt coordinates (centered, angular design)
    bolt = [
        (size/2 - 15, 60),      # Top
        (size/2 + 5, size/2 - 20),  # Middle right
        (size/2 - 5, size/2 - 20),  # Middle left
        (size/2 + 15, size/2 + 10), # Lower right
        (size/2, size/2 + 10),      # Lower middle
        (size/2 + 10, size - 60),   # Bottom right
        (size/2 - 5, size/2 + 20),  # Middle lower
        (size/2 + 5, size/2 + 20),  # Middle lower right
        (size/2 - 15, 60),          # Back to top
    ]

    # Draw lightning with glow effect
    for offset in range(10, 0, -1):
        alpha = int(100 - offset * 8)
        glow_color = (255, 220, 0, alpha)
        offset_bolt = [(x + offset/2, y) for x, y in bolt]
        draw.polygon(offset_bolt, fill=glow_color)

    # Draw main lightning bolt
    draw.polygon(bolt, fill=lightning_color)

    # Add highlight to lightning
    highlight = [
        (size/2 - 10, 70),
        (size/2, size/2 - 10),
        (size/2 - 3, size/2 - 10),
        (size/2 - 13, 70),
    ]
    draw.polygon(highlight, fill=(255, 255, 200, 200))

    # Draw "G1000" text at bottom
    try:
        # Try to use a system font
        font_size = 36
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    text = "G1000"
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size - text_width) / 2
    text_y = size - 50

    # Draw text shadow
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 150))
    # Draw text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    # Save as ICO with multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

    # Create list of resized images
    images = []
    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)

    # Save as .ico file
    output_path = 'app_icon.ico'
    images[0].save(output_path, format='ICO', sizes=[s for s in icon_sizes])

    print(f"✓ Icon created: {output_path}")
    print("  - Electric blue gradient background")
    print("  - Lightning bolt design")
    print("  - G1000 branding")
    print("  - Multiple sizes for Windows compatibility")

    return output_path

if __name__ == "__main__":
    print("=" * 50)
    print("Generating Scraper G1000 Icon")
    print("=" * 50)
    print()

    icon_path = create_icon()

    print()
    print("Icon ready for desktop app build!")
    print("=" * 50)
