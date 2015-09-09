import flask
import os
from flask_router import FlaskRouter

def get_app():
    app = flask.Flask(__name__)
    app.config['URL_MODULES'] = [
            'flask.ext.xxl.apps.admin.urls.routes',
    ]
    app.config['ROOT_PATH'] = os.path.realpath(os.path.dirname(__file__))
    app.config['REGISTER_BLUEPRINTS'] = True

    router = FlaskRouter(app)
    return app

if __name__ == "__main__":
    get_app().run(host='0.0.0.0',port=4455,debug=True)
