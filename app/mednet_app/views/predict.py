from flask import Blueprint, redirect, send_from_directory, current_app, request, url_for
from PIL import Image
import torch
from torchvision import transforms
from torch import Tensor
from mednet_app.utils.file_manager import FileManager
from ..models.model_loader import load_model

bp = Blueprint('predict', __name__, url_prefix='/predict')

classnames = ['Hand', 'BreastMRI', 'ChestCT', 'HeadCT', 'AbdomenCT', 'CXR']

def transform_image(image_path) -> Tensor:
    my_transforms = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))])
    image = Image.open(image_path)
    return my_transforms(image).unsqueeze(0)

def predict(filename):
    file_abs_path = FileManager(current_app.config['UPLOAD_PATH']).get_file_abs_path(filename)
    model = current_app.config['MODEL']
    tensor = transform_image(file_abs_path)
    outputs = model(tensor)
    _, predict = torch.max(outputs, 1)
    class_id = predict.item()
    class_name = classnames[class_id]
    return { 'filename': filename, 'class_id': class_id, 'class_name': class_name }

@bp.route('/', methods=['GET', 'POST'])
def predict_all_images():
    if request.method == 'POST':
        results = []
        files_names = FileManager(current_app.config['UPLOAD_PATH']).get_all_files_names()
        for file_name in files_names:
            result = predict(file_name)
            results.append(result)
        return render_template('predict/predict.html', results=results)
    return redirect(url_for('home.index'))


@bp.route('/<path:filename>', methods=['GET', 'POST'])
def predict_image(filename):
    if request.method == 'POST':
        result = predict(filename)
        return render_template('predict/predict.html', results=[result])
    return redirect(url_for('home.index'))
