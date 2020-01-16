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
        self.toCheck = []
        self.blackHash = np.random.randint(10000, 1000000000, size = (n,n))
        self.whiteHash = np.random.randint(10000, 1000000000, size = (n,n))
        self.hashTable = [0]
        self.modifsValue = dict()

    
    def checkMove(self, move):
        if(self.value[move[0]+1, move[1]+1] != self.EMPTY):
            score = self.calculatePoint()
            raise Exception("Les règles sont pourtant simples !!! : ")


    def hash(self):
        new = self.hashTable[-1]
        for i in self.modifsValue:
            if self.modifsValue[i] == self.BLACK:
                new ^= self.blackHash[i]
            else:
                new ^= self.whiteHash[i]
        if new in self.hashTable:
            score = self.calculatePoint()
            raise Exception("Les règles sont pourtant simples !!! : ")
        else:
            self.hashTable.append(new)


    def play(self, move):
        if move == (-1,-1):
            self.passRound += 1
            if self.passRound == 2:
                score = self.calculatePoint()
                raise Exception("OUI!!!! la partie est finie : " + str(score))
            self.nextPlayer *=-1
            self.round +=1
            return
        self.passRound = 0;
        
        self.checkMove(move)

        self.value[move[0]+1, move[1]+1] = self.nextPlayer
        self.modifsValue[move] = self.nextPlayer
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
        #if self.round == self.maxturn:
        #    score = self.calculatePoint()
        #    raise Exception("Vous avez vraiment joué si longtemps ? --' : " + str(score))
        
        self.hash()

        self.nextPlayer *=-1

        
    def decreaseDegre(self, coord):
        self.degre[self.getParent(coord)] -= 1
        if self.degre[self.getParent(coord)] == 0:
            self.destroy(coord)


    def destroy(self, coord):
        self.parent[coord] = [-1,-1]
        self.degre[coord] = 0
        tmp = self.value[coord[0]+1, coord[1]+1]
        if coord in self.modifsValue:
            del self.modifsValue[coord]
        else :
            self.modifsValue[coord] = tmp
        self.value[coord[0]+1, coord[1]+1] = self.EMPTY
        for x,y in self.MOVE:
            if(self.value[coord[0]+x+1, coord[1]+y+1] == tmp * -1):
                self.degre[self.getParent((coord[0]+x, coord[1]+y))] += 1
                
            elif(self.value[coord[0]+x+1, coord[1]+y+1] == tmp):
                self.destroy((coord[0]+x, coord[1]+y))


    def getParent(self, coord):
        if self.parent[coord][0] == -1 and self.parent[coord][1] == -1:
            return coord
        parcoord = self.getParent((self.parent[coord][0], self.parent[coord][1]))
        self.parent[coord][0] = parcoord[0]
        self.parent[coord][1] = parcoord[1]
        return parcoord


    def merge(self, coord1, coord2):
        self.degre[self.getParent(coord2)] += self.degre[self.getParent(coord1)]
        self.parent[self.getParent(coord1)] = self.getParent(coord2) 


    def explore(self, type, coord):
        #print(coord , type, self.toCheck)
        self.toCheck.remove(coord)
        toret = [type, 1]
        for x,y in self.MOVE:
            #print(coord, x, y)
            val = self.value[coord[0]+x+1, coord[1]+y+1]
            if val == self.EMPTY and (coord[0]+x, coord[1]+y) in self.toCheck:
                res = self.explore(toret[0], (coord[0]+x, coord[1]+y))
                if toret[0] is None:
                    toret[0] = res[0]
                elif toret[0] is not None and toret[0] != res[0]:
                    toret[0] = 0
                toret[1] += res[1]
            elif val != self.EMPTY:
                if val == self.BORDER:
                    continue
                if toret[0] is None:
                    toret[0] = val
                elif toret[0] is not None and val != toret[0]:
                    toret[0] = 0
            #print(coord, toret)
        return toret


    def calculatePoint(self):
        point = [0,0]
        for x in range(self.n):
            for y in range(self.n):
                val = self.value[x+1,y+1]
                if val == self.EMPTY:
                    self.toCheck.append((x,y))
                elif val == self.BLACK:
                    point[0] +=1
                elif val == self.WHITE:
                    point[1] += 1
        while(len(self.toCheck) > 0):
            pos = self.toCheck[0]
            res = self.explore(None, pos)
            if res[0] == self.BLACK:
                point[0] += res[1]
            elif res[0] == self.WHITE:
                point[1] += res[1]
        return point


    def clone(self):
        toret = Board(n)
        toret.value = np.copy(self.value)
        toret.parent = np.copy(self.parent)
        toret.degre = np.Copy(self.degre)
        toret.nextPlayer = self.nextPlayer
        toret.passRound = self.passRound
        toret.n = self.n
        toret.round = self.round