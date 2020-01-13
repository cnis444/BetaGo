import numpy as np

class Board(object):
    BLACK = 1
    WHITE = -1
    EMPTY = 0
    BORDER = 2

    def __init__(self, n):
        self.value = np.zeros((n+2,n+2), dtype=int)
        self.value[0,:] = self.value[-1,:] = self.value[:,0] = self.value[:,-1] = BORDER
        self.parent = np.ones((n,n,2), dtype=int) * -1
        self.degre = np.zeros((n,n), dtype=int)
        self.nextPlayer = BLACK
        self.passRound = 0
        self.n = n
        self.round = 0

    
    def play(self, move):
        """ move = (x, y)  """
        if move == (-1,-1):
            self.passRound += 1
            if self.passRound == 2:
                raise Exception("OUI!!!! la partie est finie")
            self.nextPlayer *=-1
            return
        self.passRound = 0;
        move = (move[0]+1, move[1]+1)
        if(self.value[move] != EMPTY):
            raise Exception("Les règles sont pourtant simples !!!")

        self.value[move] = self.nextPlayer;

        for x,y in [(1,0), (0,1), (-1,0), (0,-1)]:
            if(self.value[move[0]+x, move[1]+y] == self.nextPlayer * -1):
                pass
            


    def destroy(self, coord):
        pass

    def getParent(self, coord):
        pass

    def merge(self, coord1, coord2):
        pass

    def clone(self):
        toret = Board(n)
        toret.value = np.copy(self.value)
        toret.parent = np.copy(self.parent)
        toret.degre = np.Copy(self.degre)
        toret.nextPlayer = self.nextPlayer
        toret.passRound = self.passRound
        toret.n = self.n
        toret.round = self.round




