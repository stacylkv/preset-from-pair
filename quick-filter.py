# !venv-lut/bin/python3.10
import cv2
import numpy as np
import os
from tqdm import tqdm

def increase_exposure(img, factor=1.5):
    img = img / 255.0
    img = np.power(img, 1 / factor)
    return (img * 255).clip(0, 255).astype(np.uint8)

def increase_brightness(img, delta=30):
    return np.clip(img + delta, 0, 255).astype(np.uint8)

def add_fade(img, amount=20):
    faded = img.astype(np.float32)
    faded = faded * (1 - amount / 100.0) + (amount * 255 / 100.0)
    return np.clip(faded, 0, 255).astype(np.uint8)

def warm_tone(img, warmth=10):
    b, g, r = cv2.split(img.astype(np.float32))
    r += warmth
    b -= warmth / 2
    return np.clip(cv2.merge([b, g, r]), 0, 255).astype(np.uint8)

def tezza_style(img):
    img = increase_exposure(img, factor=1.6)
    img = increase_brightness(img, delta=35)
    #img = add_fade(img, amount=15)
    #img = warm_tone(img, warmth=8)
    return img

def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in tqdm(os.listdir(input_dir)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        input_path = os.path.join(input_dir, filename)
        img = cv2.imread(input_path)
        if img is None:
            print(f"⚠️ Failed to read {filename}, skipping.")
            continue

        adjusted = tezza_style(img)

        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, adjusted)

if __name__ == '__main__':
    process_folder(
        input_dir='input_images',
        output_dir='output_images'  # Можно отключить, если обрабатываешь 300 фото
    )
