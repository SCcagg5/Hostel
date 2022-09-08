import time
from rethinkdb import RethinkDB

DATABASES = {
    "Hotel":
       [
        "period",
       ]
    }



class Rethink():
    def __init__(self, schema = DATABASES, table = None, seed = None):
        self.re = RethinkDB()
        self.r = RethinkDB()
        self.db = None
        self.conn = None
        self.init = False
        self.__check_db(schema)
        self.__connect(schema)
        self.table(table, seed)

    def table(self, table = None, seed = None):
        if table is not None:
            self.r = self.r.db(self.db).table(table)
            if self.init is True and seed is not None:
                for i in seed:
                    self.r.insert(i).run(self.conn)

    def __check_db(self, database):
        if not isinstance(database, dict):
            raise self.RethinkError("Schema should be dict")
        if len(database) > 1:
            raise self.RethinkError("Only one database should be configured in schema")
        if  len(database) == 0:
            raise self.RethinkError("One database should be configured in schema")
        db_name = list(database)[0]
        if db_name == "test":
            raise self.RethinkError(f"Database can't be named 'test'")
        if not isinstance(database[db_name], list) or \
           any(not isinstance(table, str) for table in database[db_name]):
            raise self.RethinkError(f"Schema['{db_name}']: should be a list of str")
        return self

    def __init(self, database):
        succes = False
        for _ in range(10):
            try:
                db_list = self.r.db_list().run(self.conn)
                succes = True
                break
            except:
                time.sleep(2)
                continue
        if succes is False:
            raise self.RethinkError("Can't read database")
        if "test" in db_list:
            self.r.db_drop("test").run(self.conn)
        for db_name in database:
            if db_name not in db_list:
                self.r.db_create(db_name).run(self.conn)
            table_list = self.r.db(db_name).table_list().run(self.conn)
            for table in database[db_name]:
                if table not in table_list:
                    self.r.db(db_name).table_create(table).run(self.conn)
        self.init = True
        return self

    def __connect(self, database = None):
        succes = False
        for _ in range(10):
            try:
                self.conn = self.r.connect("rethink", 28015, password="")
                succes = True
                break
            except:
                time.sleep(1)
                continue
        if succes is False:
            raise self.RethinkError("Can't connect to database")
        if database is not None:
            self.__init(database)
        self.db = list(database.keys())[0]
        return self

    class RethinkError(Exception):
        pass
