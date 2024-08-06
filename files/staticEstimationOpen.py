import sys,os


def pieceCount(boardPos,color):
    if(color=='W'):
        return boardPos.count('W')
    else:
        return boardPos.count('B')

# static estimation for the opening game
def staticEstimationOpen(boardPos):
    if type(boardPos)!=list:
        boardPos=list(boardPos)
    numWhitePieces=pieceCount(boardPos,'W')
    numBlackPieces=pieceCount(boardPos,'B')  
    return numWhitePieces-numBlackPieces