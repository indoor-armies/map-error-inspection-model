import os
import csv
from tqdm import tqdm
from pprint import pprint
import random
import shutil

MAX_TRAIN_DATASET_SIZE = 750 # MB
MAX_TEST_DATASET_SIZE = 250   # MB

# Creating necessary folders

print("[*] Creating necessary folders")

if not os.path.exists('mini_dataset'):
    os.makedirs('mini_dataset')

if not os.path.exists('mini_dataset/train_image'):
    os.makedirs('mini_dataset/test_image')

if not os.path.exists('mini_dataset/train_image/labeled_data'):
    os.makedirs('mini_dataset/train_image/labeled_data')

if not os.path.exists('mini_dataset/train_label'):
    os.makedirs('mini_dataset/train_label')


# Parsing train_labels.csv

print("[*] Parsing train_labels.csv")

train_label_file = open("dataset/train_label/train_label.csv")
csv_reader = csv.reader(train_label_file)

images = []

for row in csv_reader:
    image_name = row[0]
    errors = row[1:]

    image_path = os.path.join("dataset/train_image/labeled_data", image_name)
    image_stats = os.stat(image_path)
    image_size = image_stats.st_size / (1024 * 1024) # MB
    
    data = {
        "image_name": image_name,
        "image_path": image_path,
        "image_size": image_size,
        "errors": errors
    }

    images.append(data)

# Randomly selecting images from train_label.csv upto MAX_TRAIN_DATASET_SIZE

print("[*] Randomly selecting images from train_label.csv upto MAX_TRAIN_DATASET_SIZE")

total_train_image_collected_size = 0
randomly_collected__train_image_sample = []

while True:
    if total_train_image_collected_size > MAX_TRAIN_DATASET_SIZE:
        break

    random_index = random.randint(0, len(images) - 1)
    random_image = images[random_index]
    del images[random_index]
    randomly_collected__train_image_sample.append(random_image)
    total_train_image_collected_size += random_image["image_size"]

# Creating Sampled Train Image Dataset

print("[*] Creating Sampled Train Image Dataset")

for image in tqdm(randomly_collected__train_image_sample):
    target_path = "mini_dataset/train_image/labeled_data"
    image_name = image["image_name"]
    image_path = image["image_path"]
    shutil.copy(image_path, os.path.join(target_path, image_name))

# Creating Sample Train Label Csv

print("[*] Creating Sample Train Label Csv")

sample_train_label_file = open("mini_dataset/train_label/train_label.csv", "w")
csv_writer = csv.writer(sample_train_label_file)

for image in tqdm(randomly_collected__train_image_sample):
    image_name = image["image_name"]
    errors = image["errors"]
    csv_writer.writerow([image_name] + errors)

# Randomly selecting images from test_images folder upto MAX_TEST_DATASET_SIZE

print("[*] Randomly selecting images from test_images folder upto MAX_TEST_DATASET_SIZE")

total_test_image_collected_size = 0
randomly_collected_test_image_sample = []

test_image_dataset_path = "dataset/test_image"
image_names = [ image_name for image_name in os.listdir(test_image_dataset_path) 
                if image_name.endswith(".png") ]

while True:
    if total_test_image_collected_size > MAX_TEST_DATASET_SIZE:
        break

    random_index = random.randint(0, len(image_names) - 1)
    random_image_name = image_names[random_index]
    random_image_path = os.path.join(test_image_dataset_path, random_image_name)
    random_image_stats = os.stat(random_image_path)
    random_image_size = random_image_stats.st_size / (1024 * 1024) # MB
    del image_names[random_index]

    total_test_image_collected_size += random_image_size

    data = {
        "image_name": random_image_name,
        "image_path": random_image_path,
        "image_size": random_image_size
    }

    randomly_collected_test_image_sample.append(data)

# Creating Sampled Test Image Dataset

print("[*] Creating Sampled Test Image Dataset")

for image in tqdm(randomly_collected_test_image_sample):
    target_path = "mini_dataset/test_image"
    image_name = image["image_name"]
    image_path = image["image_path"]
    shutil.copy(image_path, os.path.join(target_path, image_name))    