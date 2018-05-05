# -*- coding: utf-8 -*-
"""
PegSolitaire_Solver.py
@author: Kostas Klimantakis dai16010
"""

import time
import winsound

#metavlhtes pou prepei na einai orates se ola to programma
Moves = []
NoM = 0
finalMove = []
solved = False
timeLimit = 0.0
centerX = 0
centerY = 0

#main
def main():
    global timeLimit
    method=''
    while(method!="depth" and method!="best"):
        method = input("Please select algorith (depth/best):\n")
    timeLimit = float(input("Give a time limit -in seconds- (press '-1' for no time limit):\n"))
    Algorithm(method)

#vasikos genikos algori8mos
def Algorithm(method):
    global Moves
    global NoM
    global finalMove
    global solved
    global timeLimit
    global x
    global y
    global start_time
    global centerX 
    global centerY 
    
    #anagnwsh arxeiou
    while(True):
        try:
            inputFile = open(input("Give the inputFile name:\n"),"r")
        except FileNotFoundError:
            print("No such file.")
        else:
            break
        
    start_time = time.time()
    problem = inputFile.readlines()
    y,x = problem[0].split(' ')
    y = int(y)
    x = int(x)  
    centerX = x//2
    centerY = y//2-1
    problem = problem[1:y+1]
    
    for i in range(y):
        problem[i] = problem[i].replace(' ','')
        problem[i] = problem[i].replace('\n','')
        
    #8esh prwtou komvou
    root = problem
    rootNode = Node(Node.non,root,None,0)
    Recursive(method,rootNode)

    #an exoun dokimastei oles oi pi8anes kinhsei
    #to programma termatizei
    winsound.Beep(1000, 1000)
    input("Cannot solve it.\nPress any key to exit.")
    exit()


#gia ka8e lista paidiwn epektynei anadromika to dentro
def Recursive(method,parent, path=[]):
    global solved
    global centerX
    global centerY
    global timeLimit

    path.append(parent)
    if(winCheck(parent.data) == 1):
                solved = True
                finalMove.append(parent)
                
                exportSolution(method,getSolutionPath(finalMove))
    nextNodesList = nextMoves(parent)
    if(method=="best"):
        nextNodesList = sortNodes(nextNodesList)
        nextNodesList = nextNodesList[::-1]
    for child in nextNodesList:
        if child not in path:
            n = Node(Node.non,child,parent,child.rank)
            path = Recursive(method,child, path)
    if(timeLimit != -1.0):
        if((time.time() - start_time) >= timeLimit):
            winsound.Beep(1000, 1000)
            input("Time Out!\nPress any key to exit.")
            exit()
    return path

#h klasi node symvolizei ka8e komvo tou dentrou
#(dld to apotelesma ka8e memonomenhs kinhshs)
#opou ferei plhrofories opws to iD tou , ton gonea tou,
#to stigmeiotypo tou tamplo klp
class Node():
    non = 0

    def __init__(self,iD,dt,pr,r):
        self.iD = Node.non
        self.data = dt
        self.parent = pr
        self.rank = r
        Node.non = Node.non + 1

    def getParent(self):
        return self.parent

#4 pi8anes kinhseis einai efiktes ka8e fora
#epistrefei mia lista me ta pi8ana stigmeiotypa twn pi8anwn autwn kinhsewn(paidiwn)
#pou proerxontai apo ena prohgoumeno(goneas)
def nextMoves(parent):
    global NoM
    global centerX
    global centerY
    newNodes = []
    problem = parent.data
    problemBuf = []
    for i in range(x):
        problemBuf.append(problem[i][:])
        
    for j in range(y):
        for i in range(x):
                if(problem[j][i]=='2'):
                    #print(problem[j][i+2]=='1',problem[j][i+1]=='1',i<=x-3)
                    #print("Space at:",j,i)
                    if(j>=2 and problem[j-2][i]=='1' and problem[j-1][i]=='1'):
                        NoM += 1
                        Moves.append(str((i,j-2,i,j,Node.non)))
                        #print("Move",j-2,i,"to",j,i,"and remove",j-1,i,'\
                        buf = problemBuf[j][:i]+'1'+problemBuf[j][i+1:]
                        problemBuf[j] = buf
                        #aka problem[j][i] = '1'
                        buf = problemBuf[j-1][:i]+'2'+problemBuf[j-1][i+1:]
                        problemBuf[j-1] = buf
                        #aka problem[j-1][i] = '2'
                        buf = problemBuf[j-2][:i]+'2'+problemBuf[j-2][i+1:]
                        problemBuf[j-2] = buf
                        #aka problem[j-2][i] = '1'
                        newNodes.append(Node(Node.non,problemBuf,parent,getRank(centerX,centerY,i,j-1)))
                        problemBuf = []
                        for i in range(x):
                            problemBuf.append(problem[i][:])

                    if(i<=x-3 and problem[j][i+2]=='1' and problem[j][i+1]=='1'):
                        NoM += 1
                        Moves.append(str((i+2,j,i,j,Node.non)))
                        #print("Move",j,i+2,"to",j,i,"and remove",j,i+1,'\
                        buf = problemBuf[j][:i]+'1'+problemBuf[j][i+1:]
                        problemBuf[j] = buf
                        buf = problemBuf[j][:i+1]+'2'+problemBuf[j][i+2:]
                        problemBuf[j] = buf
                        buf = problemBuf[j][:i+2]+'2'+problemBuf[j][i+3:]
                        problemBuf[j] = buf
                        newNodes.append(Node(Node.non,problemBuf,parent,getRank(centerX,centerY,i+1,j)))
                        problemBuf = []
                        for i in range(x):
                            problemBuf.append(problem[i][:])
                    if(j<=y-3 and problem[j+2][i]=='1' and problem[j+1][i]=='1'):
                        NoM += 1
                        Moves.append(str((i,j+2,i,j,Node.non)))
                        #print("Move",j+2,i,"to",j,i,"and remove",j+1,i,'\
                        buf = problemBuf[j][:i]+'1'+problemBuf[j][i+1:]
                        problemBuf[j] = buf
                        buf = problemBuf[j+1][:i]+'2'+problemBuf[j+1][i+1:]
                        problemBuf[j+1] = buf
                        buf = problemBuf[j+2][:i]+'2'+problemBuf[j+2][i+1:]
                        problemBuf[j+2] = buf
                        newNodes.append(Node(Node.non,problemBuf,parent,getRank(centerX,centerY,i,j+1)))
                        problemBuf = []
                        for i in range(x):
                            problemBuf.append(problem[i][:])                    
                    if(i>=2 and problem[j][i-2]=='1' and problem[j][i-1]=='1'):
                        NoM += 1
                        Moves.append(str((i-2,j,i,j,Node.non)))
                        #print("Move",j,i-2,"to",j,i,"and remove",j,i-1,'\n')
                        buf = problemBuf[j][:i]+'1'+problemBuf[j][i+1:]
                        problemBuf[j] = buf
                        buf = problemBuf[j][:i-1]+'2'+problemBuf[j][i:]
                        problemBuf[j] = buf
                        buf = problemBuf[j][:i-2]+'2'+problemBuf[j][i-1:]
                        newNodes.append(Node(Node.non,problemBuf,parent,getRank(centerX,centerY,i-1,j)))
                        problemBuf[j] = buf
                        problemBuf = []
                        for i in range(x):
                            problemBuf.append(problem[i][:])

    return newNodes

#the bigger the rank, the bigger the priority
#se periptwsh tou algori8mou 'best'
#oi komvoi ta3inomountai me vash to rank tous
#pou einai ousiastika h apostash tous apo to kentro tou tamplo
#me skopo na mhn afisoume peg stis akres opou synh8ws odhgei se adie3odo
def getRank(cx,cy,i,j):
    return abs(cx-i) + abs(cy-j)

def sortNodes(nodeList):
    return sorted(nodeList, key=lambda node: node.rank) 

#exontas krathsei to teleytaio komvo pou einai sthn ousia h lysh
#epanalhptika apo gonea se paidi ftanoume 3ana ston prwto komvo
#kratontas to monopati ths lyshs
def getSolutionPath(finalMove):
    solution = []
    solution.append(finalMove[0].iD)
    par = finalMove[0].getParent()
    while(par.getParent() != None):
        solution.append(par.iD)
        par = par.getParent()
    print("Solved in",time.time() - start_time,"seconds.\nMaking",len(solution), "moves.")
    print("After searching",NoM, "potential moves in total.")
    return solution

#elegxos tou plh8ous twn pegs
def winCheck(board):
    counter = 0
    for j in range(y):
        counter += board[j].count('1')
    return counter

#e3agwgh se .txt twn kinhsewn pou odhgoun se lysh
def exportSolution(method,solution):
    
    if(method=="depth"):
        outputFile=open("pegSolitaire_SolutionDFS.txt","w")
    elif(method=="best"):
        outputFile=open("pegSolitaire_SolutionBEST.txt","w")
    else:
        input("Error no solution method found.\nPress any key to exit.")
    
    outputFile.write(str(len(solution)))
    outputFile.write('\n')
            
    for i in Moves:
        if(int(i[13:i.find(')')]) in solution):
            outputFile.write(i[1])
            outputFile.write(' ')
            outputFile.write(i[4])
            outputFile.write(' ')
            outputFile.write(i[7])
            outputFile.write(' ')
            outputFile.write(i[10])
            outputFile.write('\n')
    outputFile.close()
    winsound.Beep(1000, 1000)
    input("Press any key to exit.\n")
    exit()
    
if __name__ == "__main__":
    main()
