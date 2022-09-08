from .rethink import Rethink
import datetime

class Room(Rethink):
    def __init__(self):
        self.seed = [
            {
                "id": 1,
                "name": 'SR',
                "price": 1000.00
            },
            {
                "id": 2,
                "name": 'S',
                "price": 720.00
            },
            {
                "id": 3,
                "name": 'JS',
                "price": 500.00
            },
            {
                "id": 4,
                "name": 'CD',
                "price": 300.00
            },
            {
                "id": 5,
                "name": 'CS',
                "price": 150.00
            }
        ]
        super().__init__(table = "room", seed = self.seed)

    def book(self, rooms):
        total = 0.00
        data = list(self.r.run(self.conn))
        ret= {}
        for room in data:
            if 'name' in room and room['name'] in rooms:
                price = room['price'] * int(rooms[room['name']])
                ret[room['name']] = {
                    "price": price
                }
                total = total + price
        return [True, {'rooms': ret, 'total': total}, None]

    def get(self, rooms):
        data = list(self.r.run(self.conn))
        ret = {}
        for room in data:
            if 'name' in room and room['name'] in rooms:
                av = int(rooms[room['name']])
                if av > 0:
                    ret[room['name']] = {
                        "price": room['price'],
                        "availability": av
                    }
        return [True, ret, None]
