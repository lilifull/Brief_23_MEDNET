import os
from flask import Flask
from .models.model_loader import load_model
from .utils.file_manager import FileManager
from .views.home import bp as bp_home
from .views.predict import bp as bp_predict
from .views.uploads import bp as bp_uploads
import pathlib

def create_app(app_config=None):
    #  create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(app_config)

    # Checks if necessary paths exists
    paths = [app.instance_path, os.path.join(pathlib.Path().parent.resolve(), app.config['UPLOAD_PATH'])] 
    for path in paths:
        try:
            os.makedirs(path)
        except OSError:
            pass

    # load model once config is loaded
    app.config['MODEL'] = load_model(app.config['MODEL_PATH'])

    # clean uploads folder
    FileManager(app.config['UPLOAD_PATH']).delete_all_files()

    # verify that the app is running correctly
    @app.route('/health')
    def health():
        return 'App is running correctly'
    
    # register blueprints
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_predict)
    app.register_blueprint(bp_uploads)

    return app
