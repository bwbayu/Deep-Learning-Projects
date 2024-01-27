from app.model.user_image import UserImage
from app import response, app, db
from flask import request
import os
import tensorflow as tf
import numpy as np

def index():
    try:
        user = UserImage.query.all()
        datas = []
        for data in user:
            datas.append({
                'id': data.id,
                'image': data.image,
                'classes': data.classes
            })
        return datas
    except Exception as e:
        print(e)
        return []

animal_dict = {0: "cat", 1: "dog", 2: "elephant", 3: "horse", 4: "lion"}
def save(model):
    try:
        imagefile = request.files['imagefile']
        filename = imagefile.filename
        # error handling gaada image yg dipilih
        if(filename == ''):
            return "empty", "Not Selected"
        
        # error handling beda format image
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if imagefile.filename.split('.')[-1].lower() not in allowed_extensions:
            return "not image format", "Different Format"


        imagepath = os.path.join('app\\static', filename)
        if not os.path.exists(imagepath):
            imagefile.save(imagepath)
        # PREPROCESSING
        image = tf.keras.utils.load_img(imagepath, target_size=(224, 224))
        input_arr = tf.keras.utils.img_to_array(image)
        input_arr = np.array([input_arr])/255.0
        predictions = model.predict(input_arr)[0]
        model_output = np.array(predictions)
        max_index = np.argmax(model_output)
        result = animal_dict[max_index]
        # PREDICT
        image = UserImage(image=filename, classes=result)
        db.session.add(image)
        db.session.commit()
        return str(result), str(filename)
    except Exception as e:
        print(e)
        return response.badRequest([], "An error occurred")

def deleteImage(id):
    try:
        row = UserImage.query.get(id)
        if row:
            db.session.delete(row)
            db.session.commit()
            return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False, 'error': 'Row not found'}