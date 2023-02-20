import torch

def load_model(model_path):
    model=torch.load(model_path, map_location=torch.device('cpu'))
    model.eval()
    return model
