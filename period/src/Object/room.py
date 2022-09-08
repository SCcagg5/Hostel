from .rethink import Rethink
import datetime

class Room(Rethink):
    def __init__(self):
        self.seed = [
            {
                "id": 0,
                "effect": 1.0
            },
            {
                "id": 1,
                "effect": 1.0
            },
            {
                "id": 2,
                "effect": 0.9
            },
            {
                "id": 3,
                "effect": 0.9
            },
            {
                "id": 4,
                "effect": 1.1
            },
            {
                "id": 5,
                "effect": 1.1
            },
            {
                "id": 6,
                "effect": 1.0
            },
        ]
        super().__init__(table = "period", seed = self.seed)

    def book(self, rooms, date):
        for room in rooms['rooms']:
            rooms['rooms'][room]['price'] = round(rooms['rooms'][room]['price'] * dict(self.r.get(date).run(self.conn))['effect'], 2)
        rooms['total'] = round(rooms['total'] * dict(self.r.get(date).run(self.conn))['effect'], 2)
        return [True, rooms, None]

    def get(self, rooms, date):
        for room in rooms:
            rooms[room]['price'] = round(rooms[room]['price'] * dict(self.r.get(date).run(self.conn))['effect'], 2)
        return [True, rooms, None]
