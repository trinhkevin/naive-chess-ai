#!/usr/bin/env python3

'''
  Chess board class
  Andrew Callahan, Anthony Luc, Kevin Trinh
  Machine Learning
  03/22/2018
'''

import chess
from bitarray import bitarray

'''
will use this later for visual representation of board
import chess.pgn
'''

#p1piece -> 8x8x6
#p2piece -> ''
#repetitions -> 8x8x2
#turn -> 1
#p1 castling -> 2
#p2 castling -> 2
#no-progress -> 50

#951 total bits (neurons)

class Chessboard(object):
  def __init__(self):
    self.board = chess.Board()
    self.netinputs = bitarray(951)
    
  def __str__(self):
    return str(self.board)

  def move(self, _move):
    self.board.push_san(_move)

  def checkmate(self):
    return self.board.is_game_over()

  def stalemate(self):
    return self.board.is_stalemate()

  def draw(self):
    return self.board.is_insufficient_material()

  def check(self):
    return self.board.is_check()

  def getNetInputs(self):
    return self.netinputs

  def turns(self):
    s = []
    while True:
      try:
        move = self.board.pop()
      except IndexError:
        break
      s.append(move)
    t = []
    while len(s) > 0:
      t.append(self.board.copy())
      move = s.pop()
      self.board.push(move)
    return t

  def genInputBits(self):
    index = 0
    for p in ['P', 'R' , 'N' ,'B', 'Q' ,'K', 'p' , 'r' , 'n' , 'b' , 'q' ,'k']:
      for i in range(64):
        if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
          self.netinputs[index] = True
        else:
          self.netinputs[index] = False
        index += 1
   
    for i in range(128):
      self.netinputs[index + i] = False

    index += 128 # skipping repetitions for now
    
    self.netinputs[index] = self.board.turn
    index += 1
    self.netinputs[index] = self.board.has_kingside_castling_rights(chess.WHITE)
    index += 1
    self.netinputs[index] = self.board.has_queenside_castling_rights(chess.WHITE)
    index += 1
    self.netinputs[index] = self.board.has_kingside_castling_rights(chess.BLACK)
    index += 1
    self.netinputs[index] = self.board.has_queenside_castling_rights(chess.BLACK)
    index += 1
    # check this
    self.netinputs[index] = self.board.can_claim_fifty_moves()
    index += 1
    
    for i in range(50):
      self.netinputs[index + i] = 0
      #somehow figure this out?
    
if __name__ == '__main__':
  c = Chessboard()
  c.move("e4")
  c.move("e5")
  c.move("Qh5")
  c.move("Nc6")
  c.move("Bc4")
  c.move("Nf6")
  c.move("Qxf7")
  for i in c.turns():
    print(i)

  '''
  c.geninputbits()
  print(c)
  print(c.getinputbits())
  '''