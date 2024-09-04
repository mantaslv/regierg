import exifread
from datetime import datetime

def get_image_date(image_path):
	with open(image_path, 'rb') as img_file:
		tags = exifread.process_file(img_file)
		date_taken = tags.get('EXIF DateTimeOriginal')
		if date_taken:
			return datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S')
		else:
			return "Date not available in EXIF data"

image_path = 'screen_images/test5.jpg'
all_metadata = get_image_date(image_path)
print(all_metadata)
