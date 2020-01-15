
from go import Board

b = Board(5)

while 1:
    print(b.value,"\n",b.parent,"\n", b.degre)
    x = int(input("x:"))
    y = int(input("y:"))
    b.play((x,y))
