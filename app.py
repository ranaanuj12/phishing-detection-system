from flask import Flask, request, jsonify
from model import model

app = Flask(_name_)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    features = [[
        data['length'],
        data['hasHttps'],
        data['hasAt'],
        data['hasHyphen']
    ]]

    prediction = model.predict(features)[0]

    result = "PHISHING" if prediction == 1 else "SAFE"

    return jsonify(result)

if _name_ == '_main_':
    app.run(port=5000)