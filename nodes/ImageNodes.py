import torch
import numpy as np
import torch.nn.functional as F
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
from PIL import Image
import cv2


class BVImageDifferenceHeatmap:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE", {}),
                "image2": ("IMAGE", {}),
                "overlay_strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 5.0, "step": 0.01}),
                "colormap": (["jet", "viridis", "plasma", "inferno", "magma", "cividis", "turbo", "hot", "cool", "jet_r", "viridis_r", "plasma_r", "inferno_r", "magma_r", "cividis_r", "turbo_r", "hot_r", "cool_r"],),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "FLOAT", "INT")
    RETURN_NAMES = ("heatmap", "overlay_image1", "overlay_image2", "difference_strength", "mse_value")
    FUNCTION = "process_difference"
    CATEGORY = "🌀 BVortex Nodes/Image Processing"

    def process_difference(self, image1, image2, overlay_strength, colormap):
        # Ensure images are in the expected format: [B, H, W, C]
        if image1.shape != image2.shape:
            raise ValueError(f"The two images have different sizes: {image1.shape} and {image2.shape}")

        # Step 1: Convert to [B, C, H, W] for torch operations
        image1 = image1.permute(0, 3, 1, 2).contiguous()
        image2 = image2.permute(0, 3, 1, 2).contiguous()

        # Step 2: Compute the difference and normalize
        difference = torch.abs(image1 - image2)
        max_diff, _ = torch.max(difference.reshape(difference.size(0), -1), dim=1, keepdim=True)
        max_diff = max_diff.view(-1, 1, 1, 1)
        normalized_diff = difference / (max_diff + 1e-8)

        # Calculate the overall difference strength as a float between 0 and 1
        difference_strength = torch.mean(normalized_diff).item()

        # Step 3: Create the heatmap using Gaussian blur for smoothing
        heatmap = normalized_diff.mean(dim=1, keepdim=True)  # Convert to grayscale
        heatmap_np = heatmap.squeeze().cpu().numpy()  # Convert to numpy array for processing
        blurred_heatmap_np = gaussian_filter(heatmap_np, sigma=15)  # Apply stronger Gaussian blur for cloud effect

        # Invert the heatmap (black for no change, white for maximum change)
        inverted_heatmap_np = 1 - blurred_heatmap_np

        # Step 4: Create a color heatmap using Matplotlib
        fig, ax = plt.subplots(figsize=(blurred_heatmap_np.shape[1] / 100, blurred_heatmap_np.shape[0] / 100), dpi=100)
        ax.imshow(inverted_heatmap_np, cmap=colormap)
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig)
        buf.seek(0)

        # Convert the saved heatmap image back to tensor
        heatmap_image = Image.open(buf).convert('RGBA')  # Ensure 4 channels (RGBA)
        heatmap_tensor = torch.from_numpy(np.array(heatmap_image)).float() / 255.0  # Normalize to [0, 1]
        heatmap_tensor = heatmap_tensor.permute(2, 0, 1).unsqueeze(0).to(image1.device)  # [B, C, H, W]
        heatmap_tensor = F.interpolate(heatmap_tensor, size=(image1.shape[2], image1.shape[3]), mode='bilinear')
        heatmap_tensor = torch.clamp(heatmap_tensor, 0, 1).permute(0, 2, 3, 1)  # [B, H, W, C]

        # Step 5: Extract start and end colors for transparency mapping
        cmap = cm.get_cmap(colormap)
        start_color = torch.tensor(cmap(0)[:3], device=image1.device)  # Get RGB values for the leftmost color (start)
        end_color = torch.tensor(cmap(1)[:3], device=image1.device)  # Get RGB values for the rightmost color (end)

        # Step 6: Calculate transparency based on the color mapping
        diff_color = (heatmap_tensor[..., :3] - start_color.view(1, 1, 1, 3)).abs().sum(dim=-1, keepdim=True)
        max_diff_color = (end_color - start_color).abs().sum()
        alpha_tensor = torch.clamp(diff_color / max_diff_color, 0, 1) * overlay_strength  # Adjust overlay strength
        alpha_tensor = alpha_tensor.permute(0, 3, 1, 2)  # [B, 1, H, W]

        # Step 7: Overlay heatmap on image1 and image2 using calculated transparency
        overlay_image1 = (1 - alpha_tensor) * image1 + alpha_tensor * heatmap_tensor[..., :3].permute(0, 3, 1, 2)
        overlay_image2 = (1 - alpha_tensor) * image2 + alpha_tensor * heatmap_tensor[..., :3].permute(0, 3, 1, 2)

        # Ensure the values are clamped between 0 and 1
        overlay_image1 = torch.clamp(overlay_image1, 0, 1).permute(0, 2, 3, 1)
        overlay_image2 = torch.clamp(overlay_image2, 0, 1).permute(0, 2, 3, 1)

        # Step 8: Calculate Mean Squared Error (MSE) between image1 and image2 using numpy
        image1_np = image1.permute(0, 2, 3, 1).squeeze().cpu().numpy() * 255.0  # Convert to numpy and scale to [0, 255]
        image2_np = image2.permute(0, 2, 3, 1).squeeze().cpu().numpy() * 255.0
        mse_value = int(np.mean((image1_np - image2_np) ** 2))

        return heatmap_tensor, overlay_image1, overlay_image2, difference_strength, mse_value


NODE_CLASS_MAPPINGS = {
    "BV Image Difference Heatmap": BVImageDifferenceHeatmap,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BV Image Difference Heatmap": "🌀 BV Image Difference Heatmap",
}
