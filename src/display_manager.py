import os
import epd13in3E
from inky.auto import auto
from utils.image_utils import resize_image, change_orientation
from plugins.plugin_registry import get_plugin_instance
from PIL import Image
import numpy as np

class DisplayManager:
    def __init__(self, device_config):
        """
        Manages the display and rendering of images.

        :param device_config: The device configuration (Config class).
        """
        self.device_config = device_config
        self.epd = epd13in3E.EPD()
        self.epd.Init()

        # Store display resolution in device config
        device_config.update_value("resolution", [int(self.epd.width), int(self.epd.height)])

    def apply_dithering(self, image):
        """
        Applies Floyd-Steinberg dithering to the image.
        
        :param image: Pillow Image object
        :return: Dithered Pillow Image object
        """
        image = image.convert("L")  # Convert to grayscale
        image_data = np.array(image, dtype=np.uint8)
        height, width = image_data.shape
        
        for y in range(height):
            for x in range(width):
                old_pixel = image_data[y, x]
                new_pixel = 255 if old_pixel > 127 else 0
                image_data[y, x] = new_pixel
                error = old_pixel - new_pixel
                
                if x < width - 1:
                    image_data[y, x + 1] += error * 7 / 16
                if y < height - 1:
                    if x > 0:
                        image_data[y + 1, x - 1] += error * 3 / 16
                    image_data[y + 1, x] += error * 5 / 16
                    if x < width - 1:
                        image_data[y + 1, x + 1] += error * 1 / 16
        
        return Image.fromarray(image_data.astype(np.uint8))

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

        # Resize, adjust orientation, and apply dithering
        image = change_orientation(image, self.device_config.get_config("orientation"))
        image = resize_image(image, self.device_config.get_resolution(), plugin_config.get('image_settings', []))
        image = self.apply_dithering(image)

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
        # Save the image
        image.save(self.device_config.current_image_file)

        # Resize, adjust orientation, and apply dithering
        image = resize_image(image, self.device_config.get_resolution())
        image = self.apply_dithering(image)

        # Display the image on the Inky display
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()
