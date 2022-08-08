from utils import list_images,crop_image
from tqdm import tqdm

image_list = list_images('mini_dataset/test_image')

for image in tqdm(image_list):
    image_location = image['file_path']
    output_location = "cropped_images/" + image['file_name']
    crop_image(image_location, output_location)
