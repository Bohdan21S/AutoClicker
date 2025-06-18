import json
import time
import logging
from pynput import mouse, keyboard
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActionRecorder:
    """Class for recording user actions (mouse and keyboard) and saving them to a file."""

    def __init__(self):
        """Initialize the ActionRecorder."""
        self.actions = []
        self.start_time = None
        self.recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        logger.info("ActionRecorder initialized")

    def start_recording(self):
        """Start recording user actions.

        This method initializes the action list, sets up mouse and keyboard listeners,
        and begins recording user actions.
        """
        try:
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

            logger.info("Recording started")
            print("Recording started. Press Esc to stop recording.")
            return True
        except Exception as e:
            logger.error(f"Error starting recording: {str(e)}")
            print(f"Error starting recording: {str(e)}")
            return False

    def stop_recording(self):
        """Stop recording user actions.

        This method stops the mouse and keyboard listeners and finalizes the recording.

        Returns:
            bool: True if recording was stopped, False if it wasn't recording.
        """
        if not self.recording:
            logger.warning("Attempted to stop recording, but not currently recording")
            return False

        try:
            self.recording = False

            # Stop listeners
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()

            logger.info(f"Recording stopped. Recorded {len(self.actions)} actions.")
            print("Recording stopped.")
            return True
        except Exception as e:
            logger.error(f"Error stopping recording: {str(e)}")
            print(f"Error stopping recording: {str(e)}")
            return False

    def _record_action(self, action_type, **kwargs):
        """Record an action with the given type and parameters.

        Args:
            action_type (str): The type of action (mouse_move, mouse_click, etc.)
            **kwargs: Additional parameters for the action.
        """
        if not self.recording:
            return

        try:
            action = {
                'type': action_type,
                'time': time.time() - self.start_time,
                **kwargs
            }
            self.actions.append(action)
        except Exception as e:
            logger.error(f"Error recording {action_type} action: {str(e)}")

    def on_mouse_move(self, x, y):
        """Record mouse movement.

        Args:
            x (int): X coordinate of the mouse.
            y (int): Y coordinate of the mouse.
        """
        self._record_action('mouse_move', x=x, y=y)

    def on_mouse_click(self, x, y, button, pressed):
        """Record mouse clicks.

        Args:
            x (int): X coordinate of the mouse.
            y (int): Y coordinate of the mouse.
            button (Button): The button that was clicked.
            pressed (bool): True if the button was pressed, False if released.
        """
        self._record_action('mouse_click', x=x, y=y, button=str(button), pressed=pressed)

    def on_mouse_scroll(self, x, y, dx, dy):
        """Record mouse scrolling.

        Args:
            x (int): X coordinate of the mouse.
            y (int): Y coordinate of the mouse.
            dx (int): Horizontal scroll amount.
            dy (int): Vertical scroll amount.
        """
        self._record_action('mouse_scroll', x=x, y=y, dx=dx, dy=dy)

    def on_key_press(self, key):
        """Record key press events.

        Args:
            key (Key): The key that was pressed.

        Returns:
            bool: False to stop listener if Esc is pressed, None otherwise.
        """
        if not self.recording:
            return

        # Check if Esc key is pressed to stop recording
        if key == keyboard.Key.esc:
            logger.info("Escape key pressed, stopping recording")
            self.stop_recording()
            return False

        self._record_action('key_press', key=str(key))

    def on_key_release(self, key):
        """Record key release events.

        Args:
            key (Key): The key that was released.
        """
        self._record_action('key_release', key=str(key))

    def save_to_file(self, filename=None):
        """Save recorded actions to a JSON file.

        Args:
            filename (str, optional): The filename to save to. If not provided,
                a filename with the current timestamp will be generated.

        Returns:
            str: The filename the actions were saved to, or None if there was an error.
        """
        if not self.actions:
            logger.warning("No actions to save")
            print("No actions to save.")
            return None

        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recorded_actions_{timestamp}.json"

            with open(filename, 'w') as f:
                json.dump(self.actions, f, indent=4)

            logger.info(f"Saved {len(self.actions)} actions to {filename}")
            print(f"Actions saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving to file: {str(e)}")
            print(f"Error saving to file: {str(e)}")
            return None

def main():
    """Main function to run the recorder."""
    try:
        recorder = ActionRecorder()
        print("Action Recorder")
        print("===============")
        print("This program will record your mouse and keyboard actions.")
        print("Press Enter to start recording and Esc to stop.")

        input("Press Enter to start recording...")
        if not recorder.start_recording():
            logger.error("Failed to start recording")
            return

        # Wait for recording to stop (when Esc is pressed)
        try:
            while recorder.recording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Recording interrupted by user (Ctrl+C)")
            recorder.stop_recording()

        # Save the recorded actions
        recorder.save_to_file()
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
