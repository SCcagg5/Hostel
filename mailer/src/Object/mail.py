from jinja2 import Environment, BaseLoader, meta
import datetime
try:
    from .rethink import Rethink
except:
    pass

class Mail(Rethink):
    def __init__(self):
        super().__init__()
        self.conn = self.conn.table('mail')
        self.model = {
            "to": None,
            "subject": None,
            "html": None,
            "status": [],
            "last_update": None,
            "sent": False,
            "retry": 0
        }
        self.data = None

    def get(self, id):
        if not self.__exist():
            return [False, "Mail doesn't exist", 404]
        return [True, self.data, None]

    def list(self, expand = False):
        func_map = lambda doc: {
            "id": doc["id"],
            "to": doc['to'],
            "subject": doc['subject'],
            "status": doc['status'],
            "last_update": doc['last_update'],
            "sent": doc['sent'],
            "retry": doc['retry']
        }
        if expand:
            func_map = lambda doc: {
                "id": doc["id"],
                "to": doc['to'],
                "subject": doc['subject'],
                "status": doc['status'],
                "html": doc['html'],
                "last_update": doc['last_update'],
                "sent": doc['sent'],
                "retry": doc['retry']
            }
        ret = list(
                self.conn.map(
                    func_map
                ).run()
              )
        return [True, ret, None]

    def new(self, to, subject, html):
        if isinstance(to, str):
            to = [to]
        if not isinstance(to, list) or not all(isinstance(t, str) for t in to):
            return [False, "Invalid recipient(s)", 400]
        if not isinstance(subject, str):
            return [False, "Invalid subject", 400]
        ret = {}
        for t in to:
            ret[t] = self.__push(t, subject, html)
        return [True, ret, None]

    def __exist(self):
        res = list(self.conn.filter(lambda doc: doc['id'] == self.name).run())
        if len(res) > 0:
            self.data = res[0]
            return True
        return False

    def __push(self, to, subject, html):
        now = str(datetime.datetime.utcnow())
        data = self.model
        data['to'] = to
        data['subject'] = subject
        data['html'] = html
        data['status'].append(
                {
                    'event': 'queued',
                    'date': now
                }
            )
        data['last_update'] = now
        self.conn.insert([data]).run()
        return True
