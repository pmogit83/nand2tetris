// Bugs volontaires...

// Computes R0 = 2 + 3  (R0 refers to RAM[0])
// 123456 = 11110001001000000 => 17 bits   

@2
D=A=8
@3PLOUF
@123456
D=D+A
@0
M=D=X;Z;Y

