from PIL import Image, ImageDraw
import numpy as np
import os
import sys
from datetime import date
import shutil

# Allow importing from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.progress import get_year_progress

# --- Settings ---
width, height = 800, 100
duration = 3  # seconds
fps = 30

# Directories
base_dir = os.path.dirname(__file__)
output_frames = os.path.join(base_dir, "frames")
output_video = os.path.join(base_dir, "output")
os.makedirs(output_frames, exist_ok=True)
os.makedirs(output_video, exist_ok=True)

# --- Progress ---
today, progress, _, _ = get_year_progress()

# --- Frame generator ---
def make_frame(t):
    progress_now = (t / duration) * progress
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    total_blocks = 100
    block_width, spacing, block_height = 6, 2, height - 5
    filled_blocks = int(progress_now * total_blocks)

    x = (width - (total_blocks * (block_width + spacing) - spacing)) // 2
    y = (height - block_height) // 2

    for i in range(total_blocks):
        color = (0, 0, 0, 255) if i < filled_blocks else (220, 220, 220, 255)
        draw.rectangle([x, y, x + block_width, y + block_height], fill=color)
        x += block_width + spacing

    return np.array(img)

# --- Generate PNG frames ---
for i in range(int(duration * fps)):
    t = i / fps
    frame = make_frame(t)
    frame_path = os.path.join(output_frames, f"frame_{i:04d}.png")
    Image.fromarray(frame).save(frame_path)

# --- Compile to .mov ---
mov_path = os.path.join(output_video, f"progress_bar_{today}.mov")
ffmpeg_cmd = f"""
ffmpeg -y -framerate {fps} -i "{output_frames}/frame_%04d.png" \
-c:v qtrle -pix_fmt argb "{mov_path}"
"""
os.system(ffmpeg_cmd.strip())

# --- Cleanup ---
shutil.rmtree(output_frames)
print(f"✅ Saved: {mov_path}")
