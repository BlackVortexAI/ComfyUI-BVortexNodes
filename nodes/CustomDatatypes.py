class BV_IMAGE_PIPE:
    def __init__(self, image, count, count_zero_padding, offset_count, offset_count_zero_padding, caption=""):
        self.image = image
        self.count = count
        self.count_zero_padding = count_zero_padding
        self.offset_count = offset_count
        self.offset_count_zero_padding = offset_count_zero_padding
        self.caption = caption

class BV_UPSCALE_CONFIG_PIPE:
    def __init__(self, upscale_lowres, lowres_limit, resolution_steps, max_resolution):
        self.upscale_lowres = upscale_lowres
        self.lowres_limit = lowres_limit
        self.resolution_steps = resolution_steps
        self.max_resolution = max_resolution
