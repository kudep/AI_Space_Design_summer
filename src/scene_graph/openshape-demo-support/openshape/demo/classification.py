import torch
import torch.nn.functional as F
from collections import OrderedDict
from . import lvis


@torch.no_grad()
def pred_lvis_sims(pc_encoder: torch.nn.Module, pc):
    ref_dev = next(pc_encoder.parameters()).device
    enc = pc_encoder(torch.tensor(pc[:, [0, 2, 1, 3, 4, 5]].T[None], device=ref_dev)).cpu()
    sim = torch.matmul(F.normalize(lvis.feats, dim=-1), F.normalize(enc, dim=-1).squeeze())
    argsort = torch.argsort(sim, descending=True)
    return OrderedDict((lvis.categories[i], sim[i]) for i in argsort if i < len(lvis.categories))


@torch.no_grad()
def pred_custom_sims(pc_encoder: torch.nn.Module, pc, cats, feats):
    ref_dev = next(pc_encoder.parameters()).device
    enc = pc_encoder(torch.tensor(pc[:, [0, 2, 1, 3, 4, 5]].T[None], device=ref_dev)).cpu()
    sim = torch.matmul(F.normalize(feats, dim=-1), F.normalize(enc, dim=-1).squeeze())
    argsort = torch.argsort(sim, descending=True)
    return OrderedDict((cats[i], sim[i]) for i in argsort if i < len(cats))
