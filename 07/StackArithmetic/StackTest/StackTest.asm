// ==== Global initializations :
// Global initializations end ===

// ==== Conversion of StackArithmetic\StackTest\StackTest.vm :
// push constant 17: 
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17: 
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-eq1-TRUE
D;JEQ
D=0
@StackTest-eq1-END
0;JMP
(StackTest-eq1-TRUE)
D=-1
(StackTest-eq1-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 17: 
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 16: 
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-eq2-TRUE
D;JEQ
D=0
@StackTest-eq2-END
0;JMP
(StackTest-eq2-TRUE)
D=-1
(StackTest-eq2-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 16: 
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17: 
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-eq3-TRUE
D;JEQ
D=0
@StackTest-eq3-END
0;JMP
(StackTest-eq3-TRUE)
D=-1
(StackTest-eq3-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 892: 
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891: 
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-lt4-TRUE
D;JLT
D=0
@StackTest-lt4-END
0;JMP
(StackTest-lt4-TRUE)
D=-1
(StackTest-lt4-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 891: 
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 892: 
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-lt5-TRUE
D;JLT
D=0
@StackTest-lt5-END
0;JMP
(StackTest-lt5-TRUE)
D=-1
(StackTest-lt5-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 891: 
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891: 
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-lt6-TRUE
D;JLT
D=0
@StackTest-lt6-END
0;JMP
(StackTest-lt6-TRUE)
D=-1
(StackTest-lt6-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767: 
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766: 
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-gt7-TRUE
D;JGT
D=0
@StackTest-gt7-END
0;JMP
(StackTest-gt7-TRUE)
D=-1
(StackTest-gt7-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766: 
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767: 
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-gt8-TRUE
D;JGT
D=0
@StackTest-gt8-END
0;JMP
(StackTest-gt8-TRUE)
D=-1
(StackTest-gt8-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766: 
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766: 
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@StackTest-gt9-TRUE
D;JGT
D=0
@StackTest-gt9-END
0;JMP
(StackTest-gt9-TRUE)
D=-1
(StackTest-gt9-END)
@SP
A=M
M=D
@SP
M=M+1

// push constant 57: 
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 31: 
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 53: 
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

// add: 
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

// push constant 112: 
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub: 
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

// neg: 
@SP
M=M-1
A=M
M=-M
@SP
M=M+1

// and: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M&D
@SP
M=M+1

// push constant 82: 
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or: 
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M|D
@SP
M=M+1

// not: 
@SP
M=M-1
A=M
M=!M
@SP
M=M+1

