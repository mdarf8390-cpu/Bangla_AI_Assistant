import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

print("Tesseract Path:")
print(pytesseract.pytesseract.tesseract_cmd)

print("\nVersion:")
print(pytesseract.get_tesseract_version())

print("\nTaking Screenshot...")

image = ImageGrab.grab()

print("Running OCR...")

text = pytesseract.image_to_string(image)

print("\nOCR Result:")
print(text[:500])