import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from flag_recognition import FlagRecongnition

class FlagRecognitionApp:
    def __init__(self):
        root = tk.Tk()
        root.title("Flag Recognition")
        self.flag_recognition = FlagRecongnition()
        self.flag_recognition.preprocess_data('data')


        # Load the trained model
        self.flag_recognition.load_model('model/flag_recognition_model.h5')
        self.class_labels = list(self.flag_recognition.train_generator.class_indices.keys())

        # UI Elements
        self.label = Label(root, text="Select an image to predict the flag", font=("Arial", 16))
        self.label.pack(pady=10)

        self.image_label = Label(root)
        self.image_label.pack(pady=10)

        self.result_label = Label(root, text="", font=("Arial", 14), fg="green")
        self.result_label.pack(pady=10)

        self.select_button = Button(root, text="Select Image", command=self.select_image, font=("Arial", 12))
        self.select_button.pack(pady=10)
        self.root = root


    def select_image(self):
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            # Display the selected image
            img = Image.open(file_path)
            img = img.resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

            # Predict the flag
            self.predict_image(file_path)

    def predict_image(self, img_path):
        # Preprocess the image
        img = image.load_img(img_path, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Make a prediction
        predictions = self.flag_recognition.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        predicted_label = self.class_labels[predicted_class]

        # Display the result
        self.result_label.config(text=f"Predicted Flag: {predicted_label}")


if __name__ == "__main__":
    # Prepare the flag recognition model
    # flag_recognition = FlagRecongnition()
    # flag_recognition.preprocess_data('data')

    # Create the Tkinter app
    app = FlagRecognitionApp()
    app.root.mainloop()
