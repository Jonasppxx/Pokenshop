import os
from PIL import Image, ExifTags

def resize_image(image_path, output_path, target_width=500):
    with Image.open(image_path) as img:
        # Correct orientation based on EXIF data
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(orientation, 1)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Cases: image don't have getexif
            pass

        # Calculate the new height to maintain the aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(target_width * aspect_ratio)

        # Resize the image
        img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        img.save(output_path)

def process_images(input_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                image_path = os.path.join(root, file)
                output_path = image_path  # Overwrite the original image
                resize_image(image_path, output_path)

if __name__ == "__main__":
    input_folder = 'images'
    process_images(input_folder)