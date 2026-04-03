# Pi NFC Toolkit

![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Interface](https://img.shields.io/badge/interface-I2C-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A clean, colour-coded terminal toolkit for the **PN532 NFC module** on Raspberry Pi. Scan tags, read UIDs, write URL payloads directly to NTAG cards, save card data to file, and trigger custom Python scripts per card — all from a simple interactive menu.

---

## Features

| Feature | Description |
|---|---|
| **Scan Info** | Read a card's UID and automatically detect its type |
| **Save Card** | Scan a card and save its UID to a `.txt` file |
| **Write Card** | Write a URL as an NDEF payload directly onto a tag |
| **Card Action** | Bind a card UID to a Python script — scan to trigger |
| **Card Mapper** | Map multiple UIDs to individual functions in `cards.py` |

---

## Hardware Required

- Raspberry Pi (any model with I2C support)
- PN532 NFC/RFID Module
- 4× jumper wires (Female-to-Female)
- NTAG213, NTAG215, NTAG216, or MIFARE Classic cards/fobs

---

## Hardware Setup

### 1. Prepare the Module

1. Solder the header pins onto the PN532 board
2. Set **Switch 1** to the **ON** position (up)
3. Set **Switch 2** to the **OFF** position (down)

> This configures the module to communicate over **I2C**. The 8-pin connector is not needed.

### 2. Wire to the Raspberry Pi

| PN532 Pin | Raspberry Pi Pin |
|---|---|
| VCC | 5V — Pin 2 |
| GND | GND — Pin 6 |
| SDA | GPIO2 / SDA — Pin 3 |
| SCL | GPIO3 / SCL — Pin 5 |

---

## Software Setup

### 3. Enable I2C on the Pi

Open a terminal and run:

```bash
sudo raspi-config
```

Navigate using the arrow keys:

```
Interface Options → I2C → Enable
```

Then select **Finish** and restart your Pi:

```bash
sudo shutdown -r now
```

---

### 4. Update Your System

```bash
sudo apt update
```

---

### 5. Install System Packages

```bash
sudo apt install python3-pip python3-venv i2c-tools python3-libgpiod python3-smbus -y
```

---

### 6. Create the Project Folder

```bash
mkdir ~/nfc_project
cd ~/nfc_project
```

---

### 7. Set Up a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> You will see `(venv)` at the start of your terminal prompt when the environment is active.

---

### 8. Install Python Dependencies

```bash
pip install adafruit-blinka adafruit-circuitpython-pn532
```

---

### 9. Download the Scripts

Clone this repository or manually copy `nfc.py` and `cards.py` into your project folder.

---

## Usage

Make sure the PN532 is connected and your virtual environment is active, then run:

```bash
python3 nfc.py
```

You will be presented with the main menu:

```
1) Scan Info
2) Save Card
3) Write Card
4) Create Card Action
```

> Press `Ctrl+C` at any time to exit the script.

---

## Card Mapper — `cards.py`

`cards.py` lets you map specific NFC cards to individual Python functions — so different cards trigger different actions automatically.

### Step 1 — Get Your Card UIDs

Run `nfc.py` and use **option 1 (Scan Info)** to scan each of your cards and note down their UIDs.

### Step 2 — Edit `cards.py`

Open `cards.py` and replace `UID1` / `UID2` with your actual card UIDs:

```python
uids_functions = {
    'A1B2C3D4': card1,
    'E5F6A7B8': card2,
}
```

### Step 3 — Write Your Functions

Fill in `card1()` and `card2()` with whatever Python code you want each card to trigger. You can add as many cards as you like by following the same pattern.

### Step 4 — Run It

```bash
python3 cards.py
```

Scan a card — if its UID is recognised, its function runs automatically.

---

## Reactivating the Environment

If you restart your Pi and need to run the scripts again, navigate to your project folder and reactivate the virtual environment first:

```bash
cd ~/nfc_project
source venv/bin/activate
```

Then run whichever script you need.

---

## Supported Card Types

| Card | UID Length | Notes |
|---|---|---|
| NTAG213 / 215 / 216 | 7 bytes | Best for NDEF URL writing |
| MIFARE Classic / NTAG | 4 bytes | Supported for scanning and actions |

---

## Notes

- Use `Ctrl+Shift+V` in the terminal to paste (instead of `Ctrl+V`)
- Use `Ctrl+C` to exit any running script
- The 8-pin connector on the PN532 is **not required** when using I2C

---

## License

MIT — free to use, modify, and share.
