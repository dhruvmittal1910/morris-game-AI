import sys
def main():
    pos=sys.argv[1]
    if type(pos)!=list:
        pos=list(pos)
    
    for i in range(18):
        if pos[i]=='B':
            pos[i]='W'
        elif pos[i]=='W':
            pos[i]='B'
    
    print(''.join(pos))
    

    

if __name__ == "__main__":
    main()