#!/usr/bin/env python3

import numpy as np

# =====================================================
# PARAMETRY ZX81
# =====================================================

SCREEN_COLS = 32
SCREEN_ROWS = 24
CHAR_WIDTH = 8
CHAR_HEIGHT = 8

SCREEN_WIDTH = SCREEN_COLS * CHAR_WIDTH
SCREEN_HEIGHT = SCREEN_ROWS * CHAR_HEIGHT

RAM_SIZE = 1024  # 1KB jak oryginał
VIDEO_RAM_START = 0


# =====================================================
# GENERATOR ZNAKÓW 8×8
# =====================================================

def generate_font():
    """
    Bardzo uproszczony font bitmapowy 8x8
    Generujemy znaki A-Z i 0-9
    """
    font = {}

    for i in range(26):
        letter = chr(ord('A') + i)
        bitmap = np.zeros((8, 8), dtype=np.uint8)
        bitmap[1:7, 1:7] = 1
        font[letter] = bitmap

    for i in range(10):
        digit = chr(ord('0') + i)
        bitmap = np.zeros((8, 8), dtype=np.uint8)
        bitmap[:, :] = 1
        font[digit] = bitmap

    font[" "] = np.zeros((8, 8), dtype=np.uint8)

    return font


FONT = generate_font()


# =====================================================
# ZX81 PRO
# =====================================================

class ZX81Pro:

    def __init__(self):
        self.ram = [0] * RAM_SIZE
        self.framebuffer = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.uint8)

    # =====================================================
    # VIDEO RENDER
    # =====================================================

    def render(self):
        self.framebuffer.fill(0)

        for row in range(SCREEN_ROWS):
            for col in range(SCREEN_COLS):

                addr = VIDEO_RAM_START + row * SCREEN_COLS + col
                if addr >= RAM_SIZE:
                    continue

                char_code = self.ram[addr]
                char = self.decode_char(char_code)

                bitmap = FONT.get(char, FONT[" "])

                y = row * CHAR_HEIGHT
                x = col * CHAR_WIDTH

                self.framebuffer[y:y+8, x:x+8] = bitmap

    def decode_char(self, code):
        if 1 <= code <= 26:
            return chr(ord('A') + code - 1)
        if 27 <= code <= 36:
            return chr(ord('0') + code - 27)
        return " "

    def print_ascii(self):
        for y in range(0, SCREEN_HEIGHT, 8):
            line = ""
            for x in range(0, SCREEN_WIDTH, 8):
                block = self.framebuffer[y:y+8, x:x+8]
                if block.sum() > 0:
                    line += "█"
                else:
                    line += " "
            print(line)

    # =====================================================
    # BASIC INTERPRETER (UPROSZCZONY)
    # =====================================================

    def basic(self, code: str):
        """
        Obsługa:
        CLS
        PRINT "TEXT"
        """

        lines = code.strip().split("\n")

        cursor = 0

        for line in lines:

            line = line.strip().upper()

            if line == "CLS":
                self.ram = [0] * RAM_SIZE
                cursor = 0

            elif line.startswith("PRINT"):
                text = line.split('"')[1]

                for ch in text:
                    self.ram[cursor] = self.encode_char(ch)
                    cursor += 1

    def encode_char(self, ch):
        if ch == " ":
            return 0
        if ch.isalpha():
            return ord(ch.upper()) - ord('A') + 1
        if ch.isdigit():
            return ord(ch) - ord('0') + 27
        return 0


# =====================================================
# DEMO
# =====================================================

if __name__ == "__main__":

    zx = ZX81Pro()

    zx.basic("""
    CLS
    PRINT "HELLO ZX81"
    PRINT "2026"
    """)

    zx.render()

    print("=== ZX81 PRO SCREEN ===")
    zx.print_ascii()