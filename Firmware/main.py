# You import all the IOs of your board
import board
import digitalio
import rotaryio

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler

# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# Add the macro and encoder extensions
macros = Macros()
encoder_handler = EncoderHandler()
keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)

# Define your pins here
# 6 pins for 6 keys + encoder pins
PINS = [
    board.D3,   # First key
    board.D4,   # Second key
    board.D2,   # Third key
    board.D1,   # Fourth key
    board.D0,   # Fifth key
    board.D5,   # Sixth key
    board.D6,   # Encoder A
    board.D7,   # Encoder B
    board.D8,   # Encoder Button
    ]

# Setup Rotary Encoder
encoder = rotaryio.IncrementalEncoder(board.D6, board.D7)
encoder_button = digitalio.DigitalInOut(board.D8)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS[:6],  # First 6 pins for keys
    value_when_pressed=False,
)

# Encoder Handler Functions
def encoder_volume_control(encoder, delta):
    """Handle volume control with rotary encoder"""
    if delta > 0:
        # Volume up
        return [Tap(KC.VOLU)]
    elif delta < 0:
        # Volume down
        return [Tap(KC.VOLD)]


def switch_audio_output_macro():
    """Macro to open Sound settings in Windows"""
    return [
        Press(KC.LWIN),
        Tap(KC.R),
        Release(KC.LWIN),
        Tap(KC.S),
        Tap(KC.O),
        Tap(KC.U),
        Tap(KC.N),
        Tap(KC.D),
        Tap(KC.ENTER)
    ]

# Configure Encoder
encoder_handler.encoders = [
    (encoder, encoder_volume_control),
]

# Define macros for specific applications
def ctrl_c_macro():
    return [
        Press(KC.LCTL),
        Tap(KC.C),
        Release(KC.LCTL)
    ]

def ctrl_v_macro():
    return [
        Press(KC.LCTL),
        Tap(KC.V),
        Release(KC.LCTL)
    ]

def save_macro():
    return [
        Press(KC.LCTL),
        Tap(KC.S),
        Release(KC.LCTL)
    ]

def screenshot_macro():
    return [
        Press(KC.LSFT),
        Press(KC.LCTL),
        Tap(KC.S),
        Release(KC.LCTL),
        Release(KC.LSFT)
    ]

def open_steam_macro():
    return [
        Press(KC.LWIN),
        Tap(KC.R),
        Release(KC.LWIN),
        Tap(KC.S),
        Tap(KC.T),
        Tap(KC.E),
        Tap(KC.A),
        Tap(KC.M),
        Tap(KC.ENTER)
    ]

def open_orca_slicer_macro():
    return [
        Press(KC.LWIN),
        Tap(KC.R),
        Release(KC.LWIN),
        Tap(KC.O),
        Tap(KC.R),
        Tap(KC.C),
        Tap(KC.A),
        Tap(KC.ENTER)
    ]

# Here you define the buttons corresponding to the pins
keyboard.keymap = [
    [
        KC.MACRO(ctrl_c_macro),            # First key: Ctrl+C
        KC.MACRO(ctrl_v_macro),            # Second key: Ctrl+V
        KC.MACRO(save_macro),              # Third key: Save (Ctrl+S)
        KC.MACRO(screenshot_macro),        # Fourth key: Screenshot
        KC.MACRO(open_steam_macro),        # Fifth key: Open Steam
        KC.MACRO(open_orca_slicer_macro),  # Sixth key: Open Orca Slicer
        KC.MACRO(switch_audio_output_macro)# Momentary Switch: Open Sound Settings
    ]
]

# Main loop with encoder tracking
last_position = 0

# Start kmk!
if __name__ == '__main__':
    keyboard.go()