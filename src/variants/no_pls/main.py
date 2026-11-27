import os
import re
from variants.no_pls import LSB as lsb
from variants.no_pls import AES as Cipher
from pathlib import Path
from definitions import get_project_root

# Constants file names and paths.
INPUT_IMG_DIR = os.path.join(get_project_root(), "data/images/input/")
OUTPUT_IMG_DIR = os.path.join(get_project_root(), "data/images/output/")

def _encode():
    img = _select_image(INPUT_IMG_DIR, "Input")

    # Gets stego image path.
    img_number = int(re.findall("\\d", img.name)[0])
    output_img = f"{OUTPUT_IMG_DIR}out{img_number}.png"

    # Gets secret message and password.
    secret_message = input("Enter the secret message: ")
    sec_msg_password = input("\nEnter a secure password: ")

    # Encrypts message and then hides it in the input image.
    encoded_message = Cipher.encrypt(secret_message, sec_msg_password)
    print(f"{encoded_message}\n")
    
    try:
        lsb.lsb_encoding(encoded_message, str(img), output_img)
        print(f"\nSaved stego image to {output_img}")
    except ValueError as error_msg:
        print(error_msg)
    

def _decode():
    # Stops if no stego images exist.
    if not _list_images(OUTPUT_IMG_DIR):
        print("\nError: No output images found. Encode an image first.")
        return
    
    img = _select_image(OUTPUT_IMG_DIR, "Output")

    # Decodes secret message.
    try:
        decoded_text = lsb.lsb_decoding(str(img))
        print(f"{decoded_text}\n")
    except ValueError as error_msg:
        print(f"\n{error_msg}")
        return

    # Gets password input.
    sec_msg_password = input("Enter the secret message password: ")

    # Decrypts the secret message.
    try:
        final_message = Cipher.decrypt(decoded_text, sec_msg_password)
        print("\nFinal message: ", final_message)
    except ValueError:
        print("\nError: Wrong secret message password.")

# Returns a list of file paths for images within "directory".
def _list_images(directory: str):
    images = []

    for path in Path(directory).iterdir():
        # Only appends accepted image files (i.e., skips files such as .gitkeep).
        if path.suffix.lower() in (".png", ".jpg", ".jpeg"):
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
        img_num = int(re.findall("\\d", list_images[i].name)[0])
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
