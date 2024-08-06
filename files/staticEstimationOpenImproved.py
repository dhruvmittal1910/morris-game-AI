import sys,os
from files import MiniMax

def pieceCount(boardPos,color):
    if(color=='W'):
        return boardPos.count('W')
    else:
        return boardPos.count('B')

def numberOfMills(board,color):
    count=0
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
    
    if type(board)!=list:
        board=list(board)
    
    for i in range(18):
        if(board[i]==color):
            possible_mills=mills[i]
            for mill in possible_mills:
                if(board[mill[0]]==color and board[mill[1]]==color and board[mill[2]]==color):
                    count=count+1
    return count
        
    

# static estimation for the opening game
def staticEstimationOpenImproved(boardPos):
    if type(boardPos)!=list:
        boardPos=list(boardPos)
    numWhitePieces=pieceCount(boardPos,'W')
    numBlackPieces=pieceCount(boardPos,'B') 
    
     
    return 100*(numWhitePieces-numBlackPieces) + 5*(numberOfMills(boardPos,'W'))-10*(numberOfMills(boardPos,'B'))