from flask import Blueprint, request, render_template, current_app
from PIL import Image
import torch
from torchvision import transforms
from torch import Tensor
from ..models.model_loader import load_model

bp = Blueprint('predict', __name__, url_prefix='/predict')

classnames = ['Hand', 'BreastMRI', 'ChestCT', 'HeadCT', 'AbdomenCT', 'CXR']

def transform_image(image_load) -> Tensor:
    my_transforms = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((64,64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))])
    image = Image.open(image_load)
    return my_transforms(image).unsqueeze(0)

@bp.route('/', methods=['POST'])
def prediction():
    image = request.files['image']
    model = current_app.config['MODEL']
    tensor = transform_image(image)
    outputs = model(tensor)
    max_value, max_index = torch.max(outputs, 1)
    class_id = max_index.item()
    class_name = classnames[class_id]
    return render_template('predict/predict.html', class_id=class_id, class_name=class_name)
