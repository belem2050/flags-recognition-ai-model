import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt


class FlagRecongnition:

    def __init__(self) -> None:
        pass


    def preprocess_data(self, data_dir, img_size=(128, 128), batch_size=32, validation_split=0.2):

        datagen = ImageDataGenerator(
            rescale=1.0/255.0,
            validation_split=validation_split,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            rotation_range=20
        )

        self.train_generator = datagen.flow_from_directory(
            data_dir,
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training'
        )

        self.validation_generator = datagen.flow_from_directory(
            data_dir,
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation'
        )

    def build_model(self, input_shape, num_classes):
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(num_classes, activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    def fit_model(self, epochs = 25):

        self.history = self.model.fit(
            self.train_generator,
            epochs=epochs,
            validation_data=self.validation_generator
        )

    def evaluate_model(self):

        loss, accuracy = self.model.evaluate(self.validation_generator)
        print(f'loss: {loss}, accurracy: {accuracy}')
    
    def load_model(self, model_path):
        self.model = load_model(model_path)

    
    def save_model(self, path):
        self.model.save(path)

    def plot_history(self):
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['accuracy'], label='train_accuracy')
        plt.plot(self.history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['loss'], label='train_loss')
        plt.plot(self.history.history['val_loss'], label='val_loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

    def predict_image(self, img_path, img_size=(128, 128)):
        img = image.load_img(img_path, target_size=img_size)
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        class_labels = list(self.train_generator.class_indices.keys())
        print(f"The predicted class is: {class_labels[predicted_class]}")


    def get_number_of_classes(self):
        num_classes = len(self.train_generator.class_indices)
        return num_classes

