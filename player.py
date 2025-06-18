import json
import time
import pyautogui
import sys
from pynput.mouse import Button
from pynput.keyboard import Key


class ActionPlayer:
    def __init__(self, filename=None):
        self.actions = []
        self.filename = filename

        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to upper-left corner to abort
        pyautogui.PAUSE = 0  # No pause between pyautogui commands (we'll handle timing)

    def load_from_file(self, filename=None):
        """Load recorded actions from a JSON file."""
        if filename:
            self.filename = filename

        if not self.filename:
            print("Error: No filename specified.")
            return False

        try:
            with open(self.filename, 'r') as f:
                self.actions = json.load(f)
            print(f"Loaded {len(self.actions)} actions from {self.filename}")
            return True
        except FileNotFoundError:
            print(f"Error: File {self.filename} not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error: File {self.filename} is not a valid JSON file.")
            return False

    def play(self):
        """Play back the recorded actions."""
        if not self.actions:
            print("No actions to play. Load a file first.")
            return

        print(f"Playing back {len(self.actions)} actions...")
        print("Move mouse to upper-left corner to abort.")
        print("Starting in 3 seconds...")
        time.sleep(3)

        # Get the first action's time as reference
        start_time = time.time()
        last_action_time = 0

        for action in self.actions:
            # Calculate how long to wait before executing this action
            action_time = action['time']
            time_to_wait = action_time - last_action_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)

            # Execute the action based on its type
            action_type = action['type']

            if action_type == 'mouse_move':
                pyautogui.moveTo(action['x'], action['y'])

            elif action_type == 'mouse_click':
                button = action['button']
                pressed = action['pressed']

                # Convert pynput button string to pyautogui button
                if 'left' in button:
                    button_name = 'left'
                elif 'right' in button:
                    button_name = 'right'
                elif 'middle' in button:
                    button_name = 'middle'
                else:
                    button_name = 'left'  # Default to left button

                if pressed:
                    pyautogui.mouseDown(x=action['x'], y=action['y'], button=button_name)
                else:
                    pyautogui.mouseUp(x=action['x'], y=action['y'], button=button_name)

            elif action_type == 'mouse_scroll':
                # PyAutoGUI uses clicks, not exact pixel values for scrolling
                # Convert dy to clicks (approximate)
                clicks = int(action['dy'] * 5)  # Adjust multiplier as needed
                pyautogui.scroll(clicks)

            elif action_type == 'key_press':
                key_str = action['key']

                # Handle special keys
                if key_str.startswith("Key."):
                    key_name = key_str[4:]  # Remove "Key." prefix

                    # Map pynput special keys to pyautogui keys
                    special_keys = {
                        'alt': 'alt',
                        'alt_l': 'altleft',
                        'alt_r': 'altright',
                        'alt_gr': 'altright',
                        'backspace': 'backspace',
                        'caps_lock': 'capslock',
                        'cmd': 'command',
                        'cmd_l': 'winleft',
                        'cmd_r': 'winright',
                        'ctrl': 'ctrl',
                        'ctrl_l': 'ctrlleft',
                        'ctrl_r': 'ctrlright',
                        'delete': 'delete',
                        'down': 'down',
                        'end': 'end',
                        'enter': 'enter',
                        'esc': 'escape',
                        'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
                        'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
                        'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
                        'home': 'home',
                        'insert': 'insert',
                        'left': 'left',
                        'page_down': 'pagedown',
                        'page_up': 'pageup',
                        'right': 'right',
                        'shift': 'shift',
                        'shift_l': 'shiftleft',
                        'shift_r': 'shiftright',
                        'space': 'space',
                        'tab': 'tab',
                        'up': 'up'
                    }

                    if key_name in special_keys:
                        pyautogui.keyDown(special_keys[key_name])
                    else:
                        print(f"Unsupported special key: {key_str}")

                # Handle regular keys
                elif key_str.startswith("'") and key_str.endswith("'"):
                    # Extract the character from the string representation
                    char = key_str[1:-1]
                    pyautogui.keyDown(char)
                else:
                    print(f"Unsupported key format: {key_str}")

            elif action_type == 'key_release':
                key_str = action['key']

                # Handle special keys
                if key_str.startswith("Key."):
                    key_name = key_str[4:]  # Remove "Key." prefix

                    # Map pynput special keys to pyautogui keys (same mapping as above)
                    special_keys = {
                        'alt': 'alt',
                        'alt_l': 'altleft',
                        'alt_r': 'altright',
                        'alt_gr': 'altright',
                        'backspace': 'backspace',
                        'caps_lock': 'capslock',
                        'cmd': 'command',
                        'cmd_l': 'winleft',
                        'cmd_r': 'winright',
                        'ctrl': 'ctrl',
                        'ctrl_l': 'ctrlleft',
                        'ctrl_r': 'ctrlright',
                        'delete': 'delete',
                        'down': 'down',
                        'end': 'end',
                        'enter': 'enter',
                        'esc': 'escape',
                        'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
                        'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
                        'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
                        'home': 'home',
                        'insert': 'insert',
                        'left': 'left',
                        'page_down': 'pagedown',
                        'page_up': 'pageup',
                        'right': 'right',
                        'shift': 'shift',
                        'shift_l': 'shiftleft',
                        'shift_r': 'shiftright',
                        'space': 'space',
                        'tab': 'tab',
                        'up': 'up'
                    }

                    if key_name in special_keys:
                        pyautogui.keyUp(special_keys[key_name])
                    else:
                        print(f"Unsupported special key: {key_str}")

                # Handle regular keys
                elif key_str.startswith("'") and key_str.endswith("'"):
                    # Extract the character from the string representation
                    char = key_str[1:-1]
                    pyautogui.keyUp(char)
                else:
                    print(f"Unsupported key format: {key_str}")

            # Update the last action time
            last_action_time = action_time

        print("Playback completed.")


def main():
    player = ActionPlayer()

    print("Action Player")
    print("=============")
    print("This program will play back recorded actions from a JSON file.")

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the path to the JSON file with recorded actions: ")

    if player.load_from_file(filename):
        input("Press Enter to start playback (or Ctrl+C to cancel)...")
        player.play()


if __name__ == "__main__":
    main()