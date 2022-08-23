import csv
import cv2
import keras
from utils import convert_image_to_black_and_white, list_images
from pprint import pprint
from tqdm import tqdm
import random

def get_number_of_images(directory):
    images = list_images(directory)
    return len(images)

def one_hot_encode(labels, number_of_class):
    hot_encoding = [0] * number_of_class
    for label in labels:
        label = int(label)
        hot_encoding[label] = 1
    return hot_encoding

def parse_training_csv(csv_file_path):
    NUMBER_OF_CLASSES = 10

    csv_file = open(csv_file_path)
    csv_reader = csv.reader(csv_file)

    images = []
    for row in csv_reader:
        image_name = row[0]
        errors = row[1:]
        data = {
            "image_name": image_name,
            "errors": errors,
            "one_hot_encoding": one_hot_encode(errors, NUMBER_OF_CLASSES)
        }
        images.append(data)
    
    return images

def search_image_name_in_parsed_data(image_name, parsed_data):
    for data in parsed_data:
        data_image_name = data["image_name"]
        if data_image_name == image_name:
            return data
    return None

def create_model(input_shape, num_classes):
    model = keras.models.Sequential([
        keras.layers.Flatten(input_shape=input_shape),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(num_classes, activation='sigmoid')
    ])
    model.compile(
        optimizer='rmsprop',
        loss = "binary_crossentropy",
        metrics=['accuracy']
    )
    return model

def training_batch_generator(training_image_dir, training_label_csv, max_batch_size):
    parsed_csv = parse_training_csv(training_label_csv)
    dir_image_datas = list_images(training_image_dir)

    pre_baked_data = []
    for dir_image_data in dir_image_datas:
        image_name = dir_image_data["file_name"]
        image_path = dir_image_data["file_path"]
        image_size = dir_image_data["file_size"]
        label_data = search_image_name_in_parsed_data(image_name, parsed_csv)

        data = {
            "image_path": image_path,
            "image_size": image_size, # Byte
            "errors": label_data["errors"],
            "one_hot_encoding": label_data["one_hot_encoding"]
        }

        pre_baked_data.append(data)

    max_batch_size_in_byte = max_batch_size * 1080 * 1080
    total_collected_batch_size = 0

    while True:
        print("[*] Loading a new batch")

        baked_batch = []
    
        if len(pre_baked_data) == 0:
            break

        progress_bar = tqdm(total=max_batch_size_in_byte)

        while True:
            if total_collected_batch_size >= max_batch_size_in_byte:
                break

            if len(pre_baked_data) == 0:
                break

            random_pre_baked_data_index = random.randint(0, len(pre_baked_data) - 1)
            random_pre_baked_data = pre_baked_data[random_pre_baked_data_index]
            
            random_image_data = cv2.imread(image_path)
            random_image_data_gray = convert_image_to_black_and_white(random_image_data)
            random_pre_baked_data["image_data"] = random_image_data_gray.tolist()
            
            baked_batch.append(random_pre_baked_data)

            random_image_size = random_pre_baked_data["image_size"]
            total_collected_batch_size += random_image_size

            del pre_baked_data[random_pre_baked_data_index]
            progress_bar.update(random_image_size)

        total_collected_batch_size = 0
        yield baked_batch

    yield None


training_image_dir_path = "cropped_images"
training_label_csv_path = "mini_dataset/train_label/train_label.csv"

training_batch = training_batch_generator(
    training_image_dir = training_image_dir_path,
    training_label_csv = training_label_csv_path,
    max_batch_size = 5 # MB
)

IMAGE_WIDTH = 220
IMAGE_HEIGHT = 400
NUM_OF_CLASSES = 10
EPOCHS = 10

model = create_model(
    input_shape = (IMAGE_HEIGHT, IMAGE_WIDTH),
    num_classes = NUM_OF_CLASSES
)

while True:
    batch = next(training_batch)

    if batch is None:
        break

    print("\n[*] Separating Image Data and One Hot Encoding")
    training_images = [ image_data["image_data"] for image_data in batch ]
    training_labels = [ image_data["one_hot_encoding"] for image_data in batch ]

    print("[*] Fitting Data")
    model.fit(training_images, training_labels, epochs=EPOCHS, validation_split=0.2)