import os
from PIL import Image
import piexif

# target folder
folder_path = "images" # replace with your directory
# target size
new_size = (143, 143)

def resize_image(image_path, output_folder, size):
    img = Image.open(image_path)
    img.thumbnail(size)

    output_path = os.path.join(output_folder, os.path.basename(image_path))
    img.save(output_path)

    # check image extension
    if image_path.lower().endswith(('.jpg', '.jpeg')):
        try:
            # setting EXIF tag
            exif_dict = piexif.load(output_path)
            exif_dict["0th"][piexif.ImageIFD.Make] = "Resized Image"
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, output_path)
        except piexif.InvalidImageDataError:
            print(f"Image {output_path} does not contain valid EXIF data.")
        except Exception as e:
            print(f"Error occurred: {e}")

    # deleting original image after conversion
    os.remove(image_path)

def main():
    # output_folder = os.path.join(folder_path, "Resized")
    output_folder = f"{folder_path}_resized"
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')): # add any other image types if you need
            print("Resizing")
            resize_image(os.path.join(folder_path, filename), output_folder, new_size)
            
if __name__ == "__main__":
    main()
