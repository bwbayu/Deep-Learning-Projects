from app.model.user_sentiment import UserSentimen
from app import response, app, db
from flask import request
from app.utils.preprocessing import data_preprocessing

# fungsi untuk mengambil data user review
def index():
    try:
        user = UserSentimen.query.all() # query select *
        data = formatarray(user) # ubah ke format dictionary
        return data
    except Exception as e:
        print(e)
        return []

# menampung data dari db dalam array
def formatarray(datas):
    array = []
    for data in datas: # hasil querynya diiterasi kemudian diubah ke format dictionary kemudian ditampung dalam array
        array.append(singleObject(data))

    return array

# representasi data user sentimen berdasarkan table user_sentiment di database
def singleObject(data):
    data = {
        'id' : data.id,
        'review': data.review,
        'sentiment': data.sentiment
    }
    return data

classes = ["Negative", "Positive"]
# fungsi untuk melakukan prediksi terhadap data baru dan menyimpannya di database
def save(model):
    # bikin error handling klo textnya gaada
    try:
        review = request.form.get('review') # ambil text review dari form
        if(review == ''):
            return "empty because text is empty"
        clean_review = data_preprocessing(review) # data text di preprocessing
        sentiment = model.predict([clean_review])[0] # data dimasukkan ke model 
        users = UserSentimen(review = review, sentiment=classes[sentiment]) # mengisi column review dan sentiment pada model userSentimen
        # add dan commit ke database
        db.session.add(users)
        db.session.commit()

        return str(classes[sentiment]) #  mengembalikan value sentiment untuk di tampilkan pada website
    except Exception as e:
        print(e)
        return response.badRequest([], "An error occurred")

def delete(id):
    try:
        row = UserSentimen.query.get(id)
        if row:
            db.session.delete(row)
            db.session.commit()
            return {'success': True}

    except Exception as e:
        print(e)
        return {'success': False, 'error': 'Row not found'}