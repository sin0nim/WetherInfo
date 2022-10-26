from wether import Wether


class FirstPage:
    data = []

    @classmethod
    def plus_data(cls, gd: tuple, wid: str) -> list:
        cw = Wether(gd[1], gd[2], wid)
        cls.data.append({'name': gd[0].upper(), 'data': (cw.card, cw.temp, cw.state)})
