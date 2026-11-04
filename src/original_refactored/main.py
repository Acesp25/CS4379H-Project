from original_refactored  import LSB as lsb
from original_refactored  import AES as Cipher
import os
from pathlib import Path
from definitions import PROJECT_ROOT as PROJECT_ROOT

def main():
    # Constants file names and paths.
    PLS_TXT_PATH = os.path.join(PROJECT_ROOT, "data/pls.txt")
    PLS_TXT_ENC_PATH = os.path.join(PROJECT_ROOT, "data/pls.txt.enc")
    OUTPUT_TXT_PATH = os.path.join(PROJECT_ROOT, "data/out.txt")
    INPUT_IMG_DIR = os.path.join(PROJECT_ROOT, "data/images/input/")
    OUTPUT_IMG_DIR = os.path.join(PROJECT_ROOT, "data/images/output/")
    INPUT_IMAGES = ["in1.png", "in2.png", "in3.png", "in4.png", "in5.png"]
    OUTPUT_IMAGES = ["out1.png", "out2.png", "out3.png", "out4.png", "out5.png"]

    # Gets user input.
    select = input("Enter E for Encoding or D for Decoding: ").upper()

    if select == "E":
        # Deletes non-image output files if they exist.
        if os.path.exists(OUTPUT_TXT_PATH):
            os.remove(OUTPUT_TXT_PATH)

        if os.path.exists(PLS_TXT_PATH):
            os.remove(PLS_TXT_PATH)

        if os.path.exists(PLS_TXT_ENC_PATH):
            os.remove(PLS_TXT_ENC_PATH)

        # User selects which image to process.
        print("\n" + "List of images." + "\n")
        print("[1] Input image 1")
        print("[2] Input image 2")
        print("[3] Input image 3")
        print("[4] Input image 4")
        print("[5] Input image 5" + "\n")
        user_input = input("Select an image to process <1/2/3/4/5>: ")

        # Validates user input.
        VALID_INPUT = ["1", "2", "3", "4", "5"]

        while (user_input not in VALID_INPUT):
            print("\n" + "Error: Invalid input. Select from: <1/2/3/4/5>")
            user_input = input("\n" + "Select an image to process: ")

        # Specifies for the program which image will be used.
        selected_input_img = INPUT_IMG_DIR
        corresponding_output_img = OUTPUT_IMG_DIR

        match (user_input):
            case "1":
                selected_input_img = selected_input_img + INPUT_IMAGES[0]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[0]
            case "2":
                selected_input_img = selected_input_img + INPUT_IMAGES[1]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[1]
            case "3":
                selected_input_img = selected_input_img + INPUT_IMAGES[2]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[2]
            case "4":
                selected_input_img = selected_input_img + INPUT_IMAGES[3]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[3]
            case "5":
                selected_input_img = selected_input_img + INPUT_IMAGES[4]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[4]

        # Deletes output image if it already exists.
        if os.path.exists(corresponding_output_img):
                os.remove(corresponding_output_img)

        # Gets secret message and password.
        secret_message = input("Enter the secret message: ")
        sec_msg_password = input("Enter a secure password: ")

        # Encrypts input image to produce output image and pls.
        encoded_message = Cipher.encrypt(secret_message, sec_msg_password)
        print(encoded_message)
        lsb.lsb_encoding(encoded_message, selected_input_img, corresponding_output_img)

        # Deletes `pls.txt` and replaces with `pls.txt.enc`.
        if os.path.exists(PLS_TXT_PATH):
            os.remove(PLS_TXT_PATH)

    if select == "D":
        # Gets all known output image file paths.
        output_image_paths = []

        for path in Path(OUTPUT_IMG_DIR).iterdir():
            output_image_paths.append(path)

        # Creates an array of output menu items to display to user.
        output_image_menu_items = []

        for img in output_image_paths:
            # Gets just the file name without any extra path.
            img_name = Path(img).name

            if img_name in OUTPUT_IMAGES:
                if img_name == OUTPUT_IMAGES[0]:
                    output_image_menu_items.append("Output image 1")

                if img_name == OUTPUT_IMAGES[1]:
                    output_image_menu_items.append("Output image 2")

                if img_name == OUTPUT_IMAGES[2]:
                    output_image_menu_items.append("Output image 3")

                if img_name == OUTPUT_IMAGES[3]:
                    output_image_menu_items.append("Output image 4")

                if img_name == OUTPUT_IMAGES[4]:
                    output_image_menu_items.append("Output image 5")

        # Sorts the array of output image menu items.
        output_image_menu_items = sorted(output_image_menu_items)

        # Displays the menu items to user.
        print("\n" + "List of images." + "\n")

        for i in range(len(output_image_menu_items)):
            print("[" + str(i + 1) + "] " + output_image_menu_items[i])

        user_input = input("\n" + "Select an image to process <1/2/3/4/5>: ")

        # Validates user input.
        VALID_INPUT = ["1", "2", "3", "4", "5"]

        while (user_input not in VALID_INPUT):
            print("\n" + "Error: Invalid input. Select from: <1/2/3/4/5>")
            user_input = input("\n" + "Select an image to process: ")

        # Specifies for the program which image will be used.
        selected_input_img = INPUT_IMG_DIR
        corresponding_output_img = OUTPUT_IMG_DIR

        match (user_input):
            case "1":
                selected_input_img = selected_input_img + INPUT_IMAGES[0]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[0]
            case "2":
                selected_input_img = selected_input_img + INPUT_IMAGES[1]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[1]
            case "3":
                selected_input_img = selected_input_img + INPUT_IMAGES[2]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[2]
            case "4":
                selected_input_img = selected_input_img + INPUT_IMAGES[3]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[3]
            case "5":
                selected_input_img = selected_input_img + INPUT_IMAGES[4]
                corresponding_output_img = corresponding_output_img + OUTPUT_IMAGES[4]

        # Decodes secret message if encrypted PLS file exists.
        if os.path.exists(PLS_TXT_ENC_PATH):
            decoded_text = lsb.lsb_decoding(selected_input_img, corresponding_output_img)
            print(decoded_text)

            # Gets password input.
            sec_msg_password = input("Enter the secret message password: ")

            # Decrypts the secret message.
            final_message = Cipher.decrypt(decoded_text, sec_msg_password)
            print("Final message: ", final_message)
        else:
            print("Error: PLS file was not found.")

if __name__ == '__main__' :
	main()
