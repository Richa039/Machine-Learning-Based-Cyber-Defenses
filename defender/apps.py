import lief
import pandas as pd
from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from defender.models.our_attr_extractor import CustomPEExtractor

def create_app(model, vect):
    app = Flask(__name__)
    app.config['model'] = model
    app.config['vect'] = vect
    # analyse a sample
    @app.route('/', methods=['POST'])
    def post():
        # curl -XPOST --data-binary @somePEfile http://127.0.0.1:8080/ -H "Content-Type: application/octet-stream"
        if request.headers['Content-Type'] != 'application/octet-stream':
            resp = jsonify({'error': 'expecting application/octet-stream'})
            resp.status_code = 400  # Bad Request
            return resp

        bytez = request.data

        try:
            # initialize feature extractor with bytez
            vect = app.config['vect']
            pe_att_ext = CustomPEExtractor(bytez, vect)
            # extract PE attributes
            tokens = pe_att_ext.extract()

            model = app.config['model']

            # query the model
            y_pred_prob = model.predict_proba(tokens)
            # print(y_pred_prob)
            result = (y_pred_prob[:, 1] > 0.9).astype(int)
            # [0.1, 0.9]
            print('LABEL = ', result)
        except Exception as e:
            print("Error:", e)
            result = 1


        # if not isinstance(result, int) or result not in {0, 1}:
        #     resp = jsonify({'error': 'unexpected model result (not in [0,1])'})
        #     resp.status_code = 500  # Internal Server Error
        #     return resp

        resp = jsonify({'result': int(result[0])})
        resp.status_code = 200
        return resp

    # get the model info
    @app.route('/model', methods=['GET'])
    def get_model():
        # curl -XGET http://127.0.0.1:8080/model
        resp = jsonify(app.config['model'].model_info())
        resp.status_code = 200
        return resp

    return app
