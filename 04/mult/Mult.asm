// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// __ Algorithm :
// R2 = 0
// R3 = 0
// While R3 < R1 :
//	R2 += R0
//	R3 += 1
// End while

// __ R2 = 0 :
@R2
M=0
// __ R3 = 0 :
@R3
M=0
(BEGINWHILE)
@R3
D=M		// D = R3
@R1
D=D-M	// D = R3 - R1
@ENDWHILE
D;JGE		// If R3 - R1 >= 0 Goto ENDWHILE
@R0
D=M		// D = R0
@R2
M=D+M	// R2 = R0 + R2
@R3
M=M+1	// R3 = R3 + 1
@BEGINWHILE
0;JMP
(ENDWHILE)
@ENDWHILE
0;JMP
