#!/usr/bin/env python3
"""
Generate blue glowing SG logo for all icon sizes
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_sg_logo(size, output_path):
    """Create a blue glowing SG logo at specified size"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define blue glow colors
    glow_color = (30, 144, 255, 255)  # Dodger blue
    bright_color = (100, 200, 255, 255)  # Bright blue

    # Calculate sizes
    padding = size // 8
    circle_size = size - (padding * 2)

    # Draw outer glow circles (multiple layers for glow effect)
    for i in range(8, 0, -1):
        glow_alpha = int(40 * (i / 8))
        glow_offset = i * 2
        glow_circle_size = circle_size + glow_offset
        glow_x = (size - glow_circle_size) // 2
        draw.ellipse(
            [glow_x, glow_x, glow_x + glow_circle_size, glow_x + glow_circle_size],
            fill=(30, 144, 255, glow_alpha)
        )

    # Draw main circle with gradient effect
    circle_x = padding
    draw.ellipse(
        [circle_x, circle_x, circle_x + circle_size, circle_x + circle_size],
        fill=glow_color
    )

    # Draw brighter inner circle for depth
    inner_padding = padding + size // 20
    inner_size = size - (inner_padding * 2)
    draw.ellipse(
        [inner_padding, inner_padding, inner_padding + inner_size, inner_padding + inner_size],
        fill=bright_color
    )

    # Try to use a good font, fall back to default if not available
    try:
        # Try different font paths
        font_size = int(size * 0.45)
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:\\Windows\\Fonts\\arialbd.ttf",
        ]

        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break

        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Draw "SG" text
    text = "SG"

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    text_x = (size - text_width) // 2 - bbox[0]
    text_y = (size - text_height) // 2 - bbox[1]

    # Draw text shadow for depth
    shadow_offset = max(1, size // 64)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text,
              fill=(0, 0, 50, 200), font=font)

    # Draw main text in white
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    # Apply slight blur for smoothness
    if size > 64:
        img = img.filter(ImageFilter.SMOOTH)

    # Save the image
    img.save(output_path, 'PNG')
    print(f"✓ Generated {output_path} ({size}x{size})")

    return img

def create_ico_file(png_path, ico_path):
    """Convert PNG to ICO format with multiple sizes"""
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img = Image.open(png_path)

    # Create list of images at different sizes
    images = []
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        images.append(resized)

    # Save as ICO
    images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images], append_images=images[1:])
    print(f"✓ Generated {ico_path}")

def main():
    """Generate all required icon sizes"""
    icons_dir = "/home/user/scraper-g1000/scraper-g1000-tauri/src-tauri/icons"

    print("🎨 Generating blue glowing SG logos...\n")

    # Define all required sizes
    icon_sizes = {
        'icon.png': 512,
        '32x32.png': 32,
        '128x128.png': 128,
        '128x128@2x.png': 256,
        'Square30x30Logo.png': 30,
        'Square44x44Logo.png': 44,
        'Square71x71Logo.png': 71,
        'Square89x89Logo.png': 89,
        'Square107x107Logo.png': 107,
        'Square142x142Logo.png': 142,
        'Square150x150Logo.png': 150,
        'Square284x284Logo.png': 284,
        'Square310x310Logo.png': 310,
        'StoreLogo.png': 50,
    }

    # Generate all PNG icons
    for filename, size in icon_sizes.items():
        output_path = os.path.join(icons_dir, filename)
        create_sg_logo(size, output_path)

    # Generate .ico file from the 512px PNG
    print("\n🔄 Converting to .ico format...")
    create_ico_file(
        os.path.join(icons_dir, 'icon.png'),
        os.path.join(icons_dir, 'icon.ico')
    )

    print("\n✅ All icons generated successfully!")
    print("🎯 Blue glowing SG logo is now your app icon")

if __name__ == '__main__':
    main()
