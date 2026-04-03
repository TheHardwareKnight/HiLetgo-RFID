import board
import busio
import os
import subprocess
from adafruit_pn532.i2c import PN532_I2C

GREEN = "\033[92m"
RESET = "\033[0m"

def gprint(text=""):
    print(GREEN + str(text) + RESET)

def clear():
    os.system("clear")

def pause():
    input(GREEN + "\nPress Enter to continue..." + RESET)
    main()

# -----------------------
# PN532 Setup
# -----------------------

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()

# -----------------------
# Card Helpers
# -----------------------

def wait_for_card():
    gprint("\nScan NFC card...")
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is not None:
            uid_hex = ''.join("{:02X}".format(i) for i in uid)
            return uid_hex, uid


def get_card_type(uid):
    if len(uid) == 7:
        return "NTAG213/215/216"
    elif len(uid) == 4:
        return "MIFARE / NTAG"
    else:
        return "Unknown"

# -----------------------
# NDEF Writing
# -----------------------

def write_ndef(payload):
    gprint("\nScan tag to write...")
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is None:
            continue

        ndef = bytearray([0x03, len(payload)]) + payload + bytearray([0xFE])
        page = 4

        for i in range(0, len(ndef), 4):
            block = ndef[i:i+4]
            while len(block) < 4:
                block += b"\x00"
            pn532.ntag2xx_write_block(page, block)
            page += 1

        gprint("\nWrite successful")
        break

    pause()

# -----------------------
# NDEF URL Builder
# -----------------------

def ndef_url(url):
    prefix = 0x00

    if url.startswith("http://www."):
        prefix = 0x01
        url = url[11:]
    elif url.startswith("https://www."):
        prefix = 0x02
        url = url[12:]
    elif url.startswith("http://"):
        prefix = 0x03
        url = url[7:]
    elif url.startswith("https://"):
        prefix = 0x04
        url = url[8:]

    payload = bytearray([
        0xD1,
        0x01,
        len(url) + 1,
        0x55,
        prefix
    ]) + url.encode()

    return payload

# -----------------------
# Scan Info
# -----------------------

def scan_info():
    clear()
    uid_hex, uid = wait_for_card()
    gprint("\nUID: " + uid_hex)
    gprint("Type: " + get_card_type(uid))
    pause()

# -----------------------
# Save Card
# -----------------------

def save_card():
    clear()
    uid_hex, uid = wait_for_card()
    gprint("\nUID: " + uid_hex)

    path = input(GREEN + "\nEnter filename: " + RESET)

    if "/" not in path:
        path = os.getcwd() + "/" + path
    if not path.endswith(".txt"):
        path += ".txt"

    with open(path, "w") as f:
        f.write("UID=" + uid_hex)

    gprint("\nSaved to " + path)
    pause()

# -----------------------
# Write Card (LINK ONLY)
# -----------------------

def write_card():
    clear()
    gprint("Write Link to NFC Tag")
    gprint("Enter the FULL link including https://")

    url = input(GREEN + "\nLink: " + RESET)

    if not url.startswith("http://") and not url.startswith("https://"):
        gprint("\nInvalid link. Must start with http:// or https://")
        pause()
        return

    payload = ndef_url(url)
    write_ndef(payload)

# -----------------------
# Card Action
# -----------------------

def create_card_action():
    clear()
    uid = input(GREEN + "Enter UID to trigger script: " + RESET).upper()
    script = input(GREEN + "Enter python file path: " + RESET)

    gprint("\nWaiting for card...")

    while True:
        read_uid, raw = wait_for_card()
        if read_uid == uid:
            gprint("\nCard matched")
            subprocess.run(["python3", script])
            break

    pause()

# -----------------------
# Main Menu
# -----------------------

def main():
    clear()
    gprint("1) Scan Info")
    gprint("2) Save Card")
    gprint("3) Write Card")
    gprint("4) Create Card Action")

    choice = input(GREEN + "\n> " + RESET)

    if choice == "1":
        scan_info()
    elif choice == "2":
        save_card()
    elif choice == "3":
        write_card()
    elif choice == "4":
        create_card_action()
    else:
        main()


main()
