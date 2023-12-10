#!/usr/bin/python

import sys
import json
import socket

# get_score(player, board)
# player - identifier for player
# board - board state being examined
# ---------------------------------------
# Produces the difference in score between players with current board state
def get_score(player, board):
  opp = 0
  if player == 1:
    opp = 2
  else:
    opp = 1

  pScore = 0
  oppScore = 0
  for i in range(8):
    for j in range(8):
      if board[i][j] == player:
        pScore += 1
      elif board[i][j] == opp:
        oppScore += 1
  
  return pScore - oppScore


# get_move_list(player, board)
# player - identifier for player
# board - board state being examined
# -------------------------------------
# gets list of possible moves for player with a board state
def get_move_list(player, board):
  opp = 0
  if player == 1:
    opp = 2
  else:
    opp = 1

  moves = {}
  for i in range(8): # Finds played tiles of player and checks for flanks
    for j in range(8):
      if board[i][j] == player:
        if i <=6 and board[i+1][j] == opp: # checks down
          k = i+2
          while k <= 7:
            if (board[k][j] == player):
              break
            if (board[k][j] == 0):
              if (k, j) in moves:
                moves[(k, j)] += 1
              else:
                moves[(k, j)] = 1
              break
            k += 1
        if i >= 1 and board[i-1][j] == opp: # checks up
          k = i-2
          while k >= 0:
            if (board[k][j] == player):
              break
            if (board[k][j] == 0):
              if (k, j) in moves:
                moves[(k, j)] += 1
              else:
                moves[(k, j)] = 1
              break
            k -= 1
        if j <= 6 and board[i][j+1] == opp: # checks right
          k = j+2
          while k <= 7:
            if (board[i][k] == player):
              break
            if (board[i][k] == 0):
              if (i, k) in moves:
                moves[(i, k)] += 1
              else:
                moves[(i, k)] = 1
              break
            k += 1
        if j >= 1 and board[i][j-1] == opp: # checks left
          k = j-2
          while k >= 0:
            if (board[i][k] == player):
              break
            if (board[i][k] == 0):
              if (i, k) in moves:
                moves[(i, k)] += 1
              else:
                moves[(i, k)] = 1
              break
            k -= 1
        if i <= 6 and j <= 6 and board[i+1][j+1] == opp: # checks down right
          k = i+2
          t = j+2
          while k <= 7 and t <= 7:
            if (board[k][t] == player):
              break
            if (board[k][t] == 0):
              if (k, t) in moves:
                moves[(k, t)] += 1
              else:
                moves[(k, t)] = 1
              break
            k += 1
            t += 1
        if i >= 1 and j <= 6 and board[i-1][j+1] == opp: # checks up right
          k = i-2
          t = j+2
          while k >= 0 and t <= 7:
            if (board[k][t] == player):
              break
            if (board[k][t] == 0):
              if (k, t) in moves:
                moves[(k, t)] += 1
              else:
                moves[(k, t)] = 1
              break
            k -= 1
            t += 1
        if i <= 6 and j >= 1 and board[i+1][j-1] == opp: # checks down left
          k = i+2
          t = j-2
          while k <= 7 and t >= 0:
            if (board[k][t] == player):
              break
            if (board[k][t] == 0):
              if (k, t) in moves:
                moves[(k, t)] += 1
              else:
                moves[(k, t)] = 1
              break
            k += 1
            t -= 1
        if i >= 1 and j >= 1 and board[i-1][j-1] == opp: # checks up left
          k = i-2
          t = j-2
          while k >= 0 and t >= 0:
            if (board[k][t] == player):
              break
            if (board[k][t] == 0):
              if (k, t) in moves:
                moves[(k, t)] += 1
              else:
                moves[(k, t)] = 1
              break
            k -= 1
            t -= 1
  return moves


# flips_possible(player, board, move, d, opp)
# player - current player who has flips being examined
# board - board state being examined
# move - the move from which flanks are checked from
# d - x and y value to indicate which direction is being checked for flips
# opp - opposing player identifier
# ---------------------------------------------------------
# checks for possible flips with move
def flips_possible(player, board, move, d, opp):
  if move[0] <= 7 and move[0] >= 0 and move[1] <= 7 and move[1] >= 0:
    if board[move[0]][move[1]] == opp:
      x = move[0]
      y = move[1]
      while x >= 1 and x <= 6 and y >= 1 and y <= 6:
        x += d[0]
        y += d[1]
        if (board[x][y] == 0): # checks for gaps
          return False
        if (board[x][y] == player): # checks for flanking player piece
          return True
  return False


# flips(player, board, move, d, opp)
# player - current player identifier
# board - current board state being examined
# move - location that flipped tiles start from
# d - direction indicator for x and y axis to flip tokens
# opp - identifier for opponent of player
# ------------------------------------------------------
# makes flips and returns the new board
def flips(player, board, move, d, opp):
  x = move[0]
  y = move[1]
  while board[x][y] == opp:
    board[x][y] == player
    x += d[0]
    y += d[1]
  
  return board


# make_move(player, board, move)
# player - identifier for player
# board - current board state being examined
# move - current move being made by player on the board
# ------------------------------------------------------
# makes move and changes board accordingly
def make_move(player, board, move):
  x = move[0]
  y = move[1]
  
  board[x][y] = player
  opp = 0
  if player == 1:
    opp = 2
  else:
    opp = 1

  if flips_possible(player, board, [x+1,y], [1,0], opp): # down
    board = flips(player, board, [x+1,y], [1,0], opp)
  if flips_possible(player, board, [x-1,y], [-1,0], opp): # up
    board = flips(player, board, [x-1,y], [-1,0], opp)
  if flips_possible(player, board, [x,y+1], [0,1], opp): # left
    board = flips(player, board, [x,y+1], [0,1], opp)
  if flips_possible(player, board, [x,y-1], [0,-1], opp): # right
    board = flips(player, board, [x,y-1], [0,-1], opp)
  if flips_possible(player, board, [x-1,y-1], [-1,-1], opp): # up left
    board = flips(player, board, [x-1,y-1], [-1,-1], opp)
  if flips_possible(player, board, [x-1,y+1], [-1,1], opp): # up right
    board = flips(player, board, [x-1,y+1], [-1,1], opp)
  if flips_possible(player, board, [x+1,y-1], [1,-1], opp): # down left
    board = flips(player, board, [x+1,y-1], [1,-1], opp)
  if flips_possible(player, board, [x+1,y+1], [1,1], opp): # down right
    board = flips(player, board, [x+1,y+1], [1,1], opp)

  return board


# game_over(board)
# board - board state being examined
# -----------------------------------------------------------
# determines if there is any more moves to make in the game (i.e. when the game over state is reached)
def game_over(board):
  pList = get_move_list(1, board)
  oList = get_move_list(2, board)
  if len(pList) == 0 and len(oList) == 0:
    return True
  return False


# minimax_val(player, board, curTurn, search)
# player - player whos turn it was at the beginning of the minimax_val call
# board - current board state being examined
# curTurn - indicator for current player turn within the minimax iterations
# search - how deep the current minimax search has gone (starts at 1, ends at 5)
# ------------------------------------------------------------
# finds best move based off val from current board state, looking search value deep
def minimax_val(player, board, curTurn, search):
  opp = 0
  if curTurn == 1:
    opp = 2
  else:
    opp = 1
  
  if search == 5 or game_over(board):
    return get_score(player, board)
  
  moves = get_move_list(curTurn, board)
  movesCount = len(moves)
  movesList = list(moves.keys())

  if movesCount == 0:
    return minimax_val(player, board, opp, search + 1)
  else:
    bestMoveVal = -9999999999
    if player != curTurn:
      bestMoveVal == 999999
    for i in movesList:
      tempBoard = board
      tempBoard = make_move(curTurn, tempBoard, [i[0], i[1]])
      val = minimax_val(player, tempBoard, opp, search+1)

      if player == curTurn:
        if val > bestMoveVal:
          bestMoveVal = val
      else:
        if val < bestMoveVal:
          bestMoveVal = val
    return bestMoveVal


# get_move_minimax(player, board)
# player - current player indicator
# board - current board state being examined
# ------------------------------------------------------------
# takes in current player and board state and uses minimax to determine opt move
def get_move_minimax(player, board):
  movesCount = 0
  opp = 0
  if player == 1:
    opp = 2
  else:
    opp = 1

  moves = get_move_list(player, board)
  movesList = list(moves.keys())
  movesCount = len(moves)

  if movesCount == 0:
    return [-1, -1]
  else:
    bestMoveVal = -9999999999
    bestMove = [movesList[0][0], movesList[0][1]]
    for i in movesList:
      tempBoard = board
      tempBoard = make_move(player, tempBoard, [i[0], i[1]])

      val = minimax_val(player, tempBoard, opp, 1)
      if val > bestMoveVal:
        bestMoveVal = val
        bestMove = [i[0], i[1]]

    return bestMove


# get_move(player, board)
# player - current player having move checked
# board - current board state being examined
# ------------------------------------------------------
# Returns move for player to take
# THIS FUNCTION WAS USED INITIALLY BEFORE REPLACED BY MINIMAX IMPLEMENTATION
# Aspects of this initial implementaion can be found throughout the minimax implementation
# such as get_move_list() function

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move_minimax(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
