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


NODE_CLASS_MAPPINGS = {
    "BV Subgraph Title": BVSubgraphTitle,
    "BV Subgraph Heading": BVSubgraphHeading,
    "BV Subgraph Divider": BVSubgraphDivider,
    "BV Subgraph Spacer": BVSubgraphSpacer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Subgraph Title": "🌀 BV Subgraph Title",
    "BV Subgraph Heading": "🌀 BV Subgraph Heading",
    "BV Subgraph Divider": "🌀 BV Subgraph Divider",
    "BV Subgraph Spacer": "🌀 BV Subgraph Spacer"
}
