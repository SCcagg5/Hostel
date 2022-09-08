from .rethink import Rethink
import datetime

class Option(Rethink):
    def __init__(self):
        self.seed = [
            {
                "id": 1,
                "name": 'garage',
                "price": 25.00
            },
            {
                "id": 2,
                "name": 'romance',
                "price": 50.00
            },
            {
                "id": 3,
                "name": 'breakfeast',
                "price": 30.00
            },
            {
                "id": 4,
                "name": 'bed',
                "price": 0.00
            }
        ]
        super().__init__(table = "option", seed = self.seed)

    def book(self, options):
        total = 0.00
        data = list(self.r.run(self.conn))
        ret= {}
        for option in data:
            if option['name'] in options:
                price = option['price'] * int(options[option['name']])
                ret[option['name']] = {
                    "price": price
                }
                total = total + price
        return [True, {'options': ret, 'total': total}, None]

    def get(self, options):
        data = list(self.r.run(self.conn))
        ret = {}
        for option in data:
            if option['name'] in options:
                av = int(options[option['name']])
                ret[option['name']] = {
                    "price": option['price']
                }
                if av > -1:
                    ret[option['name']]['availability'] = av
        return [True, ret, None]
