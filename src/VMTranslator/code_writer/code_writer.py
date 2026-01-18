from src.VMTranslator.code_writer.library.segmentMap import SEGMENT_MAP

class CodeWriter:
    def __init__(self, filepath):
        self.file_name = self.get_file_name(filepath)
        with open(self.file_name, 'w') as f:
            return

    def get_file_name(self, filepath):
        tokens = filepath.split('.')
        return f"""{tokens[0]}.asm"""

    def writeArithmetic(self, command, line_number):
        with open(self.file_name, "a") as out_file:
            asm = ''
            if command == 'add':
                asm = self.get_add()
            elif command == 'sub':
                asm = self.get_sub()
            elif command == 'neg':
                asm = self.get_neg()
            elif command == 'eq':
                asm = self.get_eq(line_number)
            elif command == 'gt':
                asm = self.get_gt(line_number)
            elif command == 'lt':
                asm = self.get_lt(line_number)
            elif command == 'and':
                asm = self.get_and()
            elif command == 'or':
                asm = self.get_or()
            elif command == 'not':
                asm = self.get_not()
            if len(asm):
                out_file.write(asm)

    def writePushPop(self, command, segment, index):
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

    def get_add(self):
       return """
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D+M
        """

    def get_sub(self):
        return """
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=M-D
        """

    def get_neg(self):
        return """
        @SP
        A=M
        A=A-1
        M=-M
        """

    def get_eq(self, line_number):
        return f"""
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        D=D-M
        @EQ_{line_number}
        D;JEQ
        @SP
        A=M
        A=A-1
        M=0
        @END_{line_number}
        0;JMP
        (EQ_{line_number})
        @SP
        A=M
        A=A-1
        M=-1
        (END_{line_number})
        """

    def get_gt(self, line_number):
        return f"""
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        D=D-M
        @GT_{line_number}
        D;JLT
        @SP
        A=M
        A=A-1
        M=0
        @END_{line_number}
        0;JMP
        (GT_{line_number})
        @SP
        A=M
        A=A-1
        M=-1
        (END_{line_number})
        """

    def get_lt(self, line_number):
        return f"""
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        D=D-M
        @LT_{line_number}
        D;JGT
        @SP
        A=M
        A=A-1
        M=0
        @END_{line_number}
        0;JMP
        (LT_{line_number})
        @SP
        A=M
        A=A-1
        M=-1
        (END_{line_number})
        """
    def get_and(self):
        return """
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D&M
        """

    def get_or(self):
        return """
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D|M
        """

    def get_not(self):
        return """
        @SP
        A=M
        A=A-1
        M=!M
        """