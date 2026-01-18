from src.VMTranslator.parser.parse import Parser
from src.VMTranslator.code_writer.code_writer import CodeWriter
from src.VMTranslator.parser.library.commandType import CommandType

class VMTranslator:
  def __init__(self):
    return

  def encode(self, filepath):
    self.parser = Parser(filepath)
    self.code = CodeWriter(filepath)
    while self.parser.hasMoreLines():
      self.parser.advance()
      if self.parser.commandType() == CommandType.C_PUSH:
        cmd, seg, idx = self.parser.get_instruction()
        self.code.writePushPop(cmd, seg, idx)
      elif self.parser.commandType() == CommandType.C_ARITHMETIC:
        cmd = self.parser.get_instruction()[0]
        self.code.writeArithmetic(cmd, self.parser.line_number)