import random
from typing import Optional
import math

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals


class MyBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.is_portal_entry = False
        
    def displacement(self, current_position: Position, goal_position: Position):
        return math.sqrt((current_position.x - goal_position.x) ** 2 + (current_position.y - goal_position.y) ** 2)
    
    def is_teleporter_position (self, current_position : Position, board: Board):
        list_portal = [x for x in board.game_objects if x.type == "TeleportGameObject"]
        for portal in list_portal:
            if (position_equals(current_position, portal.position)):
                return True
        return False
    
    def is_diamond_position (self, current_position : Position, board: Board):
        list_diamond = [x for x in board.game_objects if x.type == "DiamondGameObject"]
        for diamond in list_diamond:
            print("IsDiamond: Current position:", current_position)
            print("Diamond position : ", diamond)
            if (position_equals(current_position, diamond.position)):
                return True
        return False
    
    def possible_direction(self, current_position: Position, board: Board):
        direction_available = []
        
        if current_position.x > 0:
            direction_available.append((-1, 0))
        if current_position.x < board.width - 1:
            direction_available.append((1, 0))

        if current_position.y > 0:
            direction_available.append((0, -1))
        if current_position.y < board.height - 1:
            direction_available.append((0, 1))
        
        return direction_available
    
    def portal_to_diamond_displacement(self, current_position: Position, portal_one_position: Position, portal_two_position: Position, board: Board):
        displacement_bot_to_portal_one = self.displacement(current_position, portal_one_position)
        displacement_bot_to_portal_two = self.displacement(current_position, portal_two_position)

        if displacement_bot_to_portal_one <= displacement_bot_to_portal_two:
            initial_to_portal_displacement = displacement_bot_to_portal_one
            portal_to_finish_displacement = portal_two_position
            initial_portal = portal_one_position
        else:
            initial_to_portal_displacement = displacement_bot_to_portal_two
            portal_to_finish_displacement = portal_one_position
            initial_portal = portal_two_position

        displacement_to_diamond = []
        for diamond in board.diamonds:
            displacement_to_diamond.append((diamond.position, self.displacement(portal_to_finish_displacement, diamond.position)))
        shortest_displacement = min(displacement_to_diamond, key=lambda x: x[1])
        shortest_displacement_to_diamond = shortest_displacement[1]

        total_displacement = shortest_displacement_to_diamond + initial_to_portal_displacement

        return initial_portal, total_displacement
    
    def portal_to_base_displacement(self, current_position: Position, portal_one_position: Position, portal_two_position: Position, board_bot: GameObject):
        displacement_bot_to_portal_one = self.displacement(current_position, portal_one_position)
        displacement_bot_to_portal_two = self.displacement(current_position, portal_two_position)
        base_position = board_bot.properties.base


        if displacement_bot_to_portal_one <= displacement_bot_to_portal_two:
            initial_to_portal_displacement = displacement_bot_to_portal_one
            portal_to_finish_displacement = portal_two_position
            initial_portal = portal_one_position
        else:
            initial_to_portal_displacement = displacement_bot_to_portal_two
            portal_to_finish_displacement = portal_one_position
            initial_portal = portal_two_position


        displacement_to_base = self.displacement(portal_to_finish_displacement, base_position)
        total_displacement = displacement_to_base + initial_to_portal_displacement
        

        return initial_portal, total_displacement
    
    def find_portal_position(self, board: Board):
        list_portal = [x for x in board.game_objects if x.type == "TeleportGameObject"]
        return list_portal[0].position, list_portal[1].position

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        first_portal_position, second_portal_position = self.find_portal_position(board)
        base = board_bot.properties.base
        time_rem = props.milliseconds_left
        print("Current bot position : ", current_position)
        print("First portal position : ", first_portal_position)
        print("Second portal position : ", second_portal_position)
        print("Base : ", base)
        print("DIAMOND : ", props.diamonds)
        if props.diamonds == 5:
            initial_portal_position, effective_portal_base_displacement = self.portal_to_base_displacement(current_position,first_portal_position, second_portal_position, board_bot)
            if (self.displacement(current_position,base) > effective_portal_base_displacement):
                self.goal_position = initial_portal_position
            else:
                self.goal_position = base
        else:
            # print(board.game_objects)
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
            try:
                minDiamond = min(listJarak, key = lambda x: x[1])
                initial_portal_position, effective_portal_diamond_displacement = self.portal_to_diamond_displacement(current_position, first_portal_position, second_portal_position, board)
                if (minDiamond[1] > effective_portal_diamond_displacement):
                    self.goal_position = initial_portal_position
                else:
                    self.goal_position = minDiamond[0]
            except:
                initial_portal_position, effective_portal_base_displacement = self.portal_to_base_displacement(current_position,first_portal_position, second_portal_position, board_bot)
                if (self.displacement(current_position,base) > effective_portal_base_displacement):
                    self.goal_position = initial_portal_position
                else:
                    self.goal_position = base
            
            if (self.is_teleporter_position(current_position, board)):
                direction_available  = self.possible_direction(current_position, board)
                print("Direction available :", direction_available)
                
                for direction in direction_available:
                    expected_position = Position(current_position.x+direction[0], current_position.y+direction[1])
                    if (not self.is_teleporter_position(expected_position, board)):
                        if (self.is_diamond_position(expected_position, board)):
                            return direction
                        else:
                            minDiamond = min(listJarak, key = lambda x: x[1])
                            self.goal_position = minDiamond[0]
                            

            if time_rem <= 10000:
                if(props.diamonds > 1):
                    initial_portal_position, effective_portal_base_displacement = self.portal_to_base_displacement(current_position,first_portal_position, second_portal_position, board_bot)
                    if (self.displacement(current_position,base) > effective_portal_base_displacement):
                        self.goal_position = initial_portal_position
                    else:
                        self.goal_position = base

        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        print(current_position)
        print(self.goal_position)
        print(delta_x, delta_y)
        return delta_x, delta_y