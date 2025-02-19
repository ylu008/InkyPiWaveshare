import os
import epd13in3E
from inky.auto import auto
from utils.image_utils import resize_image, change_orientation
from plugins.plugin_registry import get_plugin_instance
from PIL import Image

# Define the six colors supported by Waveshare E Ink
WAVESHARE_PALETTE = [
    (0, 0, 0),        # Black
    (255, 255, 255),  # White
    (255, 255, 0),    # Yellow
    (255, 0, 0),      # Red
    (0, 0, 255),      # Blue
    (0, 255, 0),      # Green
]

def quantize_image(image):
    """
    Converts an image to the 6-color palette supported by Waveshare E Ink
    using dithering.
    """
    # Convert image to RGB if not already
    image = image.convert("RGB")

    # Create a palette image with only the 6 supported colors
    palette_image = Image.new("P", (1, 1))
    palette = []
    for color in WAVESHARE_PALETTE:
        palette.extend(color)  # Flatten RGB tuples
    palette_image.putpalette(palette + [0] * (256 - len(WAVESHARE_PALETTE)) * 3)

    # Convert the image using the custom palette with dithering
    return image.quantize(palette=palette_image, dither=Image.Dither.FLOYDSTEINBERG)

class DisplayManager:
    def __init__(self, device_config):
        """
        Manages the display and rendering of images.

        :param config: The device configuration (Config class).
        """
        self.device_config = device_config
        self.epd = epd13in3E.EPD()
        self.epd.Init()
        self.epd.Clear()

        # store display resolution in device config
        device_config.update_value("resolution", [int(self.epd.width), int(self.epd.height)])

    def display_plugin(self, plugin_settings):
        """
        Generates and displays an image based on plugin settings.

        :param plugin_settings: Dictionary containing plugin settings.
        """
        plugin_id = plugin_settings.get("plugin_id")
        plugin_config = next((plugin for plugin in self.device_config.get_plugins() if plugin['id'] == plugin_id), None)

        if not plugin_config:
            raise ValueError(f"Plugin '{plugin_id}' not found.")
        self.epd.Init()

        plugin_instance = get_plugin_instance(plugin_config)
        image = plugin_instance.generate_image(plugin_settings, self.device_config)

        # Save the image
        image.save(self.device_config.current_image_file)

        # Resize and adjust orientation
        image = change_orientation(image, self.device_config.get_config("orientation"))
        image = resize_image(image, self.device_config.get_resolution(), plugin_config.get('image_settings', []))

        # Convert the image to the supported colors using dithering
        image = quantize_image(image)

        # Display the image on the Inky display
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()

    def display_image(self, image):
        """
        Displays the image provided.

        :param image: Pillow Image object.
        """
        if not image:
            raise ValueError(f"No image provided.")
        
        self.epd.Init()
        
        # Resize and adjust orientation
        image = resize_image(image, self.device_config.get_resolution())

        # Convert the image to the supported colors using dithering
        image = quantize_image(image)

        # Save the processed image
        image.save(self.device_config.current_image_file)

        # Display the image on the Inky display
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()
