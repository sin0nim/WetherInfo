import requests
from datetime import datetime


class Wether:
    def __init__(self, lat, lon, wid):
        request_line = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={wid}&units=metric'
        r = requests.get(request_line)
        self.code = r.status_code
        if not r.ok:
            self.state = 'Chilly'
            self.temp = 0
            self.card = 'card evening-morning'
        else:
            r_text = r.text
            temp = r_text[r_text.find('temp') + 6:]
            self.temp = round(float(temp[:temp.find(',')]))

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
            local_time = datetime.utcnow()

            lt = (int(local_time.strftime('%H')) + shift) % 24
            if 5 <= lt < 11 or 17 < lt <= 22:
                self.card = 'card evening-morning'
            elif 11 <= lt <= 17:
                self.card = 'card day'
            else:
                self.card = 'card night'
