import pyautogui
from datetime import datetime
from pynput import mouse, keyboard
import pytesseract


class CaptureScreen:
    def __init__(self, config=None):
        self.start_capture_key = config['start_capture_key'] if config else 's'
        self.exit_key = config['exit_key'] if config else 'q'
        self.mouse_listener = None
        self.keyboard_listener = None
        self.pressed_x = 0
        self.pressed_y = 0
        self.released_x = 0
        self.released_y = 0

    def capture_screen(self, region=None):
        screenshot = pyautogui.screenshot(region=region)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot.save(f'screenshot_{timestamp}.png')
        string = self.ocr(screenshot)
        print(string)
        return screenshot

    def ocr(self, image):
        return pytesseract.image_to_string(image, lang='chi_tra')

    def on_click(self, x, y, button, pressed):
        if pressed:
            print(f'Mouse pressed at ({x}, {y}) with {button}')
            self.pressed_x = x
            self.pressed_y = y
        if not pressed:
            print(f'Mouse released at ({x}, {y}) with {button}')
            self.released_x = x
            self.released_y = y
            self.capture_screen(region=(min(self.pressed_x, self.released_x), min(self.pressed_y, self.released_y),
                                        abs(self.released_x - self.pressed_x), abs(self.released_y - self.pressed_y)))

    def on_press(self, key):
        print(f'Key pressed: {key}')
        try:
            if key.char == self.start_capture_key:  # 按下 's' 鍵開始監聽滑鼠事件
                print("Start capturing mouse events")
                self.mouse_listener=mouse.Listener(on_click=self.on_click)
                self.mouse_listener.start()
            if key.char == self.exit_key:  # 按下 'q' 鍵結束程式
                if self.mouse_listener is not None:
                    self.mouse_listener.stop()
                print("Exit")
                return False

        except AttributeError:
            pass

    def start_capture(self):
        with keyboard.Listener(on_press=self.on_press) as self.keyboard_listener:
            self.keyboard_listener.join()


if __name__ == '__main__':
    capture_screen=CaptureScreen()
    capture_screen.start_capture()
