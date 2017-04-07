#!/usr/local/bin/python3

import operator
import itertools

class NotYourCup(Exception):
  pass

new_player=((4,4,4,4,4,4),0)
new_game=(new_player, new_player)

def repeating_moves(cups):
  moves=[]
  cup=0
  for counters in cups:
    if 6-cup==counters:
      moves.append(cup)
    cup+=1
  return moves

def move(cup, mine, yours):
  my_cups, my_home = mine
  your_cups, your_home = yours
  if cup < 0 or cup > 5 or my_cups[cup] == 0:
    return ((my_cups, my_home), (your_cups, your_home), True)
  stones = my_cups[cup]
  offset = cup + 1
  board = list(my_cups) + [my_home] + list(your_cups)
  board[cup] = 0
  masks = []
  while stones > 0:
    m, stones = get_mask(stones, offset, len(board))
    offset = 0
    masks.append(m)
  for m in masks:
    board = [operator.add(a, b) for a, b in zip(board, m)]
  again = m[6] == 1 and m[7] == 0
  if not again:
    last = 12 - len(list(itertools.takewhile(lambda a: a == 0, reversed(m))))
    if last > -1 and last < 6 and board[last] == 1 and board[12 - last] > 0:
      board[6] += board[last]
      board[last] = 0
      board[6] += board[12 - last]
      board[12 - last] = 0
  return ((tuple(board[:6]), board[6]), (tuple(board[7:]), your_home), again)

def get_mask(stones, offset, size):
  laying = min(stones, size - offset)
  return ([0] * offset + [1] * laying + [0] * (size - laying - offset),
          stones - laying)

def steal(board, player, i):
  if board[i] == 1 and i in player_cups[player] and board[opposite[i]] > 0:
    board[home_index[player]] = board[home_index[player]] + 1 + \
                                board[opposite[i]]
    board[i] = 0
    board[opposite[i]] = 0

def is_game_over(mine, yours):
  my_cups, my_home = mine
  your_cups, your_home = yours
  return all(map(lambda stones: stones == 0, my_cups)) or \
         all(map(lambda stones: stones == 0, your_cups))

def to_display(mine, yours):
  my_cups, my_home = mine
  your_cups, your_home = yours
  return ['\t{5}\t{4}\t{3}\t{2}\t{1}\t{0}'.format(*your_cups),
          '{0}\t\t\t\t\t\t\t{1}'.format(your_home, my_home),
          '\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(*my_cups)]

def score(player):
  cups, home = player
  return sum(cups) + home

def all_moves(mine, yours):
  my_cups, my_home = mine
  result_moves=[]
  valid_moves = [cup for cup in range(0, 6) if my_cups[cup] > 0]
  for m in valid_moves:
    new_mine, new_yours, again=move(m, mine, yours)
    if again:
      result_moves+=[([m]+seq, home) for seq, home in all_moves(new_mine, new_yours)]
    else:
      result_cups, result_home=new_mine
      result_moves.append(([m],(new_mine, new_yours)))
  return result_moves
  
def choose_move_max_score(mine, yours):
  """Return the move that maximises my_home after this turn"""
  move_seqs=all_moves(mine, yours)
  best_home=-1
  best_move_seq=None
  for seq, ((cups,home), yours)  in move_seqs:
    if home>=best_home:
      best_move_seq=seq
      best_home=home
  #TODO tie-break for equal scores?
  return best_move_seq

def choose_move_hoarder(mine, yours):
  '''Maximise the counters in my cups and home'''
  move_seqs=all_moves(mine, yours)
  best_total=-1
  best_move_seq=None
  for seq, ((cups,home), yours)  in move_seqs:
    if home+sum(cups)>=best_total:
      best_move_seq=seq
      best_total=home+sum(cups)
  return best_move_seq

#TODO alternative move choosers
# random
# sniper
# hoarder
# turn hog
