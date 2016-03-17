import sys
import os
#USE R13-R15 

jumpLabelCounter = 0
callReturnCounter = 0

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

def pop(popLine,methodName):
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
		re+="@%s.%s\n" % (methodName , popLine[2])
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

def push(pushLine,methodName):
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
		re+="@%s.%s\n" % (methodName , pushLine[2])
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

def label(line, methodName):
	re="({})\n".format(methodName+"_"+line[1])
	return re

def goto(line, methodName):	
	if line[0] == "goto":
		return "@{}\n0;JMP\n".format(methodName+"_"+line[1])
	else:
		re = popD()
		re += "@{}\nD;JNE\n".format(methodName+"_"+line[1])
		return re

def call(line,methodName):
	global callReturnCounter
	callReturnCounter+=1
	returnLabel = "{}_{}_{}".format(methodName,line[1],callReturnCounter)
	re="@{}\n".format(returnLabel)
	re+="D=A\n"
	re+=pushD() ##push return label
	re+="@LCL\n"
	re+="D=M\n"
	re+=pushD() ##push local
	re+="@ARG\n"
	re+="D=M\n"
	re+=pushD() ##push argument pointer
	re+="@THIS\n"
	re+="D=M\n"
	re+=pushD() ##push this
	re+="@THAT\n"
	re+="D=M\n"
	re+=pushD() ##push that
	re+="@SP\n"
	re+="D=M\n"
	re+="@LCL\n"
	re+="M=D\n"
	offset = int(line[2]) + 5 # new arg = SP -( numArgs + 5)
	re+="@{}\n".format(offset)
	re+="D=D-A\n"
	re+="@ARG\n"
	re+="M=D\n"
	re+="@{}\n".format(line[1])
	re+="0;JMP\n"
	re+="({})\n".format(returnLabel)
	return re

def function(line,methodName):
	re="({})\n".format(line[1])
	re+="D=0\n"
	for _ in range(int(line[2])):
		re+=pushD()
	return re

def returnCall():
	re="@LCL\n"
	re+="D=M\n"
	re+="@R13\n"
	re+="M=D\n" ##R13 = frame
	re+="@5\n"
	re+="AD=D-A\n"
	re+="D=M\n"
	re+="@R14\n"
	re+="M=D\n" ##R14 = return address
	re+=popD()
	re+="@ARG\n"
	re+="A=M\n"
	re+="M=D\n" ##Return value now in correct place

	re+="D=A+1\n"
	re+="@SP\n"
	re+="M=D\n" ## *SP = *ARG + 1

	re+="@R13\n"
	re+="D=M\n"
	re+="@1\n"
	re+="A=D-A\n"
	re+="D=M\n"
	re+="@THAT\n"
	re+="M=D\n"		# That = *frame -1

	re+="@R13\n"
	re+="D=M\n"
	re+="@2\n"
	re+="A=D-A\n"
	re+="D=M\n"
	re+="@THIS\n"
	re+="M=D\n"		# this = *frame - 2

	re+="@R13\n"
	re+="D=M\n"
	re+="@3\n"
	re+="A=D-A\n"
	re+="D=M\n"
	re+="@ARG\n"
	re+="M=D\n"		# ARG = *frame -3

	re+="@R13\n"
	re+="D=M\n"
	re+="@4\n"
	re+="A=D-A\n"
	re+="D=M\n"
	re+="@LCL\n"
	re+="M=D\n"		# LCL = *frame -4

	re+="@R14\n"
	re+="A=M\n"
	re+="0;JMP\n"
	return re


def loadFile(fileName):
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
def bootStrap():
	re="//bootStrap\n"
	re+="@256\n"
	re+="D=A\n"
	re+="@SP\n"
	re+="M=D\n"
	re+= call(["call", "Sys.init","0"] ,"Sys")	
	re+="//end bootStrap\n"
	re+="\n"
	re+="\n"
	return re

def convertVMfoldertoASM(folderName):
	if folderName.endswith('/'):
		folderName = folderName[:-1]
	childFolder = folderName[folderName.rfind("/")+1:]
	outFileName = "{}/{}.asm".format(folderName, childFolder)
	outFile = open(outFileName, 'w')
	print "Writting '%s' program to: %s" % (childFolder, outFileName)
	outFile.write(bootStrap())
	for vm in os.listdir(folderName):
		if vm.endswith(".vm"):
			convertVMtoASM("{}/{}".format(folderName,vm),outFile)
	print("Hasta la vista, baby!")

def convertVMtoASM(vmfilename, outFile):
	fileName = vmfilename
	period = fileName.rfind(".")
	slash = fileName.rfind("/")
	methodName = fileName[slash+1:period]
	#print "Methodname = '{}'".format(methodName)
	loaded=loadFile(vmfilename)
	print "Appending %12s program to: %s" % ("'"+methodName+"'", outFile.name)
	for line in loaded:
		out="whaaaaa"
		if(line[0] == "push"):
			out= push(line,methodName)
		elif(line[0] == "pop"):
			out= pop(line,methodName)
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
		elif(line[0] == "call"):
			out= call(line,methodName)
		elif(line[0] == "function"):
			out= function(line,methodName)
		elif(line[0] == "return"):
			out= returnCall()
		elif(line[0] == "label"):
			out= label(line,methodName)
		elif(line[0] == "if-goto" or line[0] == "goto"):
			out= goto(line,methodName)
		outFile.write(out)

folder = sys.argv[1]
convertVMfoldertoASM(folder)