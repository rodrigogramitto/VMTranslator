from pathlib import Path
from collections import deque
from src.VMTranslator.parser.library.commands import Commands

class Parser:
  def __init__(self, filepath):
    filepath = Path(filepath).resolve()
    self.cur_instruction = None
    self.commands = Commands()
    with open(filepath) as file:
      self.lines = deque(file.readlines())

  def hasMoreLines(self):
    return len(self.lines) > 0

  def advance(self):
    while self.hasMoreLines():
      curline = self.lines.popleft()
      curline = curline.split("//")[0].strip()
      if not curline:
        continue
      self.cur_instruction = curline.split(' ')
      return

  def commandType(self):
    if self.cur_instruction[0] == 'push':
      return 'C_PUSH'
    elif self.cur_instruction[0] == 'pop':
      return 'C_POP'
    elif self.cur_instruction[0] in self.commands.arithmetic_logic:
      return 'C_ARITHMETIC'

  def arg1(self):
    return self.cur_instruction[0]

  def arg2(self):
    return self.cur_instruction[1] if self.commandType() in self.commands.non_logic else None