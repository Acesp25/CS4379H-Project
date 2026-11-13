from colorama import just_fix_windows_console
from termcolor import colored
from original_refactored import main as original
from variants.compact_pls import main as compact_pls
from variants.drop_hex_encode import main as drop_hex_encode
from variants.no_pls import main as no_pls

PROGRAM_NAMES = ["Original (Refactored)", "Compact PLS", "No Hex Encoding", "No PLS"] # Stores names of program variants.
VALID_INPUT = ["A", "B", "C", "D"] # Stores all valid user input.

def _create_divider(text: str) -> str:
    return "=" * len(text)
    
def main():
    # Enables ANSI encoding in older Windows terminal apps.
    just_fix_windows_console()

    # Prints intro text.
    title = "Improving Security of LSB Steganography"
    subtitle = "CS 4379H - Group 2, Fall 2026"

    print(f"\n{colored(title, "green", attrs = ["bold"])}")
    print(f"{colored(subtitle, "light_grey", attrs = ["bold"])}")

    # Prints a horizonal separator based on whichever above string (title, subtitle) is longer.
    longer_str = max(title, subtitle, key = len)

    print(colored(_create_divider(longer_str), "light_grey", attrs = ["bold"]) + "\n")

    # Prints commands and options.
    print(f"{colored("Select a version to run.", "light_grey")}\n")
    print(f"{colored("\t[A] ", "light_grey", attrs = ["bold"])}{colored(PROGRAM_NAMES[0], "light_grey")}")
    print(f"{colored("\t[B] ", "light_grey", attrs = ["bold"])}{colored("Aaron", "blue", attrs = ["bold"])}{colored(" - " + PROGRAM_NAMES[1], "light_grey")}")
    print(f"{colored("\t[C] ", "light_grey", attrs = ["bold"])}{colored("Skylar", "blue", attrs = ["bold"])}{colored(" - " + PROGRAM_NAMES[2], "light_grey")}")
    print(f"{colored("\t[D] ", "light_grey", attrs = ["bold"])}{colored("John", "blue", attrs = ["bold"])}{colored(" - " + PROGRAM_NAMES[3], "light_grey")}\n")

    # Gets user input.
    user_input = input(colored("Input: ", "green", attrs = ["bold"])).strip().upper()

    # Validates user input.
    while (user_input not in VALID_INPUT):
        print()
        print(f"{colored("Error", "red", attrs = ["bold", "underline"])}{colored(": Invalid user input! Select from: <A/B/C/D>", "red", attrs = ["bold"])}\n")
        user_input = input(colored("Input: ", "green", attrs = ["bold"])).strip().upper()

    # Prints loading notification.
    longer_str = max(PROGRAM_NAMES[0], PROGRAM_NAMES[1], PROGRAM_NAMES[2], PROGRAM_NAMES[3])

    print(f"\n{colored(_create_divider(f"Loading {longer_str}..."), "light_grey", attrs = ["bold"])}\n")

    # Encodes user input to index of "PROGRAM_NAMES".
    user_input_encoder = {
        "A": 0, 
        "B": 1, 
        "C": 2, 
        "D": 3
    }
    
    # Confirms to the user which option they selected.
    print(f"{colored("Loading " + PROGRAM_NAMES[user_input_encoder[user_input]] + "...", "light_grey", attrs = ["bold", "italic"])}\n")
    print(f"{colored(_create_divider(f"Loading {longer_str}..."), "light_grey", attrs = ["bold", "italic"])}\n")

    # Decides which program to run.
    match (user_input):
        case "A":
            original.main()
        case "B":
            compact_pls.main()
        case "C":
            drop_hex_encode.main()
        case "D":
            no_pls.main()

if __name__ == "__main__":
    main()
