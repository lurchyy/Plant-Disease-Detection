from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from time import sleep
import os
import numpy as np
import cv2
import glob

model = load_model('main_model.h5')
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])

def delete_images():
    folder_path = "static/img"

    # List all files in the folder
    files = os.listdir(folder_path)
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)


app = Flask(__name__)

app.config['SECRET_KEY'] = '68fc6950751c97a96d0541332788a58e'
app.config['UPLOAD_FOLDER'] = "static/img"

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload")

class CaptureFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Capture")

def predict_disease(test_image):
    img = cv2.imread(test_image)
    img = img / 255.0
    img = cv2.resize(img, (128, 128))
    img = img.reshape(1, 128, 128, 3)
    prediction = model.predict(img)
    pred_class = np.argmax(prediction, axis=-1)
    # List Of Classes
    Plant_disease = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',      'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',  'Tomato___healthy']
    
    for i in range(len(Plant_disease)):
        plant, disease = Plant_disease[i].split("___")
        regularised_disease = ""
        for j in range(len(disease)):
            if disease[j] == "_":
                regularised_disease += " "
            else:
                regularised_disease += disease[j]
        Plant_disease[i] = {"plant":plant, "disease":regularised_disease}
    res=Plant_disease[pred_class[0]]

    return res

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    delete_images()
    return render_template("capture.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    delete_images()
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename("leaf.jpg")))
        return redirect(url_for('uploaded'))
    return render_template("upload.html", form=form)

@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    sleep(1)
    if not os.listdir('static/img'):
        return redirect('upload')
    return render_template("uploaded.html")

@app.route('/captured', methods=['GET', 'POST'])
def captured():
    sleep(1)
    if not os.listdir('static/img'):
        return redirect('capture')
    jpg_files = glob.glob("static/img/*.jpg")
    image_path = os.path.join(jpg_files[0])
    return render_template("captured.html", file={'image':image_path})

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    jpg_files = glob.glob("static/img/*.jpg")
    image_path = os.path.join(jpg_files[0])
    results = predict_disease(image_path)
    return render_template("prediction.html", prediction={'results':results, 'image':image_path})


if __name__ == '__main__':
    app.run(debug=True)
