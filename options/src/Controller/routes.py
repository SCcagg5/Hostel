from Model.option import *

def setuproute(app, call):
    @app.route('/',                                 ['OPTIONS', 'GET', 'POST'],   lambda x = None: call([])                                                                                         )
    @app.route('/options',                          ['OPTIONS', 'POST'],   lambda x = None: call([option_get])                                                                                      )
    @app.route('/options/book',                     ['OPTIONS', 'POST'],   lambda x = None: call([option_book])                                                                                     )
    def base():
        return
