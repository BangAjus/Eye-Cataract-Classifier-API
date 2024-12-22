import cv2
import numpy as np
import tensorflow as tf
import base64
import os
from app.config import UPLOAD_FOLDER

model_path = 'C:\Projek Dajjal\Biomedics Project\Eye Cataract Classifier TF/results\model\model1_2024-12-20.h5'
model = tf.keras.models.load_model(model_path)

def base64_conv(string):

    try:
        string = string.split(",")[1]
        image_data = base64.b64decode(string)

        output_path = os.path.join(UPLOAD_FOLDER, "output_image.jpg")
        with open(output_path, "wb") as file:
            file.write(image_data)

        print(f"Image saved as {output_path}")
        return True
    
    except:
        return False

def crop_pupil(img_path):

    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    image_blurred = cv2.GaussianBlur(image, (7, 7), 0)
    
    _, thresh = cv2.threshold(image_blurred,
                              50, 255, 
                              cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh,
                                   cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)
    pupil_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(pupil_contour)

    pupil_roi = image[y:y+h, x:x+w]
    pupil_roi = cv2.resize(pupil_roi, (128, 128))

    return pupil_roi

def cataract_prediction(image):

    image = crop_pupil(image)
    image = image / 255.0  
    image = np.expand_dims(image, axis=0) 
    
    predictions = model.predict(image)
    class_names = ['katarak_immatur', 'katarak_matur', 'mata_normal']  
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class = class_names[predicted_class_index]

    return predicted_class