import numpy as np



BLACK = 1
WHITE = -1
EMPTY = 0
BORDER = 2



class InvalideMoveException(Exception) :


    def __init__(self, winner, message):
        self.winner = winner
        self.message = message


    def __str__(self):
        winner = "blanc." if self.winner == WHITE else "noire."
        return "Les règles sont pourtant simples !!! " + self.message + " Le vainqueur est le joueur " + winner



class GameEndedException(Exception) :


    def __init__(self, scores, message):
        self.scores = scores
        self.message = message
        if self.scores[WHITE] > self.scores[BLACK]:
            self.winner = WHITE  
        elif self.scores[WHITE] < self.scores[BLACK]:
            self.winner = BLACK
        else:
            self.winner = EMPTY


    def __str__(self):
        if self.winner != EMPTY:
            winner = "blanc." if self.winner == WHITE else "noire."
            endMessage = " Le vainqueur est le joueur " + winner
        else:
            endMessage = "Il n'y a pas de vainqueur."
        return "La partie et finie !!! " + self.message + endMessage



class KoRuleException(InvalideMoveException) :


    def __init__(self, winner):
        return super().__init__(winner, "Il ne peut y avoir deux fois le même plateau.")



class InvalidePlacementException(InvalideMoveException) :

    def __init__(self, winner):
        return super().__init__(winner, "On doit jouer là où il n'y a pas de pierre.")



class OnGoDanException(InvalideMoveException) :


    def __init__(self, winner):
        return super().__init__(winner, "On doit jouer sur la plateau.")



class Board(object):
    

    def __init__(self, n, maxturn = None):
        self.maxturn = maxturn if maxturn is not None else 2*n*n
        self.value = np.zeros((n+2,n+2), dtype=int)
        self.value[0,:] = self.value[-1,:] = self.value[:,0] = self.value[:,-1] = BORDER
        self.parent = np.ones((n,n,2), dtype=int) * -1
        self.degre = np.zeros((n,n), dtype=int)
        self.nextPlayer = BLACK
        self.passRound = 0
        self.n = n
        self.round = 0
        self.MOVE = [(1,0), (0,1), (-1,0), (0,-1)]
        self.toCheck = []
        self.blackHash = np.random.randint(1, 1000000000, size = (n,n))
        self.whiteHash = np.random.randint(1, 1000000000, size = (n,n))
        self.hashTable = [0]
        self.modifsValue = dict()

    
    def checkMove(self, move):
        if(self.value[move[0]+1, move[1]+1] != EMPTY):
            raise InvalidePlacementException(self.nextPlayer * -1)
        if move[0] < 0 or move[0] >= self.n or move[1] < 0 or move[1] >= self.n :
            raise OnGoDanException(self.nextPlayer * -1)

    def hash(self):
        new = self.hashTable[-1]
        for i in self.modifsValue:
            if self.modifsValue[i] == BLACK:
                new ^= self.blackHash[i]
            else:
                new ^= self.whiteHash[i]
        if new in self.hashTable:
            score = self.calculatePoint()
            raise KoRuleException(self.nextPlayer * -1)
        else:
            self.hashTable.append(new)
        self.modifsValue = dict()


    def play(self, move):
        if move == (-1,-1):
            self.passRound += 1
            if self.passRound == 2:
                score = self.calculatePoint()
                raise GameEndedException(score, "")
            self.nextPlayer *=-1
            self.round +=1
            return
        self.passRound = 0;
        
        self.checkMove(move)

        self.value[move[0]+1, move[1]+1] = self.nextPlayer
        self.modifsValue[move] = self.nextPlayer
        self.degre[move] = 0
        for x,y in self.MOVE:
            if(self.value[move[0]+x+1, move[1]+y+1] == EMPTY):
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
            score = self.calculatePoint()
            raise GameEndedException(score, "Vous avez vraiment joué si longtemps ? --'")
        
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
        self.value[coord[0]+1, coord[1]+1] = EMPTY
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
        self.toCheck.remove(coord)
        toret = [type, 1]
        for x,y in self.MOVE:
            val = self.value[coord[0]+x+1, coord[1]+y+1]
            if val == EMPTY and (coord[0]+x, coord[1]+y) in self.toCheck:
                res = self.explore(toret[0], (coord[0]+x, coord[1]+y))
                if toret[0] is None:
                    toret[0] = res[0]
                elif toret[0] is not None and toret[0] != res[0]:
                    toret[0] = 0
                toret[1] += res[1]
            elif val != EMPTY:
                if val == BORDER:
                    continue
                if toret[0] is None:
                    toret[0] = val
                elif toret[0] is not None and val != toret[0]:
                    toret[0] = 0
        return toret


    def calculatePoint(self):
        point = [0,0]
        for x in range(self.n):
            for y in range(self.n):
                val = self.value[x+1,y+1]
                if val == EMPTY:
                    self.toCheck.append((x,y))
                elif val == BLACK:
                    point[0] +=1
                elif val == WHITE:
                    point[1] += 1
        while(len(self.toCheck) > 0):
            pos = self.toCheck[0]
            res = self.explore(None, pos)
            if res[0] == BLACK:
                point[0] += res[1]
            elif res[0] == WHITE:
                point[1] += res[1]
        return {BLACK: point[0], WHITE: point[1]}


    def clone(self):
        toret = Board(n)
        toret.value = np.copy(self.value)
        toret.parent = np.copy(self.parent)
        toret.degre = np.Copy(self.degre)
        toret.nextPlayer = self.nextPlayer
        toret.passRound = self.passRound
        toret.n = self.n
        toret.round = self.round