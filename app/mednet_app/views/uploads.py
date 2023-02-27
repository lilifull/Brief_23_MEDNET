from ..utils.file_manager import FileManager
from flask import Blueprint, redirect, request, send_from_directory, current_app, url_for

bp = Blueprint('uploads', __name__, url_prefix='/uploads')

@bp.route('/', methods=['POST', 'DELETE'])
def delete_all_files():
    if request.method == 'DELETE' or request.form.get('_method') == 'DELETE':
        FileManager(current_app.config['UPLOAD_PATH']).delete_all_files()
    return redirect(url_for('home.index'))

@bp.route('/<path:filename>', methods=['GET'])
def get_file(filename):
    print('get', request.method)
    return send_from_directory(directory='uploads', path=filename)

@bp.route('/<path:filename>', methods=['POST', 'DELETE'])
def delete_file(filename):
    if request.method == 'DELETE' or request.form.get('_method') == 'DELETE': 
        FileManager(current_app.config['UPLOAD_PATH']).delete_file(filename)
    return redirect(url_for('home.index'))
