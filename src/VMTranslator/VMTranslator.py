from pathlib import Path
from src.VMTranslator.parser.parse import Parser
from src.VMTranslator.code_writer.code_writer import CodeWriter
from src.VMTranslator.parser.library.commandType import CommandType

class VMTranslator:
  def __init__(self, filepath):
    self.out_file = ''
    self.parser = None
    self.code = None
    p = Path(filepath)

    # Initialize codewriter
    self.out_file = p.stem + '.asm'
    self.code = CodeWriter(self.out_file)

    if p.is_file() and p.suffix == '.vm':
      file_name = p.resolve()
      self.parser = Parser(file_name)
      self.code.set_cur_file(file_name.stem)
      self.encode()
    elif p.is_dir():
      self.out_file = p.name + '.asm'
      self.code.bootstrap()
      self.encode_directory(p)

  #need function to clear parser queue and reset loop on new file
  def encode_directory(self, directory):
      for file_path in directory.iterdir():
        file = Path(file_path).resolve()
        if file.suffix == '.vm':
          self.parser = Parser(file)
          self.code.set_cur_file(file.stem)
          self.encode()


  def encode(self):
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
      elif cur_cmd_type == CommandType.C_FUNCTION:
        cmd, function_name, params = self.parser.get_instruction()
        self.code.writeFunction(function_name, params)
      elif cur_cmd_type == CommandType.C_RETURN:
        self.code.writeReturn()
      elif cur_cmd_type == CommandType.C_CALL:
        cmd, function_name, n_args = self.parser.get_instruction()
        self.code.writeCall( function_name, n_args)