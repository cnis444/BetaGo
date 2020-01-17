
from go import Board

b = Board(19)

for x in range(19):
    for y in range(19):
        #print(b.value)
        b.play((x,y))


#dic = dict()

#dic[(1,1)] = 0
#dic[(1,2)] = 3
#dic[(2,2)] = 5

#del dic[(2,2)]
#for x in dic:
#    print(x, dic[x])

#print(254 ^ 128 ^ 128)