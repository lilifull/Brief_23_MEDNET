from flask import Flask, render_template, request
from PIL import Image
from torchvision import transforms
import torch
import numpy 

app = Flask(__name__)

PATH = "saved_jit_best_model.pt"
model = torch.jit.load(PATH, map_location=torch.device('cpu'))
model.eval()

def transform_image(image_load):
    my_transforms = transforms.Compose([
        transforms.Resize(64),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))])
    
    image = Image.open(image_load)
    return my_transforms(image).unsqueeze(0)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def prediction():
        image = request.files['image']
        classnames = ['Hand', 'BreastMRI', 'ChestCT', 'HeadCT', 'AbdomenCT', 'CXR']

        tensor = transform_image(image)
        outputs = model(tensor)
        score_pred, prediction = torch.max(outputs, 1)
        id = prediction.numpy()[0]
        classname=classnames[id]
        return render_template('predict.html', id=id, classname=classname)

# a simple page that says hello
@app.route('/health')
def health():
    return 'App is running correctly'

if __name__ == '__main__':
    app.run(debug=True)
