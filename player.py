import json
import time
import pyautogui
import sys
import logging

from pynput import keyboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActionPlayer:
    """Class for playing back recorded actions from a JSON file."""

    STARTUP_DELAY = 0

    # Map pynput special keys to pyautogui keys
    SPECIAL_KEYS_MAP = {
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

    def __init__(self, filename=None):
        """Initialize the ActionPlayer.

        Args:
            filename (str, optional): Path to the JSON file with recorded actions.
        """
        self.actions = []
        self.filename = filename

        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to upper-left corner to abort
        pyautogui.PAUSE = 0  # No pause between pyautogui commands (we'll handle timing)
        logger.info("ActionPlayer initialized")

    def load_from_file(self, filename=None):
        """Load recorded actions from a JSON file.

        Args:
            filename (str, optional): Path to the JSON file with recorded actions.
                If not provided, uses the filename from initialization.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        if filename:
            self.filename = filename

        if not self.filename:
            logger.error("No filename specified")
            return False

        try:
            with open(self.filename, 'r') as f:
                self.actions = json.load(f)
            logger.info(f"Loaded {len(self.actions)} actions from {self.filename}")
            return True
        except FileNotFoundError:
            logger.error(f"File {self.filename} not found")
            return False
        except json.JSONDecodeError:
            logger.error(f"File {self.filename} is not a valid JSON file")
            return False
        except Exception as e:
            logger.error(f"Error loading file: {str(e)}")
            return False

    def _convert_button_name(self, button):
        """Convert pynput button string to pyautogui button name.

        Args:
            button (str): Button string from pynput.

        Returns:
            str: Button name for pyautogui.
        """
        if 'left' in button:
            return 'left'
        elif 'right' in button:
            return 'right'
        elif 'middle' in button:
            return 'middle'
        else:
            logger.warning(f"Unknown button: {button}, defaulting to left")
            return 'left'  # Default to left button

    def _handle_key(self, key_str, is_press=True):
        """Handle key press or release.

        Args:
            key_str (str): Key string from pynput.
            is_press (bool): True for key press, False for key release.
        """
        action = "keyDown" if is_press else "keyUp"

        # Handle special keys
        if key_str.startswith("Key."):
            key_name = key_str[4:]  # Remove "Key." prefix

            if key_name in self.SPECIAL_KEYS_MAP:
                if is_press:
                    pyautogui.keyDown(self.SPECIAL_KEYS_MAP[key_name])
                else:
                    pyautogui.keyUp(self.SPECIAL_KEYS_MAP[key_name])
            else:
                logger.warning(f"Unsupported special key: {key_str}")

        # Handle regular keys
        elif key_str.startswith("'") and key_str.endswith("'"):
            # Extract the character from the string representation
            char = key_str[1:-1]
            if is_press:
                pyautogui.keyDown(char)
            else:
                pyautogui.keyUp(char)
        else:
            logger.warning(f"Unsupported key format: {key_str}")

    def _handle_mouse_move(self, action):
        """Handle mouse movement action.

        Args:
            action (dict): Action data.
        """
        try:
            pyautogui.moveTo(action['x'], action['y'])
        except Exception as e:
            logger.error(f"Error in mouse move: {str(e)}")

    def _handle_mouse_click(self, action):
        """Handle mouse click action.

        Args:
            action (dict): Action data.
        """
        try:
            button = self._convert_button_name(action['button'])
            pressed = action['pressed']

            if pressed:
                pyautogui.mouseDown(x=action['x'], y=action['y'], button=button)
            else:
                pyautogui.mouseUp(x=action['x'], y=action['y'], button=button)
        except Exception as e:
            logger.error(f"Error in mouse click: {str(e)}")

    def _handle_mouse_scroll(self, action):
        """Handle mouse scroll action.

        Args:
            action (dict): Action data.
        """
        try:
            # PyAutoGUI uses clicks, not exact pixel values for scrolling
            # Convert dy to clicks (approximate)
            clicks = int(action['dy'] * 5)  # Adjust multiplier as needed
            pyautogui.scroll(clicks)
        except Exception as e:
            logger.error(f"Error in mouse scroll: {str(e)}")

    def play(self):
        """Play back the recorded actions."""
        if not self.actions:
            logger.warning("No actions to play. Load a file first.")
            return

        logger.info(f"Playing back {len(self.actions)} actions...")
        print("Move mouse to upper-left corner to abort.")

        print(f"Starting...")
        time.sleep(self.STARTUP_DELAY)

        last_action_time = 0

        try:
            for action in self.actions:
                # Calculate how long to wait before executing this action
                action_time = action['time']
                time_to_wait = action_time - last_action_time

                if time_to_wait > 0:
                    time.sleep(time_to_wait)

                # Execute the action based on its type
                action_type = action['type']

                if action_type == 'mouse_move':
                    self._handle_mouse_move(action)

                elif action_type == 'mouse_click':
                    self._handle_mouse_click(action)

                elif action_type == 'mouse_scroll':
                    self._handle_mouse_scroll(action)

                elif action_type == 'key_press':
                    self._handle_key(action['key'], is_press=True)

                elif action_type == 'key_release':
                    self._handle_key(action['key'], is_press=False)

                else:
                    logger.warning(f"Unknown action type: {action_type}")

                # Update the last action time
                last_action_time = action_time

            logger.info("Playback completed.")
        except pyautogui.FailSafeException:
            logger.info("Playback aborted by failsafe (mouse moved to upper-left corner)")
        except Exception as e:
            logger.error(f"Error during playback: {str(e)}")
            print(f"Error during playback: {str(e)}")


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
        # Flag to track if playback has started
        playback_started = False

        # Function to handle key presses before playback starts
        def on_pre_playback_key_press(key):
            nonlocal playback_started
            if key == keyboard.Key.enter and not playback_started:
                playback_started = True
                print("Enter key pressed - starting playback...")
                return False  # Stop this listener

        # Start a keyboard listener that waits for Enter key
        print("Press Enter to start playback (or Ctrl+C to cancel)...")
        with keyboard.Listener(on_press=on_pre_playback_key_press) as listener:
            listener.join()  # Wait for Enter key

        # Start playback
        player.play()

if __name__ == "__main__":
    main()
