from flask import Flask, request, jsonify
from keras.preprocessing import image
from itertools import compress
from io import BytesIO
from keras_applications import inception_v3
import base64, json, requests, numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/hello/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'


@app.route('/homeappliance/predict/', methods=['POST'])
def home_appliance():
    img = image.img_to_array(image.load_img(BytesIO(base64.b64decode(request.form['b64'])),
                                            target_size=(224, 224))) / 255.

    payload = {
        "instances": [{'input_image': img.tolist()}]
    }

    r = requests.post('http://163.122.226.25:9001/v1/models/ApplianceDamageAnalyzer:predict', json=payload)

    classes = ['building', 'minor', 'moderate', 'nodamage', 'severe', 'vehicle']

    pred = json.loads(r.content.decode('utf-8'))

    return jsonify(inception_v3.decode_predictions(np.array(pred['predictions'])))


@app.route('/vehiclebuilding/predict/', methods=['POST'])
def vehicle_building():
    img = image.img_to_array(image.load_img(BytesIO(base64.b64decode(request.form['b64'])),
                                            target_size=(224, 224))) / 255.

    payload = {
        "instances": [{'input_image': img.tolist()}]
    }

    r = requests.post('http://163.122.226.25:9000/v1/models/DamageAnalyzer:predict', json=payload)

    classes = ['building', 'minor', 'moderate', 'nodamage', 'severe', 'vehicle']
    pred = json.loads(r.content.decode('utf-8'))

    # filtr = np.vectorize(lambda x: 1 if x > 0.5 else 0)(pred['predictions'])[0]
    # response = {'predicitons': list(compress(classes, filtr))}

    sorted_preds = list(zip(classes, np.array(pred['predictions'][0]).tolist()))
    sorted_preds.sort(key=lambda x: -x[1])

    return jsonify(sorted_preds)
