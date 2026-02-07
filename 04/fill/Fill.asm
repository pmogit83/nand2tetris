// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// The screen matches a 256 x 512 / 16 = 8192 16-bits words. To fill it with  
// wordvalue, we start from the SCREEN address, we set it to wordvalue and we 
// iterate while incrementing the address until the 8192 words have been filled.

(KBREAD)
@24576
D=M
// __ If D <> 0, blacken the screen :
@BLACKSCREEN
D;JNE
// __ Else, clean it :
@WHITESCREEN
0;JMP

// __ Fill the screen with the value found in wordvalue :
(FILLSCREEN)
@wordcount
M=0
(SCREENLOOP)
// __ Compute destination address and save it into R0 :
@wordcount
D=M
@SCREEN
A=A+D
D=A
@R0
M=D
// __ Put destination value into D :
@wordvalue
D=M
// __ Get destination address from R0 :
@R0
A=M
M=D
// __ Increment wordcount :
@wordcount
M=M+1
D=M
@8192
// @3
D=A-D
// __ Loop if wordcount < 8192, hence if 8192 - wordcount > 0 
@SCREENLOOP
D;JGT
// __ Else, go back to read keyboard :
@KBREAD
0;JMP

// __ Blacken the screen :
(BLACKSCREEN)
@wordvalue
M=-1
@FILLSCREEN
0;JMP

// __ Clean the screen :
(WHITESCREEN)
@wordvalue
M=0
@FILLSCREEN
0;JMP

// __ Program end :
(ENDWHILE)
@ENDWHILE
0;JMP
