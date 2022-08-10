import csv
import cv2
import keras
from utils import convert_image_to_black_and_white, list_images

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

def training_image_batch_generator(image_dir, batch_size):
    image_datas = list_images(image_dir)
    number_of_batches = len(image_datas) // batch_size

    for _ in range(number_of_batches):
        batch_images = []
        
        for _ in range(batch_size):
            image_data = image_datas.pop()
            image_path = image_data['file_path']
            image = cv2.imread(image_path)
            image = convert_image_to_black_and_white(image).tolist()
            batch_images.append(image)
        
        yield batch_images

def training_label_batch_generator(csv_file_path, batch_size):
    parsed_training_csv_file = parse_training_csv(csv_file_path)
    number_of_batches = len(parsed_training_csv_file) // batch_size

    for _ in range(number_of_batches):
        batch_labels = []
        
        for _ in range(batch_size):
            label = parsed_training_csv_file.pop()
            one_hot_encoding = label['one_hot_encoding']
            batch_labels.append(one_hot_encoding)
        
        yield batch_labels


# image = cv2.imread("mini_dataset/train_image/labeled_data/train_00037.png")
# gray = convert_image_to_black_and_white(image).tolist()

# train_images = [ gray ]
# train_labels = [ [1, 0, 0, 0, 0, 0, 0] ]

training_images_path = "mini_dataset/train_image/labeled_data"
training_labels_csv_path = "mini_dataset/train_label/train_label.csv"
batch_size = 10
number_of_batches = get_number_of_images(training_images_path) // batch_size

training_image_batch = training_image_batch_generator(training_images_path, batch_size)
training_label_batch = training_label_batch_generator(training_labels_csv_path, batch_size)

image_width = 1080
image_height = 2400

input_shape = (image_height, image_width, 1)
num_classes = 7

print("[*] Loading first batch of images...")
train_images = next(training_image_batch)
train_labels = next(training_label_batch)

print("[*] Creating model...")
model = create_model(input_shape, num_classes)

print("[*] Training model...")
model.fit(train_images, train_labels, epochs=10) 