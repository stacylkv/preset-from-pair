# !venv-lut/bin/python3.10
import cv2
import numpy as np
import os
from tqdm import tqdm

# Warmth — color temperature adjustment
def apply_warmth(img, warmth):
    b, g, r = cv2.split(img.astype(np.float32))
    factor = warmth / 100.0  # normalize warmth to [0, 1]
    # Tezza-like: warm up reds and cool down blues
    r += 30 * factor         # max ±30
    b -= 20 * factor         # max ∓20

    img = cv2.merge([b, g, r])
    return np.clip(img, 0, 255).astype(np.uint8)

# Apply iPhone-style adjustments
# - Exposure: increase midtones
# - Brightness: shift up
# - Brilliance: soft lift of shadows
# - Warmth: adjust color temperature
def apply_iphone_style(img, exposure=0.8, brightness=35, brilliance=0.5, warmth=-35):
    img = img.astype(np.float32)

    # Exposure — multiply midtones
    img *= 1 + exposure

    # Brightness — moving up the entire image
    img += brightness

    # Brilliance — soften shadows
    shadows = img < 128
    img[shadows] += brilliance * (128 - img[shadows])

    # Warmth — calling the warmth function
    img = apply_warmth(img, warmth)

    return np.clip(img, 0, 255).astype(np.uint8)

def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in tqdm(os.listdir(input_dir)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        path = os.path.join(input_dir, filename)
        img = cv2.imread(path)

        adjusted = apply_iphone_style(
            img,
            exposure=0.8,     # +80% light exposure
            brightness=35,    # +35 brightness
            brilliance=0.5,   # lighten shadows by 50%
            warmth=-35        # cool down by 35
        )

        cv2.imwrite(os.path.join(output_dir, filename), adjusted)

if __name__ == '__main__':
    process_folder('input_images', 'output_images')
      