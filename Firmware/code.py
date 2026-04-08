import board
import neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC, ConsumerKey
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap

# ==============================================================================
# OrangeLego's HackPad v1 Firmware
# Profiles: Default (red), Gaming (green), Helldivers 2 (blue)
# SW1 (bottom right) = cycle profiles
# Encoder button = open Volume Mixer
# Rotate encoder left/right to change volume
# ==============================================================================


# ==============================================================================
# Keyboard setup
# ==============================================================================
keyboard = KMKKeyboard()
macros          = Macros()
layers          = Layers()
holdtap         = HoldTap()
encoder_handler = EncoderHandler()
keyboard.modules.append(macros)
keyboard.modules.append(layers)
keyboard.modules.append(holdtap)
keyboard.modules.append(encoder_handler)

# HoldTap threshold: tap under 400ms = tap action, hold 400ms+ = hold action
holdtap.tap_time = 400


# ==============================================================================
# Built-in XIAO RP2040 NeoPixel RGB LED on pin NEOPIXEL
# Shows the current profile as a colour:
#   Red   = Profile 0: Default
#   Green = Profile 1: Gaming
#   Blue  = Profile 2: Helldivers 2
# ==============================================================================
led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

PROFILE_COLOURS = [
    (0,   0,   255), # Profile 0: Default    = Blue
    (0,   255, 0),   # Profile 1: Gaming     = Green
    (255, 0,   0),   # Profile 2: Helldivers = Red
]

def set_led(layer):
    led[0] = PROFILE_COLOURS[layer]

# Set LED to red on startup (Profile 0)
set_led(0)


# ==============================================================================
# Consumer keys (media keys not built into this version of KMK)
# 0xE9 = Volume Up, 0xEA = Volume Down, 0xCD = Play/Pause
# ==============================================================================
VOLU = ConsumerKey(0xE9)
VOLD = ConsumerKey(0xEA)
MPLY = ConsumerKey(0xCD)


# ==============================================================================
# Key switch pin mapping
# Physical layout (viewed from front):
#   SW6  SW4  SW2
#   SW5  SW3  SW1
#              SW8 (encoder)
# ==============================================================================
PINS = [
    board.D7,    # SW1 - bottom right
    board.D8,    # SW2 - top right
    board.D9,    # SW3 - bottom middle
    board.D10,   # SW4 - top middle
    board.D5,    # SW5 - bottom left
    board.D6,    # SW6 - top left
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)


# ==============================================================================
# Encoder pin mapping
# A and B are the rotation pins, D4 is the push button
# ==============================================================================
encoder_handler.pins = ((board.D3, board.D2, board.D4, False),)


# ==============================================================================
# LED watcher - updates the NeoPixel colour whenever the active layer changes
# KMK extensions can hook into before_matrix_scan to run code every cycle
# ==============================================================================
LAYER_COUNT  = 3
_last_layer  = [0]

class LedWatcher:
    def during_bootup(self, keyboard):      return keyboard
    def before_matrix_scan(self, keyboard):
        current = keyboard.active_layers[0]
        if current != _last_layer[0]:
            _last_layer[0] = current
            set_led(current % LAYER_COUNT)
            print(f"Layer changed: active_layers={keyboard.active_layers}, using index {current % LAYER_COUNT}")
        return keyboard

    def after_matrix_scan(self, keyboard):      return keyboard
    def before_hid_send(self, keyboard):        return keyboard
    def after_hid_send(self, keyboard):         return keyboard
    def on_powersave_enable(self, keyboard):    return keyboard
    def on_powersave_disable(self, keyboard):   return keyboard

keyboard.extensions.append(LedWatcher())


# ==============================================================================
# Volume Mixer macro (encoder button on every layer)
# Opens Windows Volume Mixer via Win+R > sndvol
# ==============================================================================
def volume_mixer_macro(keyboard):
    yield Press(KC.LWIN)
    yield Tap(KC.R)
    yield Release(KC.LWIN)
    yield Tap(KC.S)
    yield Tap(KC.N)
    yield Tap(KC.D)
    yield Tap(KC.V)
    yield Tap(KC.O)
    yield Tap(KC.L)
    yield Tap(KC.ENTER)


# ==============================================================================
# Helper to type a full file path into the Win+R dialog
# Handles special characters like colons, backslashes, spaces, parentheses
# ==============================================================================
def type_string(s):
    result = []
    for ch in s:
        if ch == ':':
            result.append(Tap(KC.COLN))
        elif ch == '\\':
            result.append(Tap(KC.BSLS))
        elif ch == ' ':
            result.append(Tap(KC.SPACE))
        elif ch == '(':
            result.append(Tap(KC.LPRN))
        elif ch == ')':
            result.append(Tap(KC.RPRN))
        elif ch == '-':
            result.append(Tap(KC.MINS))
        elif ch == '.':
            result.append(Tap(KC.DOT))
        elif ch.isupper():
            result.append(Press(KC.LSFT))
            result.append(Tap(getattr(KC, ch)))
            result.append(Release(KC.LSFT))
        else:
            result.append(Tap(getattr(KC, ch.upper())))
    return result


# ==============================================================================
# Default profile macros
# General shortcuts for everyday use
# ==============================================================================

def ctrl_c_macro(keyboard):
    # Copy selected text or file
    yield Press(KC.LCTL)
    yield Tap(KC.C)
    yield Release(KC.LCTL)

def ctrl_v_macro(keyboard):
    # Paste clipboard contents
    yield Press(KC.LCTL)
    yield Tap(KC.V)
    yield Release(KC.LCTL)

def task_manager_macro(keyboard):
    # Open Task Manager directly (Ctrl+Shift+Esc)
    yield Press(KC.LCTL)
    yield Press(KC.LSFT)
    yield Tap(KC.ESCAPE)
    yield Release(KC.LSFT)
    yield Release(KC.LCTL)

def screenshot_macro(keyboard):
    # Open Windows Snipping Tool (Win+Shift+S)
    yield Press(KC.LWIN)
    yield Press(KC.LSFT)
    yield Tap(KC.S)
    yield Release(KC.LSFT)
    yield Release(KC.LWIN)

def open_steam_macro(keyboard):
    # Launch Steam via Win+R with full exe path
    yield Press(KC.LWIN)
    yield Tap(KC.R)
    yield Release(KC.LWIN)
    yield Tap(KC.NO)
    for action in type_string('C:\\Program Files (x86)\\Steam\\steam.exe'):
        yield action
    yield Tap(KC.ENTER)

def open_orca_slicer_macro(keyboard):
    # Launch Orca Slicer via Win+R with full exe path
    yield Press(KC.LWIN)
    yield Tap(KC.R)
    yield Release(KC.LWIN)
    yield Tap(KC.NO)
    for action in type_string('C:\\Program Files\\OrcaSlicer\\orca-slicer.exe'):
        yield action
    yield Tap(KC.ENTER)


# ==============================================================================
# Helldivers 2 stratagem macros
# Each macro holds Left Alt to open the stratagem menu, enters the directional
# sequence, then releases Alt. Make sure your in-game stratagem key is Left Alt.
#
# Physical layout:
#   SW6 Resupply         SW4 Machine Gun Sentry    SW2 Orbital Laser
#   SW5 Spear Launcher   SW3 Eagle Airstrike        SW1 CYCLE PROFILE
# ==============================================================================

def stratagem(sequence):
    # Helper that wraps a directional sequence with Alt hold/release
    def macro(keyboard):
        for key in sequence:
            yield Tap(key)
    return macro

# Resupply: Down Down Up Right
resupply_macro = stratagem([KC.DOWN, KC.DOWN, KC.UP, KC.RIGHT])

# Machine Gun Sentry: Down Up Right Right Up
mg_sentry_macro = stratagem([KC.DOWN, KC.UP, KC.RIGHT, KC.RIGHT, KC.UP])

# Orbital Laser: Right Down Up Right Down
orbital_laser_macro = stratagem([KC.RIGHT, KC.DOWN, KC.UP, KC.RIGHT, KC.DOWN])

# Spear Launcher: Down Down Up Down Down
spear_macro = stratagem([KC.DOWN, KC.DOWN, KC.UP, KC.DOWN, KC.DOWN])

# Eagle Airstrike: Up Right Down Right
eagle_airstrike_macro = stratagem([KC.UP, KC.RIGHT, KC.DOWN, KC.RIGHT])

# Eagle 500kg Bomb: Up Right Down Down Down
eagle_500kg_macro = stratagem([KC.UP, KC.RIGHT, KC.DOWN, KC.DOWN, KC.DOWN])


# ==============================================================================
# Encoder map (same across all profiles)
# Left    = Volume Down
# Right   = Volume Up
# Button  = Open Volume Mixer
# ==============================================================================
encoder_handler.map = [
    ((VOLU, VOLD, KC.MACRO(volume_mixer_macro)),),  # Default profile
    ((VOLU, VOLD, KC.MACRO(volume_mixer_macro)),),  # Gaming profile
    ((VOLU, VOLD, KC.MACRO(volume_mixer_macro)),),  # Helldivers 2 profile
]


# ==============================================================================
# Keymaps for each profile
# Key order matches PINS list: SW1, SW2, SW3, SW4, SW5, SW6
# SW1 is always cycle profile on every layer
#
# Physical layout reminder:
#   SW6  SW4  SW2
#   SW5  SW3  SW1  <-- SW1 always cycles profile
# ==============================================================================
keyboard.keymap = [

    # Profile 0: Default (LED = Red)
    # General shortcuts for everyday use
    [
        KC.HT(KC.MACRO(ctrl_c_macro), KC.TO(1)),  # SW1 bottom right  : Tap=Copy, Hold=Cycle to Gaming
        KC.MACRO(ctrl_v_macro),            # SW2 top right     : Paste (Ctrl+V)
        KC.MACRO(task_manager_macro),      # SW3 bottom middle : Task Manager (Ctrl+Shift+Esc)
        KC.MACRO(screenshot_macro),        # SW4 top middle    : Screenshot (Win+Shift+S)
        KC.MACRO(open_steam_macro),        # SW5 bottom left   : Open Steam
        KC.MACRO(open_orca_slicer_macro),  # SW6 top left      : Open Orca Slicer
    ],

    # Profile 1: Gaming (LED = Green)
    # F13-F17 are free keys you can bind to anything in-game
    [
        KC.HT(MPLY, KC.TO(2)),  # SW1 bottom right  : Tap=Play/Pause, Hold=Cycle to Helldivers
        KC.F13,                       # SW2 top right     : Custom in-game bind
        KC.F14,                       # SW3 bottom middle : Custom in-game bind
        KC.F15,                       # SW4 top middle    : Custom in-game bind
        KC.F16,                       # SW5 bottom left   : Custom in-game bind
        KC.F17,                       # SW6 top left      : Push to Talk (bind F17 in Discord)
    ],

    # Profile 2: Helldivers 2 (LED = Blue)
    # Holds Left Alt, enters stratagem sequence, releases Alt
    # Make sure Left Alt is your stratagem menu key in-game
    [
        KC.HT(KC.MACRO(eagle_500kg_macro), KC.TO(0)),  # SW1 bottom right  : Tap=Eagle 500kg, Hold=Cycle to Default
        KC.MACRO(orbital_laser_macro),     # SW2 top right     : Orbital Laser       (R D U R D)
        KC.MACRO(eagle_airstrike_macro),   # SW3 bottom middle : Eagle Airstrike     (U R D R)
        KC.MACRO(mg_sentry_macro),         # SW4 top middle    : Machine Gun Sentry  (D U R R U)
        KC.MACRO(spear_macro),             # SW5 bottom left   : Spear Launcher      (D D U D D)
        KC.MACRO(resupply_macro),          # SW6 top left      : Resupply            (D D U R)
    ],
]


if __name__ == '__main__':
    keyboard.go()