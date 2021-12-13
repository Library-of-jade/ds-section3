
import os
from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import dbms
import pickle
import warnings

warnings.filterwarnings(action='ignore')

model = ''
with open('model.pkl','rb') as pickle_file:
   model = pickle.load(pickle_file)


DB_FILEPATH = './weather.db'

app = Flask(__name__)
app.config['WEATHER_CSV_FILE'] = os.path.join(os.path.dirname(__file__), '2011_2021.csv')

spare, char_num_change = dbms.init_database(DB_FILEPATH)

@app.route('/')
def index():
    return render_template('index.html'), 200


@app.route('/predict')
def predict():
    '''
    예측 부분
    '''
    X = spare.copy()

    if request.args.get('지역') != '':
        if char_num_change[request.args.get('지역')] != '':
            X['지점'] = char_num_change[request.args.get('지역')]

    if request.args.get("평균기온") !='':
        X['평균기온(°C)'] = float(request.args.get("평균기온"))

    if request.args.get("최저기온") !='':
        X['최저기온(°C)'] = float(request.args.get("최저기온"))

    if request.args.get("최고기온") !='':
        X['최고기온(°C)'] = float(request.args.get("최고기온"))

    if request.args.get("최대순간풍속") !='':
        X['최대 순간 풍속(m/s)'] = float(request.args.get("최대순간풍속"))

    if request.args.get("최대풍속") !='':
        X['최대 풍속(m/s)'] = float(request.args.get("최대풍속"))

    if request.args.get("평균풍속") !='':
        X['평균 풍속(m/s)'] = float(request.args.get("평균풍속"))

    if request.args.get("이슬점온도") !='':
        X['평균 이슬점온도(°C)'] = float(request.args.get("이슬점온도"))

    if request.args.get("최소상대습도") !='':
        X['최소 상대습도(%)'] = float(request.args.get("최소상대습도"))

    if request.args.get("상대습도") !='':
        X['평균 상대습도(%)'] = float(request.args.get("상대습도"))

    if request.args.get("현지기압") !='':
        X['평균 현지기압(hPa)'] = float(request.args.get("현지기압"))

    if request.args.get("최고기압") !='':
        X['최고 해면기압(hPa)'] = float(request.args.get("최고기압"))

    if request.args.get("최저기압") !='':
        X['최저 해면기압(hPa)'] = float(request.args.get("최저기압"))

    if request.args.get("평균기압") !='':
        X['평균 해면기압(hPa)'] = float(request.args.get("평균기압"))

    if request.args.get("월") !='':
        X['월'] = int(request.args.get("월"))


    pred = model.predict([X])
    print(pred)
    if pred == 1:
        return render_template('Yes.html'), 200
    else:
        return render_template('No.html'), 200





if __name__ == "__main__":
    app.run(debug=True)