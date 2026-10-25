import hashlib
import random
import os
from PIL import Image

import PLShandler as plsh

img = Image.open(r"images/in1.png")
[row, col] = img.size


def PLSgen(row, col, lenEncodedText):
    locators = random.sample(range(row * col), lenEncodedText * 3)
    with open("pls.txt", "w") as locatorFile:
        locatorFile.writelines(f"{locator}\n" for locator in locators)
    return locators


def LsbEncoding(encodedText):
    encodedBytes = encodedText.encode("latin-1")
    locators = PLSgen(row, col, len(encodedBytes))
    for byteIndex, value in enumerate(encodedBytes):
        bits = format(value, "08b")
        for pixelOffset in range(3):
            locator = locators[byteIndex * 3 + pixelOffset]
            rr = locator // col
            rc = locator % col
            rgb = img.getpixel((rr, rc))
            newRgb = list(rgb)
            firstBit = pixelOffset * 3
            for channel, bitIndex in enumerate(range(firstBit, min(firstBit + 3, 8))):
                component = rgb[channel]
                if component % 2 != int(bits[bitIndex]):
                    newRgb[channel] = component + 1 if component == 0 else component - 1
            img.putpixel((rr, rc), tuple(newRgb))
    img.save("images/out1.png")
    plsPassword = input("Insert Password for pls encyption :")
    key = hashlib.sha256(plsPassword.encode()).digest()
    plsh.encrypt_file(key, 'pls.txt')


def LsbDecoding():
    plspassword = input("Insert Password for pls decryption :")
    key = hashlib.sha256(plspassword.encode()).digest()
    plsh.decrypt_file(key, 'pls.txt.enc', 'out.txt')
    stegoImage = Image.open(r"images/out1.png")
    decodedBytes = bytearray()
    with open("out.txt", "r") as locatorFile:
        while True:
            firstLocator = locatorFile.readline()
            if not firstLocator:
                break
            locators = [int(firstLocator)]
            locators.extend(int(locatorFile.readline()) for _ in range(2))
            bits = []
            for locator in locators:
                rr = locator // col
                rc = locator % col
                rgb = stegoImage.getpixel((rr, rc))
                for component in rgb:
                    if len(bits) == 8:
                        break
                    bits.append(str(component & 1))
            decodedBytes.append(int("".join(bits), 2))
    if os.path.exists("out.txt"):
        os.remove("out.txt")
    if os.path.exists("pls.txt.enc"):
        os.remove("pls.txt.enc")
    return decodedBytes.decode("latin-1")
