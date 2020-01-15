import numpy as np

class Board(object):
    BLACK = 1
    WHITE = -1
    EMPTY = 0
    BORDER = 2

    def __init__(self, n, maxturn = None):
        self.maxturn = maxturn if maxturn is not None else n*n
        self.value = np.zeros((n+2,n+2), dtype=int)
        self.value[0,:] = self.value[-1,:] = self.value[:,0] = self.value[:,-1] = self.BORDER
        self.parent = np.ones((n,n,2), dtype=int) * -1
        self.degre = np.zeros((n,n), dtype=int)
        self.nextPlayer = self.BLACK
        self.passRound = 0
        self.n = n
        self.round = 0
        self.MOVE = [(1,0), (0,1), (-1,0), (0,-1)]

    
    def play(self, move):
        if move == (-1,-1):
            self.passRound += 1
            if self.passRound == 2:
                raise Exception("OUI!!!! la partie est finie")
            self.nextPlayer *=-1
            self.round +=1
            return
        self.passRound = 0;
        
        if(self.value[move[0]+1, move[1]+1] != self.EMPTY):
            raise Exception("Les règles sont pourtant simples !!!")



        self.value[move[0]+1, move[1]+1] = self.nextPlayer;    
        self.degre[move] = 0

        for x,y in self.MOVE:
            if(self.value[move[0]+x+1, move[1]+y+1] == self.EMPTY):
                self.degre[move] += 1

        for x,y in self.MOVE:
            if(self.value[move[0]+x+1, move[1]+y+1] == self.nextPlayer * -1):
                self.decreaseDegre((move[0]+x, move[1]+y))
            if(self.value[move[0]+x+1, move[1]+y+1] == self.nextPlayer):
                self.degre[self.getParent((move[0]+x, move[1]+y))] -= 1

        for x,y in self.MOVE:
            if(self.value[move[0]+x+1, move[1]+y+1] == self.nextPlayer):
                self.merge(move, (move[0]+x, move[1]+y))

        if self.degre[self.getParent(move)] == 0:
            self.destroy(move)

        self.round +=1
        if self.round == self.maxturn:
            raise Exception("Vous avez vraiment joué si longtemps ? --'")
        
        self.nextPlayer *=-1

        

        
    def decreaseDegre(self, coord):
        self.degre[self.getParent(coord)] -= 1
        if self.degre[self.getParent(coord)] == 0:
            self.destroy(coord)


    def destroy(self, coord):
        print("distroille : ", coord)
        self.parent[coord] = [-1,-1]
        self.degre[coord] = 0
        self.value[coord[0]+1, coord[1]+1] = self.EMPTY
        for x,y in self.MOVE:
            if(self.value[coord[0]+x+1, coord[1]+y+1] == self.value[coord[0]+1, coord[1]+1] * -1):
                self.degre[self.getParent((move[0]+x, move[1]+y))] += 1
                
            elif(self.value[coord[0]+x+1, coord[1]+y+1] == self.value[coord[0]+1, coord[1]+1]):
                self.destroy((move[0]+x, move[1]+y))


    def getParent(self, coord):
        print("recur : ", coord)
        if self.parent[coord][0] == -1 and self.parent[coord][1] == -1:
            return coord
        parcoord = self.getParent((self.parent[coord][0], self.parent[coord][1]))
        print("testparent ", self.parent[coord], " ", parcoord)
        self.parent[coord][0] = parcoord[0]
        self.parent[coord][1] = parcoord[1]
        return parcoord


    def merge(self, coord1, coord2):
        self.degre[self.getParent(coord2)] += self.degre[self.getParent(coord1)]
        self.parent[self.getParent(coord1)] = self.getParent(coord2) 
        

    def clone(self):
        toret = Board(n)
        toret.value = np.copy(self.value)
        toret.parent = np.copy(self.parent)
        toret.degre = np.Copy(self.degre)
        toret.nextPlayer = self.nextPlayer
        toret.passRound = self.passRound
        toret.n = self.n
        toret.round = self.round




