import torch
import torch.nn as nn
from huggingface_hub import hf_hub_download
from .ppat_rgb import Projected, PointPatchTransformer


def module(state_dict: dict, name):
    return {'.'.join(k.split('.')[1:]): v for k, v in state_dict.items() if k.startswith(name + '.')}


def G14(s):
    model = Projected(
        PointPatchTransformer(512, 12, 8, 512*3, 256, 384, 0.2, 64, 6),
        nn.Linear(512, 1280)
    )
    model.load_state_dict(module(s['state_dict'], 'module'))
    return model


def L14(s):
    model = Projected(
        PointPatchTransformer(512, 12, 8, 1024, 128, 64, 0.4, 256, 6),
        nn.Linear(512, 768)
    )
    model.load_state_dict(module(s, 'pc_encoder'))
    return model


def B32(s):
    model = PointPatchTransformer(512, 12, 8, 1024, 128, 64, 0.4, 256, 6)
    model.load_state_dict(module(s, 'pc_encoder'))
    return model


model_list = {
    "openshape-pointbert-vitb32-rgb": B32,
    "openshape-pointbert-vitl14-rgb": L14,
    "openshape-pointbert-vitg14-rgb": G14,
}


def load_pc_encoder(name):
    s = torch.load(hf_hub_download("OpenShape/" + name, "model.pt"), map_location='cpu')
    model = model_list[name](s).eval()
    if torch.cuda.is_available():
        model.cuda()
    return model
