import sys
import os

from src.VMTranslator.VMTranslator import VMTranslator

def main():
    # Expect exactly one argument: the input .asm file
    if len(sys.argv) != 2:
        print("Usage: python hackAssembler.py <file.asm>")
        sys.exit(1)

    input_path = sys.argv[1]

    # Basic validation
    if not input_path.endswith(".asm"):
        print("Error: input file must have a .asm extension")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    translator = VMTranslator()
    print('success')
    #assembler.assemble(input_path)


if __name__ == "__main__":
    main()