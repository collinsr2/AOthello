#!/usr/bin/python

import sys
import json
import socket

def get_move(player, board):
  opp = 0
  if player == 1:
    opp = 2
  else:
    opp = 1
  
  # TODO determine valid moves
  moves = {}
  for i in range(8): # Finds played tiles of player and checks for flanks
    for j in range(8):
      if board[i][j] == player:
        if i <=6 and board[i+1][j] == opp: # down
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
        if i >= 1 and board[i-1][j] == opp: # up
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
        if j <= 6 and board[i][j+1] == opp: # right
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
        if j >= 1 and board[i][j-1] == opp: # left
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
        if i <= 6 and j <= 6 and board[i+1][j+1] == opp: #down right
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
        if i >= 1 and j <= 6 and board[i-1][j+1] == opp: # up right
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
        if i <= 6 and j >= 1 and board[i+1][j-1] == opp: # down left
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
        if i >= 1 and j >= 1 and board[i-1][j-1] == opp: # up left
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

  # TODO determine best move
  best = ()
  if len(moves) == 0: # if player has no valid moves
    return best
  else:
    bestC = 0
    for i in moves:
      if moves[i] > bestC:
        bestC == moves[i]
        best = i
  
  return [best[0], best[1]]

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

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
