import sys
from flask import Flask, render_template, request, flash
from geocode import Geocode
from wether import Wether
from config import Config
from firstPage import FirstPage

app = Flask(__name__)
app.config.from_object(Config)


gc = Geocode()


init_names = ['Boston', 'New York', 'Edmonton']

for name in init_names:
    coords = gc.find(name)
    FirstPage.plus_data(coords, Config.wether_key)

dict_with_weather_info = FirstPage.data


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    return render_template('index.html', weather=dict_with_weather_info)


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        city_name = request.form['city_name']
    else:
        return None
    # get coordinates
    coord = gc.find(city_name)
    if coord is None or city_name == '':
        print(f'City "{city_name}" is not found.')
        flash(message=f'City name "{city_name}" is not found')
        return render_template('index.html', weather=dict_with_weather_info)
    else:
        try:
            cw = Wether(coord[1], coord[2], Config.wether_key)
        except RuntimeError:
            print(f'RuntimeError {cw.code}')
            flash(message='WetherAPI request error', category="error")
            return render_template('index.html', weather=dict_with_weather_info)
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
