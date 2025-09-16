import gradio as gr
import io
import sys
from PIL import Image
sys.path.insert(0, 'src')

from rayt.camera import Camera
from rayt.cli import random_scene
from rayt.numba_renderer import render_with_numba
from rayt.vec3 import Point3, Vec3

def render_image(image_width, samples_per_pixel, aspect_ratio_str, max_depth):
    """
    Renders an image using the rayt library and returns it.
    """
    # --- Capture stdout ---
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()

    # --- Run the rendering logic ---
    aspect_ratio = eval(aspect_ratio_str)
    image_height = int(image_width / aspect_ratio)
    world = random_scene()
    camera = Camera(
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),
        vfov=20.0,
        aspect_ratio=aspect_ratio,
        aperture=0.1,
        focus_dist=10.0,
    )

    render_with_numba(world, camera, image_width, image_height, samples_per_pixel, max_depth)

    # --- Restore stdout and get the PPM data ---
    sys.stdout = old_stdout
    ppm_data = captured_output.getvalue()

    # --- Convert PPM to Image ---
    # The PPM data is in a string, so we need to wrap it in a file-like object
    ppm_file = io.BytesIO(ppm_data.encode())
    image = Image.open(ppm_file)

    return image

# --- Create the Gradio Interface ---
with gr.Blocks() as iface:
    gr.Markdown("# Ray Tracing in One Weekend")
    gr.Markdown("A Python implementation of the book by Peter Shirley, rendered with Numba.")

    with gr.Row():
        with gr.Column():
            image_width = gr.Slider(label="Image Width", minimum=100, maximum=1200, value=300, step=10)
            samples_per_pixel = gr.Slider(label="Samples Per Pixel", minimum=1, maximum=200, value=20, step=1)
            max_depth = gr.Slider(label="Max Ray Depth", minimum=1, maximum=100, value=50, step=1)
            aspect_ratio = gr.Dropdown(label="Aspect Ratio", choices=["16/9", "3/2", "1/1"], value="16/9")
            render_button = gr.Button("Render Image")
        with gr.Column():
            output_image = gr.Image(label="Rendered Image", type="pil")

    render_button.click(
        fn=render_image,
        inputs=[image_width, samples_per_pixel, aspect_ratio, max_depth],
        outputs=output_image
    )

if __name__ == "__main__":
    iface.launch()
