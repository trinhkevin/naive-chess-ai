#!/usr/bin/env python3

'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

DATAFILE = '../data/data.json'

import json

if __name__ == '__main__':
	games = json.load(open(DATAFILE))