"""
Create a cute icon for Mathmagotchi
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 icon (high resolution for retina displays)
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a cute rounded square background (like a tamagotchi device)
margin = 20
bg_color = (255, 182, 217)  # Soft pink
draw.rounded_rectangle([margin, margin, size-margin, size-margin],
                       radius=40, fill=bg_color)

# Draw inner screen (purple border)
border_width = 12
screen_margin = margin + 25
border_color = (74, 20, 140)  # Purple
draw.rounded_rectangle([screen_margin, screen_margin, size-screen_margin, size-screen_margin],
                       radius=30, fill=border_color)

# Draw screen content (yellow/cream)
screen_inner = screen_margin + border_width
screen_color = (255, 249, 196)  # Light yellow
draw.rounded_rectangle([screen_inner, screen_inner, size-screen_inner, size-screen_inner],
                       radius=20, fill=screen_color)

# Try to draw cute math symbols
try:
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 80)
        small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        small_font = font

    # Draw cute math symbols in the screen
    text_color = (107, 27, 154)  # Purple

    # Draw ∑ (sigma - summation symbol) or use emoji
    center_x = size // 2
    center_y = size // 2 - 10

    # Draw main math symbol
    draw.text((center_x, center_y), "🧮", font=font, fill=text_color, anchor="mm")

    # Draw small decorative elements
    draw.text((center_x - 40, center_y + 45), "∑", font=small_font, fill=text_color, anchor="mm")
    draw.text((center_x + 40, center_y + 45), "∫", font=small_font, fill=text_color, anchor="mm")

except Exception as e:
    print(f"Font rendering issue: {e}")
    # Draw simple shapes as fallback
    center = size // 2
    draw.ellipse([center-30, center-30, center+30, center+30], fill=(107, 27, 154))

# Save the icon
icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
img.save(icon_path, 'PNG')
print(f"Icon saved to: {icon_path}")

# Also create smaller versions for better scaling
for icon_size in [512, 256, 128, 64, 32, 16]:
    resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    resized.save(icon_path.replace('.png', f'_{icon_size}.png'), 'PNG')

print("All icon sizes created!")
