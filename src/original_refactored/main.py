import LSB as lsb
import AES as Cipher
import os

def main():
    PLS_TXT_PATH = "../data/pls.txt"
    PLS_TXT_ENC_PATH = "../data/pls.txt.enc"
    OUTPUT_TXT_PATH = "../data/out.txt"
    INPUT_IMG_DIR = "../data/images/input"
    OUTPUT_IMG_DIR = "../data/images/output"
    INPUT_IMAGES = ["in1.png", "in2.png", "in3.png", "in4.png", "in5.png"]
    OUTPUT_IMAGES = ["out1.png", "out2.png", "out3.png", "out4.png", "out5.png"]

    select = input("Enter E for Encoding or D for Decoding: ")

    if select == "E":
        # Deletes output images if they already exist.
        for output_image in OUTPUT_IMAGES:
            if os.path.exists(OUTPUT_IMG_DIR + output_image):
                os.remove(OUTPUT_IMG_DIR + output_image)

        # Deletes other output files if they exist.
        if os.path.exists(OUTPUT_TXT_PATH):
            os.remove(OUTPUT_TXT_PATH)

        if os.path.exists(PLS_TXT_PATH):
            os.remove(PLS_TXT_PATH)

        if os.path.exists(PLS_TXT_ENC_PATH):
            os.remove(PLS_TXT_ENC_PATH)

        # User selects which image to process.
        print("\n" + "List of images." + "\n")
        print("[1] Input image 1" + "\n")
        print("[1] Input image 2" + "\n")
        print("[1] Input image 3" + "\n")
        print("[1] Input image 4" + "\n")
        print("[1] Input image 5" + "\n")
        user_input = input("Select an image to process <1/2/3/4/5>: ")

        # Validates user input.
        VALID_INPUT = ["1", "2", "3", "4", "5"]

        while (user_input not in VALID_INPUT):
            print("\n" + "Error: Invalid input. Select from: <1/2/3/4/5>")
            user_input = input("\n" + "Selection an image to process: ")

        # Specifies for the program which image will be used.
        image_selection = INPUT_IMG_DIR

        match (user_input):
            case "1":
                image_selection = image_selection + INPUT_IMAGES[0]
            case "2":
                image_selection = image_selection + INPUT_IMAGES[1]
            case "3":
                image_selection = image_selection + INPUT_IMAGES[2]
            case "4":
                image_selection = image_selection + INPUT_IMAGES[3]
            case "5":
                image_selection = image_selection + INPUT_IMAGES[4]

        # Gets secret message and password.
        secret_message = input("Enter the secret message: ")
        sec_msg_password = input("Enter a secure password: ")

        # Encrypts input image to produce output image and pls.
        encoded_message = Cipher.encrypt(secret_message, sec_msg_password)
        print(encoded_message)
        lsb.LsbEncoding(encoded_message)

        # TODO: Explore why the original author included this final if statement here.
        if os.path.exists(PLS_TXT_PATH):
            os.remove(PLS_TXT_PATH)

    if select == "D":
        # Decodes secret message if encrypted PLS file exists.
        if os.path.exists(PLS_TXT_ENC_PATH):
            decoded_text = lsb.LsbDecoding()
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
