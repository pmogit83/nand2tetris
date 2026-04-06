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

// ======================== Conversion of FunctionCalls\StaticsTest\Class1.vm : 
// FunctionCalls\StaticsTest\Class1.vm, [function Class1.set 0] : 
(Class1.set)
// -- Function without local variable...

// FunctionCalls\StaticsTest\Class1.vm, [push argument 0] : 
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

// FunctionCalls\StaticsTest\Class1.vm, [pop static 0] : 
@SP
M=M-1
A=M
D=M
@Class1.0
M=D

// FunctionCalls\StaticsTest\Class1.vm, [push argument 1] : 
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

// FunctionCalls\StaticsTest\Class1.vm, [pop static 1] : 
@SP
M=M-1
A=M
D=M
@Class1.1
M=D

// FunctionCalls\StaticsTest\Class1.vm, [push constant 0] : 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Class1.vm, [return] : 
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

// FunctionCalls\StaticsTest\Class1.vm, [function Class1.get 0] : 
(Class1.get)
// -- Function without local variable...

// FunctionCalls\StaticsTest\Class1.vm, [push static 0] : 
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Class1.vm, [push static 1] : 
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Class1.vm, [sub] : 
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

// FunctionCalls\StaticsTest\Class1.vm, [return] : 
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


// ======================== Conversion of FunctionCalls\StaticsTest\Class2.vm : 
// FunctionCalls\StaticsTest\Class2.vm, [function Class2.set 0] : 
(Class2.set)
// -- Function without local variable...

// FunctionCalls\StaticsTest\Class2.vm, [push argument 0] : 
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

// FunctionCalls\StaticsTest\Class2.vm, [pop static 0] : 
@SP
M=M-1
A=M
D=M
@Class2.0
M=D

// FunctionCalls\StaticsTest\Class2.vm, [push argument 1] : 
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

// FunctionCalls\StaticsTest\Class2.vm, [pop static 1] : 
@SP
M=M-1
A=M
D=M
@Class2.1
M=D

// FunctionCalls\StaticsTest\Class2.vm, [push constant 0] : 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Class2.vm, [return] : 
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

// FunctionCalls\StaticsTest\Class2.vm, [function Class2.get 0] : 
(Class2.get)
// -- Function without local variable...

// FunctionCalls\StaticsTest\Class2.vm, [push static 0] : 
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Class2.vm, [push static 1] : 
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Class2.vm, [sub] : 
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

// FunctionCalls\StaticsTest\Class2.vm, [return] : 
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


// =========================== Conversion of FunctionCalls\StaticsTest\Sys.vm : 
// FunctionCalls\StaticsTest\Sys.vm, [function Sys.init 0] : 
(Sys.init)
// -- Function without local variable...

// FunctionCalls\StaticsTest\Sys.vm, [push constant 6] : 
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Sys.vm, [push constant 8] : 
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Sys.vm, [call Class1.set 2] : 
@RETURN_FROM_Class1.set.1
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
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(RETURN_FROM_Class1.set.1)

// FunctionCalls\StaticsTest\Sys.vm, [pop temp 0 // Dumps the return value] : 
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

// FunctionCalls\StaticsTest\Sys.vm, [push constant 23] : 
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Sys.vm, [push constant 15] : 
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\StaticsTest\Sys.vm, [call Class2.set 2] : 
@RETURN_FROM_Class2.set.1
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
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(RETURN_FROM_Class2.set.1)

// FunctionCalls\StaticsTest\Sys.vm, [pop temp 0 // Dumps the return value] : 
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

// FunctionCalls\StaticsTest\Sys.vm, [call Class1.get 0] : 
@RETURN_FROM_Class1.get.1
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
@Class1.get
0;JMP
(RETURN_FROM_Class1.get.1)

// FunctionCalls\StaticsTest\Sys.vm, [call Class2.get 0] : 
@RETURN_FROM_Class2.get.1
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
@Class2.get
0;JMP
(RETURN_FROM_Class2.get.1)

// FunctionCalls\StaticsTest\Sys.vm, [label WHILE] : 
(Sys.init:WHILE)
// FunctionCalls\StaticsTest\Sys.vm, [goto WHILE] : 
@Sys.init:WHILE
0;JMP

// -- Infinite loop at program end :
(ENDPRGM)
@ENDPRGM
0;JMP
