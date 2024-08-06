import sys
import os

parent_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from files import MiniMax


def readFile(name):
    file=open(name,"r")
    content=file.read()
    file.close()
    return content

def writeFile(name,content):
    file=open(name,"w")
    file.write(content)
    file.close()
    

def main():
    startPosition=readFile(sys.argv[1])
    print("starting position : ", startPosition)
    
     
    nextPosition=MiniMax.MiniMaxOpeningBlack(startPosition,int(sys.argv[3]))
    print("next position: ",nextPosition)
    
    
    # write the output to board2.txt
    writeFile(sys.argv[2],nextPosition)
    
    
    

if __name__ == "__main__":
    main()