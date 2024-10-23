from safetensors.torch import load_file
import folder_paths as comfy_paths

class BVImageSizeWithMath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "operation": (["add", "sub", "mult", "div"], {"default": "mult"}),
            },
            "optional": {
                "math_value": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("HEIGHT", "WIDTH")

    FUNCTION = "process_image_size"

    CATEGORY = "🌀 BVortex Nodes/Util"

    def process_image_size(self, image, operation="add", math_value=1):
        height = image.shape[1]
        width = image.shape[2]

        if operation == "add":
            new_height = height + math_value
            new_width = width + math_value
        elif operation == "sub":
            new_height = height - math_value
            new_width = width - math_value
        elif operation == "mult":
            new_height = height * math_value
            new_width = width * math_value
        elif operation == "div":
            if math_value != 0:
                new_height = height // math_value
                new_width = width // math_value
            else:
                raise ValueError("Division by zero is not allowed.")
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return new_height, new_width


class BVStringToCombo:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
            },
        }

    RETURN_TYPES = ("COMBO",)
    RETURN_NAMES = ("COMBO",)
    FUNCTION = "string_to_combo"
    CATEGORY = "🌀 BVortex Nodes/Util"

    def string_to_combo(self, text):
        combo = list()

        if text != "":
            values = text.split(',')
            combo = values[0]

        return (combo,)


class BVLoraBlocksNode:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        file_list = comfy_paths.get_filename_list("loras")
        file_list.insert(0, "None")
        return {"required": {"lora_name": (file_list,)}}

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("LORA_BLOCKS",)
    FUNCTION = "get_lora_blocks"
    CATEGORY = "🌀 BVortex Nodes/Util"

    def get_lora_blocks(self, lora_name):
        try:
            lora_path = comfy_paths.get_full_path("loras", lora_name)
            # Load the state dictionary from the file
            state_dict = load_file(lora_path)

            # Extract and return the keys from the state dictionary
            return list(state_dict.keys())
        except Exception as e:
            print(f"Error loading LoRA blocks: {e}")
            return []


NODE_CLASS_MAPPINGS = {
    "BV Image Size with Math": BVImageSizeWithMath,
    "BV String to Combo": BVStringToCombo,
    "BV Show LoRA Blocks": BVLoraBlocksNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Image Size with Math": "🌀 BV Image Size with Math",
    "BV String to Combo": "🌀 BV String to Combo",
    "BV Show LoRA Blocks": "🌀 BV Show LoRA Blocks"
}
