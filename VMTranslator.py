import sys
import os

from src.VMTranslator.VMTranslator import VMTranslator

def main():
    # Expect exactly one argument: the input .asm file
    if len(sys.argv) != 2:
        print("Usage: python hackAssembler.py <file.vm>")
        sys.exit(1)

    input_path = sys.argv[1]

    translator = VMTranslator(input_path)
    #translator.encode()


if __name__ == "__main__":
    main()