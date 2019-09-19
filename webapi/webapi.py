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

app = Flask(__name__)
api = Api(app, prefix="/api")
CORS(app)


def getArray(dataurlb64):
    offset = len('data:image/png;base64,')
    dataURL = dataurlb64[offset:]
    binary_data = a2b_base64(dataURL)
    return np.array(Image.open(BytesIO(binary_data)).convert('L'))


def getBase64(pil_img):
    sio = BytesIO()
    pil_img.save(sio, 'PNG', quality=20,optimize=True)
    contents = base64.b64encode(sio.getvalue()).strip()
    sio.close()
    return contents


def array2base64(array):
    im = Image.fromarray(array.astype(np.uint8))
    return 'data:image/png;base64,'+getBase64(im).decode()


class Classify(Resource):
    def post(self):
        data = request.form
        img = getArray(data["inputDataURL"]) 
        return jsonify({"targetDataURL": array2base64(np.rot90(img))})


api.add_resource(Classify, '/post')

if __name__ == '__main__':
   app.run(port=5002, debug=True)