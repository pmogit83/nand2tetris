// ============================================================================
//                    Code created by VMTranslator.py V1.10                    
// ============================================================================

// -- Code without bootstrap...

// ============= Conversion of FunctionCalls\SimpleFunction\SimpleFunction.vm : 
// FunctionCalls\SimpleFunction\SimpleFunction.vm, [function SimpleFunction.test 2] : 
(SimpleFunction.test)
// -- Setting 2 local variable(s) to 0 :
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [push local 0] : 
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [push local 1] : 
@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [add] : 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [not] : 
@SP
M=M-1
A=M
M=!M
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [push argument 0] : 
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [add] : 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [push argument 1] : 
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [sub] : 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1

// FunctionCalls\SimpleFunction\SimpleFunction.vm, [return] : 
// -- R14 = FRAME = LCL :
@LCL
D=M
@R14
M=D
// -- R13 = *(FRAME-5) = Return address :
@R13
M=D
M=M-1
M=M-1
M=M-1
M=M-1
M=M-1
A=M
D=M
@R13
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R14
M=M-1
A=M
D=M
@THAT
M=D
@R14
M=M-1
A=M
D=M
@THIS
M=D
@R14
M=M-1
A=M
D=M
@ARG
M=D
@R14
M=M-1
A=M
D=M
@LCL
M=D
@R13
A=M
0;JMP

// -- Infinite loop at program end :
(ENDPRGM)
@ENDPRGM
0;JMP
