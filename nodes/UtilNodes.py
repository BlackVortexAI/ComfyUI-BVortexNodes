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


NODE_CLASS_MAPPINGS = {
    "BV Image Size with Math": BVImageSizeWithMath,
    "BV String to Combo": BVStringToCombo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Image Size with Math": "🌀 BV Image Size with Math",
    "BV String to Combo": "🌀 BV String to Combo"
}
