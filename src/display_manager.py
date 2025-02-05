import os
import epd13in3E
from inky.auto import auto
from utils.image_utils import resize_image, change_orientation
from plugins.plugin_registry import get_plugin_instance


class DisplayManager:
    def __init__(self, device_config):
        """
        Manages the display and rendering of images.

        :param config: The device configuration (Config class).
        :param default_image: Path to the default image to display.
        """
        self.device_config = device_config
        self.epd = epd13in3E.EPD()
        self.epd.Init()

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

        plugin_instance = get_plugin_instance(plugin_config)
        image = plugin_instance.generate_image(plugin_settings, self.device_config)

        # Save the image
        image.save(self.device_config.current_image_file)

        # Resize and adjust orientation
        image = change_orientation(image, self.device_config.get_config("orientation"))
        image = resize_image(image, self.device_config.get_resolution(), plugin_config.get('image_settings', []))

        # Display the image on the Inky display
        self.epd.display(self.epd.getbuffer(image))

    def display_image(self, image):
        """
        Displays the image provided.

        :param image: Pillow Image object.
        """
        if not image:
            raise ValueError(f"No image provided.")

        # Save the image
        image.save(self.device_config.current_image_file)

        # Resize and adjust orientation
        image = resize_image(image, self.device_config.get_resolution())

        # Display the image on the Inky display
        self.epd.display(self.epd.getbuffer(image))
