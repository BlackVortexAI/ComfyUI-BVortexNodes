# BVortex Nodes for ComfyUI

Welcome to BVortex Nodes, a collection of custom nodes designed to extend the functionality of [ComfyUI](https://github.com/comfyanonymous/ComfyUI), providing enhanced image processing capabilities, particularly in the domain of image captioning and resolution management. It also contains helper nodes that facilitate the use of subgraphs. 

## Node Details

This repository contains several nodes that are specifically designed to work with ComfyUI's workflows. Below, you'll find descriptions of the main nodes included:

### BV Subgraph Title / BV Subgraph Heading / BV Subgraph Divider /BV Subgraph Spacer

These four nodes are used to connect to an input from a subgraph and generate a corresponding UI element in the subgraph node. This makes it possible to visually structure and separate input fields.

### BV Conditional ImagePipe Splitter

The **BV Conditional ImagePipe Splitter** node is used to separate images based on their resolution. It takes an input image pipe and splits it into two groups:
- **TO_UPSCALE**: Images whose smaller dimension is below a specified threshold (default: 768 pixels).
- **HIGH_RES_IMAGES**: Images that meet or exceed the resolution limit.

This node is useful for managing images that require upscaling, directing lower-resolution images for further processing while keeping the high-resolution ones intact.

### BV Image Caption Saver

The **BV Image Caption Saver** node allows users to save images along with their corresponding captions. It generates a text file for each image, containing the caption, and supports custom filenames using placeholders like:
- `%count` for image count (with optional offset).
- `%res` for the image resolution.

Additionally, you can organize saved images into subfolders based on their resolution, making it easy to categorize them by quality. The resolution categories are based on steps of 256 pixels.

### BV ImagePipe Junction

The **BVImagePipeJunction** node allows you to read images and captions from an image pipe and also reintegrate them into the pipe. This node is useful for attaching new captions or replacing images in an existing image pipe.

### BV Image Pipe Loader

The **BVImagePipeLoader** node is used to load images from a directory into the image pipe, assigning them with their corresponding count and offset count. The offset count is calculated using the start index. Zero padding defines the number of leading zeros in the numbering, e.g., with a value of 3, '001' or '010' would be generated.

This node also allows you to limit the number of images loaded, define a starting index, and manage file types to ensure flexibility in the workflow.

### BV Image Pipe Merger

The **BVImagePipeMerger** node is used to merge two previously split image pipes back into one after the upscaling process. The merged images are sorted based on their count to maintain the correct sequence, making it easier to manage large sets of images in a coherent manner.

### BV Upscale Config

The **BV Upscale Config** node helps in defining configuration settings for upscaling, such as whether low-resolution images should be upscaled, the resolution limit, and the maximum resolution allowed. This ensures consistent quality and helps automate the decision-making process for upscaling in workflows.

## Installation

To use BVortex Nodes in your ComfyUI setup:

1. Clone this repository into your ComfyUI's nodes directory:
   ```sh
   git clone https://github.com/BlackVortexAI/ComfyUI-BVortexNodes.git
   ```
2. Restart ComfyUI to load the new nodes.

## Usage

These nodes are designed for advanced workflows in image processing, providing greater control over image resolution, upscaling requirements, and captioning. You can easily integrate them into your existing ComfyUI workflows to enhance automation and flexibility.

### Example Workflow
1. Use **BVImagePipeLoader** to load images into the workflow.
2. Apply **BV Conditional ImagePipe Splitter** to divide images based on resolution.
3. Save categorized images and captions using **BV Image Caption Saver**.

## Contributing
Contributions are welcome! If you have any suggestions or find issues, please create an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact
For any questions, feel free to reach out or open an issue in the GitHub repository.

