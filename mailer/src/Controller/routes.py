from Model.template import *
from Model.mail import *

def setuproute(app, call):
    @app.route('/',                             ['OPTIONS', 'GET'],         lambda x = None: call([]))

    @app.route('/template',                     ['OPTIONS', 'GET'],         lambda x = None: call([template_list]))
    @app.route('/template',                     ['OPTIONS', 'POST'],        lambda x = None: call([template_new]))
    @app.route('/template/<>',                  ['OPTIONS', 'GET'],         lambda x = None: call([template_get]))
    @app.route('/template/<>',                  ['OPTIONS', 'POST'],        lambda x = None: call([template_get, template_customize]))

    @app.route('/mail',                         ['OPTIONS', 'GET'],         lambda x = None: call([mail_list]))
    @app.route('/mail/template/<>',             ['OPTIONS', 'POST'],        lambda x = None: call([template_get, template_customize, mail_new]))
    @app.route('/mail/<>',                      ['OPTIONS', 'GET'],         lambda x = None: call([mail_get]))

    def base():
        return
