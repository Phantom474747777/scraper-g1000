"""
Generate professional Scraper G1000 icon
Lightning bolt inside light bulb with electric blue gradient
"""

from PIL import Image, ImageDraw
import math

def create_icon():
    """Create a stunning app icon"""

    # Create 256x256 image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ===== BACKGROUND: Electric Blue Gradient Circle =====
    center_x, center_y = size // 2, size // 2
    max_radius = 118

    # Draw gradient circles from outside to inside
    for i in range(100):
        progress = i / 100
        radius = int(max_radius * (1 - progress * 0.3))

        # Electric blue to purple gradient
        r = int(20 + progress * 80)      # 20 -> 100
        g = int(40 + progress * 160)     # 40 -> 200
        b = int(100 + progress * 155)    # 100 -> 255
        alpha = int(200 + progress * 55) # 200 -> 255

        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    fill=(r, g, b, alpha))

    # Outer glow ring
    for i in range(8):
        alpha = int(100 - i * 12)
        draw.ellipse([center_x - max_radius - i*2, center_y - max_radius - i*2,
                     center_x + max_radius + i*2, center_y + max_radius + i*2],
                    outline=(0, 200, 255, alpha), width=2)

    # Main border ring
    draw.ellipse([center_x - max_radius, center_y - max_radius,
                 center_x + max_radius, center_y + max_radius],
                outline=(0, 230, 255, 255), width=4)

    # ===== LIGHT BULB =====
    # Bulb glass (rounded top)
    bulb_top = 70
    bulb_bottom = 160
    bulb_left = center_x - 45
    bulb_right = center_x + 45

    # Glass bulb with gradient
    for i in range(30):
        alpha = int(180 - i * 3)
        offset = i
        draw.ellipse([bulb_left + offset, bulb_top + offset,
                     bulb_right - offset, bulb_bottom - offset//2],
                    outline=(200, 230, 255, alpha), width=1)

    # Main bulb outline
    draw.ellipse([bulb_left, bulb_top, bulb_right, bulb_bottom],
                outline=(220, 240, 255, 255), width=3)

    # Bulb base (screw threads)
    base_top = bulb_bottom - 5
    base_height = 25
    thread_width = bulb_right - bulb_left

    # Draw screw threads
    for i in range(4):
        y = base_top + i * 6
        draw.rectangle([bulb_left, y, bulb_right, y + 3],
                      fill=(180, 180, 200, 255))
        draw.rectangle([bulb_left, y + 3, bulb_right, y + 5],
                      fill=(140, 140, 160, 255))

    # Bottom cap
    cap_y = base_top + base_height
    draw.ellipse([bulb_left - 3, cap_y - 3, bulb_right + 3, cap_y + 8],
                fill=(160, 160, 180, 255))
    draw.ellipse([bulb_left - 2, cap_y - 2, bulb_right + 2, cap_y + 6],
                fill=(200, 200, 220, 255))

    # ===== LIGHTNING BOLT (Inside Bulb) =====
    # Electric yellow lightning with glow
    bolt_scale = 0.8
    lightning = [
        (center_x - 8*bolt_scale, 85),           # Top
        (center_x + 8*bolt_scale, 110),          # Upper right
        (center_x, 110),                         # Upper middle
        (center_x + 12*bolt_scale, 135),         # Middle right
        (center_x + 3*bolt_scale, 135),          # Middle center
        (center_x + 10*bolt_scale, 155),         # Lower right
        (center_x - 5*bolt_scale, 125),          # Lower left
        (center_x + 3*bolt_scale, 125),          # Lower middle
        (center_x - 8*bolt_scale, 85),           # Back to top
    ]

    # Glow effect
    for glow in range(15, 0, -1):
        alpha = int(150 - glow * 8)
        glow_bolt = [(x + (glow/3 if x > center_x else -glow/3), y) for x, y in lightning]
        draw.polygon(glow_bolt, fill=(255, 255, 100, alpha))

    # Main lightning bolt
    draw.polygon(lightning, fill=(255, 240, 0, 255))

    # Bright highlight on lightning
    highlight = [
        (center_x - 6*bolt_scale, 90),
        (center_x + 5*bolt_scale, 110),
        (center_x - 1*bolt_scale, 110),
        (center_x - 6*bolt_scale, 90),
    ]
    draw.polygon(highlight, fill=(255, 255, 220, 200))

    # ===== GLOW RAYS (from lightning) =====
    num_rays = 8
    for i in range(num_rays):
        angle = (i / num_rays) * 2 * math.pi
        for length in range(20, 5, -2):
            x_end = center_x + math.cos(angle) * length
            y_end = 120 + math.sin(angle) * length
            alpha = int(100 - length * 3)
            draw.line([center_x, 120, x_end, y_end],
                     fill=(255, 255, 150, alpha), width=2)

    # ===== TEXT: "G1000" =====
    # Draw at bottom
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    text = "G1000"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    text_y = 200

    # Text shadow
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 180))
    # Main text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
    # Text highlight
    draw.text((text_x - 1, text_y - 1), text, font=font, fill=(200, 240, 255, 100))

    # ===== SAVE AS ICO =====
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []

    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)

    output_path = 'scraper_icon.ico'
    images[0].save(output_path, format='ICO', sizes=[s for s in icon_sizes])

    # Also save as PNG for preview
    img.save('icon_preview.png', 'PNG')

    print("=" * 60)
    print("ICON CREATED!")
    print("=" * 60)
    print()
    print("Design:")
    print("  💡 Light bulb with glass effect")
    print("  ⚡ Electric yellow lightning bolt inside")
    print("  🌀 Electric blue gradient background")
    print("  ✨ Glowing rays and effects")
    print("  📝 G1000 branding text")
    print()
    print("Files created:")
    print(f"  - {output_path} (Windows icon)")
    print("  - icon_preview.png (preview image)")
    print()
    print("=" * 60)

    return output_path

if __name__ == "__main__":
    create_icon()
