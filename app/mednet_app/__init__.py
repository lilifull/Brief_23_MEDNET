import os
from flask import Flask
from .views.home import bp as bp_home
from .views.predict import bp as bp_predict
from .models.model_loader import load_model

def create_app(app_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(app_config)

    # load model once config is loaded
    app.config['MODEL'] = load_model(app.config['MODEL_PATH'])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # verify that the app is running correctly
    @app.route('/health')
    def health():
        return 'App is running correctly'
    
    # register blueprints
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_predict)

    return app
