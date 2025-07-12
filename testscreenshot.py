import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
from PIL import Image

img_path = "test_screenshot.png"
cv2_image = cv2.imread(img_path)
if cv2_image is None:
    raise FileNotFoundError(f"Görsel bulunamadı: {img_path}")

# Gri ton + 4x büyütme
gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
gray = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

# Hafif blur
gray = cv2.GaussianBlur(gray, (3, 3), 0)

# Otsu threshold
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Invert thresh de dene
thresh_inv = cv2.bitwise_not(thresh)

# Büyük kernel ile morfolojik işlemler
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
thresh_inv = cv2.morphologyEx(thresh_inv, cv2.MORPH_CLOSE, kernel)
thresh_inv = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, kernel)

# OCR ayarları
psm_modes = [6, 7, 11, 13, 8]
results = []
for img, label in [(thresh, 'normal'), (thresh_inv, 'invert')]:
    pil_image = Image.fromarray(img)
    for psm in psm_modes:
        config = f'--oem 1 --psm {psm} -c tessedit_char_whitelist=0123456789 '
        result = pytesseract.image_to_string(pil_image, lang='eng', config=config)
        print(f"OCR ({label}, PSM {psm}): {repr(result)}")
        results.append((label, psm, result))

# En çok rakam içeren sonucu seç
best = max(results, key=lambda x: sum(c.isdigit() for c in x[2]))
print(f"Seçilen Sonuç ({best[0]}, PSM {best[1]}): {repr(best[2])}")

