import os
import re
from original_refactored  import LSB as lsb
from original_refactored  import AES as Cipher
from pathlib import Path
from definitions import get_project_root

# Constants file names and paths.
PLS_TXT_PATH = os.path.join(get_project_root(), "data/pls.txt")
PLS_TXT_ENC_PATH = os.path.join(get_project_root(), "data/pls.txt.enc")
OUTPUT_TXT_PATH = os.path.join(get_project_root(), "data/out.txt")
INPUT_IMG_DIR = os.path.join(get_project_root(), "data/images/input/")
OUTPUT_IMG_DIR = os.path.join(get_project_root(), "data/images/output/")

# Returns a list of file paths for images within "directory".
def _list_images(directory: str):
    images = []

    for path in Path(directory).iterdir():
        images.append(path)

    # Ensures images are sorted correctly, e.g., "in1.png, in2.png, in3.png, ...".
    return sorted(images)

# Returns user image selection.
def _select_image(directory: str, img_type: str):
    list_images = _list_images(directory)
    valid_labels = "ABCDE"
    true_labels = valid_labels[:len(list_images)] # Only contains labels for amount of images that actually exist.

    print()

    # Prints menu options to user, e.g., "[A] Input image 1".
    for i in range(len(true_labels)):
        img_num = int(re.findall("\d", list_images[i].name)[0])
        print(f"[{true_labels[i]}] {img_type} image {img_num}")

    print()

    # Gets & validates user input.
    while True:
        user_input = input("Select an image to process: ").strip().upper()

        print()

        if user_input and user_input in true_labels:
            break
        else:
            print("Error: Invalid input. Try again.")

    # Returns the path of the image selected by the user.
    return list_images[true_labels.index(user_input)]

def _encode():
    # Deletes non-image output files if they exist.
    if os.path.exists(OUTPUT_TXT_PATH):
        os.remove(OUTPUT_TXT_PATH)

    if os.path.exists(PLS_TXT_PATH):
        os.remove(PLS_TXT_PATH)

    if os.path.exists(PLS_TXT_ENC_PATH):
        os.remove(PLS_TXT_ENC_PATH)

    img = _select_image(INPUT_IMG_DIR, "Input")

    # Deletes corresponding output image if it exists.
    img_number = int(re.findall("\d", img.name)[0])
    output_img = f"{OUTPUT_IMG_DIR}out{img_number}.png"

    if os.path.exists(output_img):
        os.remove(output_img)

    # Gets secret message and password.
    secret_message = input("Enter the secret message: ")
    sec_msg_password = input("\nEnter a secure password: ")

    # Encrypts input image to produce output image and pls.
    encoded_message = Cipher.encrypt(secret_message, sec_msg_password)
    print(f"{encoded_message}\n")
    lsb.lsb_encoding(encoded_message, str(img), output_img)

    # Deletes "pls.txt" and replaces with "pls.txt.enc".
    if os.path.exists(PLS_TXT_PATH):
        os.remove(PLS_TXT_PATH)

def _decode():
    # Exits early if there is nothing to decode.
    if not os.path.exists(PLS_TXT_ENC_PATH):
        print("\nError: Encrypted PLS file was not found.")
        return

    if not _list_images(OUTPUT_IMG_DIR):
        print("\nError: No output images found. Encode an image first.")
        return
    
    img = _select_image(OUTPUT_IMG_DIR, "Output")

    # Gets corresponding input image.
    img_number = int(re.findall("\d", img.name)[0])
    input_img = f"{INPUT_IMG_DIR}in{img_number}.png"

    # Decodes secret message.
    decoded_text = lsb.lsb_decoding(input_img, str(img))
    print(f"{decoded_text}\n")

    # Gets password input.
    sec_msg_password = input("Enter the secret message password: ")

    # Decrypts the secret message.
    final_message = Cipher.decrypt(decoded_text, sec_msg_password)
    print("\nFinal message: ", final_message)

def main():
    # Gets user input.
    select = input("Enter E for Encoding or D for Decoding: ").strip().upper()

    if select == "E":
        _encode()
    elif select == "D":
        _decode()
    else:
        print("\nError: Invalid input. Try running the program again.")

if __name__ == '__main__' :
	main()
