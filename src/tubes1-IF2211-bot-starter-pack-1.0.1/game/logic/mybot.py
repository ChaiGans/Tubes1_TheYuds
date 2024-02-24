import random
from typing import Optional
import math

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class MyBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
    def displacement(self, currentPos: Position, targetPos: Position):
        return math.sqrt((currentPos.x-targetPos.x)**2 + (currentPos.y-targetPos.y)**2)

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        currentPos = board_bot.position
        print("DIAMOND = ", props.diamonds)
        if props.diamonds == 5:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            print("BOT GUA")
            print(board_bot.position)
            print("SEMUA BOT")
            print(board.bots)
            print("DIAMONDS")
            listJarak = []
            for diamond in board.diamonds:
                print(diamond.position)
                print("Jarak: ")
                print(self.displacement(board_bot.position,diamond.position))
                if props.diamonds == 4:
                    if diamond.properties.points != 2:
                        listJarak.append((diamond.position, self.displacement(board_bot.position,diamond.position)))
                else:
                    listJarak.append((diamond.position, self.displacement(board_bot.position,diamond.position)))
                    
            minDiamond = min(listJarak, key = lambda x: x[1])
            self.goal_position = minDiamond[0]

        delta_x, delta_y = get_direction(
            currentPos.x,
            currentPos.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y