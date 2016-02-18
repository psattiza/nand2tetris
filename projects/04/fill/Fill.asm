// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
(TOP)

	@KBD
	D=M;
	@A
	D; JGT
	@White
	0; JMP
	//256*512 pixles = 16384 bytes, 24575 last thing
(A)
	@I
	M=-1;
(LOOP)
	@I
	M=M+1;
	D=M;
	@SCREEN
	A=A+D;
	M=-1;
	D=A;
	@24575
	D=A-D;
	@LOOP
	D;JNE
	@TOP
	0;JMP
(White)
	@I
	M=-1;
(WLOOP)
	@I
	M=M+1;
	D=M;
	@SCREEN
	A=A+D;
	M=0;
	D=A;
	@24575
	D=A-D;
	@WLOOP
	D;JNE
	@TOP
	0;JMP
(END)
	0; JMP // Infinite loop to stall simulator