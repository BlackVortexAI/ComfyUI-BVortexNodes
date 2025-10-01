from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class BVSubgraphTitle:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "title": ("BV_SUB_TITLE", {"default": "Section Title"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = True

    def out(self, title):
        return ()


class BVSubgraphHeading:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "heading": ("BV_SUB_HEADING", {"default": "Section Subtitle"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = True

    def out(self, heading):
        return ()


class BVSubgraphDivider:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "divider": ("BV_SUB_DIVIDER", {})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = True

    def out(self, divider):
        return ()


class BVSubgraphSpacer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "spacer": ("BV_SUB_SPACER", {})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = True

    def out(self, spacer):
        return ()


class BVSubgraphIntSlider:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BV_SUB_INT_SLIDER", {"default": 0}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = False

    def out(self, value):
        try:
            return (int(round(float(value))),)
        except Exception:
            return (0,)


def _round_fixed(value, places: int) -> float:
    try:
        q = Decimal(10) ** (-places)
        d = Decimal(str(float(value)))
        return float(d.quantize(q, rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError, TypeError):
        return 0.0


class BVSubgraphFloat1Slider:
    FIXED_PREC = 1

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BV_SUB_FLOAT1_SLIDER", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = False

    def out(self, value):
        return (_round_fixed(value, self.FIXED_PREC),)


class BVSubgraphFloat2Slider:
    FIXED_PREC = 2

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BV_SUB_FLOAT2_SLIDER", {"default": 0.00}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = False

    def out(self, value):
        return (_round_fixed(value, self.FIXED_PREC),)


class BVSubgraphFloat3Slider:
    FIXED_PREC = 3

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BV_SUB_FLOAT3_SLIDER", {"default": 0.000}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "out"
    CATEGORY = "🌀 BVortex Nodes/Subgraph"
    OUTPUT_NODE = False

    def out(self, value):
        return (_round_fixed(value, self.FIXED_PREC),)


NODE_CLASS_MAPPINGS = {
    "BV Subgraph Title": BVSubgraphTitle,
    "BV Subgraph Heading": BVSubgraphHeading,
    "BV Subgraph Divider": BVSubgraphDivider,
    "BV Subgraph Spacer": BVSubgraphSpacer,
    "BV Subgraph Int Slider": BVSubgraphIntSlider,
    "BV Subgraph Float1 Slider": BVSubgraphFloat1Slider,
    "BV Subgraph Float2 Slider": BVSubgraphFloat2Slider,
    "BV Subgraph Float3 Slider": BVSubgraphFloat3Slider,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Subgraph Title": "🌀 BV Subgraph Title",
    "BV Subgraph Heading": "🌀 BV Subgraph Heading",
    "BV Subgraph Divider": "🌀 BV Subgraph Divider",
    "BV Subgraph Spacer": "🌀 BV Subgraph Spacer",
    "BV Subgraph Int Slider": "🌀 BV Subgraph Int Slider",
    "BV Subgraph Float1 Slider": "🌀 BV Subgraph Float1 Slider",
    "BV Subgraph Float2 Slider": "🌀 BV Subgraph Float2 Slider",
    "BV Subgraph Float3 Slider": "🌀 BV Subgraph Float3 Slider",
}
