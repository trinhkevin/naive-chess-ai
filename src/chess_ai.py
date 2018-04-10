#!/usr/bin/env python3




'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	04/05/2018
'''

# https://python-chess.readthedocs.io/en/v0.23.0/core.html


DATAFILE = '../data/games.json'
C = 1.41
ITERATIONS = 500

import json
import chessboard
import math
import random
import copy


class AI:
  def __init__(self, board):
    self.tree =StateNode(board)

  def monteCarlo(self):
    for i in range(ITERATIONS):
      MCTS(self.tree)
    '''
    curr = root
    while len(curr.children):
      print(curr.getBestChild().move)
      curr = curr.getBestChild()
    '''
    result = self.tree.getBestChild()
    self.tree = result
    return self.tree
class StateNode:
  def __init__(self, board, move=None):
    self.visits = 0
    self.value = 0
    self.board = board
    self.children = set()
    self.turn = self.board.getTurn()
    self.move = move

  def isTerminal(self):
    return self.board.board.is_game_over()

  def terminalValue(self):
    if self.board.board.result() == '1/2-1/2':
      return 0
    elif self.board.board.result() == '1-0':
      return 1
    elif self.board.board.result() == '0-1':
      return -1
    else:
      print('Error: invalid terminal')
      exit(1)

  def createChildren(self):

    for move in self.board.getLegalMoves():
      board = copy.deepcopy(self.board)
      board.move_uci(move)
      child = StateNode(board, move)
      self.children.add(child)
   
  def getBestChild(self):
    '''
    # If there are no possible children,
    # set the node terminal and give it a value
    if len(self.children) == 0:
      self.terminal = True
      if self.board.is_stalemate():
        self.terminalValue = 0
      else:
        # White's turn, so white lost
        if self.board.getTurn():
          self.terminalValue = -1
        # Black's turn, so black lost
        else:
          self.terminalValue = 1
      return None
    '''

    # Else, find the best child
    bestChild = None
    for child in self.children:
      if bestChild is None or child.value / child.visits > bestChild.value / bestChild.visits:
        bestChild = child;
    return bestChild

  def UCB_sample(self):
    result = None
    resultUCB = None
    for child in self.children:
      candidateUCB = UCB(child.value/child.visits, self.visits, child.visits)
      if result is None or candidateUCB > resultUCB:
        result = child
        resultUCB = candidateUCB
    return result

  def playout(self):
    testBoard = self.board.copy()
    while testBoard.result() == '*':
      legalMoves = [x for x in testBoard.legal_moves]
      if not len(legalMoves):
        break
      move = legalMoves[random.randint(0, len(legalMoves) - 1)]
      testBoard.push(move)
    if testBoard.is_stalemate():
      return 0
    elif testBoard.is_game_over():
      return -1 if testBoard.turn else 1
    return 0
    if testBoard.result() == '1/2-1/2':
      return 0
    else:
      return -1 if testBoard.result() == '0-1' else 1

  def updateValue(self, winner):
    if winner == 0:
      self.value += 0.5
    if self.turn:
      if winner == 1:
        self.value += 1
    else:
      if winner == -1:
        self.value +=1

def UCB(v, N, n_i):
  return v + C * math.sqrt(math.log(N)/n_i)

def monteCarlo(chessboard):
  root = StateNode(chessboard)
  for i in range(ITERATIONS):
    MCTS(root)
  return root.getBestChild()

def MCTS(state):
  if state.isTerminal():
    return state.terminalValue()
  state.visits += 1
  if len(state.children) == 0:
    state.createChildren()
  for child in state.children:
    if child.visits == 0:
      child.visits = 1
      child.value = 0
      winner = child.playout()
      child.updateValue(winner)
      state.updateValue(winner)
      return winner
  next_state = state.UCB_sample()
  winner = MCTS(next_state)
  state.updateValue(winner)
  return winner

if __name__ == '__main__':
  c = chessboard.Chessboard()
  c.move('g2g4')
  c.move('a7a6')
  c.move('c2c4')
  c.move('e7e6')
  c.move('f2f4')
  ai = AI(c)
  for i in range(0, 100):
    print(ai.monteCarlo().move)
