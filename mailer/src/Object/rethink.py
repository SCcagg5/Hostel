import time
from rethinkdb import RethinkDB

class Rethink():
    def __init__(self):
        self.r = r = RethinkDB()
        self.conn = None
        try:
            self.conn = get_conn().db("mailer")
        except:
            pass

dbs = {
    "mailer":
       [
        "mail",
        "template"
       ]
    }

def init():
    red = RethinkDB()
    for _ in range(10):
        try:
            red.connect("rethink-mailer", 28015, password="").repl()
            red.db_list().run()
            break
        except:
            continue
        time.sleep(2)
    if red is None:
        print("cannot connect to db")
        exit(1)
    else:
        db_list = red.db_list().run()
        if "test" in db_list:
            red.db_drop("test").run()
        for i in dbs:
            if i not in db_list:
                red.db_create(i).run()
            for j in dbs[i]:
                if j not in red.db(i).table_list().run():
                    red.db(i).table_create(j).run()
    return red

def get_conn():
    r = RethinkDB()
    r.connect("rethink-mailer", 28015, password="").repl()
    return r

init()
