import hashlib
import random
import os
import numpy as np
from PIL import Image
import PLShandler as plsh

# File name and path constants.
PLS_TXT_PATH = "../../data/pls.txt"
PLS_TXT_ENC_PATH = "../../data/pls.txt.enc"
OUTPUT_TXT_PATH = "../../data/out.txt"
INPUT_IMG_DIR = "../../data/images/input/"
OUTPUT_IMG_DIR = "../../data/images/output/"
INPUT_IMAGES = ["in1.png", "in2.png", "in3.png", "in4.png", "in5.png"]
OUTPUT_IMAGES = ["out1.png", "out2.png", "out3.png", "out4.png", "out5.png"]

# Other constants used in this script.
pls = []

# TODO: Document this func.
def data_list_in_bit(data):
    data_bits = list(format(c, '08b') for c in bytearray(data.encode('latin-1')))
    return data_bits

# TODO: Document this func.
def pls_gen(encoded_txt_len, input_img_path: str):
    img = Image.open(rf"{input_img_path}")
    [row, col] = img.size
    new_arr = []

    for i in range(row * col):
        new_arr.append(i)

    for i in range(len(new_arr) - 1, 0, -1):
        j = random.randint(0, i + 1)
        new_arr[i], new_arr[j] = new_arr[j], new_arr[i]

    for i in range(encoded_txt_len * 3):
        pls.append(new_arr[i])

    pixel_locator_sequence = np.array(pls)
    np.savetxt(PLS_TXT_PATH, pixel_locator_sequence, delimiter = "\t")

# TODO: Document this func.
def lsb_encoding(encoded_txt, input_img_path: str, output_img_path: str):
    # Creates PLS text file.
    pls_gen(len(encoded_txt), input_img_path)

    # Variables.
    img = Image.open(rf"{input_img_path}")
    [row, col] = img.size
    data_bits = data_list_in_bit(encoded_txt)
    dr = 0

    for i in range(0, len(encoded_txt) * 3, 3):
        dc = 0

        for j in range(0, 3):
            rr = pls[i + j] // col
            rc = pls[i + j] % col
            rgb = img.getpixel((rr, rc))
            value = []
            idx = 0

            for k in rgb:
                if (k % 2 == 0 and data_bits[dr][dc] == "1"):
                    if (k == 0):
                        k += 1
                    else:
                        k -= 1

                if (k % 2 == 1 and data_bits[dr][dc] == "0"):
                    k -= 1

                value.append(k)
                idx += 1
                dc += 1

                if (dc >= 8):
                    break

            if (dc >= 8):
                value.append(rgb[2])

            new_rgb = (value[0], value[1], value[2])

            img.putpixel((rr, rc), new_rgb)

        dr += 1

    # Saves output image file.
    img.save(output_img_path)

    # Gets user input for PLS password and encrypts the PLS file.
    pls_password = input("Insert password for PLS encryption: ")
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.encrypt_file(key, PLS_TXT_PATH)

# TODO: Document this func.
def lsb_decoding(input_img_path: str, output_img_path: str):
    # Gets user-created PLS password and decrypts PLS file.
    pls_password = input("Insert password for PLS decryption: ")
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.decrypt_file(key, PLS_TXT_ENC_PATH, OUTPUT_TXT_PATH)
    pls = np.genfromtxt(OUTPUT_TXT_PATH, delimiter = "\t")

    # Removes files since they are no longer needed.
    if os.path.exists(OUTPUT_TXT_PATH):
        os.remove(OUTPUT_TXT_PATH)

    if os.path.exists(PLS_TXT_ENC_PATH):
        os.remove(PLS_TXT_ENC_PATH)

    # Gets the secret message.
    [row, col] = Image.open(rf"{input_img_path}").size
    stego_image = Image.open(rf"{output_img_path}")
    decoded_text_in_bits = []

    for i in range(0, len(pls), 3):
        ithChar = ""

        for j in range(0, 3):
            rr = pls[i + j] // col
            rc = pls[i + j] % col
            rgb = stego_image.getpixel((rr, rc))

            for k in rgb:
                if (k & 1):
                    ithChar += "1"
                else:
                    ithChar += "0"

        ithChar = ithChar[:-1]
        decoded_text_in_bits.append((ithChar))

    decoded_text = ""

    # Translates decoded text from bits to str.
    for i in decoded_text_in_bits:
        decoded_text += chr(int(i, 2))

    return decoded_text
