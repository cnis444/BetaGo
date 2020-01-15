
from go import Board

b = Board(19)

while 1:
    print(b.value)
    x = int(input("x:"))
    y = int(input("y:"))
    b.play((x,y))

