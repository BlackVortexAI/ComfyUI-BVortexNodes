import math
import os

import numpy as np
import torch
from PIL import Image, ImageOps
from .CustomDatatypes import BV_IMAGE_PIPE
from .CustomDatatypes import BV_UPSCALE_CONFIG_PIPE

class BVConditionalImagePipeSplitter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_pipe": ("BV_IMAGE_PIPE", {}),
            },
            "optional": {
                "opt_caption_config_pipe": ("BV_UPSCALE_CONFIG_PIPE", {
                    "forceInput": True,
                }),
                "upscale_lowres": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled"
                }),
                "lowres_limit": ("INT", {
                    "default": 768,
                    "min": 256,
                    "max": 2048,
                    "step": 256
                })
            },
        }

    RETURN_TYPES = ("BV_IMAGE_PIPE", "BV_IMAGE_PIPE")
    RETURN_NAMES = ("TO_UPSCALE", "HIGH_RES_IMAGES")

    OUTPUT_IS_LIST = (True, True)
    INPUT_IS_LIST = (True, False, False, False)

    FUNCTION = "image_pipe_splitter"

    CATEGORY = "🌀 BVortex Nodes/Captioning"

    def image_pipe_splitter(self, image_pipe: list[BV_IMAGE_PIPE], opt_caption_config_pipe: BV_UPSCALE_CONFIG_PIPE = None, upscale_lowres: bool = True, lowres_limit: int = 768):
        to_upscale = []
        high_res_images = []

        limit = lowres_limit[0] if isinstance(lowres_limit, list) else lowres_limit
        upscale = upscale_lowres[0] if isinstance(upscale_lowres, list) else upscale_lowres

        if opt_caption_config_pipe is not None:
            print("Config detected. Use config!")
            opt_caption_config_pipe = opt_caption_config_pipe[0] if isinstance(opt_caption_config_pipe, list) else opt_caption_config_pipe
            limit = opt_caption_config_pipe.lowres_limit
            upscale = opt_caption_config_pipe.upscale_lowres



        for entry in image_pipe:
            if (entry.image.shape[2] < limit or entry.image.shape[1] < limit) and upscale:
                to_upscale.append(entry)
            else:
                high_res_images.append(entry)

        return to_upscale, high_res_images


class BVImageCaptionSaver:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_pipe": ("BV_IMAGE_PIPE", {}),
                "folder": ("STRING", {"multiline": False}),
                "filename": ("STRING", {"default": "%count_%res", "multiline": False}),
                "make_resolution_sub_folder": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled"
                }),
            },
        }

    INPUT_IS_LIST = True,

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "image_caption_saver"

    CATEGORY = "🌀 BVortex Nodes/Captioning"

    def image_caption_saver(self, image_pipe: list[BV_IMAGE_PIPE], folder: str, filename: str,
                            make_resolution_sub_folder: bool):

        for entry in image_pipe:
            res = entry.image.shape[2]
            if res > entry.image.shape[1]:
                res = entry.image.shape[1]

            res_normalized = math.floor(res / 256) * 256
            if res_normalized > 1024:
                res_normalized = 1024

            res_normalized = str(res_normalized)

            if res_normalized == "0":
                res_normalized = "lowres"

            dir = folder[0]

            if not os.path.exists(dir):
                os.mkdir(dir)

            if make_resolution_sub_folder:
                if not os.path.exists(dir + os.sep + res_normalized):
                    os.mkdir(dir + os.sep + res_normalized)
                dir = dir + os.sep + res_normalized

            file_name = filename[0].replace("%count", entry.offset_count_zero_padding).replace("%res", res_normalized)
            for image in entry.image:
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                img_file = f"{file_name}.png"
                img.save(os.path.join(dir, img_file), compress_level=4)
                if entry.caption is not None:
                    txt_file = file_name + ".txt"
                    file_path = os.path.join(dir, txt_file)
                    with open(file_path, 'w') as f:
                        f.write(entry.caption)
        return {"state": "ok"}


class BVImagePipeJunction:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_pipe": ("BV_IMAGE_PIPE", {}),
            },
            "optional": {
                "images": ("IMAGE", {}),
                "captions": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("BV_IMAGE_PIPE", "IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE_PIPE", "IMAGES", "CAPTIONS")
    OUTPUT_IS_LIST = (True, True, True)
    INPUT_IS_LIST = (True, True, True)

    FUNCTION = "image_pipe_junction"

    CATEGORY = "🌀 BVortex Nodes/Captioning"

    def image_pipe_junction(self, image_pipe: list[BV_IMAGE_PIPE], images=None, captions=None):
        if images is not None and len(image_pipe) != len(images):
            raise ValueError(
                f"The size of images ({len(images)}) is not the same as the size of image_pipe ({len(image_pipe)})")

        if captions is not None and len(image_pipe) != len(captions):
            raise ValueError(
                f"The size of captions ({len(captions)}) is not the same as the size of image_pipe ({len(image_pipe)})")

        for i, image_entry in enumerate(image_pipe):
            if images is not None:
                image_entry.image = images[i]
            if captions is not None:
                image_entry.caption = captions[i]


        updated_images = []
        updated_captions = []

        for entry in image_pipe:
            updated_images.append(entry.image)
            updated_captions.append(entry.caption)


        return image_pipe, updated_images, updated_captions


class BVImagePipeLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "zero_padding": ("INT", {"default": 3, "min": 0, "step": 1}),
                "image_load_cap": ("INT", {"default": 0, "min": 0, "step": 1}),
                "start_index": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("BV_IMAGE_PIPE", "STRING", "STRING")
    RETURN_NAMES = ("IMAGE_PIPE", "FILE PATH", "PATH")
    OUTPUT_IS_LIST = (True, True, False)

    FUNCTION = "load_image_pipe"

    CATEGORY = "🌀 BVortex Nodes/Captioning"

    def load_image_pipe(self, directory: str, zero_padding: int = 3, image_load_cap: int = 0, start_index: int = 0):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")
        dir_files = os.listdir(directory)
        if len(dir_files) == 0:
            raise FileNotFoundError(f"No files in directory '{directory}'.")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]

        dir_files = sorted(dir_files)
        dir_files = [os.path.join(directory, x) for x in dir_files]

        dir_files = dir_files[start_index:]

        images_data = []
        masks = []
        file_paths = []

        limit_images = False
        if image_load_cap > 0:
            limit_images = True
        image_count = 0
        image_count_offset = start_index

        for image_path in dir_files:
            if os.path.isdir(image_path) and os.path.ex:
                continue
            if limit_images and image_count >= image_load_cap:
                break
            i = Image.open(image_path)
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            images_data.append(BV_IMAGE_PIPE(image, image_count, str(image_count).zfill(zero_padding),
                                             image_count_offset, str(image_count_offset).zfill(zero_padding)))


            masks.append(mask)
            file_paths.append(str(image_path))
            image_count += 1
            image_count_offset += 1
        return images_data, file_paths, directory


class BVImagePipeMerger:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_pipe_1": ("BV_IMAGE_PIPE", {}),
                "image_pipe_2": ("BV_IMAGE_PIPE", {}),
            }
        }

    RETURN_TYPES = ("BV_IMAGE_PIPE",)
    RETURN_NAMES = ("IMAGE_PIPE",)
    OUTPUT_IS_LIST = (True,)
    INPUT_IS_LIST = (True, True)

    FUNCTION = "image_pipe_merger"

    CATEGORY = "🌀 BVortex Nodes/Captioning"

    def image_pipe_merger(self, image_pipe_1: list[BV_IMAGE_PIPE], image_pipe_2: list[BV_IMAGE_PIPE]):
        merged_images = image_pipe_1 + image_pipe_2

        merged_images.sort(key=lambda x: x.count)

        return (merged_images,)


class BVUpscaleConfig:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "upscale_lowres": ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"}),
                "lowres_limit": ("INT", {
                    "default": 768,
                    "min": 256,
                    "max": 2048,
                    "step": 256
                }),
                "resolution_steps": ("INT", {
                    "default": 256,
                    "min": 256,
                    "max": 2048,
                    "step": 256
                }),
                "max_resolution": ("INT", {
                    "default": 1024,
                    "min": 256,
                    "max": 2048,
                    "step": 256
                }),
            }
        }

    RETURN_TYPES = ("BV_UPSCALE_CONFIG_PIPE",)
    RETURN_NAMES = ("CAPTION_CONFIG_PIPE",)

    FUNCTION = "upscale_config"

    CATEGORY = "🌀 BVortex Nodes/Captioning"

    def upscale_config(self, upscale_lowres: bool, lowres_limit: int, resolution_steps: int, max_resolution: int):
        return (BV_UPSCALE_CONFIG_PIPE(upscale_lowres, lowres_limit, resolution_steps, max_resolution),)


NODE_CLASS_MAPPINGS = {
    "BV Conditional ImagePipe Splitter": BVConditionalImagePipeSplitter,
    "BV Image Caption Saver": BVImageCaptionSaver,
    "BV ImagePipe Junction": BVImagePipeJunction,
    "BV ImagePipe Loader": BVImagePipeLoader,
    "BV ImagePipe Merger": BVImagePipeMerger,
    "BV Upscale Config": BVUpscaleConfig
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Conditional ImagePipe Splitter": "🌀 BV Conditional ImagePipe Splitter",
    "BV Image Caption Saver": "🌀 BV Image Caption Saver",
    "BV ImagePipe Junction": "🌀 BV ImagePipe Junction",
    "BV ImagePipe Loader": "🌀 BV ImagePipe Loader",
    "BV ImagePipe Merger": "🌀 BV ImagePipe Merger",
    "BV Upscale Config": "🌀 BV Upscale Config"
}
