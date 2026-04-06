// ============================================================================
//                    Code created by VMTranslator.py V1.10                    
// ============================================================================

// -- Code without bootstrap...

// ============= Conversion of ProgramFlow\FibonacciSeries\FibonacciSeries.vm : 
// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push argument 1] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop pointer 1           // that = argument[1]] : 
@3
D=A
@1
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push constant 0] : 
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop that 0              // first element in the series = 0] : 
@THAT
D=M
@0
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push constant 1] : 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop that 1              // second element in the series = 1] : 
@THAT
D=M
@1
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push argument 0] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push constant 2] : 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [sub] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop argument 0          // num_of_elements -= 2 (first 2 elements are set)] : 
@ARG
D=M
@0
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [label MAIN_LOOP_START] : 
(FibonacciSeries:MAIN_LOOP_START)
// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push argument 0] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [if-goto COMPUTE_ELEMENT // if num_of_elements > 0, goto COMPUTE_ELEMENT] : 
@SP
M=M-1
A=M
D=M
@FibonacciSeries:COMPUTE_ELEMENT
D;JNE

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [goto END_PROGRAM        // otherwise, goto END_PROGRAM] : 
@FibonacciSeries:END_PROGRAM
0;JMP

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [label COMPUTE_ELEMENT] : 
(FibonacciSeries:COMPUTE_ELEMENT)
// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push that 0] : 
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push that 1] : 
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [add] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop that 2              // that[2] = that[0] + that[1]] : 
@THAT
D=M
@2
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push pointer 1] : 
@3
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push constant 1] : 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [add] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop pointer 1           // that += 1] : 
@3
D=A
@1
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push argument 0] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [push constant 1] : 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [sub] : 
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

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [pop argument 0          // num_of_elements--] : 
@ARG
D=M
@0
D=A+D
@FibonacciSeries.i
M=D
@SP
M=M-1
A=M
D=M
@FibonacciSeries.i
A=M
M=D

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [goto MAIN_LOOP_START] : 
@FibonacciSeries:MAIN_LOOP_START
0;JMP

// ProgramFlow\FibonacciSeries\FibonacciSeries.vm, [label END_PROGRAM] : 
(FibonacciSeries:END_PROGRAM)
// -- Infinite loop at program end :
(ENDPRGM)
@ENDPRGM
0;JMP
