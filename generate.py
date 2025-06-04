from datetime import datetime, date
from PIL import Image, ImageDraw
import os

# --- Settings ---
width = 800
height = 50
total_blocks = 100
block_width = 6
block_spacing = 2
block_height = 40
bg_color = (255, 255, 255)
fill_color = (0, 0, 0)

# --- Calculate year progress ---
today = date.today()
start = date(today.year, 1, 1)
end = date(today.year + 1, 1, 1)
days_in_year = (end - start).days
days_passed = (today - start).days
progress_pct = days_passed / days_in_year
blocks_filled = int(progress_pct * total_blocks)

# --- Create image ---
img = Image.new("RGB", (width, height), bg_color)
draw = ImageDraw.Draw(img)

x = (width - (total_blocks * (block_width + block_spacing) - block_spacing)) // 2
y = (height - block_height) // 2

for i in range(total_blocks):
    color = fill_color if i < blocks_filled else (220, 220, 220)
    draw.rectangle([x, y, x + block_width, y + block_height], fill=color)
    x += block_width + block_spacing

# --- Save image ---
os.makedirs("output", exist_ok=True)
filename = f"output/progress_bar_{today}.png"
img.save(filename)
print(f"✅ Progress bar saved to: {filename}")
