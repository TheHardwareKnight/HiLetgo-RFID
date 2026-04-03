import board
import busio
from adafruit_pn532.i2c import PN532_I2C

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize PN532
pn532 = PN532_I2C(i2c, debug=False)

# Configure PN532
pn532.SAM_configuration()

print("Waiting for NFC card...")

# -----------------------
# Card Functions
# -----------------------
# Use nfc.py to scan your cards and get their UIDs first,
# then paste each UID into the uids_functions dictionary below.

def card1():
    # Paste your code for card 1 here
    pass

def card2():
    # Paste your code for card 2 here
    pass

# -----------------------
# UID → Function Map
# -----------------------
# Replace 'UID1' and 'UID2' with your actual card UIDs
# e.g. 'A1B2C3D4': card1

uids_functions = {
    'UID1': card1,
    'UID2': card2,
    # Add more UID-function pairs as needed
}

# -----------------------
# Main Loop
# -----------------------

while True:
    uid = pn532.read_passive_target(timeout=0.5)

    if uid is not None:
        uid_hex = ''.join(['{:02X}'.format(i) for i in uid])
        print("Card detected! UID:", uid_hex)

        if uid_hex in uids_functions:
            func = uids_functions[uid_hex]
            print(f"Executing function for UID {uid_hex}...")
            func()
        else:
            print("UID not recognised.")
