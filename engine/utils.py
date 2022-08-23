import cv2
import os

def crop_image(image_location, output_location):
    img = cv2.imread(image_location)
    img = cv2.resize(img, (264, 586))
    final_image = img[100:500, 0:220]
    cv2.imwrite(output_location, final_image)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def list_images(directory):
    files = os.listdir(directory)
    images = []

    for file_name in files:
        if file_name.endswith(".png"):
            file_path = os.path.join(directory, file_name)
            file_size = get_file_size(file_path)
            data = {
                "file_name": file_name,
                "file_path": file_path,
                "file_size": file_size,
            }
            images.append(data)  

    return images

def convert_image_to_black_and_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)