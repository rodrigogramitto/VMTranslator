from src.VMTranslator.parser.parse import Parser
from src.VMTranslator.code_writer.code_writer import CodeWriter

class VMTranslator:
  def __init__(self):
    self.code = CodeWriter()

  def encode(self, filepath):
    self.parser = Parser(filepath)
    while self.parser.hasMoreLines():
      self.parser.advance()