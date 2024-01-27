# untuk menampilkan data berupa json dari db
from flask import jsonify, make_response

# fungsi untuk respon berhasil
def success(values, message):
    res = {
        'data':values,
        'message':message
    }

    return make_response(jsonify(res)),200

# fungsi untuk respon gagal
def badRequest(values, message):
    res = {
        'data':values,
        'message':message
    }

    return make_response(jsonify(res)),400