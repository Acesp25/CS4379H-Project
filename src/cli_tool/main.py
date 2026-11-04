from colorama import just_fix_windows_console
from termcolor import colored
from original_refactored import main as original
from variants.compact_pls import main as compact_pls
from variants.drop_hex_encode import main as drop_hex_encode
from variants.no_pls import main as no_pls

def _create_divider(text: str) -> str:
    return "=" * len(text)
    
def main():
    # Enables ANSI encoding in older Windows terminal apps.
    just_fix_windows_console()

    # Prints intro text.
    title = "Improving Security of LSB Steganography"
    subtitle = "CS 43798H - Group 2, Fall 2026"

    print("\n" + colored(title, "green", attrs = ["bold"]))
    print(colored(subtitle, "light_grey", attrs = ["bold"]))

    longer_str = max(title, subtitle, key = len)

    print(colored(_create_divider(longer_str), "light_grey", attrs = ["bold"]) + "\n")

    # Prints commands and options.
    PROGRAM_NAMES = ["Original (Refactored)", "Compact PLS", "No Hex Encoding", "No PLS"]

    print(colored("Select a version to run.", "light_grey") + "\n")
    print(colored("\t[A] ", "light_grey", attrs = ["bold"]) + colored(PROGRAM_NAMES[0], "light_grey"))
    print(colored("\t[B] ", "light_grey", attrs = ["bold"]) + colored("Aaron", "blue", attrs = ["bold"]) + colored(" - " + PROGRAM_NAMES[1], "light_grey"))
    print(colored("\t[C] ", "light_grey", attrs = ["bold"]) + colored("Skylar", "blue", attrs = ["bold"]) + colored(" - " + PROGRAM_NAMES[2], "light_grey"))
    print(colored("\t[D] ", "light_grey", attrs = ["bold"]) + colored("John", "blue", attrs = ["bold"]) + colored(" - " + PROGRAM_NAMES[3], "light_grey") + "\n")

    # Gets user input.
    user_input = input(colored("Input: ", "green", attrs = ["bold"])).strip().upper()

    # Validates user input.
    VALID_INPUT = ["A", "B", "C", "D"]

    while (user_input not in VALID_INPUT):
        print()
        print(colored("Error", "red", attrs = ["bold", "underline"]) + colored(": Invalid user input! Select from: <A/B/C/D>", "red", attrs = ["bold"]) + "\n")
        user_input = input(colored("Input: ", "green", attrs = ["bold"])).strip().upper()

    # Prints loading notification.
    longer_str = max(PROGRAM_NAMES[0], PROGRAM_NAMES[1], PROGRAM_NAMES[2], PROGRAM_NAMES[3])

    print("\n" + colored(_create_divider("Loading " + longer_str + "..."), "light_grey", attrs = ["bold"]) + "\n")

    match (user_input):
        case "A":
            print(colored("Loading " + PROGRAM_NAMES[0] + "...", "light_grey", attrs = ["bold", "italic"]) + "\n")
        case "B":
            print(colored("Loading " + PROGRAM_NAMES[1] + "...", "light_grey", attrs = ["bold", "italic"]) + "\n")
        case "C":
            print(colored("Loading " + PROGRAM_NAMES[2] + "...", "light_grey", attrs = ["bold", "italic"]) + "\n")
        case "D":
            print(colored("Loading " + PROGRAM_NAMES[3] + "...", "light_grey", attrs = ["bold", "italic"]) + "\n")
    
    print(colored(_create_divider("Loading " + longer_str + "..."), "light_grey", attrs = ["bold", "italic"]) + "\n")

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
