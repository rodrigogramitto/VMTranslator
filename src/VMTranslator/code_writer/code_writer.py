from src.VMTranslator.code_writer.library.segmentMap import SEGMENT_MAP
import textwrap

class CodeWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cur_file = ''
        self.call_id = 1
        with open(self.file_name, 'w') as f:
            return

    def set_cur_file(self, file_name):
        self.cur_file = file_name

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
                out_file.write(textwrap.dedent(asm))

    def writePushPop(self, command, segment, index):
        with open(self.file_name, "a") as out_file:
            asm = ''
            if command == 'push':
                asm = self.writePush(segment, index)
            elif command == 'pop':
                asm = self.writePop(segment,index)
            if len(asm):
                out_file.write(textwrap.dedent(asm))

    def writePush(self, segment, index):
        if segment == 'constant':
            return self.push_constant(index)
        elif segment == 'temp':
            return self.push_temp(index)
        elif segment == 'static':
            return self.push_static(index, self.cur_file)
        elif segment == 'pointer':
            return self.push_pointer(index)
        elif self.is_valid_segment(segment):
            return self.push_segment(index, self.get_segment_pointer(segment))
        else:
            raise ValueError("segment invalid")

    def writePop(self, segment, index):
        if segment == 'temp':
            return self.get_pop_temp(index)
        elif segment == 'static':
            return self.get_pop_static(index, self.cur_file)
        elif segment == 'pointer':
            return self.get_pop_pointer(index)
        elif self.is_valid_segment(segment):
            return self.get_pop_segment(self.get_segment_pointer(segment), index)
        else:
            raise ValueError("segment invalid")

    def get_pop_segment(self, segment, index):
        return f"""
        @{segment}
        D=M
        @{index}
        D=D+A
        @R13
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @R13
        A=M
        M=D
        """

    def get_pop_temp(self, index):
        idx = 5 + int(index)
        return f"""
        @SP
        M=M-1
        A=M
        D=M
        @{idx}
        M=D
        """

    def get_pop_static(self, index, filename):
        return f"""
        @SP
        M=M-1
        A=M
        D=M
        @{filename}.{index}
        M=D
        """

    def get_pop_pointer(self, index):
        addr = 'THIS' if index == '0' else 'THAT'
        return f"""
        @SP
        M=M-1
        A=M
        D=M
        @{addr}
        M=D
        """

    def push_constant(self, index):
        return f"""
        @{index}
        D=A
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
        D=D+A
        A=D
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def push_static(self, index, filename):
        return f"""
        @{filename}.{index}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def push_temp(self, index):
        temp_idx = 5 + int(index)
        return f"""
        @{temp_idx}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def push_pointer(self, index):
        idx = 'THIS' if index == '0' else 'THAT'
        return f"""
        @{idx}
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

    def setFileName(self):
        return

    def writeLabel(self, label):
        asm = f"""({label})"""
        self.write_asm(asm)

    def writeGoto(self, label):
        asm = f"""
            @{label}
            0;JMP
        """
        self.write_asm(asm)

    def writeIf(self, label):
        asm = f"""
            @SP
            M=M-1
            A=M
            D=M
            @{label}
            D;JNE
        """
        self.write_asm(asm)


    def writeFunction(self, function_name, n_vars):
        var_init = """
        @SP
        A=M
        M=0
        @SP
        M=M+1
        """
        asm = f"""
        ({function_name})
        """
        asm += var_init * int(n_vars)
        self.write_asm(asm)

    def writeCall(self, function_name, n_args):
        asm = f"""
        @{function_name}$ret.{self.call_id}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        {self.get_segment_push('LCL')}
        {self.get_segment_push('ARG')}
        {self.get_segment_push('THIS')}
        {self.get_segment_push('THAT')}
        @SP
        D=M
        @{n_args}
        D=D-A
        @5
        D=D-A
        @ARG
        M=D
        @SP
        D=M
        @LCL
        M=D
        @{function_name}
        0;JMP
        ({function_name}$ret.{self.call_id})
        """
        self.call_id += 1
        self.write_asm(asm)

    def get_segment_push(self, segment):
        return f"""
        @{segment}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def writeReturn(self):
        asm = f"""
        // endFrame = LCL
        @LCL
        D=M
        @endFrame
        M=D
        // returnAddress = *(endFrame - 5)
        @5
        D=D-A
        A=D
        D=M
        @retAddress
        M=D
        // Pop stack into ARG
        @SP
        M=M-1
        A=M
        D=M
        @ARG
        A=M
        M=D
        // SP = ARG + 1
        @ARG
        D=M+1
        @SP
        M=D
        // Restore that *(endFrame - 1)
        @endFrame
        D=M
        A=D-1
        D=M
        @THAT
        M=D
        // restore this *(endFrame - 2)
        @2
        D=A
        @endFrame
        D=M-D
        A=D
        D=M
        @THIS
        M=D
        // restore arg  *(endFrame - 3)
        @3
        D=A
        @endFrame
        D=M-D
        A=D
        D=M
        @ARG
        M=D
        // restore lcl *(endFrame - 4)
        @4
        D=A
        @endFrame
        D=M-D
        A=D
        D=M
        @LCL
        M=D
        // goto return address
        @retAddress
        A=M
        0;JMP
        """
        self.write_asm(asm)

    def close(self):
        return

    def write_asm(self, asm):
        with open(self.file_name, "a") as out_file:
            if len(asm):
                out_file.write(textwrap.dedent(asm))

    def write_bootstrap(self):
        asm = f"""
        @256
        D=A
        @SP
        M=D
        """
        self.write_asm(asm)

    def bootstrap(self):
        self.write_bootstrap()
        self.writeCall('Sys.init', 0)
