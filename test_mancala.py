#!/usr/bin/env python3

from mancala import new_player, move, to_display, is_game_over, choose_move, \
  repeating_moves, all_moves
from unittest import TestCase, main

class TestMove(TestCase):
  def test_empty_cup(self):
    self.assertEqual((((4,4,0,4,4,4),0), new_player, True),
                     move(2,((4,4,0,4,4,4),0), new_player))

  def test_not_your_cup_low(self):
    self.assertEqual((new_player, new_player, True),
                     move(-1, new_player, new_player))

  def test_not_your_cup_high(self):
    self.assertEqual((new_player, new_player, True),
                     move(8, new_player, new_player))

  def test_before_home(self):
    self.assertEqual((((4,0,5,5,5,5),0),((4,4,4,4,4,4),0),False),
                     move(1, new_player, new_player))

  def test_home(self):
    self.assertEqual((((4,4,0,5,5,5),1),((4,4,4,4,4,4),0),True),
                     move(2, new_player, new_player))

  def test_passed_home(self):
    b = [4,4,6,4,4,4,0,4,4,4,4,4,4,0]
    self.assertEqual((((4,4,0,5,5,5),1),((5,5,4,4,4,4),0),False),
                     move(2, ((4,4,6,4,4,4),0), new_player))

  def test_passed_opponent_home_move(self):
    b = [4,4,12,4,4,4,0,4,4,4,4,4,4,0]
    self.assertEqual((((5,5,0,5,5,5),1),((5,5,5,5,5,5),0),False),
                     move(2, ((4,4,12,4,4,4),0), new_player))

  def test_empty_cup_steal(self):
    b = [4,4,4,4,4,0,0,4,4,4,4,4,4,0]
    self.assertEqual((((4,0,5,5,5,0),5),((0,4,4,4,4,4),0),False),
                     move(1, ((4,4,4,4,4,0),0),new_player))


class TestIsGameOver(TestCase):
  def test_game_not_over(self):
    self.assertFalse(is_game_over(new_player, 
                                          new_player))

  def test_game_over_me(self):
    self.assertTrue(is_game_over(((0,0,0,0,0,0),10),((1,0,0,0,0,0),12)))

  def test_game_over_you(self):
    self.assertTrue(is_game_over(((0,0,0,1,0,0),10),((0,0,0,0,0,0),12)))


class TestToDisplay(TestCase):
  def test_to_display(self):
    self.assertEqual(['\t12\t11\t10\t9\t8\t7',
                      '20\t\t\t\t\t\t\t10',
                      '\t1\t2\t3\t4\t5\t6'],
                     to_display(((1,2,3,4,5,6),10),
                                        ((7,8,9,10,11,12),20)))


class TestAllMoves(TestCase):
  def test_one_valid_move(self):
    self.assertEqual([[3]], all_moves(((0,0,0,1,0,0),0),
                                            new_player))

  def test_one_scoring_move(self):
    self.assertEqual([[0],[3],[4]], all_moves(((1,0,0,4,1,0),0),
                                            ((0,0,0,0,0,1),0)))

  def test_two_scoring_moves(self):
    self.assertEqual([[0],[3],[5]], all_moves(((1,0,0,4,0,2),0),
                                            new_player))

  def test_repeating_move(self):
    self.assertEqual([[0],
                      [3,0],
                      [3,4],
                      [3,5],
                      [4, 0],
                      [4, 3, 0],
                      [4, 3, 4],
                      [4, 3, 5],
                      [4, 5],
                      [5, 0],
                      [5, 3, 0],
                      [5, 3, 4],
                      [5, 3, 5, 0],
                      [5, 3, 5, 4],
                      [5, 4, 0],
                      [5, 4, 3, 0],
                      [5, 4, 3, 4],
                      [5, 4, 3, 5],
                      [5, 4, 5, 0],
                      [5, 4, 5, 3, 0],
                      [5, 4, 5, 3, 4],
                      [5, 4, 5, 3, 5, 0],
                      [5, 4, 5, 3, 5, 4]],
                     all_moves(((1,0,0,3,2,1),0),
                                          ((0,0,0,0,0,1),0)))


class TestChooseMove(TestCase):
  def test_one_valid_move(self):
    self.assertEqual(3, choose_move(((0,0,0,1,0,0),0),
                                            new_player))

  def test_one_scoring_move(self):
    self.assertEqual(3, choose_move(((1,0,0,4,1,0),0),
                                            ((0,0,0,0,0,1),0)))

  def test_two_scoring_moves(self):
    self.assertEqual(4, choose_move(((1,0,0,4,1,0),0),
                                            new_player))

  def test_repeating_move(self):
    self.assertEqual([5,4,5,3,5],
                     choose_move(((1,0,0,3,2,1),0),
                                          ((0,0,0,0,0,1),0)))


class TestRepeatMovePossible(TestCase):
  def test_no_repeating_move(self):
    self.assertEqual([],
                     repeating_moves((1,2,3,4,5,6)))

  def test_single_repeating_move(self):
    self.assertEqual([5],
                     repeating_moves((0,0,0,0,0,1)))
    self.assertEqual([4],
                     repeating_moves((0,0,0,0,2,0)))
    self.assertEqual([3],
                     repeating_moves((0,0,0,3,0,0)))
    self.assertEqual([2],
                     repeating_moves((0,0,4,0,0,0)))
    self.assertEqual([1],
                     repeating_moves((0,5,0,0,0,0)))
    self.assertEqual([0],
                     repeating_moves((6,0,0,0,0,0)))

if __name__ == '__main__':
  main()
