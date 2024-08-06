import sys,os,math
parent_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from files import staticEstimationOpen,staticEstimationMidEnd


positionEvaluated=0




def closeMill(j,board):
    # return true if move of white piece at pos j closes a mill
    
    mills={
        0:[[0,2,4]],#a0,b1,c2
        1:[[1,3,5],[1,8,17]],# g0,f1,e2  g0,g3,g6
        2:[[0,2,4]],# a0,b1,c2  
        3:[[1,3,5],[3,7,14]],# g0,f1,e2   f1,f3,f5
        4:[[0,2,4]],# a0,b1,c2  
        5:[[1,3,5],[5,6,11]],# g0,f1.e2  e2,e3,e4
        6:[[5,6,11],[6,7,8]],# e2,e3,e4  e3,f3,g3
        7:[[3,7,14],[6,7,8]],# f1,f3,f5  e3,f3,,g3
        8:[[1,8,17],[6,7,8]],# g0,g3,g6  e3,f3,g3
        9:[[9,12,15],[9,10,11]],# c4,b5,a6   c4,d4,e4
        10:[[9,10,11],[10,13,16]],# c4,d4,e4   d4,d5,d6
        11:[[9,10,11],[11,14,17]],# c4,d4,e4   e4,f5,g6
        12:[[9,12,15],[12,13,14]],# c4,b5,a6   b5,d5,f5
        13:[[10,13,16],[12,13,14]],# d4,d5,d6   b5,d5,f5
        14:[[11,14,17],[12,13,14]],# e4,f5,g6   b5,d5,f5
        15:[[9,12,15],[15,16,17]],# c4,b5,a6   a6,d6,g6
        16:[[10,13,16],[15,16,17]],# d4,d5,d6   a6,d6,g6
        17:[[11,14,17],[15,16,17]],# e4,f5,g6   a6,d6,g6
    }
    
    possible_mills=mills[j]
    piece=board[j]
    for mill in possible_mills:
        if(board[mill[0]]==piece and board[mill[1]]==piece and board[mill[2]]==piece):
            return True
    return False


def invert(board):
    if type(board)!=list:
        board=list(board)
    for i in range(18):
        if(board[i]=='W'):
            board[i]='B'
        elif (board[i]=='B'):
            board[i]='W'
    return ''.join(board)


def generateRemove(board,positions):
    # this function to remove blck piece when white forms a mill
    count=0
    for i in range(18):
        if(board[i]=='B'):
            if not closeMill(i,board):
                # removed the black piece
                new=board.copy()
                if type(new)!=list:
                    new=list(new)
                new[i]='x'
                positions.append(''.join(new))
                count=1
                
    if count==0:
        positions.append(''.join(board))


def generateAdd(boardPos):
    # board size is 18
    # positions is different board positions and stored in a list as in case of L in handout
    positions=[]
    # checking all possible positions for white piece to be placed
    
    for i in range(0,18):
        if(boardPos[i]=='x'):
            # copying the board to a variable in form of list
            if type(boardPos)!=list:
                boardPos=list(boardPos)
            b=boardPos.copy()
            b[i]='W'
            # now check if mill is closed or not
            if(closeMill(i,b)):
                # if true then can remove a piece of other player
                generateRemove(b,positions)
            else:
                # apppended
                positions.append(''.join(b))
    return positions

   

def generateMovesOpening(boardPos):
    return generateAdd(boardPos)


def MinMax(boardPos,alpha,beta,depth):
    # minmax main beta change hoga
    if depth==0:
        global positionEvaluated
        positionEvaluated=positionEvaluated+1
        invertBoardPos=invert(boardPos)
        staticEstimate=staticEstimationOpen.staticEstimationOpen(invertBoardPos)
        return boardPos,staticEstimate,depth
    
    else:
        invertBoardPos=invert(boardPos)
        availMoves=generateMovesOpening(invertBoardPos)
        v=10000
        bestMoveToNode=""
        for nextMove in availMoves:
            actualMove=invert(nextMove)
            output=MaxMin(actualMove,alpha,beta,depth-1)
            if(v>output[1]):
                v=output[1]
                bestMoveToNode=actualMove
                if(v<=alpha):
                    return bestMoveToNode,v,depth
                else:
                    beta=min(v,beta)
        return bestMoveToNode,v,depth


def MaxMin(boardPos,alpha,beta,depth):
    # maxmin main alpha change hoga
    if depth==0:
        global positionEvaluated
        positionEvaluated=positionEvaluated+1
        staticEstimate=staticEstimationOpen.staticEstimationOpen(boardPos)
        return boardPos,staticEstimate,depth
    else:
        availMoves=generateMovesOpening(boardPos)
        v=-10000
        bestMoveToNode=""
        for nextMove in availMoves:
            output=MinMax(nextMove,alpha,beta,depth-1)
            
            if(v<output[1]):
                v=output[1]
                bestMoveToNode=nextMove
                
                if(v>=beta):
                    return bestMoveToNode,v,depth
                else:
                    alpha=max(v,alpha)
        
        return bestMoveToNode,v,depth
                    
                    
def AlphaBetaOpening(p1,p2):
    depth=p2
    boardPos=p1
    alpha=-10000
    beta=10000
    move=MaxMin(boardPos,alpha,beta,depth)
    
    print("Board Position : ",''.join(move[0]))
    print("Positions evaluated  by static estimation : ",positionEvaluated)
    print("MINIMAX Estimate : ",move[1])
    
    if type(move[0])!=list:
        return move[0]
    else:
        return ''.join(move[0])
        
    
    
# // mid game and end game
def pieceCount(boardPos,color):
    if(color=='W'):
        return boardPos.count('W')
    else:
        return boardPos.count('B')


def generateHopping(boardPos):
    positions=[]
    if type(boardPos)!=list:
        boardPos=list(boardPos)
    
    # 18 because 18 positions in total
    for a in range(18):
        if(boardPos[a]=='W'):
            for b in range(18):
                if boardPos[b]=='x':
                    newBoard=boardPos.copy()
                    newBoard[a]='x'
                    newBoard[b]='W'
                    if(closeMill(b,newBoard)):
                        generateRemove(newBoard,positions)
                    else:
                        # print(newBoard,"hop")
                        positions.append(''.join(newBoard))



def generateMove(boardPos):
    positions=[]
    if type(boardPos)!=list:
        boardPos=list(boardPos)
    
    
    neighbors={
        0:[1,15], #g0,a6
        1:[0,3,8], #a0,f1,g3
        2:[0,3,4,12], #a0,f1,c2,b5
        3:[1,2,5,7],  #g0,b1,e2,f3
        4:[2,5,9],  #b1,e2,c4
        5:[3,4,6],  #f1,c2,e3
        6:[5,7,11],  #e2,f3,e4
        7:[3,6,8,14], #f1,e3,g3,f5
        8:[1,7,17],   #g0,f3,g6
        9:[4,10,12],  #c2,d4,b5
        10:[9,11,13], #c4,e4,d5
        11:[6,10,14], #e3,d4,f5
        12:[2,9,13,15], #b1,c4,d5,a6
        13:[10,12,14,16], #d4,b5,f5,g6
        14:[7,11,13,17], #f3,e4,d5,g6
        15:[0,12,16],  #a0,b5,g6
        16:[13,15,17],  #d5,a6,g6
        17:[8,14,16]   #g3,f5,g6
    }
    
    for loc in range(18):
        if boardPos[loc]=='W':
            location=neighbors[loc]
            # print(location)
            for j in location:
                if boardPos[j]=='x':
                    newBoard=boardPos.copy()
                    newBoard[loc]='x'
                    newBoard[j]='W'
                    if(closeMill(j,newBoard)):
                        # print("removing")
                        generateRemove(newBoard,positions)
                    else:
                        positions.append(''.join(newBoard))
    
    return positions
            
        

def generateMovesMidEndGame(boardPos):
    if type(boardPos)!=list:
        boardPos=list(boardPos)
    count=pieceCount(boardPos,'W')
    # if player has less than 3 pieces that means they lost.
    if count<3:
        return None
    if count==3:
        return generateHopping(boardPos)
    else:
        return generateMove(boardPos)
    

def MinMaxGame(boardPos,alpha,beta,depth):
    
    if depth==0:
        global positionEvaluated
        positionEvaluated=positionEvaluated+1
        staticEstimate=staticEstimationMidEnd.staticEstimationMidEnd(boardPos)
        return boardPos,staticEstimate,depth
    
    else:
        
        
        # invert the board when it is MinMax
        invertedBoardPos=invert(boardPos)
        availMoves=generateMovesMidEndGame(invertedBoardPos)
        v=10000
        
        if(availMoves==None):
            staticEstimate=v
            positionEvaluated=positionEvaluated+1
            return boardPos,staticEstimate,depth
        
        
        bestMoveToNode=""
        for nextMove in availMoves:
            actualMove=invert(nextMove)
            output=MaxMinGame(actualMove,alpha,beta,depth-1)
            
            if(v>output[1]):
                v=output[1]
                bestMoveToNode=actualMove
                if(v<=alpha):
                    return bestMoveToNode,v,depth
                else:
                    beta=min(v,beta)
                    
                    
        return bestMoveToNode,v,depth 



def MaxMinGame(boardPos,alpha,beta,depth):
    # move has boardPos and staticEstimate as fields
    if depth==0:
        global positionEvaluated
        positionEvaluated=positionEvaluated+1
        staticEstimate=staticEstimationMidEnd.staticEstimationMidEnd(boardPos)
        return boardPos,staticEstimate,depth
    else:    
        availMoves=generateMovesMidEndGame(boardPos)
        v=-10000
        if(availMoves==None):
            staticEstimate=v
            positionEvaluated=positionEvaluated+1
            return boardPos,staticEstimate,depth
        bestMoveToNode=""
        for nextMove in availMoves:
            output=MinMaxGame(nextMove,alpha,beta,depth-1)
          
            if(v<output[1]):
                v=output[1]
                bestMoveToNode=nextMove
                if(v>=beta):
                    return bestMoveToNode,v,depth
                else:
                    alpha=max(alpha,v)
                    
                    
        return bestMoveToNode,v,depth  

def AlphaBetaGame(p1,p2):
    depth=p2
    boardPos=p1
    alpha=-10000
    beta=10000
    move=MaxMinGame(boardPos,alpha,beta,depth)
    
    print("Board Position : ",''.join(move[0]))
    print("Positions evaluated  by static estimation : ",positionEvaluated)
    print("MINIMAX Estimate : ",move[1])
    
    if type(move[0])!=list:
        return move[0]
    else:
        return ''.join(move[0])
    
    
    