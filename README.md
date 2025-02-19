# InkyPiWaveshare
<img src="./docs/images/cover-photo.jpg" />

## Overview
InkyPiWaveshare is a project that integrates a Waveshare e-ink display with a Raspberry Pi, allowing for dynamic content updates. This project is designed to be simple, efficient, and extensible for various display applications, such as news updates, calendar events, or AI-generated content.

## Features
- Supports Waveshare e-ink displays
- Python-based interface
- Customizable content updates
- Low-power consumption for long-term use
- AI-generated dad jokes (because why not?)

## Hardware Requirements
- Raspberry Pi (any model with GPIO support)
- Waveshare e-ink display
- SD card with Raspberry Pi OS
- Power supply for Raspberry Pi

## Installation
1. Clone this repository to your Raspberry Pi:
   ```sh
   git clone https://github.com/ylu008/InkyPiWaveshare.git
   cd InkyPiWaveshare
   ```
2. Run the display script:
   ```sh
   sudo bash install/install.sh
   ```

## Usage
- Image Upload: Upload and display any image from your browser
- Newspaper: Show daily front pages of major newspapers from around the world
- Clock: Customizable clock faces for displaying time
- AI Image: Generate images from text prompts using OpenAI's DALL·E
- AI Text: Display dynamic text content using OpenAI's GPT-4o text models

## Contributing
Pull requests are welcome! Feel free to improve functionality, optimize code, or add new display features.

## License
This project is licensed under the GPL 3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgement
This project is building on https://github.com/fatihak/InkyPi