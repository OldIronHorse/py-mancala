#!/usr/bin/env python3

from mancala import new_player, is_game_over, to_display, move, choose_move_max_score, \
  score

if __name__ == '__main__':
  player = new_player
  computer = new_player
  while not is_game_over(player, computer):
    print()
    for line in to_display(player, computer):
      print(line)
    print('\t(1)\t(2)\t(3)\t(4)\t(5)\t(6)')
    player_move_seq=choose_move_max_score(player,computer)
    print("Player one's move(s):{}".format([cup+1 for cup in player_move_seq]))
    for cup in player_move_seq:
      player, computer, again = move(cup, player, computer)
    if is_game_over(player, computer):
      break
    computer_move_seq=choose_move_max_score(computer, player)
    print(computer, player, computer_move_seq)
    print("Player two's move(s):{}".format([cup+1 for cup in computer_move_seq]))
    for cup in computer_move_seq:
      print('\t(6)\t(5)\t(4)\t(3)\t(2)\t(1)')
      for line in to_display(player, computer):
        print(line)
      computer, player, again=move(cup, computer, player)
  print("Game over")
  for line in to_display(player, computer):
    print(line)
  player_score = score(player)
  computer_score = score(computer)
  if player_score == computer_score:
    print("It's draw!")
  else:
    print( "Player {0} won [{1}:{2}]".format(
                                    'one' if player_score > computer_score 
                                          else 'two',
                                    player_score, computer_score))
