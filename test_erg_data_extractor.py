import pytest
from erg_data_extractor import extract_erg_data
from PIL import Image

def test_extract_erg_data():
    try:
        # Load a sample erg screen image
        img = Image.open("sample_erg_screen.jpeg")
        img.verify()  # Verify that it is, indeed, an image
    except (IOError, SyntaxError) as e:
        pytest.fail(f"Unable to load the image file: {e}")
    
    expected_data = {
        "workout": "5x6:00/2:00r",
    }
    
    extracted_data = extract_erg_data(img)
    
    assert extracted_data == expected_data