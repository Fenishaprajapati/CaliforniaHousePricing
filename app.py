import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app=Flask(__name__)

#Load the model
regmodel=pickle.load(open('regmodel.pkl','rb'))
scalar=pickle.load(open('scaler.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/predict_api', methods=['POST'])
# def predict_api():
#     data=request.json['data']
#     print(data)
#     print(np.array(list(data.values()))).reshape(1,-1)
#     new_data=scalar.transform(np.array(list(data.values()))).reshape(1,-1)
#     output=regmodel.predict(new_data)
#     print(output[0])
#     return jsonify(output[0])

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json
    print(data)  # Debugging line to see what data is received
    if not data or 'data' not in data:
        return jsonify({'error': 'Invalid input data'}), 400
    data = data['data']
    print(data)  # To ensure 'data' is present
    
    try:
        new_data = np.array(list(data.values())).reshape(1, -1)
        new_data = scalar.transform(new_data)  # Ensure scalar is initialized
        output = regmodel.predict(new_data)
        return jsonify(output[0])
    except Exception as e:
        print(e)  # Print any error that occurs
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
