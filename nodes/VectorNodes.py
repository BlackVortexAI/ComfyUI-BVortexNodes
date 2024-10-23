static_entries = [
    "INPUT LAYER", "MMDiT idx 0", "MMDiT idx 1", "MMDiT idx 2", "MMDiT idx 3", "MMDiT idx 4", "MMDiT idx 5",
    "MMDiT idx 6", "MMDiT idx 7", "MMDiT idx 8", "MMDiT idx 9", "MMDiT idx 10", "MMDiT idx 11",
    "MMDiT idx 12", "MMDiT idx 13", "MMDiT idx 14", "MMDiT idx 15", "MMDiT idx 16", "MMDiT idx 17",
    "MMDiT idx 18", "DiT idx 0", "DiT idx 1", "DiT idx 2", "DiT idx 3", "DiT idx 4", "DiT idx 5",
    "DiT idx 6", "DiT idx 7", "DiT idx 8", "DiT idx 9", "DiT idx 10", "DiT idx 11", "DiT idx 12",
    "DiT idx 13", "DiT idx 14", "DiT idx 15", "DiT idx 16", "DiT idx 17", "DiT idx 18", "DiT idx 19",
    "DiT idx 20", "DiT idx 21", "DiT idx 22", "DiT idx 23", "DiT idx 24", "DiT idx 25", "DiT idx 26",
    "DiT idx 27", "DiT idx 28", "DiT idx 29", "DiT idx 30", "DiT idx 31", "DiT idx 32", "DiT idx 33",
    "DiT idx 34", "DiT idx 35", "DiT idx 36", "DiT idx 37"
]


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

    @classmethod
    def IS_CHANGED(self):
        return float("NaN")


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

    @classmethod
    def IS_CHANGED(self):
        return float("NaN")


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

    @classmethod
    def IS_CHANGED(self):
        return float("NaN")


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

    @classmethod
    def IS_CHANGED(self):
        return float("NaN")


class BVVectorEditDropdownNode:
    @classmethod
    def INPUT_TYPES(cls):

        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
            },
            "optional": {
                "entry_index": (["CHOOSE"] + static_entries,),
                "new_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("VECTOR",)
    FUNCTION = "edit_vector"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def edit_vector(self, vector: list, entry_index: str, new_value: float):

        # Den Index der Auswahl ermitteln
        if entry_index in static_entries:
            index_number = static_entries.index(entry_index)
            if index_number < len(vector):
                vector[index_number] = new_value
        return (vector,)

    @classmethod
    def IS_CHANGED(cls):
        return False


class BVVectorEditRangeDropdownNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
                "start_index": (["CHOOSE"] + static_entries,),
                "end_index": (["CHOOSE"] + static_entries,),
                "new_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("VECTOR",)
    FUNCTION = "edit_vector_range"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def edit_vector_range(self, vector: list, start_index: str, end_index: str, new_value: float):

        if start_index in static_entries and end_index in static_entries:
            start_idx = static_entries.index(start_index)
            end_idx = static_entries.index(end_index)
            # Ensure end_idx is within bounds and greater than or equal to start_idx
            end_idx = min(end_idx+1, len(vector))
            for i in range(start_idx, end_idx):
                if 0 <= i < len(vector):
                    vector[i] = new_value

        return (vector,)

    @classmethod
    def IS_CHANGED(cls):
        return False


class BVVectorEditRangeNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
                "start_index": ("INT", {"default": 0, "min": 0}),
                "end_index": ("INT", {"default": 1, "min": 0}),
                "new_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("VECTOR",)
    FUNCTION = "edit_vector_range"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def edit_vector_range(self, vector: list, start_index: int, end_index: int, new_value: float):
        # Ensure end_index is within bounds and greater than or equal to start_index
        end_index = min(end_index+1, len(vector))
        for i in range(start_index, end_index):
            if 0 <= i < len(vector):
                vector[i] = new_value
        return (vector,)

    @classmethod
    def IS_CHANGED(self):
        return float("NaN")


class BVVectorEditBooleanNode:
    @classmethod
    def INPUT_TYPES(cls):
        # Statische Einträge als Boolean-Felder statt Dropdown
        optional_fields = {
            entry: ("BOOLEAN", {
                "default": False,
                "label_on": "Edit",
                "label_off": "Do not edit"
            }) for entry in static_entries
        }

        return {
            "required": {
                "vector": ("LIST", {"element_type": "FLOAT"}),
                "new_value": ("FLOAT", {"default": 0.0, "step": 0.01}),
            },
            "optional": optional_fields
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("VECTOR",)
    FUNCTION = "edit_vector"
    CATEGORY = "🌀 BVortex Nodes/Vectors"

    def edit_vector(self, vector: list, new_value: float, **kwargs):
        # Bearbeiten des Vektors basierend auf den aktivierten Boolean-Feldern
        for entry, is_active in kwargs.items():
            if isinstance(is_active, bool) and is_active:
                normalized_entry = entry
                if normalized_entry in static_entries:
                    index_number = static_entries.index(normalized_entry)
                    if 0 <= index_number < len(vector):
                        vector[index_number] = new_value

        return (vector,)

    @classmethod
    def IS_CHANGED(cls):
        return False


NODE_CLASS_MAPPINGS = {
    "BV Vector of Length-n": BVVectorOfLengthNNode,
    "BV Vector Edit": BVVectorEditNode,
    "BV Vector to String": BVVectorToStringNode,
    "BV Vector to String List": BVVectorToStringListNode,
    "BV Vector Permutation": BVVectorPermutationNode,
    "BV Vector Edit Dropdown FLUX": BVVectorEditDropdownNode,
    "BV Vector Edit Range": BVVectorEditRangeNode,
    "BV Vector Edit Range Dropdown FLUX": BVVectorEditRangeDropdownNode,
    "BV Vector Edit Selector FLUX": BVVectorEditBooleanNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Vector of Length-n": "🌀 BV Vector of Length-n",
    "BV Vector Edit": "🌀 BV Vector Edit",
    "BV Vector to String": "🌀 BV Vector to String",
    "BV Vector to String List": "🌀 BV Vector to String List",
    "BV Vector Permutation": "🌀 BV Vector Permutation",
    "BV Vector Edit Dropdown FLUX": "🌀 BV Vector Edit Dropdown FLUX",
    "BV Vector Edit Range": "🌀 BV Vector Edit Range",
    "BV Vector Edit Range Dropdown FLUX": "🌀 BV Vector Edit Range Dropdown FLUX",
    "BV Vector Edit Selector FLUX": "🌀 BV Vector Edit Selector FLUX",
}
