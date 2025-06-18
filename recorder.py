import json
import time
from pynput import mouse, keyboard
from datetime import datetime


class ActionRecorder:
    def __init__(self):
        self.actions = []
        self.start_time = None
        self.recording = False
        self.mouse_listener = None
        self.keyboard_listener = None

    def start_recording(self):
        """Start recording user actions."""
        self.actions = []
        self.start_time = time.time()
        self.recording = True

        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        self.mouse_listener.start()

        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.keyboard_listener.start()

        print("Recording started. Press Esc to stop recording.")

    def stop_recording(self):
        """Stop recording user actions."""
        if self.recording:
            self.recording = False

            # Stop listeners
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()

            print("Recording stopped.")
            return True
        return False

    def on_mouse_move(self, x, y):
        """Record mouse movement."""
        if self.recording:
            self.actions.append({
                'type': 'mouse_move',
                'x': x,
                'y': y,
                'time': time.time() - self.start_time
            })

    def on_mouse_click(self, x, y, button, pressed):
        """Record mouse clicks."""
        if self.recording:
            self.actions.append({
                'type': 'mouse_click',
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed,
                'time': time.time() - self.start_time
            })

    def on_mouse_scroll(self, x, y, dx, dy):
        """Record mouse scrolling."""
        if self.recording:
            self.actions.append({
                'type': 'mouse_scroll',
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'time': time.time() - self.start_time
            })

    def on_key_press(self, key):
        """Record key press events."""
        if self.recording:
            # Check if Esc key is pressed to stop recording
            if key == keyboard.Key.esc:
                self.stop_recording()
                return False

            self.actions.append({
                'type': 'key_press',
                'key': str(key),
                'time': time.time() - self.start_time
            })

    def on_key_release(self, key):
        """Record key release events."""
        if self.recording:
            self.actions.append({
                'type': 'key_release',
                'key': str(key),
                'time': time.time() - self.start_time
            })

    def save_to_file(self, filename=None):
        """Save recorded actions to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recorded_actions_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(self.actions, f, indent=4)

        print(f"Actions saved to {filename}")
        return filename


def main():
    recorder = ActionRecorder()
    print("Action Recorder")
    print("===============")
    print("This program will record your mouse and keyboard actions.")
    print("Press Enter to start recording and Esc to stop.")

    input("Press Enter to start recording...")
    recorder.start_recording()

    # Wait for recording to stop (when Esc is pressed)
    while recorder.recording:
        time.sleep(0.1)

    # Save the recorded actions
    recorder.save_to_file()


if __name__ == "__main__":
    main()