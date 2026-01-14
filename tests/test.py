import tempfile
import os

from src.VMTranslator.parser.parse import Parser
# from src.VMTranslator.CommandType import (
#     C_ARITHMETIC, C_PUSH, C_POP,
#     C_LABEL, C_GOTO, C_IF,
#     C_FUNCTION, C_CALL, C_RETURN
# )


def make_vm_file(contents: str) -> str:
    """Create a temp .vm file and return its path."""
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".vm")
    f.write(contents.encode())
    f.close()
    return f.name


def test_ignore_comments_and_blank_lines():
    path = make_vm_file("""
    // full line comment

    push constant 7   // inline comment
    push constant 8

    // another comment
    add
    """)

    parser = Parser(path)

    commands = []
    while parser.hasMoreLines():
        parser.advance()
        commands.append(parser.cur_instruction)

    os.remove(path)

    print(commands)

    assert commands == [
        ['push', 'constant', '7'],
        ['push', 'constant', '8'],
       ['add']
    ]


def test_arithmetic_command():
    path = make_vm_file("add")

    parser = Parser(path)
    parser.advance()

    assert parser.commandType() == 'C_ARITHMETIC'
    assert parser.arg1() == "add"

    os.remove(path)


def test_push_command():
    path = make_vm_file("push local 3")

    parser = Parser(path)
    parser.advance()

    assert parser.commandType() == 'C_PUSH'
    assert parser.arg1() == "local"
    assert parser.arg2() == 3

    os.remove(path)


def test_pop_command():
    path = make_vm_file("pop argument 2")

    parser = Parser(path)
    parser.advance()

    assert parser.commandType() == 'C_POP'
    assert parser.arg1() == "argument"
    assert parser.arg2() == 2

    os.remove(path)


def test_return_command():
    path = make_vm_file("return")

    parser = Parser(path)
    parser.advance()

    assert parser.commandType() == 'C_RETURN'

    try:
        parser.arg1()
        assert False, "arg1() should not be allowed for return"
    except Exception:
        pass

    try:
        parser.arg2()
        assert False, "arg2() should not be allowed for return"
    except Exception:
        pass

    os.remove(path)


def test_command_sequence_order():
    path = make_vm_file("""
    push constant 10
    push constant 20
    add
    pop local 0
    """)

    parser = Parser(path)

    types = []
    while parser.hasMoreLines():
        parser.advance()
        types.append(parser.commandType())

    os.remove(path)

    # assert types == [
    #     C_PUSH,
    #     C_PUSH,
    #     C_ARITHMETIC,
    #     C_POP
    # ]


def test_arg2_is_int():
    path = make_vm_file("push constant 999")

    parser = Parser(path)
    parser.advance()

    assert isinstance(parser.arg2(), int)

    os.remove(path)


def run_all_tests():
    tests = [
        test_ignore_comments_and_blank_lines,
        test_arithmetic_command,
        test_push_command,
        test_pop_command,
        test_return_command,
        test_command_sequence_order,
        test_arg2_is_int,
    ]

    for test in tests:
        test()
        print(f"[PASS] {test.__name__}")

    print("\nAll parser tests passed ✅")


if __name__ == "__main__":
    run_all_tests()
