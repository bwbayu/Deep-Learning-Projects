# file untuk mengatur route website
from flask import jsonify, request, render_template, redirect, url_for, session
from app import app
from joblib import load
import tensorflow as tf
# from tf.keras.preprocessing.image import load_img
from app.controller import UserController, ImageController


# default app menampilkan seluruh isi data dari table user_sentiment
@app.route('/', methods=['GET'])
def index():
    try:
        user_data = UserController.index()
        prediction = session.get('prediction', None)
        session.pop('prediction', None)
        return render_template('index.html', user_data=user_data, prediction=prediction)
    except Exception as e:
        print(e)
        return render_template('error.html', message="An error occurred")

# fungsi untuk memuat model sentimen analisis
def load_model():
    return load('app/utils/ml_model/sentimen_analisis/model_sentimen_210124.joblib')

# route untuk prediksi data baru
@app.route('/predict', methods=['POST'])
def user():
    model = load_model()
    sentiment = UserController.save(model) # fungsi untuk memprediksi data baru dan menambahkannya ke database
    session['prediction'] = sentiment

    return redirect(url_for('index'))

@app.route('/deleteRow/<row_id>', methods=['DELETE'])
def delete_row(row_id):
    result = UserController.delete(row_id)
    return redirect(url_for('index'))

@app.route('/sentiment_analysis')
def sentiment_analysis():
    return "Hello Sentiment analysis"

@app.route('/image_classification')
def image_classification():
    try:
        image_data = ImageController.index()
        prediction = session.get('prediction', None)
        file_name = session.get('file_name', None)
        session.pop('prediction', None)
        session.pop('file_name', None)
        
        return render_template('index_ic.html', image_data=image_data, prediction=prediction, file_name=file_name)
    except Exception as e:
        print(e)
        return render_template('error.html', message="An error occurred")
    
# fungsi untuk memuat model sentimen analisis
def load_model_ic():
    return tf.keras.models.load_model('app/utils/ml_model/image_classification/model_animal.h5')

@app.route('/predict_ic', methods=['POST'])
def predict_ic():
    try:
        model = load_model_ic()
        classes, filename = ImageController.save(model)

        session['prediction'] = classes
        session['file_name'] = filename

        return redirect(url_for('image_classification'))
    except Exception as e:
        print(e)
        return render_template('error.html', message="An error occurred")

@app.route('/deleteRow_ic/<row_id>', methods=['DELETE'])
def delete_row_ic(row_id):
    try:
        result = ImageController.deleteImage(row_id)

        return redirect(url_for('image_classification'))
    except Exception as e:
        print(e)
        return render_template('error.html', message="An error occurred")
    