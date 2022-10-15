import sys

argCnt = len(sys.argv)
print(f"Args count: {str(argCnt)}")

print(f"Program name = {sys.argv[0]}")

if argCnt > 1 :
    for i in range(1, argCnt):
        print(f"Arg {str(i+1)} = {sys.argv[i]}\n")
