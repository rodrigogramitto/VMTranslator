from src.VMTranslator.parser.parse import Parser
from src.VMTranslator.code_writer.code_writer import CodeWriter

class VMTranslator:
  def __init__(self):
    self.writer = CodeWriter()
    self.parser = Parser()