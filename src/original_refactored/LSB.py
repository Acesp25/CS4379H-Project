import hashlib
import random
import os
import numpy as np
from PIL import Image
from original_refactored import PLShandler as plsh
from definitions import get_project_root

# File name and path constants.
PLS_TXT_PATH = os.path.join(get_project_root(), "data/pls.txt")
PLS_TXT_ENC_PATH = os.path.join(get_project_root(), "data/pls.txt.enc")
OUTPUT_TXT_PATH = os.path.join(get_project_root(), "data/out.txt")
INPUT_IMG_DIR = os.path.join(get_project_root(), "data/images/input/")
OUTPUT_IMG_DIR = os.path.join(get_project_root(), "data/images/output/")
INPUT_IMAGES = ["in1.png", "in2.png", "in3.png", "in4.png", "in5.png"]
OUTPUT_IMAGES = ["out1.png", "out2.png", "out3.png", "out4.png", "out5.png"]

# Global variables.
pls = []

# Gets real index values of a pixel from its img using its assigned number and col value.
# Note: "col" holds the image height, since img.size returns (width, height). This was how the original authors' had it.
def _get_pixel_position(pixel_number, col):
    x = pixel_number // col
    y = pixel_number % col

    return x, y

# Hides a single character across multiple pixels.
def _hide_character(img, char_as_bits, pixel_numbers, col):
    # Divides bits in "char_as_bits" into groups of 3, 3, 2 (one group per pixel).
    bit_groups = [char_as_bits[0:3], char_as_bits[3:6], char_as_bits[6:8]]

    # Each iteration hides 3 or less bits within a single pixel.
    for i in range(len(pixel_numbers)):
        _hide_bits_in_pixel(img, pixel_numbers[i], bit_groups[i], col)

# Hides bits in each LSB (3 max.) of an RGB pixel.
def _hide_bits_in_pixel(img, pixel_number, bits, col):
    x, y = _get_pixel_position(pixel_number, col)
    rgb = img.getpixel((x, y))
    channel_values = [rgb[0], rgb[1], rgb[2]]

    for i in range(len(bits)):
        channel_values[i] = _change_lsb(channel_values[i], bits[i])

    img.putpixel((x, y), (channel_values[0], channel_values[1], channel_values[2]))

# Changes LSB of a single pixel channel value, i.e., "R" or "G" or "B".
def _change_lsb(channel_value, new_bit: str):
    lsb = channel_value % 2

    # Only changes LSB of channel value if it does not match the new bit.
    if lsb != int(new_bit):
        # Channel value can not be negative, so add 1 if value is literally 0.
        if channel_value == 0:
            channel_value += 1
        # For all other mismatching values, subtract 1.
        else:
            channel_value -= 1

    return channel_value

def data_list_in_bit(data):
    data_bits = list(format(c, '08b') for c in bytearray(data.encode('latin-1')))
    return data_bits

# Creates the pls file.
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

# Performs encryption and encodes the secret message into the image.
def lsb_encoding(encoded_txt, input_img_path: str, output_img_path: str):
    # Creates PLS text file.
    pls_gen(len(encoded_txt), input_img_path)

    # Variables.
    img = Image.open(rf"{input_img_path}")
    col = img.size[1]
    data_bits = data_list_in_bit(encoded_txt)

    # Encodes each char of message across the image.
    for i in range(len(data_bits)):
        char_in_binary = data_bits[i]
        pls_index = i * 3
        pixel_numbers = pls[pls_index:pls_index + 3]
        _hide_character(img, char_in_binary, pixel_numbers, col)

    # Saves output image file.
    img.save(output_img_path)

    # Gets user input for PLS password and encrypts the PLS file.
    pls_password = input("Insert password for PLS encryption: ")
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.encrypt_file(key, PLS_TXT_PATH)

# Performs decryption and decodes the secret message from the image.
def lsb_decoding(input_img_path: str, output_img_path: str):
    # Gets user-created PLS password and decrypts PLS file.
    pls_password = input("Insert password for PLS decryption: ")
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.decrypt_file(key, PLS_TXT_ENC_PATH, OUTPUT_TXT_PATH)
    pls = np.genfromtxt(OUTPUT_TXT_PATH, delimiter = "\t")

    # Removes the decrypted pls output file.
    if os.path.exists(OUTPUT_TXT_PATH):
        os.remove(OUTPUT_TXT_PATH)

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
