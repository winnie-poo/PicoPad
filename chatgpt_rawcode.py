import board
import digitalio
import neopixel
from adafruit_matrixkeypad import Matrix_Keypad
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Tastenmatrix definieren
cols = [digitalio.DigitalInOut(board.GP0), digitalio.DigitalInOut(board.GP1), digitalio.DigitalInOut(board.GP2), digitalio.DigitalInOut(board.GP3)]
rows = [digitalio.DigitalInOut(board.GP4), digitalio.DigitalInOut(board.GP5), digitalio.DigitalInOut(board.GP6)]
keys = ((1, 2, 3, "A"), (4, 5, 6, "B"), (7, 8, 9, "C"), ("*", 0, "#", "D"))
keypad = Matrix_Keypad(rows, cols, keys)

# RGB LED definieren
led_red = digitalio.DigitalInOut(board.GP15)
led_red.direction = digitalio.Direction.OUTPUT
led_green = digitalio.DigitalInOut(board.GP13)
led_green.direction = digitalio.Direction.OUTPUT
led_blue = digitalio.DigitalInOut(board.GP14)
led_blue.direction = digitalio.Direction.OUTPUT
pixels = neopixel.NeoPixel(board.GP28, 1)

# Keyboard definieren
kbd = Keyboard(usb_hid.devices)

# Keyboard Layout definieren
layout = KeyboardLayoutUS(kbd)

# Funktion zur Ausführung der Tastenkombination strg+c
def copy():
    kbd.press(Keycode.CONTROL, Keycode.C)
    kbd.release_all()

# Funktion zur Ausführung der Tastenkombination strg+v
def paste():
    kbd.press(Keycode.CONTROL, Keycode.V)
    kbd.release_all()

# Funktion zur Ausführung der Tastenkombination für Taschenrechner öffnen
def calc():
    kbd.press(Keycode.WINDOWS, Keycode.R)
    kbd.release_all()
    time.sleep(0.5)
    layout.write("calc\n")

# Unendliche Schleife für das Abfragen der Tasten und Ausführen der Funktionen
while True:
    # Fließender Farbwechsel der RGB LED
    for i in range(255):
        pixels.fill((i, 255-i, 0))
        time.sleep(0.01)

    # Tastenabfrage
    keys = keypad.pressed_keys
    if keys:
        # RGB LED zu weiß umschalten
        led_red.value = True
        led_green.value = True
        led_blue.value = True
        pixels.fill((255, 255, 255))
        
        # Ausführen der entsprechenden Funktionen
        if "A" in keys:
            copy()
        if "B" in keys:
            paste()
        if "C" in keys:
            calc()

        # Warten, bis alle Tasten losgelassen werden
        while keypad.pressed_keys:
            pass
        
        # RGB LED wieder auf den Farbverlauf umschalten
        led_red.value = False
        led_green.value = False
        led_blue.value = False
