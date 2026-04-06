// ============================================================================
//                    Code created by VMTranslator.py V1.10                    
// ============================================================================

// -- Code without bootstrap...

// ========================= Conversion of ProgramFlow\BasicLoop\BasicLoop.vm : 
// ProgramFlow\BasicLoop\BasicLoop.vm, [push constant 0] : 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\BasicLoop\BasicLoop.vm, [pop local 0         // initializes sum = 0] : 
@LCL
D=M
@0
D=A+D
@BasicLoop.i
M=D
@SP
M=M-1
A=M
D=M
@BasicLoop.i
A=M
M=D

// ProgramFlow\BasicLoop\BasicLoop.vm, [label LOOP_START] : 
(BasicLoop:LOOP_START)
// ProgramFlow\BasicLoop\BasicLoop.vm, [push argument 0] : 
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

// ProgramFlow\BasicLoop\BasicLoop.vm, [push local 0] : 
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

// ProgramFlow\BasicLoop\BasicLoop.vm, [add] : 
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

// ProgramFlow\BasicLoop\BasicLoop.vm, [pop local 0	        // sum = sum + counter] : 
@LCL
D=M
@0
D=A+D
@BasicLoop.i
M=D
@SP
M=M-1
A=M
D=M
@BasicLoop.i
A=M
M=D

// ProgramFlow\BasicLoop\BasicLoop.vm, [push argument 0] : 
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

// ProgramFlow\BasicLoop\BasicLoop.vm, [push constant 1] : 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\BasicLoop\BasicLoop.vm, [sub] : 
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

// ProgramFlow\BasicLoop\BasicLoop.vm, [pop argument 0      // counter--] : 
@ARG
D=M
@0
D=A+D
@BasicLoop.i
M=D
@SP
M=M-1
A=M
D=M
@BasicLoop.i
A=M
M=D

// ProgramFlow\BasicLoop\BasicLoop.vm, [push argument 0] : 
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

// ProgramFlow\BasicLoop\BasicLoop.vm, [if-goto LOOP_START  // If counter != 0, goto LOOP_START] : 
@SP
M=M-1
A=M
D=M
@BasicLoop:LOOP_START
D;JNE

// ProgramFlow\BasicLoop\BasicLoop.vm, [push local 0] : 
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

// -- Infinite loop at program end :
(ENDPRGM)
@ENDPRGM
0;JMP
