from flask import Flask
from flask_cors import CORS
from endpoints import demo
# from werkzeug.middleware.profiler import ProfilerMiddleware
# from utils.logging_util import logger

application = Flask(__name__)
# application.wsgi_app = ProfilerMiddleware(application.wsgi_app)

application.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
application.config['RESTPLUS_VALIDATE'] = True
application.config['RESTPLUS_MASK_SWAGGER'] = False
application.config['ERROR_404_HELP'] = False

with application.app_context():
    application.register_blueprint(demo, url_prefix='/api')

@application.errorhandler(404)
def page_not_found(e):
    return 'error 404'

CORS(application)

if __name__ == "__main__":
    print('>>>>> Starting Deploy ProtagoLabs Demo server <<<<<')
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run(host='0.0.0.0', port=8088, use_reloader=False)
