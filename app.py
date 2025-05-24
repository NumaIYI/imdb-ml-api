from flask import Flask, request, jsonify
import joblib
import pandas as pd
import sqlite3
import datetime

app = Flask(__name__)

# Modeli yükle
model = joblib.load('imdb_rating_model.pkl')

# Veritabanı oluşturma (ilk başta bir kere çağrılacak)
def init_db():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            budget REAL,
            run_time_min INTEGER,
            predicted_rating REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "IMDB Rating Prediction API"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    predicted_rating = round(float(prediction[0]), 2)

    # Veritabanına kaydetme
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions (year, budget, run_time_min, predicted_rating, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data.get('year'),
        data.get('budget'),
        data.get('run_time_min'),
        predicted_rating,
        datetime.datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    return jsonify({
        'predicted_rating': predicted_rating
    })

if __name__ == '__main__':
    app.run(debug=True)
