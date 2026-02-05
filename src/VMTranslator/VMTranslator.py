from src.VMTranslator.parser.parse import Parser
from src.VMTranslator.code_writer.code_writer import CodeWriter
from src.VMTranslator.parser.library.commandType import CommandType

class VMTranslator:
  def __init__(self):
    return

  #Add folder handling:
    # if source is a file ->
    #  constructs a parser to handle the input file
    # for each vm command in input -> use parser to parse commmand, use codewriter to generate the assembly code from it

    #if source is folder
      # handles every .vm file in the folder in the manner described above

  def encode(self, filepath):
    self.parser = Parser(filepath)
    self.code = CodeWriter(filepath)
    while self.parser.hasMoreLines():
      self.parser.advance()
      if self.parser.commandType() == CommandType.C_PUSH:
        cmd, seg, idx = self.parser.get_instruction()
        self.code.writePushPop(cmd, seg, idx)
      elif self.parser.commandType() == CommandType.C_POP:
        cmd, seg, idx = self.parser.get_instruction()
        self.code.writePushPop(cmd, seg, idx)
      elif self.parser.commandType() == CommandType.C_ARITHMETIC:
        cmd = self.parser.get_instruction()[0]
        self.code.writeArithmetic(cmd, self.parser.line_number)