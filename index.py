import wandb
import numpy as np
from wandb.keras import WandbCallback
from engine.model import training_batch_generator, create_model

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

    print(training_images)

    break

    # training_image_single = [ training_images[0] ]
    # training_label_single = [ training_labels[0] ]

    # print(np.array(training_image_single).shape)
    # print(np.array(training_label_single).shape)

    # print("[*] Fitting Data")
    # model.fit(training_image_single, training_label_single, epochs=EPOCHS, validation_split=0.2)

    # break
