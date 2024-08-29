---
license: mit
metrics:
- accuracy
---

# OpenShape Inference Library

## Installation

First, you have to install a recent version of [torch](//pytorch.org/get-started/locally/) and [dgl](//www.dgl.ai/pages/start.html).

Then install the following extra dependencies:
```bash
pip install torch.redstone einops huggingface_hub
```

Finally, install OpenShape by cloning the repository and running
```bash
pip install -e .
```

## Usage

### Loading an OpenShape model

```python
import openshape
pc_encoder = openshape.load_pc_encoder('openshape-pointbert-vitg14-rgb')

# Available models:
# openshape-pointbert-vitb32-rgb, trained against CLIP ViT-B/32
# openshape-pointbert-vitl14-rgb, trained against CLIP ViT-L/14
# openshape-pointbert-vitg14-rgb, trained against OpenCLIP ViT-bigG/14 (main model in paper)
```

Models accept point clouds of shape [B, 6, N] (XYZ-RGB) and trained with N = 10000.

Point clouds should be centered at centroid and normalized into the unit ball, and RGB values should have range [0, 1].
If you don't have RGB available in your point cloud, fill with [0.4, 0.4, 0.4].

**Note:** B/32 and L/14 models has gravity axis Y; G/14 model has gravity axis Z.

### Applications

Various downstream applications can be found in the demo directory.
Check the code at https://huggingface.co/spaces/OpenShape/openshape-demo/tree/main for usage.