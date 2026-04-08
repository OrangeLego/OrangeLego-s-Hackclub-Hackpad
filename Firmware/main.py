import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC, ConsumerKey
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()
macros = Macros()
encoder_handler = EncoderHandler()
keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)

VOLU = ConsumerKey(0xEA)
VOLD = ConsumerKey(0xE9)

PINS = [
    board.D7,   # SW1 - top left     (Ctrl+C)
    board.D8,   # SW2 - bottom left  (Ctrl+V)
    board.D9,   # SW3 - top middle   (Ctrl+S)
    board.D10,  # SW4 - bottom mid   (Screenshot)
    board.D5,   # SW5 - top right    (Steam)
    board.D6,   # SW6 - bottom right (Orca Slicer)
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

encoder_handler.pins = ((board.D3, board.D2, board.D4, False),)

def open_volume_mixer_macro(keyboard):
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

encoder_handler.map = [
    ((VOLD, VOLU, KC.MACRO(open_volume_mixer_macro)),)
]

def ctrl_c_macro(keyboard):
    yield Press(KC.LCTL)
    yield Tap(KC.C)
    yield Release(KC.LCTL)

def ctrl_v_macro(keyboard):
    yield Press(KC.LCTL)
    yield Tap(KC.V)
    yield Release(KC.LCTL)

def task_manager_macro(keyboard):
    yield Press(KC.LCTL)
    yield Press(KC.LSFT)
    yield Tap(KC.ESCAPE)
    yield Release(KC.LSFT)
    yield Release(KC.LCTL)

def screenshot_macro(keyboard):
    yield Press(KC.LSFT)
    yield Press(KC.LWIN)
    yield Tap(KC.S)
    yield Release(KC.LSFT)
    yield Release(KC.LWIN)

def open_steam_macro(keyboard):
    yield Press(KC.LWIN)
    yield Tap(KC.R)
    yield Release(KC.LWIN)
    yield Tap(KC.S)
    yield Tap(KC.T)
    yield Tap(KC.E)
    yield Tap(KC.A)
    yield Tap(KC.M)
    yield Tap(KC.ENTER)

def open_orca_slicer_macro(keyboard):
    yield Press(KC.LWIN)
    yield Tap(KC.R)
    yield Release(KC.LWIN)
    yield Tap(KC.O)
    yield Tap(KC.R)
    yield Tap(KC.C)
    yield Tap(KC.A)
    yield Tap(KC.ENTER)

keyboard.keymap = [
    [
        KC.MACRO(ctrl_c_macro),             # SW1 - bottom right
        KC.MACRO(ctrl_v_macro),             # SW2 - top right
        KC.MACRO(task_manager_macro),       # SW3 - bottom middle
        KC.MACRO(screenshot_macro),         # SW4 - top middle
        KC.MACRO(open_steam_macro),         # SW5 - bottom left
        KC.MACRO(open_orca_slicer_macro),   # SW6 - top left
    ]
]

if __name__ == '__main__':
    keyboard.go()
