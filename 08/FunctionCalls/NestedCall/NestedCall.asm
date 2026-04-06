// ============================================================================
//                    Code created by VMTranslator.py V1.10                    
// ============================================================================

// -- Bootstrap code :
@256
D=A
@SP
M=D
@RETURN_FROM_Sys.init.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN_FROM_Sys.init.1)

// ============================ Conversion of FunctionCalls\NestedCall\Sys.vm : 
// FunctionCalls\NestedCall\Sys.vm, [function Sys.init 0] : 
(Sys.init)
// -- Function without local variable...

// FunctionCalls\NestedCall\Sys.vm, [push constant 4000	// test THIS and THAT context save] : 
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop pointer 0] : 
@3
D=A
@0
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 5000] : 
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop pointer 1] : 
@3
D=A
@1
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [call Sys.main 0] : 
@RETURN_FROM_Sys.main.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(RETURN_FROM_Sys.main.1)

// FunctionCalls\NestedCall\Sys.vm, [pop temp 1] : 
@5
D=A
@1
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [label LOOP] : 
(Sys.init:LOOP)
// FunctionCalls\NestedCall\Sys.vm, [goto LOOP] : 
@Sys.init:LOOP
0;JMP

// FunctionCalls\NestedCall\Sys.vm, [function Sys.main 5] : 
(Sys.main)
// -- Setting 5 local variable(s) to 0 :
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
@SP
A=M
M=0
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [push constant 4001] : 
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop pointer 0] : 
@3
D=A
@0
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 5001] : 
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop pointer 1] : 
@3
D=A
@1
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 200] : 
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop local 1] : 
@LCL
D=M
@1
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 40] : 
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop local 2] : 
@LCL
D=M
@2
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 6] : 
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop local 3] : 
@LCL
D=M
@3
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 123] : 
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [call Sys.add12 1] : 
@RETURN_FROM_Sys.add12.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(RETURN_FROM_Sys.add12.1)

// FunctionCalls\NestedCall\Sys.vm, [pop temp 0] : 
@5
D=A
@0
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push local 0] : 
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

// FunctionCalls\NestedCall\Sys.vm, [push local 1] : 
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

// FunctionCalls\NestedCall\Sys.vm, [push local 2] : 
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [push local 3] : 
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [push local 4] : 
@LCL
D=M
@4
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [add] : 
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

// FunctionCalls\NestedCall\Sys.vm, [add] : 
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

// FunctionCalls\NestedCall\Sys.vm, [add] : 
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

// FunctionCalls\NestedCall\Sys.vm, [add] : 
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

// FunctionCalls\NestedCall\Sys.vm, [return] : 
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

// FunctionCalls\NestedCall\Sys.vm, [function Sys.add12 0] : 
(Sys.add12)
// -- Function without local variable...

// FunctionCalls\NestedCall\Sys.vm, [push constant 4002] : 
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop pointer 0] : 
@3
D=A
@0
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push constant 5002] : 
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [pop pointer 1] : 
@3
D=A
@1
D=A+D
@Sys.i
M=D
@SP
M=M-1
A=M
D=M
@Sys.i
A=M
M=D

// FunctionCalls\NestedCall\Sys.vm, [push argument 0] : 
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

// FunctionCalls\NestedCall\Sys.vm, [push constant 12] : 
@12
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\NestedCall\Sys.vm, [add] : 
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

// FunctionCalls\NestedCall\Sys.vm, [return] : 
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
