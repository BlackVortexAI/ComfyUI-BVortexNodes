from daam import trace, set_seed
from diffusers import FluxPipeline
import numpy as np
import torch
from matplotlib import pyplot as plt
from comfy.model_patcher import ModelPatcher


class BVDAAM:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {}),
                "word_to_trace": ("STRING", {}),
                "unet": ("MODEL", {}),  # Ein vortrainiertes UNet-Diffusionsmodell
                "vae": ("VAE", {}),  # Ein vortrainiertes VAE-Modell
                "clip": ("CLIP", {}),  # Ein vortrainiertes CLIP-Modell
                "num_inference_steps": ("INT", {"default": 50, "min": 1, "max": 1000}),
                "device": (["cuda", "cpu"],),
            },
            "optional": {
                "seed": ("INTEGER", {}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("heatmap",)
    FUNCTION = "damm"
    CATEGORY = "🌀 BVortex Nodes/Image Processing"

    def damm(self, prompt, word_to_trace, unet, vae, clip, num_inference_steps, device, seed=-1):
        actual_seed = 0 if seed == -1 else seed
        gen = set_seed(actual_seed)

        if isinstance(unet, ModelPatcher):
            unet_model = unet.model
        elif isinstance(unet, Flux):
            unet_model = unet.model_path  # Oder eine andere relevante Eigenschaft des Flux-Modells
        else:
            unet_model = unet  # Falls 'unet' bereits ein Modell ist

        # Ähnlich für VAE und CLIP, falls sie auch ModelPatcher-Objekte sind
        if isinstance(vae, ModelPatcher):
            vae_model = vae.model
        else:
            vae_model = vae

        if isinstance(clip, ModelPatcher):
            clip_model = clip.model
        else:
            clip_model = clip

        pipe = FluxPipeline.from_pretrained(unet_model, vae=vae, text_encoder=clip, torch_dtype=torch.float16)
        pipe = pipe.to(device)
        with torch.no_grad():
            with trace(pipe) as tc:
                out = pipe(prompt, num_inference_steps=num_inference_steps, generator=gen)
                heat_map = tc.compute_global_heat_map()
                heat_map = heat_map.compute_word_heat_map(word_to_trace)
                heat_map.plot_overlay(out)
                plt.show()

                return (out,)


NODE_CLASS_MAPPINGS = {
    "BV DAAM": BVDAAM,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV DAAM": "🌀 BV DAAM",
}
