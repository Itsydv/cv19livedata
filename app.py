#importing required modules
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread
from config import Config
from time import sleep
import requests
import json

#instantiating Objects
app = Flask(__name__)
socketio = SocketIO(app)
params = Config()

#creating object to store temp data
livedata = {}

#getting records form API
def get_records():
    res = requests.request('GET', params.api_url)
    return json.loads(res.text)

#filtering unusual parameters
def filter_record(record):
    newRecord = {}
    for key in record:
        if key.lower() not in ['slug', 'premium', 'date', 'id' ]:
            newRecord[key] = record[key]
    return newRecord

#getting live Global Data
def live_global_data():
    global livedata
    while True:
        try:
            livedata = get_records()
            filtered_record = filter_record(livedata.get('Global'))
            socketio.emit('live_data', {'data':filtered_record})
            sleep(1800) #refreshes after every 30 min. ,, can't provide refreshed data due to some legal restrictions on free usage
        except Exception as e:
            print(e)

#getting live data of an specific country
@socketio.on('getLiveData')
def live_country_data(countryIndex):
    country_record = livedata['Countries']
    for index, record in enumerate(country_record):
        if int(countryIndex)-1 == index:
            newRecord = filter_record(country_record[index])
            print(newRecord)
            socketio.emit('live_c_data', {'data':newRecord}, room = request.sid)

#getting top10 countries by totalcases
def top10(records, param):
    cases = {}
    Top10 = {}
    count = 0
    for country in records:
        cases[country['Country']] = country[param]
    res = {key: val for key, val in sorted(cases.items(), key = lambda ele: ele[1], reverse = True)}
    for key in res:
        if count > 9:
            break
        Top10[key] = res[key]
        count += 1
    return filter_record(Top10)

#Index page
@app.route('/')
def home():
    livedata = get_records()
    thread = Thread(target=live_global_data)
    thread.start()
    return render_template('index.html', data=livedata, title='Covid19 Live data', param=params, top10confirmed=top10(livedata['Countries'], 'TotalConfirmed'), top10death=top10(livedata['Countries'], 'TotalDeaths'), top10recovered=top10(livedata['Countries'], 'TotalRecovered'))

#starting Application
if __name__ == '__main__':
    socketio.run(app)
