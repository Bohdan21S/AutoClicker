# AutoClicker - Action Recorder and Player

This project provides two Python programs:
1. **recorder.py** - Records user actions (mouse movements, clicks, keystrokes) with timing information
2. **player.py** - Plays back the recorded actions automatically

## Requirements

- Python 3.6 or higher
- pynput library (for recording)
- pyautogui library (for playback)

## Installation

1. Clone this repository or download the files
2. Install the required libraries:

```
pip install pynput pyautogui
```

## Usage

### Recording Actions

Run the recorder.py script:

```
python recorder.py
```

1. Press Enter to start recording
2. Perform the actions you want to record (mouse movements, clicks, keystrokes)
3. Press Esc to stop recording
4. The recorded actions will be saved to a JSON file with a timestamp in the filename (e.g., `recorded_actions_20250618_204200.json`)

### Playing Back Actions

Run the player.py script:

```
python player.py [filename]
```

Where `[filename]` is the path to the JSON file with recorded actions. If not provided, you'll be prompted to enter it.

1. After loading the file, press Enter to start playback
2. The program will wait a specific number of seconds and then start playing back the recorded actions
3. Move the mouse to the upper-left corner of the screen to abort playback (PyAutoGUI failsafe)

## How It Works

### Recorder

The recorder uses the pynput library to listen to mouse and keyboard events. Each event is recorded with:
- Type of action (mouse_move, mouse_click, mouse_scroll, key_press, key_release)
- Position (for mouse events)
- Button/key information
- Timestamp (relative to the start of recording)

All actions are saved to a JSON file for later playback.

### Player

The player reads the JSON file and uses pyautogui to replay the actions with the same timing as they were recorded. It handles:
- Mouse movements
- Mouse clicks (left, right, middle)
- Mouse scrolling
- Keyboard key presses and releases (including special keys)

## Limitations

- The player may not work perfectly for all applications, especially those that rely on absolute screen positions
- Some special keys or combinations might not be replayed correctly
- The playback might be affected by screen resolution differences between recording and playback

## Safety

- The player has a failsafe mechanism: move your mouse to the upper-left corner of the screen to abort playback
- Be careful when recording and playing back actions that could potentially be destructive (like deleting files)