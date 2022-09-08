from Model.room import *

def setuproute(app, call):
    @app.route('/',                                 ['OPTIONS', 'GET', 'POST'],   lambda x = None: call([])                                                                                         )
    @app.route('/rooms',                          ['OPTIONS', 'POST'],   lambda x = None: call([room_get])                                                                                      )
    @app.route('/rooms/book',                     ['OPTIONS', 'POST'],   lambda x = None: call([room_book])                                                                                     )
    def base():
        return
