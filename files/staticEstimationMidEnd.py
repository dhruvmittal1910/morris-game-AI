import sys,os

from files import MiniMax

def pieceCount(boardPos,color):
    if(color=='W'):
        return boardPos.count('W')
    else:
        return boardPos.count('B')

# static estimation for the opening game
def staticEstimationMidEnd(boardPos):
    if type(boardPos)!=list:
        boardPos=list(boardPos)
    numWhitePieces=pieceCount(boardPos,'W')
    numBlackPieces=pieceCount(boardPos,'B')  
    invertBoard=MiniMax.invert(boardPos)

    blackMoves=MiniMax.generateMovesMidEndGame(invertBoard)
    if(numBlackPieces<=2): return 10000
    elif(numWhitePieces<=2): return -10000
    elif(blackMoves==0 or not blackMoves): return 10000
    else: return (1000*(numWhitePieces-numBlackPieces)-len(blackMoves))
    