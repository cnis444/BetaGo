from go import Board
from math import sqrt, log
import random as rd

#maxpumperla github

explorationParameter = sqrt(2)

class Node(object):

    def __init__(self, board, p, tt, parent, move, isFinal, winner=None):
        self.board = board
        self.tt = tt
        self.p = p
        self.fils = {}
        self.parent = parent
        self.move = move
        self.isFinal = isFinal
        self.winner = winner
        

    def Backpropagation(self, p, tt):
        self.p = (self.p * self.tt + p *tt) / (self.tt + tt)
        self.tt = self.tt  + tt
        if self.parent is not None:
            self.parent.Backpropagation(p, tt)

    def Best(self):
        best = 0
        m = (-1,-1)
        for key in self.fils:
            if self.fils[key].p > best:
                best = self.fils[key].p
                m = self.fils[key].move
        return m
        
    def Expension(self):
        if self.isFinal:
            return
        for m in self.board.legal_move():
            b = self.board.clone()
            try:
                b.play(m)
                n = Node(b, 0,0,self, m, False)
            except GameEndedException as e:
                n = Node(b, 0,0,self, m, True, e.winner)
                
            self.fils[m] = n


class MonteCarlo(object):
    
    def __init__(self, board, NN):
        self.board = board
        self.root = Node(board, 0, 0, None, False)
        self.root.Expension()
        self.NN = NN

    def Search(self, nbExpension):
        for i in range(nbExpension):
            n = self.Selection(self.root)
            n.Expension()
            tt, p = self.Evaluate(n)
            n.Backpropagation(p, tt)
        return self.root.Best()


    def Selection(self, node):
        proba = self.NN.predict(node.board.reprNN())[0]
        mv = np.random.choice(node.board.index, 1, p =proba.flatten())
        if len(node.fils[mv].fils) == 0:
            return node.fils[mv]
        else :
            return self.Selection(node.fils[mv])


    def Evaluate(self, node):
        if node.isFinal:
            return 1,1 if node.winner ==  self.board.nextPlayer else 0
        return 1, self.NN.predict(node.board.reprNN())[1]
#TODO swap le board en faisant *-1




