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

// ===================== Conversion of FunctionCalls\FibonacciElement\Main.vm : 
// FunctionCalls\FibonacciElement\Main.vm, [function Main.fibonacci 0] : 
(Main.fibonacci)
// -- Function without local variable...

// FunctionCalls\FibonacciElement\Main.vm, [push argument 0] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [push constant 2] : 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\FibonacciElement\Main.vm, [lt                     // checks if n<2] : 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@Main-lt1-TRUE
D;JLT
D=0
@Main-lt1-END
0;JMP
(Main-lt1-TRUE)
D=-1
(Main-lt1-END)
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\FibonacciElement\Main.vm, [if-goto IF_TRUE] : 
@SP
M=M-1
A=M
D=M
@Main.fibonacci:IF_TRUE
D;JNE

// FunctionCalls\FibonacciElement\Main.vm, [goto IF_FALSE] : 
@Main.fibonacci:IF_FALSE
0;JMP

// FunctionCalls\FibonacciElement\Main.vm, [label IF_TRUE          // if n<2, return n] : 
(Main.fibonacci:IF_TRUE)
// FunctionCalls\FibonacciElement\Main.vm, [push argument 0] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [return] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)] : 
(Main.fibonacci:IF_FALSE)
// FunctionCalls\FibonacciElement\Main.vm, [push argument 0] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [push constant 2] : 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\FibonacciElement\Main.vm, [sub] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [call Main.fibonacci 1  // computes fib(n-2)] : 
@RETURN_FROM_Main.fibonacci.1
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
@Main.fibonacci
0;JMP
(RETURN_FROM_Main.fibonacci.1)

// FunctionCalls\FibonacciElement\Main.vm, [push argument 0] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [push constant 1] : 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\FibonacciElement\Main.vm, [sub] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [call Main.fibonacci 1  // computes fib(n-1)] : 
@RETURN_FROM_Main.fibonacci.2
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
@Main.fibonacci
0;JMP
(RETURN_FROM_Main.fibonacci.2)

// FunctionCalls\FibonacciElement\Main.vm, [add                    // returns fib(n-1) + fib(n-2)] : 
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

// FunctionCalls\FibonacciElement\Main.vm, [return] : 
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


// ====================== Conversion of FunctionCalls\FibonacciElement\Sys.vm : 
// FunctionCalls\FibonacciElement\Sys.vm, [function Sys.init 0] : 
(Sys.init)
// -- Function without local variable...

// FunctionCalls\FibonacciElement\Sys.vm, [push constant 4] : 
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// FunctionCalls\FibonacciElement\Sys.vm, [call Main.fibonacci 1   // computes the 4'th fibonacci element] : 
@RETURN_FROM_Main.fibonacci.3
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
@Main.fibonacci
0;JMP
(RETURN_FROM_Main.fibonacci.3)

// FunctionCalls\FibonacciElement\Sys.vm, [label WHILE] : 
(Sys.init:WHILE)
// FunctionCalls\FibonacciElement\Sys.vm, [goto WHILE              // loops infinitely] : 
@Sys.init:WHILE
0;JMP

// -- Infinite loop at program end :
(ENDPRGM)
@ENDPRGM
0;JMP
