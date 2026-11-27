import hashlib
import random
from PIL import Image

# Constants.
HEADER_LENGTH = 4
NUM_PIXELS_PER_CHAR = 3

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

# Returns the next 3 pixels from the pixel sequence generator.
def _next_pixels(pixel_sequence):
    return [next(pixel_sequence) for _ in range(NUM_PIXELS_PER_CHAR)]

# Yields distinct pixel numbers in a pseudo-random order seeded by the password.
def _pixel_sequence_generator(password, total_pixels):
    rng = random.Random(_seed_from_password(password))
    swaps = {}

    for i in range(total_pixels):
        j = rng.randrange(i, total_pixels)
        a, b = swaps.get(i, i), swaps.get(j, j)
        swaps[j] = a
        yield b

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

# Creates a repeatable 32-byte seed from the PLS password using PBKDF2.
def _seed_from_password(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), b"lsb-pls", 200_000)

# Converts each char of message data into an 8-bit binary string.
def data_list_in_bit(data):
    data_bits = list(format(c, "08b") for c in bytearray(data.encode("latin-1")))
    return data_bits

# Hides the message in the image using a password-based pixel order.
def lsb_encoding(encoded_txt, input_img_path: str, output_img_path: str):
    pls_password = input("Insert password for PLS: ")
    img = Image.open(input_img_path).convert("RGB") # Ensures non-RGB images can be used.
    width, height = img.size
    pixel_sequence = _pixel_sequence_generator(pls_password, width * height)

    # Stops early if the message will not fit inside the image.
    if (HEADER_LENGTH + len(encoded_txt)) * NUM_PIXELS_PER_CHAR > width * height:
        raise ValueError("Error: Message is too large for this image.")

    # Stores message length as 4 bytes so the receiver knows how many chars to read.
    header = [format(byte, "08b") for byte in len(encoded_txt).to_bytes(HEADER_LENGTH, "big")]

    # Hides both header and message within the image using 3 pixels per char.
    for bits in header + data_list_in_bit(encoded_txt):
        _hide_character(img, bits, _next_pixels(pixel_sequence), height)

    # Saves the stego image.
    img.save(output_img_path)

# Recovers the hidden message using the same password-based pixel order used to hide it.
def lsb_decoding(output_img_path: str):
    pls_password = input("Insert password for PLS: ")
    img = Image.open(output_img_path)
    width, height = img.size
    pixel_sequence = _pixel_sequence_generator(pls_password, width * height)
    
    # Reads the 4-byte header to get message length.
    header = "".join(_read_character(img, _next_pixels(pixel_sequence), height) for _ in range(HEADER_LENGTH))
    msg_length = int.from_bytes(header.encode("latin-1"), "big") 

    # Stops early if length does not fit in the image, usually means a wrong password was given by user.
    if (HEADER_LENGTH + msg_length) * NUM_PIXELS_PER_CHAR > width * height:
        raise ValueError("Error: Wrong PLS password or no hidden message.")

    # Reads each char of message & returns the decoded message.
    return "".join(_read_character(img, _next_pixels(pixel_sequence), height) for _ in range(msg_length))
