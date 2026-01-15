from src.VMTranslator.parser.library.commandType import CommandType

ARITHMETIC_COMMANDS = {
   "add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"
}

COMMAND_MAP = {
    "push": CommandType.C_PUSH,
    "pop": CommandType.C_POP,
    "label": CommandType.C_LABEL,
    "goto": CommandType.C_GOTO,
    "if-goto": CommandType.C_IF,
    "function": CommandType.C_FUNCTION,
    "call": CommandType.C_CALL,
    "return": CommandType.C_RETURN
}