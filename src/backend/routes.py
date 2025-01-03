from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, FieldVision-AI!"

@app.route('/prediction', methods=['GET'])
def prediction():
   
    score = request.form['score']
    batter_id = request.form['batter_id']
    return jsonify({
        "prediction": "prediction"
    })

if __name__== "__main__":
    app.run(debug=True, host='localhost', port=3000)
