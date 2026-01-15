from enum import Enum, auto

class CommandType(Enum):
  C_ARITHMETIC = auto()
  C_PUSH = auto()
  C_POP = auto()
  C_LABEL = auto()
  C_GOTO = auto()
  C_IF = auto()
  C_FUNCTION = auto()
  C_CALL = auto()
  C_RETURN = auto()