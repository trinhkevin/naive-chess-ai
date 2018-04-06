#!/usr/bin/env python3

'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

DATAFILE = '../data/games.json'

import json
import chessboard


class stateNode:
  def __init__(self, board):
    self.visits = 0
    self.value = 0
    self.board = board
    self.children = set()
    self.terminalValue = 0
    self.terminal = False
    self.turn = 0
  def createChildren(self):
    ###
  def bestChild(self):
    ###
  def UCB_sample(self):
    ###
  def playout(self):
    ###
  def update_value(self, winner):
    ###



def monte_carlo(board):
  #select

  #expand

  #simulate

  #backup

def MCTS(state):
  state.visits = state.visits + 1
  if (state.terminal):
    return
  if (len(state.children) == 0):
    state.createChildren()
  for child in state.children:
    if(child.visits == 0):
      child.visits = 1
      child.value = 0
      winner = child.playout()
  next_state = state.UCB_sample()
  winner = MCTS(next_state)
      #expand 
      #break
  



if __name__ == '__main__':
  games = json.load(open(DATAFILE))
  c = chessboard.Chessboard()
  print(c)
  print()
  for move in games[1]["moves"]:
    c.move(move)
    print(c)
    print()