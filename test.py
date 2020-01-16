
from go import Board

b = Board(2)

while 1:
    print(b.value)
    x = int(input("x:"))
    y = int(input("y:"))
    b.play((x,y))

#dic = dict()

#dic[(1,1)] = 0
#dic[(1,2)] = 3

#for x in dic:
#    print(x, dic[x])

#print(254 ^ 128 ^ 128)