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
