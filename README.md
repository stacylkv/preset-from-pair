# 🎨 Preset-From-Pair — Generate a LUT from Before/After Images

This script allows you to **create a LUT model (color transformation)** from a pair of images — a raw image (`before`) and its edited version (`after`, e.g. from Tezza or VSCO) — and then **apply that color style to an entire folder of images**.

---

## 📂 What the Script Does

1. Loads a pair of images: `original.jpg` (before editing) and `target.jpg` (after editing).
2. Builds a LUT model based on the color differences between them.
3. Applies the LUT to every image in the `input_images/` folder.
4. Saves the results in the `output_images/` folder.
5. (Optional) Displays a side-by-side **Before/After preview**.

---

## 🚀 How to Use

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Prepare the following files/folders:
   - `original.jpg` — original image (unprocessed)
   - `target.jpg` — edited version with your desired style
   - `input_images/` — folder with images you want to style

3. Run the script:
   ```bash
   python main.py
   ```

4. The styled images will appear in the `output_images/` folder.

---

## 🧪 Example Use Case

- `original.jpg`: raw photo from your camera
- `target.jpg`: styled photo from Tezza or another app
- The script "learns" the aesthetic from `target` and applies it to others

---

## 🧠 Features

- Saves the LUT model to `lut_model.pkl`
- Reuse the LUT by loading it later with `load_lut(path)`
- Displays Before/After comparison with matplotlib
- Fast and customizable

---

## 📦 Dependencies

Use the following `requirements.txt`:

```
numpy>=1.24
opencv-python>=4.8
matplotlib>=3.7
tqdm>=4.65
scikit-learn>=1.3
```

---

## 🧊 Potential Improvements

- Export to `.cube` LUT format
- Support for video input
- GUI for non-programmers

---

## 📸 Author

Built for creative workflows and quick aesthetic color transfer between images.  
Useful for automating styles inspired by apps like Instagram, Tezza, VSCO, and more.
