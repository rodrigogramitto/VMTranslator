from pathlib import Path
from collections import deque
from src.VMTranslator.parser.library.commandType import CommandType
from src.VMTranslator.parser.library.commands import (
  ARITHMETIC_COMMANDS,
  COMMAND_MAP
)

class Parser:
  def __init__(self, filepath):
    filepath = Path(filepath).resolve()
    self.cur_instruction = ''
    with open(filepath) as file:
      self.lines = deque(file.readlines())

  def hasMoreLines(self):
    return len(self.lines) > 0

  def get_instruction(self):
    return self.cur_instruction.split(' ')

  def advance(self):
    while self.hasMoreLines():
      curline = self.lines.popleft()
      curline = curline.split("//")[0].strip()
      if not curline:
        continue
      self.cur_instruction = curline
      return
    self.cur_instruction = ''

  def commandType(self):
    cmd = self.get_instruction()[0]
    if cmd in ARITHMETIC_COMMANDS:
      return CommandType.C_ARITHMETIC
    elif cmd in COMMAND_MAP:
      return COMMAND_MAP[cmd]
    else:
      raise ValueError(f"Unknown VM command: {cmd}")

  def arg1(self):
    ctype = self.commandType()
    tokens = self.get_instruction()

    if ctype == CommandType.C_RETURN:
      raise ValueError("arg1() called on return command")
    elif ctype == CommandType.C_ARITHMETIC:
      return tokens[0]

    return tokens[1]

  def arg2(self):
    ctype = self.commandType()
    tokens = self.get_instruction()

    if ctype not in {
      CommandType.C_PUSH,
      CommandType.C_POP,
      CommandType.C_FUNCTION,
      CommandType.C_CALL
    }:
      raise ValueError("arg2() not valid for this command type")

    return int(tokens[2])