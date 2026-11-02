import argparse
import LSB as lsb
import AES as Cipher
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Encode or decode a message in an image.")
    default_input = Path(__file__).parent / "data" / "output" / "images" / "in1.png"
    default_output = Path(__file__).parent / "data" / "output" / "images" / "out1.png"
    parser.add_argument(
        "--input",
        default=str(default_input),
        help="Original image to encode, or stego image to decode.",
    )
    parser.add_argument(
        "--output",
        default=str(default_output),
        help="Path to save the encoded image; also the stego image to read when decoding.",
    )
    args = parser.parse_args()

    select = input("Enter E for Encoding D for Decoding :")
    if select == 'E':
        if os.path.exists("out.txt"):
            os.remove("out.txt")
        if os.path.exists("pls.txt.enc"):
            os.remove("pls.txt.enc")
        if os.path.exists("pls.txt"):
            os.remove("pls.txt")

        if os.path.isfile(args.input):
            secretMessage = input("Enter the secret message :")
            passwordText = input("Password :")
            encodedMessage = Cipher.encrypt(secretMessage, passwordText)
            print(encodedMessage)
            lsb.LsbEncoding(encodedMessage, args.input, args.output)
            if os.path.exists("pls.txt"):
                os.remove("pls.txt")
        else : print("Image is not Present")

    if select == 'D':
        if os.path.exists("pls.txt.enc"):
            decodedText = lsb.LsbDecoding(args.output)
            print(decodedText)
            password = input("Enter the password :")
            finalMessage = Cipher.decrypt(decodedText, password)
            print("Final message :", finalMessage)
        else :
            print("PLS file is not present !")








main()
