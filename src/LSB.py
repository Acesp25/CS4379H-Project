import hashlib
import random
import os
import numpy as np
from PIL import Image

import PLShandler as plsh


def DataListInBit(data):
    # data is raw bytes -> flat list of bits (MSB first), 8 bits per byte
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8)).tolist()


def PLSgen(row, col, numPixels):
    if numPixels > row * col:
        raise ValueError("The input image does not have enough pixels for this message.")
    pixelLocaterSequence = list(range(row * col))
    random.shuffle(pixelLocaterSequence)
    pixelLocaterSequence = pixelLocaterSequence[:numPixels]
    np.savetxt("pls.txt", pixelLocaterSequence, delimiter="\t")
    return pixelLocaterSequence


def LsbEncoding(encodedBytes, input_image_path, output_image_path):
    img = Image.open(input_image_path)
    width, height = img.size
    dataBits = DataListInBit(encodedBytes)
    # Dense packing: every channel of every PLS pixel carries one bit,
    # so n bytes need ceil(8n / 3) pixels (was 3 pixels per hex character).
    numPixels = -(-len(dataBits) // 3)
    pls = PLSgen(width, height, numPixels)
    for p in range(numPixels):
        x = pls[p] % width
        y = pls[p] // width
        rgb = list(img.getpixel((x, y)))
        for c in range(3):
            n = 3 * p + c
            if n >= len(dataBits):
                break  # last pixel may be only partly used
            rgb[c] = (rgb[c] & 0xFE) | dataBits[n]
        img.putpixel((x, y), tuple(rgb))
    img.save(output_image_path)
    plsPassword = input("Insert Password for pls encyption :")
    key = hashlib.sha256(plsPassword.encode()).digest()
    plsh.encrypt_file(key, 'pls.txt')


def LsbDecoding(output_image_path):
    plspassword = input("Insert Password for pls decryption :")
    key = hashlib.sha256(plspassword.encode()).digest()
    plsh.decrypt_file(key, 'pls.txt.enc', 'out.txt')
    stegoImage = Image.open(output_image_path)
    width, height = stegoImage.size
    try:
        pls = np.atleast_1d(np.genfromtxt('out.txt', delimiter='\t'))
        if np.isnan(pls).any() or pls.min() < 0 or pls.max() >= width * height:
            raise ValueError
        pls = pls.astype(np.int64)
    except (UnicodeDecodeError, ValueError):
        # garbage data will output if the password is wrong
        os.remove("out.txt")
        raise SystemExit("Could not read the PLS: wrong PLS password, or "
                         "pls.txt.enc does not belong to this image.")
    if os.path.exists("out.txt"):
        os.remove("out.txt")
    if os.path.exists("pls.txt.enc"):
        os.remove("pls.txt.enc")
    bits = []
    for p in pls:
        x = int(p % width)
        y = int(p // width)
        rgb = stegoImage.getpixel((x, y))
        for k in rgb[:3]:
            bits.append(k & 1)
    # 3 * ceil(8n/3) is in [8n, 8n+2], so floor(bits / 8) recovers n exactly.
    numBytes = len(bits) // 8
    return np.packbits(np.array(bits[:numBytes * 8], dtype=np.uint8)).tobytes()