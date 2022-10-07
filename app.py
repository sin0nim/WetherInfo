import sys
from flask import Flask, render_template, request
import requests
from geocode import Geocode
import datetime
from wether import Wether

app = Flask(__name__)

dict_with_weather_info = [{'name': 'BOSTON', 'data': ("card night", 9, 'Chilly')},
                          {'name': 'NEW YORK', 'data': ("card day", 32, 'Sunny')},
                          {'name': 'EDMONTON', 'data': ("card evening-morning", -15, 'Cold')}]

gc = Geocode()


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    return render_template('index.html', weather=dict_with_weather_info)


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        city_name = request.form['city_name']
    else:
        city_name = None
    if city_name is not None:
        # get coordinates
        coord = gc.find(city_name)
        if coord is not None:
            # print(f'***coordinates = {coord}')
            try:
                cw = Wether(coord[1], coord[2])
            except ReferenceError:
                print(f'RaiseError {cw.code}')
            else:
                dict_with_weather_info.append({'name': coord[0].upper(), 'data': (cw.card, cw.temp, cw.state)})
                return render_template('index.html', weather=dict_with_weather_info)

'''            lat, lon, appid = coord[1], coord[2], 'e34f62f34cbc6a94e22b14dcffacda18'
            r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}&units=metric')
            if r.ok:
                r_text = r.text
                # print(r_text)
                temp = r_text[r_text.find('temp')+6:]
                temp = round(float(temp[:temp.find(',')]))
                # print(f'temperature = {temp}°C')
                if temp < 0:
                    state = 'Cold'
                elif 0 <= temp < 12:
                    state = 'Chilly'
                elif 12 <= temp < 22:
                    state = 'Warm'
                else:
                    state = 'Hot'

                shift = r_text[r_text.find('timezone')+10:]
                shift = int(int(shift[:shift.find(',')]) / 3600)

                local_time = datetime.datetime.now(datetime.timezone.utc)
                # print(f'local time = {local_time} | shift = {shift}')

                lt = (int(local_time.strftime('%H')) + shift) % 24
                # print(f'time = {lt}')
                if 5 <= lt < 11 or 17 < lt <= 22:
                    card = 'card evening-morning'
                elif 11 <= lt <= 17:
                    card = 'card day'
                else:
                    card = 'card night'
                dict_with_weather_info.append({'name': coord[0].upper(), 'data': (card, temp, state)})
                return render_template('index.html', weather=dict_with_weather_info)
            else:
                print(f'wether API request failed: {r.status_code}')
        else:
            print(f'City name {coord[0]} is not found')'''


@app.route('/del', methods=['GET', 'POST'])
def del_city():
    if request.method == 'POST':
        id = int(request.form['id'])
        dict_with_weather_info.pop(id)
    return render_template('index.html', weather=dict_with_weather_info)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
