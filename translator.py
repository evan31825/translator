import json
from src.capture_screen import CaptureScreen


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)
    capture_screen = CaptureScreen(config["screen_capture_config"])
    capture_screen.start_capture()