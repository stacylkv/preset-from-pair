import cv2
import numpy as np
import os
from tqdm import tqdm

# 🎨 Warmth — корректный холод/тепло сдвиг
def apply_warmth(img, warmth):
    b, g, r = cv2.split(img.astype(np.float32))
    factor = warmth / 100.0  # нормализуем от -1 до +1

    # Tezza-like: теплее → больше R, холоднее → больше B
    r += 30 * factor         # максимум ±30
    b -= 20 * factor         # максимум ∓20

    img = cv2.merge([b, g, r])
    return np.clip(img, 0, 255).astype(np.uint8)

# 📸 Применяем iPhone-стиль к изображению 
def apply_iphone_style(img, exposure=0.8, brightness=35, brilliance=0.5, warmth=-35):
    img = img.astype(np.float32)

    # 📸 Exposure — умножение midtones
    img *= 1 + exposure

    # 💡 Brightness — сдвигаем вверх
    img += brightness

    # 🌤 Brilliance — мягкое поднятие теней
    shadows = img < 128
    img[shadows] += brilliance * (128 - img[shadows])

    # 🎨 Warmth — вызываем отдельно
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
            exposure=0.8,     # +80% света
            brightness=35,    # +35 яркости
            brilliance=0.5,   # лёгкий мягкий контраст
            warmth=-35        # холоднее
        )

        cv2.imwrite(os.path.join(output_dir, filename), adjusted)

if __name__ == '__main__':
    process_folder('input_images', 'output_images')
