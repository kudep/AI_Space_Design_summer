import torch
import torch_redstone as rst
import transformers
from diffusers import StableUnCLIPImg2ImgPipeline


class Wrapper(transformers.modeling_utils.PreTrainedModel):
    def __init__(self) -> None:
        super().__init__(transformers.configuration_utils.PretrainedConfig())
        self.param = torch.nn.Parameter(torch.tensor(0.))

    def forward(self, x):
        return rst.ObjectProxy(image_embeds=x)


pipe = StableUnCLIPImg2ImgPipeline.from_pretrained(
    "diffusers/stable-diffusion-2-1-unclip-i2i-l",
    # variant="fp16",
    image_encoder = Wrapper()
)
# pe = pipe.text_encoder.text_model.embeddings
# pe.position_ids = torch.arange(pe.position_ids.shape[-1]).expand((1, -1)).to(pe.position_ids)  # workaround
if torch.cuda.is_available():
    pipe = pipe.to('cuda:' + str(torch.cuda.current_device()))
    pipe.enable_model_cpu_offload(torch.cuda.current_device())
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()


@torch.no_grad()
def pc_to_image(pc_encoder: torch.nn.Module, pc, prompt, noise_level, width, height, cfg_scale, num_steps, callback):
    ref_dev = next(pc_encoder.parameters()).device
    enc = pc_encoder(torch.tensor(pc.T[None], device=ref_dev))
    enc = torch.nn.functional.normalize(enc, dim=-1) * (768 ** 0.5) / 2
    if torch.cuda.is_available():
        enc = enc.to('cuda:' + str(torch.cuda.current_device()))
    # enc = enc.type(half)
    # with torch.autocast("cuda"):
    return pipe(
        prompt=', '.join(["best quality"] + ([prompt] if prompt else [])),
        negative_prompt="cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
        image=enc,
        width=width, height=height,
        guidance_scale=cfg_scale,
        noise_level=noise_level,
        callback=callback,
        num_inference_steps=num_steps
    ).images[0]
