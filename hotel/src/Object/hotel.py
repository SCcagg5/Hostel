from .rethink import Rethink
import datetime
import requests
import json


class Hotel(Rethink):
    def __init__(self, user_id = None):
        self.seed = [
            {
                "id": 1,
                "name": 'hotel1',
                "details":{
                    "address": "1 rue du ....",
                    "phone": "01XXXXXXXX"
                },
                "rooms": {
                    'SR': 0,
                    'S': 1,
                    'JS': 1,
                    'CD': 1,
                    'CS': 2
                },
                'options': {
                    'garage': 3,
                    'bed': 2,
                    'romance': -1,
                    'breakfeast': -1
                }
            },
            {
                "id": 2,
                "name": 'hotel2',
                "details":{
                    "address": "2 rue du ....",
                    "phone": "02XXXXXXXX"
                },
                "rooms": {
                    'SR': 2,
                    'S': 0,
                    'JS': 0,
                    'CD': 0,
                    'CS': 0
                },
                'options': {
                    'garage': 2,
                    'bed': 2,
                    'romance': -1,
                    'breakfeast': -1
                }
            }
        ]
        super().__init__(table = "hotel", seed = self.seed)
        self.user_id = user_id
        self.id = None

    def pay(self, token):
        response = requests.request("POST", "http://payment:8080/pay", headers={'Content-Type': 'application/json'}, data=json.dumps({'token': token}))
        print(json.loads(response.text))
        return [True, json.loads(response.text)['data'], None]


    def book(self, book, token = False, fromdate = None, todate = None):
        fromdate = datetime.datetime.strptime(fromdate, '%d/%m/%y')
        todate = datetime.datetime.strptime(todate, '%d/%m/%y')
        res = list(
            self.r.filter(
                {
                    "id": self.id
                }
            ).run(self.conn)
        )
        res = res[0]
        total = 0
        data = []
        if fromdate > todate:
            return [False, "invalid date", 400]
        while todate > fromdate:
            tmp = json.loads(json.dumps(res))
            date = int(fromdate.weekday())
            response = requests.request("POST", "http://options:8080/options/book", headers={'Content-Type': 'application/json'}, data=json.dumps({'options': book['options']}))
            tmp['options'] = json.loads(response.text)['data']
            response = requests.request("POST", "http://room:8080/rooms/book", headers={'Content-Type': 'application/json'}, data=json.dumps({'rooms': book['rooms']}))
            tmp['rooms'] = json.loads(response.text)['data']
            response = requests.request("POST", "http://period:8080/rooms/book", headers={'Content-Type': 'application/json'}, data=json.dumps({'rooms': tmp['rooms'], 'date': date}))
            tmp['rooms'] = json.loads(response.text)['data']
            data.append({'date': fromdate.strftime("%d/%m/%Y"), 'options': tmp['options'], 'rooms': tmp['rooms']})
            total += tmp['options']['total']
            total += tmp['rooms']['total']
            fromdate += datetime.timedelta(days=1)
        ret = {
            'name': res['name'],
            'details': res['details'],
            'reservation': data,
            'total': total
        }
        if token is True:
            response = requests.request("POST", "http://payment:8080/generate", headers={'Content-Type': 'application/json'}, data=json.dumps({'book': ret}))
            print(json.loads(response.text))
            token = json.loads(response.text)['data']
        return  [True, {"details": ret, "token": token}, None]

    def get_by_id(self, id, date):
        id = int(id)
        if not isinstance(id, int):
            return [False, "Hotel id should be a int", 400]
        ret = list(
            self.r.filter(
                {
                    "id": id
                }
            ).run(self.conn)
        )
        if len(ret) == 0:
            return [False, "Invalid calendar id", 404]
        if len(ret) > 1:
            return [False, "Internal Error", 500]
        ret = ret[0]
        self.id = id
        if date is None:
            return [True, None, None]
        date = int(datetime.datetime.strptime(date, '%d/%m/%y').weekday())
        response = requests.request("POST", "http://options:8080/options", headers={'Content-Type': 'application/json'}, data=json.dumps({'options': ret['options']}))
        ret['options'] = json.loads(response.text)['data']
        response = requests.request("POST", "http://room:8080/rooms", headers={'Content-Type': 'application/json'}, data=json.dumps({'rooms': ret['rooms']}))
        ret['rooms'] = json.loads(response.text)['data']
        response = requests.request("POST", "http://period:8080/rooms", headers={'Content-Type': 'application/json'}, data=json.dumps({'rooms': ret['rooms'], 'date': date}))
        ret['rooms'] = json.loads(response.text)['data']
        return [True, ret, None]

    def update(self, name, options):
        if self.id is None:
            return [False, "Internal Error: 013", 500]
        if not isinstance(name, str) and name is not None and len(name) < 56:
            return [False, "Name should be a string(56)", 400]
        if not isinstance(options, dict) and options is not None:
            return [False, "Options should be a dictionnary", 400]
        update = {"options": {}}
        if name is not None:
            update["name"] = name
            update["options"] = {}
        if "garage" in options:
            update["options"]["garage"] = int(options["garage"])
        if "bed" in options:
            update["options"]["bed"] = int(options["bed"])
        ret = self.r.filter(
            {
                "id": self.id
            }
        ).update(update).run(self.conn)
        ret = self.set_id(self.id)
        return ret
