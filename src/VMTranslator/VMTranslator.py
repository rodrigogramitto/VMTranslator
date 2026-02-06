from pathlib import Path
from src.VMTranslator.parser.parse import Parser
from src.VMTranslator.code_writer.code_writer import CodeWriter
from src.VMTranslator.parser.library.commandType import CommandType

class VMTranslator:
  def __init__(self, filepath):
    self.out_file = ''
    self.parser = Parser()
    p = Path(filepath)

    if p.is_file():
      file = Path(filepath).resolve()
      self.parser.setFileName(file)
      self.encode()
    elif p.is_dir():
      print('P is a directory: ', p)

  def encode(self):
    self.code = CodeWriter(self.out_file)
    while self.parser.hasMoreLines():
      self.parser.advance()
      cur_cmd_type = self.parser.commandType()
      if cur_cmd_type == CommandType.C_PUSH:
        cmd, seg, idx = self.parser.get_instruction()
        self.code.writePushPop(cmd, seg, idx)
      elif cur_cmd_type == CommandType.C_POP:
        cmd, seg, idx = self.parser.get_instruction()
        self.code.writePushPop(cmd, seg, idx)
      elif cur_cmd_type == CommandType.C_ARITHMETIC:
        cmd = self.parser.get_instruction()[0]
        self.code.writeArithmetic(cmd, self.parser.line_number)
      elif cur_cmd_type == CommandType.C_LABEL:
        label = self.parser.get_instruction()[1]
        self.code.writeLabel(label)
      elif cur_cmd_type == CommandType.C_GOTO:
        label = self.parser.get_instruction()[1]
        self.code.writeGoto(label)
      elif cur_cmd_type == CommandType.C_IF:
        label = self.parser.get_instruction()[1]
        self.code.writeIf(label)