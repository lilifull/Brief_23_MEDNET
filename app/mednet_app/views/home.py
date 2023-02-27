from ..utils.file_manager import FileManager
from flask import Blueprint, render_template, request, abort, redirect, url_for, current_app

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    filenames = FileManager(current_app.config['UPLOAD_PATH']).get_all_files_names()
    return render_template('home/index.html', filenames=filenames)

@bp.route('/', methods=['POST'])
def upload_files():
    try:
        files_to_upload = request.files.getlist('image_file')
        FileManager(current_app.config['UPLOAD_PATH']).upload_files(files_to_upload)
    except ValueError as e:
        abort(400, e)
    return redirect(url_for('home.index'))