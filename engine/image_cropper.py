from utils import list_images,crop_image
from tqdm import tqdm

target_dir = 'mini_dataset/train_image/labeled_data'
image_list = list_images(target_dir)

for image in tqdm(image_list):
    image_location = image['file_path']
    output_location = "cropped_images/" + image['file_name']
    crop_image(image_location, output_location)
