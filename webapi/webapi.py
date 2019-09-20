from binascii import a2b_base64
import base64
from io import StringIO
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from getClassifier import do_prediction

app = Flask(__name__)
api = Api(app, prefix="/api")
CORS(app)

def getArray(dataurlb64):
    offset = len('data:image/png;base64,')
    dataURL = dataurlb64[offset:]
    binary_data = a2b_base64(dataURL)
    return np.array(Image.open(BytesIO(binary_data)))

def getBase64(pil_img):
    sio = BytesIO()
    pil_img.save(sio, 'PNG', quality=20,optimize=True)
    contents = base64.b64encode(sio.getvalue()).strip()
    sio.close()
    return contents

def array2base64(array):
    im = Image.fromarray(array.astype(np.uint8))
    return 'data:image/png;base64,'+getBase64(im).decode()

input_slice = np.load("input_slice.npy")
target_slice = np.load("target_slice.npy")
input_embedding = np.load("input_embedding.npy")
target_embedding = np.load("target_embedding.npy")

class Classify(Resource):
    def post(self):
        data = request.form
        labels = getArray(data["inputDataURL"]).astype(np.uint8)

        classified = np.rot90(do_prediction(input_embedding, labels, target_embedding))
        return jsonify({"targetDataURL": array2base64(classified)})


print("Seismic loaded")
class Provide(Resource):
    def get(self):

        input_img = (input_slice[0,:,:]+np.abs(input_slice.min()))/(2*input_slice.max())*255
        output_img = (target_slice[0,:,:]+np.abs(input_slice.min()))/(2*input_slice.max())*255

        return jsonify({"targetDataURL": array2base64(np.rot90(input_img)), "inputDataURL":array2base64(np.rot90(output_img))})

api.add_resource(Classify, '/post')
api.add_resource(Provide, '/get')

if __name__ == '__main__':
   app.run(port=5002, debug=True)