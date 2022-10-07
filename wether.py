import requests
from datetime import datetime, timezone


class Wether:
    def __init__(self, lat, lon):
        id = 'e34f62f34cbc6a94e22b14dcffacda18'
        request_line = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={id}&units=metric'
        try:
            r = requests.get(request_line)
        except:
            self.code = r.status_code
            raise ReferenceError

        self.code = r.ok
        r_text = r.text
        # print(r_text)
        temp = r_text[r_text.find('temp') + 6:]
        self.temp = round(float(temp[:temp.find(',')]))

        # print(f'temperature = {temp}°C')
        if self.temp < 0:
            self.state = 'Cold'
        elif 0 <= self.temp < 12:
            self.state = 'Chilly'
        elif 12 <= self.temp < 22:
            self.state = 'Warm'
        else:
            self.state = 'Hot'

        shift = r_text[r_text.find('timezone') + 10:]
        shift = int(int(shift[:shift.find(',')]) / 3600)
        local_time = datetime.now(timezone.utc)
        # print(f'local time = {local_time} | shift = {shift}')

        lt = (int(local_time.strftime('%H')) + shift) % 24
        # print(f'time = {lt}')
        if 5 <= lt < 11 or 17 < lt <= 22:
            self.card = 'card evening-morning'
        elif 11 <= lt <= 17:
            self.card = 'card day'
        else:
            self.card = 'card night'
