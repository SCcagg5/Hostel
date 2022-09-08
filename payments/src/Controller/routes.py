from Model.payment import *


def setuproute(app, call):
    @app.route('/',                                 ['OPTIONS', 'GET', 'POST'],   lambda x = None: call([])                                                                                         )
    @app.route('/generate',                         ['OPTIONS', 'POST'],   lambda x = None: call([payment_get])                                                                                      )
    @app.route('/pay',                              ['OPTIONS', 'POST'],   lambda x = None: call([payment_pay])                                                                                     )
    def base():
        return
