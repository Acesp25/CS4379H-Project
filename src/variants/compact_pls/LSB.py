import hashlib
import random
import os
from PIL import Image
from variants.compact_pls import PLShandler as plsh
from variants.compact_pls import PLScodec
from definitions import get_project_root

# File name and path constants.
PLS_BIN_PATH = os.path.join(get_project_root(), "data/pls.bin")
PLS_BIN_ENC_PATH = os.path.join(get_project_root(), "data/pls.bin.enc")
OUTPUT_BIN_PATH = os.path.join(get_project_root(), "data/out.bin")

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

# Simply returns the LSB of a channel value number.
def _get_lsb(channel_value):
    return channel_value % 2

# Gets the LSB's from a pixel.
def _read_bits_from_pixel(img, pixel_number, col):
    x, y = _get_pixel_position(pixel_number, col)
    rgb = img.getpixel((x, y))
    bits = f"{_get_lsb(rgb[0])}{_get_lsb(rgb[1])}{_get_lsb(rgb[2])}"

    return bits

# Returns a single character retrieved from the image.
def _read_character(img, pixel_numbers, col):
    char_as_bits = ""

    # Accumulates LSBs across each pixel into a single string.
    for i in range(len(pixel_numbers)):
        char_as_bits += _read_bits_from_pixel(img, pixel_numbers[i], col)

    # Each char is 8 bits, so keeps only the first 8 bits.
    char_as_bits = char_as_bits[:8]

    # Converts the binary string into an integer.
    char_unicode_value = int(char_as_bits, 2)

    # Returns the Unicode equivalent char for the integer.
    return chr(char_unicode_value)

def data_list_in_bit(data):
    data_bits = list(format(c, "08b") for c in bytearray(data.encode("latin-1")))
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

    with open(PLS_BIN_PATH, "wb") as f:
        f.write(PLScodec.encode_pls(pls, row * col))

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
    plsh.encrypt_file(key, PLS_BIN_PATH)

# Performs decryption and decodes the secret message from the image.
def lsb_decoding(input_img_path: str, output_img_path: str):
    # Gets user-created PLS password and decrypts PLS file.
    pls_password = input("Insert password for PLS decryption: ")
    key = hashlib.sha256(pls_password.encode()).digest()
    plsh.decrypt_file(key, PLS_BIN_ENC_PATH, OUTPUT_BIN_PATH)

    input_img = Image.open(rf"{input_img_path}")
    row, col = input_img.size

    try:
        with open(OUTPUT_BIN_PATH, "rb") as f:
            pls = PLScodec.decode_pls(f.read(), row * col)
    finally:
        if os.path.exists(OUTPUT_BIN_PATH):
            os.remove(OUTPUT_BIN_PATH)

    # Gets the secret message.
    stego_image = Image.open(rf"{output_img_path}")
    total_chars = len(pls) // 3
    decoded_text = ""

    # Decodes each char of the message from the stego image.
    for i in range(total_chars):
        pls_index = i * 3
        pixel_numbers = pls[pls_index:pls_index + 3]
        decoded_text += _read_character(stego_image, pixel_numbers, col)

    return decoded_text
