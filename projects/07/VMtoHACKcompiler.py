import sys

#USE R13-R15 

jumpLabelCounter = 0
filexxx=""

def popD():
	#Function that pops into D
	#Puts top of stack into D
	#Decreases stack pointer
	re = ""
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=M\n"
	return re

def pushD():
	#Function that push from D
	#Puts D into top of stack
	#Increases stack pointer
	re=""
	re+="@SP\n"
	re+="A=M\n"
	re+="M=D\n"
	re+="@SP\n"
	re+="M=M+1\n"
	return re


#'SP': 0,'LCL': 1,'ARG': 2, 'THIS': 3,'THAT': 4, TEMP 0-7, 5-12

def pop(popLine):
	global filexxx
	re=""
	offset = int(popLine[2])
	if(popLine[1]=="temp"):
		tempSpot = 5+offset
		re+="@%d\n" % tempSpot
		re+="D=A\n"
		#re+="@R13\n"
		#re+="M=D\n"
	elif popLine[1]=="pointer" and popLine[2]=="0":
		re+="@%d\n" % 3
		re+="D=A\n"
	elif popLine[1]=="pointer" and popLine[2]=="1":
		re+="@%d\n" % 4
		re+="D=A\n"
	elif popLine[1]=="static":
		re+="@%s.%s\n" % (filexxx , popLine[2])
		re+="D=A\n"
	else:
		if(popLine[1]=="local"):
			re+="@LCL\n"
		elif(popLine[1]=="argument"):
			re+="@ARG\n"
		elif(popLine[1]=="this"):
			re+="@THIS\n"
		elif(popLine[1]=="that"):
			re+="@THAT\n"
		re+="D=M\n"
		re+="@%d\n" % offset
		re+="D=D+A\n"
	re+="@R13\n"
	re+="M=D\n"
	re+=popD()
	re+="@R13\n"
	re+="A=M\n"
	re+="M=D\n"
	return re

def push(pushLine):
	re=""
	if(pushLine[1] == "constant"):
	 	re+= "@" + pushLine[2] + "\n"
	 	re+="D=A\n"
	 	return re + pushD()
	offset = int(pushLine[2])
	if(pushLine[1]=="temp"):
		tempSpot = 5+offset
		re+="@%d\n" % tempSpot
	elif pushLine[1]=="pointer" and pushLine[2]=="0":
		re+="@%d\n" % 3
	elif pushLine[1]=="pointer" and pushLine[2]=="1":
		re+="@%d\n" % 4
	elif pushLine[1]=="static":
		re+="@%s.%s\n" % (filexxx , pushLine[2])
	else:
		if(pushLine[1]=="local"):
			re+="@LCL\n"
		elif(pushLine[1]=="argument"):
			re+="@ARG\n"
		elif(pushLine[1]=="this"):
			re+="@THIS\n"
		elif(pushLine[1]=="that"):
			re+="@THAT\n"
		re+="D=M\n"
		re+="@%d\n" % offset
		re+="A=D+A\n"
	#A=mem address = location + offest
	re+="D=M\n"
	re+=pushD()
	return re

def equalTo():
	global jumpLabelCounter
	equalLbl = "equal" + str(jumpLabelCounter)
	endLbl = "end" + str(jumpLabelCounter)
	jumpLabelCounter+=1
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=D-M\n"
	re+="@"+equalLbl+"\n"
	re+="D;JEQ\n"
	re+="D=0\n"
	re+="@"+endLbl+"\n"
	re+="0;JMP\n"
	re+="("+equalLbl+")\n"
	re+="D=-1\n"
	re+="("+endLbl+")\n"
	re+=pushD()
	return re

def lessThan():
	global jumpLabelCounter
	lessLbl = "less" + str(jumpLabelCounter)
	endLbl = "end" + str(jumpLabelCounter)
	jumpLabelCounter+=1
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=M-D\n"
	re+="@"+lessLbl+"\n"
	re+="D;JLT\n"
	re+="D=0\n"
	re+="@"+endLbl+"\n"
	re+="0;JMP\n"
	re+="("+lessLbl+")\n"
	re+="D=-1\n"
	re+="("+endLbl+")\n"
	re+=pushD()
	return re

def greaterThan():
	global jumpLabelCounter
	greatLbl = "great" + str(jumpLabelCounter)
	endLbl = "end" + str(jumpLabelCounter)
	jumpLabelCounter+=1
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=M-D\n"
	re+="@"+greatLbl+"\n"
	re+="D;JGT\n"
	re+="D=0\n"
	re+="@"+endLbl+"\n"
	re+="0;JMP\n"
	re+="("+greatLbl+")\n"
	re+="D=-1\n"
	re+="("+endLbl+")\n"
	re+=pushD()
	return re

def add():
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=D+M\n"
	re+=pushD()
	return re

def sub():
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=M-D\n"
	re+=pushD()
	return re

def negate():
	re=popD()
	re+="D=-D\n"
	re+=pushD()
	return re

def bitAnd():#D&A
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=D&M\n"
	re+=pushD()
	return re

def bitOr():
	re=popD()
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=D|M\n"
	re+=pushD()
	return re

def bitNot():
	re=""
	re+="@SP\n"
	re+="M=M-1\n"
	re+="A=M\n"
	re+="D=-1\n"
	re+="D=D-M\n"
	re+=pushD()
	return re


def loadFile(fileName):
	print "Loading in:  ", fileName
	inFile = open(fileName, 'r')
	instructions = list()
	lines = list()
	for line in inFile:
		
		if line.find("//")==0:
			#print "Line is comment"
			continue
		line = line.strip('\t\n\r')
		if line == "":
			continue
		line = line.split(" ")
		lines.append(line)
		#print line
	return lines

def convertVMtoASM(fileName):
	global filexxx 
	period = fileName.rfind(".")
	filexxx= fileName[fileName.rfind("/")+1:period]
	outFileName = fileName[0:period] + ".asm"
	outFile = open(outFileName, 'w')
	loaded=loadFile(sys.argv[1])
	print "Writting '%s' program to: %s" % (filexxx, outFileName)
	
	for line in loaded:
		out="whaaaaa"
		if(line[0] == "push"):
			out= push(line)
		elif(line[0] == "pop"):
			out= pop(line)
		elif(line[0] == "eq"):
			out= equalTo()
		elif(line[0] == "lt"):
			out= lessThan()
		elif(line[0] == "gt"):
			out= greaterThan()
		elif(line[0] == "add"):
			out= add()
		elif(line[0] == "sub"):
			out= sub()
		elif(line[0] == "neg"):
			out= negate()
		elif(line[0] == "and"):
			out= bitAnd()
		elif(line[0] == "or"):
			out= bitOr()
		elif(line[0] == "not"):
			out= bitNot()
		outFile.write(out)

file = sys.argv[1]
convertVMtoASM(file)