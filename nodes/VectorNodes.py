class BVVectorOfLengthNNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector_length": ("INT", {"default": 1, "min": 1}),
                "default_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("VECTOR",)
    FUNCTION = "initialize_vector"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def initialize_vector(self, vector_length: int, default_value: float):
        vector = [default_value] * vector_length
        return (vector,)


class BVVectorEditNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
                "entry_index": ("INT", {"default": 0, "min": 0}),
                "new_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("VECTOR",)
    FUNCTION = "edit_vector"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def edit_vector(self, vector: list, entry_index: int, new_value: float):
        if 0 <= entry_index < len(vector):
            vector[entry_index] = new_value
        return (vector,)


class BVVectorToStringNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
                "delimiter": ("STRING", {"default": ", "}),
                "include_brackets": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING_RESULT",)
    FUNCTION = "vector_to_string"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def vector_to_string(self, vector: list, delimiter: str, include_brackets: bool):
        result = delimiter.join(map(str, vector))
        if include_brackets:
            result = f"[{result}]"
        return (result,)


class BVVectorToStringListNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING_LIST",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "vector_to_string_list"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def vector_to_string_list(self, vector: list):
        string_list = list(map(str, vector))
        return (string_list,)


class BVVectorPermutationNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
                "indices_to_permute": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("PERMUTATIONS",)
    FUNCTION = "generate_permutations"
    CATEGORY = "🌀 BVortex Nodes/Vectors"
    OUTPUT_IS_LIST = (True,)

    def generate_permutations(self, vector: list, indices_to_permute: str):
        import itertools

        indices = [int(i) - 1 for i in indices_to_permute.split(",") if i.strip().isdigit()]
        permutations = []

        for combination in itertools.product([0.0, 1.0], repeat=len(indices)):
            new_vector = vector[:]
            for i, value in zip(indices, combination):
                new_vector[i] = value
            permutations.append(", ".join(map(str, new_vector)))
            # permutations.append(new_vector)

        return (permutations,)


NODE_CLASS_MAPPINGS = {
    "BV Vector of Length-n": BVVectorOfLengthNNode,
    "BV Vector Edit": BVVectorEditNode,
    "BV Vector to String": BVVectorToStringNode,
    "BV Vector to String List": BVVectorToStringListNode,
    "BV Vector Permutation": BVVectorPermutationNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Vector of Length-n": "🌀 BV Vector of Length-n",
    "BV Vector Edit": "🌀 BV Vector Edit",
    "BV Vector to String": "🌀 BV Vector to String",
    "BV Vector to String List": "🌀 BV Vector to String List",
    "BV Vector Permutation": "🌀 BV Vector Permutation",
}
