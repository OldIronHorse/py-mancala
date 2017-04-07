#!/usr/bin/env python3

from flask import Flask, jsonify, request
import logging
from mancala import new_game, move, choose_move_max_score, is_game_over

app=Flask(__name__)

all_games={}
last_game_index=0

@app.route('/games', methods=['GET', 'POST'])
def games():
  app.logger.debug('/games: %s', request)
  if request.method=='POST':
    global last_game_index
    last_game_index+=1;
    all_games[last_game_index]=new_game
    response={'status':'OK', 'id':last_game_index}
  elif request.method=='GET':
    response={'status':'OK', 'games':all_games}
  app.logger.debug('/games: %s', response)
  return jsonify(response)

@app.route('/games/<game_id>', methods=['GET'])
def games_by_id(game_id):
  app.logger.debug('/games/%s: %s', game_id, request)
  response={'status':'OK', 'game':all_games[int(game_id)]}
  app.logger.debug('/games/%s: %s', game_id, response)
  return jsonify(response)

@app.route('/games/<game_id>/move', methods=['PUT'])
def games_move(game_id):
  app.logger.debug('/games/%s/move: %s', game_id, request)
  app.logger.debug(request.get_json())
  game_id=int(game_id)
  player, computer=all_games[game_id]
  new_player, new_computer, again=move(request.get_json()['cup'],
                                       player, computer)
  if again or is_game_over(new_player, new_computer):
    all_games[game_id]=(new_player, new_computer)
    response={'status':'OK',
              'game_id':game_id,
              'game':all_games[game_id]}
  else:
    app.logger.debug("/games/%s/move: computers's turn...", game_id)
    moves=choose_move_max_score(new_computer, new_player)
    for cup in moves:
      new_computer, new_player, again=move(cup, new_computer, new_player)
    all_games[game_id]=(new_player, new_computer)
    response={'status':'OK',
              'game_id':game_id,
              'computer_moves':moves,
              'game':all_games[game_id]}
  if is_game_over(new_player, new_computer):
    response['status']='GAME_OVER'
  app.logger.debug('/games/%s/move: %s %s', game_id, response)
  return jsonify(response)

if __name__=='__main__':
  handler=logging.StreamHandler()
  handler.setLevel(logging.DEBUG)
  app.logger.addHandler(handler)
  app.logger.setLevel(logging.DEBUG)
  app.run()
