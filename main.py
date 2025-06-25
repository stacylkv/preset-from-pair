# !venv-lut/bin/python3.10
import cv2
import numpy as np
import os
import pickle
from sklearn.neighbors import KNeighborsRegressor
from tqdm import tqdm
import matplotlib.pyplot as plt

def extract_pixels(image, sample_rate=0.05):
    pixels = image.reshape(-1, 3)
    num_samples = int(len(pixels) * sample_rate)
    idx = np.random.choice(len(pixels), size=num_samples, replace=False)
    return pixels[idx]

def build_lut(source_img, target_img, sample_rate=0.05):
    source_pixels = extract_pixels(source_img, sample_rate)
    target_pixels = extract_pixels(target_img, sample_rate)
    
    model = KNeighborsRegressor(n_neighbors=3, weights='distance')
    model.fit(source_pixels, target_pixels)
    return model

def apply_lut(image, model):
    h, w, _ = image.shape
    flat_img = image.reshape(-1, 3)
    transformed = model.predict(flat_img)
    transformed = np.clip(transformed, 0, 255)
    return transformed.reshape(h, w, 3).astype(np.uint8)

def process_folder(input_dir, output_dir, model, show_preview=False):
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in tqdm(os.listdir(input_dir)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        path = os.path.join(input_dir, filename)
        img = cv2.imread(path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        transformed = apply_lut(img_rgb, model)
        
        # Визуальное сравнение
        if show_preview:
            show_comparison(img_rgb, transformed, filename)
        
        transformed_bgr = cv2.cvtColor(transformed, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(output_dir, filename), transformed_bgr)

def show_comparison(before, after, title="Preview"):
    combined = np.hstack((before, after))
    plt.figure(figsize=(12, 6))
    plt.imshow(combined)
    plt.axis('off')
    plt.title(f'{title} — Before | After')
    plt.show()

def save_lut(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def load_lut(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

# ---------------------
# 🔧 Запуск
# ---------------------
if __name__ == '__main__':
    source = cv2.imread('original.jpg')
    target = cv2.imread('target.jpg')
    
    source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    
    model = build_lut(source, target)
    
    # Сохраняем LUT
    save_lut(model, 'lut_model.pkl')
    
    # Применяем LUT к папке
    process_folder(
        input_dir='input_images',
        output_dir='output_images',
        model=model,
        show_preview=True  # покажет до/после в окне
    )
