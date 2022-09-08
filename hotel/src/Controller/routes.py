from Model.hotel import *
from Model.sso import *

def setuproute(app, call):
    @app.route('/',                                 ['OPTIONS', 'GET', 'POST'],   lambda x = None: call([])                                                                                         )
    @app.route('/sso',                              ['OPTIONS', 'GET'],           lambda x = None: call([sso_url])                                                                                  )
    @app.route('/sso/conn/<>',                      ['OPTIONS', 'GET'],           lambda x = None: call([sso_token])                                                                                )

    @app.route('/hotel/<>',                         ['OPTIONS', 'GET'],           lambda x = None: call([hotel_init, hotel_get])                                                                    )
    @app.route('/hotel/<>/edit',                    ['OPTIONS', 'POST'],           lambda x = None: call([sso_verify_token, hotel_init, hotel_update])                                              )
    @app.route('/hotel/<>/book',                    ['OPTIONS', 'POST'],           lambda x = None: call([sso_verify_token, hotel_init, hotel_get, hotel_book])                                     )
    @app.route('/pay',                              ['OPTIONS', 'POST'],           lambda x = None: call([sso_verify_token, hotel_init, hotel_pay])                                                             )
    def base():
        return
