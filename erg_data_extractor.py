import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    
    width, height = image.size
    new_size = (width * 4, height * 4)
    image = image.resize(new_size, Image.Resampling.LANCZOS)

    return image

def extract_erg_data(image_path):
    img = preprocess_image(image_path)
    text = pytesseract.image_to_string(img)
    return text

if __name__ == "__main__":
    image_path = 'sample_erg_screen.jpeg'
    extracted_data = extract_erg_data(image_path)
    print(extracted_data)