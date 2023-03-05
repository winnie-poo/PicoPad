print("Starting")

import time
import board
import pwmio
import digitalio
import pulseio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

RED_PIN = board.GP15  # Red LED pin board.GP15
GREEN_PIN = board.GP14  # Green LED pin
BLUE_PIN = board.GP13  # Blue LED pin
FADE_SLEEP = 50  # Number of milliseconds to delay between changes.

# Define PWM outputs:
red = pwmio.PWMOut(RED_PIN)
green = pwmio.PWMOut(GREEN_PIN)
blue = pwmio.PWMOut(BLUE_PIN)

# KEYTBOARD SETUP
keyboard = KMKKeyboard()
encoder = EncoderHandler()
keyboard.modules = [encoder]

# SWITCH MATRIX
keyboard.col_pins = (board.GP19, board.GP20, board.GP21, board.GP22)
keyboard.row_pins = (board.GP16, board.GP17, board.GP9)
#keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.extensions.append(MediaKeys())
# ENCODERS
encoder.pins = (board.GP12, board.GP11, board.GP10,)

keyboard.keymap = [

[
        KC.BSPC, KC.NO, KC.MPLY, KC.A,
        KC.MEH, KC.NO, KC.MPRV, KC.MNXT,
        KC.NO, KC.NO, KC.NO, KC.NO
    ]
]

encoder.map = [    (KC.VOLD, KC.VOLU, KC.MUTE)
]
# Function to simplify setting duty cycle to percent value.
def duty_cycle(percent):
    return int(percent / 1000.0 * 65535.0)

while True:
    # Fade from blue up to violet.
    for i in range(1000,):
        red.duty_cycle = duty_cycle(i)
        time.sleep(FADE_SLEEP / 1000)
    # Now fade from violet (red + blue) down to red.
    for i in range(1000, -1, -1):
        blue.duty_cycle = duty_cycle(i)
        time.sleep(FADE_SLEEP / 1000)
    # Fade from red to yellow (red + green).
    for i in range(1000):
        green.duty_cycle = duty_cycle(i)
        time.sleep(FADE_SLEEP / 1000)
    # Fade from yellow to green.
    for i in range(1000, -1, -1):
        red.duty_cycle = duty_cycle(i)
        time.sleep(FADE_SLEEP / 1000)
    # Fade from green to teal (blue + green).
    for i in range(1000):
        blue.duty_cycle = duty_cycle(i)
        time.sleep(FADE_SLEEP / 1000)
    # Fade from teal to blue.
    for i in range(1000, -1, -1):
        green.duty_cycle = duty_cycle(i)
        time.sleep(FADE_SLEEP / 1000)


