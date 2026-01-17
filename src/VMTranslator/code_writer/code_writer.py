from src.VMTranslator.code_writer.library.segmentMap import SEGMENT_MAP

class CodeWriter:
    def __init__(self, filepath):
        self.file_name = self.get_file_name(filepath)
        with open(self.file_name, 'w') as f:
            return

    def get_file_name(self, filepath):
        tokens = filepath.split('.')
        return f"""{tokens[0]}.asm"""

    def writeArithmetic(self, command):
        with open(self.file_name, "a") as out_file:
            asm = ''

            if len(asm):
                out_file.write(asm)

    def writePushPop(self, command, segment, index):
        print("command: ", command)
        with open(self.file_name, "a") as out_file:
            asm = ''
            if command == 'push':
                asm = self.writePush(segment, index)
            elif command == 'pop':
                asm = self.writePop(segment,index)
            if len(asm):
                out_file.write(asm)

    def writePush(self, segment, index):
        if segment == 'constant':
            return self.push_constant(index)
        elif self.is_valid_segment(segment):
            return self.push_segment(index, self.get_segment_pointer(segment))
        else:
            ValueError("segment invalid")

    def writePop(self, segment, index):
        return f"""
            @{segment}
            D=M
            @{index}
            D=D+M
            @addr
            M=D
            @SP
            M=M-1
            A=M
            D=M
            @addr
            M=D
        """

    def push_constant(self, index):
        return f"""
        @{index}
        D=A
        // RAM[SP]=D
        @SP
        A=M
        M=D
        //SP++
        @SP
        M=M+1
        """

    def push_segment(self, index, segment):
        return f"""
            @{segment}
            D=M
            @{index}
            D=D+M
            A=D
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
        """

    def is_valid_segment(self, segment):
        return segment in SEGMENT_MAP

    def get_segment_pointer(self, segment):
        return SEGMENT_MAP[segment]
