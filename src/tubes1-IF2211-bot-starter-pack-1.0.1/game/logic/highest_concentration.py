from typing import Optional, List
import math

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals


class HighestConcentration(BaseLogic):
    # Fungsi Konstruktor
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.is_portal_entry = False
        self.find_sector = True
        self.target_sector = []
        self.sector_index = 0

    # Fungsi untuk menghitung jarak dua titik
    def displacement(self, current_position: Position, goal_position: Position):
        return math.sqrt((current_position.x - goal_position.x) ** 2 + (current_position.y - goal_position.y) ** 2)
    
    # Fungsi untuk menentukan apakah sebuah titik mengandung teleporter atau tidak
    def is_teleporter_position (self, current_position : Position, board: Board):
        list_portal = [x for x in board.game_objects if x.type == "TeleportGameObject"]
        for portal in list_portal:
            if (position_equals(current_position, portal.position)):
                return True
        return False
    
    # Fungsi untuk menentukan apakah sebuah titik mengandung diamond atau tidak
    def is_diamond_position (self, current_position : Position, board: Board):
        list_diamond = [x for x in board.game_objects if x.type == "DiamondGameObject"]
        for diamond in list_diamond:
            # print("IsDiamond: Current position:", current_position)
            # print("Diamond position : ", diamond)
            if (position_equals(current_position, diamond.position)):
                return True
        return False
    
    # Fungsi untuk menentukan arah yang dilalui oleh robot
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
    
    # Fungsi untuk memanfaatkan portal
    def portal_utility_displacement(self, target:str, current_position: Position, portal_one_position: Position, portal_two_position: Position, board: Board, board_bot: GameObject):
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

        if target == "DiamondGameObject":
            displacement_to_diamond = []
            for diamond in board.diamonds:
                displacement_to_diamond.append((diamond.position, self.displacement(portal_to_finish_displacement, diamond.position)))
            shortest_displacement = min(displacement_to_diamond, key=lambda x: x[1])
            shortest_displacement_to_diamond = shortest_displacement[1]

            total_displacement = shortest_displacement_to_diamond + initial_to_portal_displacement
        elif target == "Base":
            base_position = board_bot.properties.base
            displacement_to_base = self.displacement(portal_to_finish_displacement, base_position)
            total_displacement = displacement_to_base + initial_to_portal_displacement
        
        
        return initial_portal, total_displacement

    # Fungsi untuk mencari posisi portal yang terdapat pada papan
    def find_portal_position(self, board: Board):
        list_portal = [x for x in board.game_objects if x.type == "TeleportGameObject"]
        return list_portal[0].position, list_portal[1].position

    # Prosedur untuk mempartisi map dari koordinat i hingga j
    def partitionMap(self, current_position:Position, board: Board, start_x: int, start_y:int, end_x: int, end_y:int, list: List[GameObject]):
        list_diamond = [x for x in board.game_objects if x.type == "DiamondGameObject"]
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                for diamond in list_diamond:
                    if position_equals(Position(y,x), diamond.position):
                        list.append(diamond)
        min_pos = min(list_diamond, key = lambda x: self.displacement(current_position,x.position))
        return min_pos.position

    # Fungsi untuk menghitung jumlah poin diamond pada partisi
    def countDiamond(self, board: Board, section: List[GameObject]) -> int:
        count = 0
        for diamonds in section:
            count += diamonds.properties.points
        return count

    # Fungsi untuk menentukan langkah selanjutnya yang akan dilalui robot
    def next_move(self, board_bot: GameObject, board: Board):

        # Inisialisasi
        props = board_bot.properties
        current_position = board_bot.position
        first_portal_position, second_portal_position = self.find_portal_position(board)
        base = board_bot.properties.base
        time_rem = props.milliseconds_left
        direction_available  = self.possible_direction(current_position, board)
            
        # Status
        # print("Current bot position : ", current_position)
        # print("First portal position : ", first_portal_position)
        # print("Second portal position : ", second_portal_position)
        # print("Base : ", base)
        # print("DIAMOND : ", props.diamonds)
        # print("Enemy bot :", board.bots)

        if props.diamonds == 5:
            initial_portal_position, effective_portal_base_displacement = self.portal_utility_displacement("Base", current_position,first_portal_position, second_portal_position, board, board_bot)
            if (self.displacement(current_position,base) > effective_portal_base_displacement):
                self.goal_position = initial_portal_position
            else:
                self.goal_position = base

            # Kasus ketika robot baru masuk ke dalam teleporter dan inventory == 5
            if (self.is_teleporter_position(current_position, board)):
                print("Direction available :", direction_available)
                
                for direction in direction_available:
                    expected_position = Position(current_position.y+direction[1], current_position.x+direction[0])
                    if (not self.is_teleporter_position(expected_position, board)):        
                        self.goal_position = base
        else:
            sectors = [[[],0, Position(0,0)] for i in range(4)]
            idx = 0
            for i in range(2):
                for j in range(2):
                    sectors[idx][2] = self.partitionMap(current_position, board, (j * board.width)//2, (i* board.height)//2, ((j+1)* board.width)//2 , ((i+1)*board.height)//2, sectors[idx][0])
                    idx += 1

            for i in range(4):
                sectors[i][1] = self.countDiamond(board, sectors[i][0])
            
            # Jika sektor yang dituju sudah ditemukan
            if(not(self.find_sector)):
                self.target_sector = sectors[self.sector_index]
                if self.target_sector[1] < 3:
                    self.find_sector = True

            # Jika ingi mencari sektor yang dituju
            if (self.find_sector):
                self.target_sector = max(sectors, key= lambda x : x[1]/self.displacement(current_position,x[2]))
                self.sector_index = sectors.index(self.target_sector)
                self.find_sector = False

            listJarak = []
            for diamond in self.target_sector[0]:
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
                initial_portal_position, effective_portal_diamond_displacement = self.portal_utility_displacement("DiamondGameObject",current_position, first_portal_position, second_portal_position, board, board_bot)
                if (minDiamond[1] > effective_portal_diamond_displacement):
                    self.goal_position = initial_portal_position
                else:
                    self.goal_position = minDiamond[0]

                # Kasus ketika robot baru masuk ke dalam teleporter dan inventory < 5 dan target robot adalah diamond
                if (self.is_teleporter_position(current_position, board)):
                    print("Direction available :", direction_available)
                    for direction in direction_available:
                        expected_position = Position(current_position.y+direction[1], current_position.x+direction[0])
                        if (not self.is_teleporter_position(expected_position, board)):
                            if (self.is_diamond_position(expected_position, board)):
                                return direction
                            else:
                                minDiamond = min(listJarak, key = lambda x: x[1])
                                self.goal_position = minDiamond[0]
                                print("GOAL POSITION AFTER TELEPORT:", self.goal_position)
            except:
                initial_portal_position, effective_portal_base_displacement = self.portal_utility_displacement("Base", current_position,first_portal_position, second_portal_position, board, board_bot)
                if (self.displacement(current_position,base) > effective_portal_base_displacement):
                    self.goal_position = initial_portal_position
                else:
                    self.goal_position = base
            
                # Kasus ketika robot baru masuk ke dalam teleporter dan inventory < 5 dan target robot adalah base 
                if (self.is_teleporter_position(current_position, board)):
                    print("Direction available :", direction_available)
                    
                    for direction in direction_available:
                        expected_position = Position(current_position.y+direction[1], current_position.x+direction[0])
                        if (not self.is_teleporter_position(expected_position, board)):        
                            self.goal_position = base

            # Kasus ketika waktu yang tersisa dalam permainan dibawah 10 detik
            if time_rem <= 10000:
                if(props.diamonds > 1):
                    initial_portal_position, effective_portal_base_displacement = self.portal_utility_displacement("Base", current_position,first_portal_position, second_portal_position, board, board_bot)
                    if (self.displacement(current_position,base) > effective_portal_base_displacement):
                        self.goal_position = initial_portal_position
                    else:
                        self.goal_position = base

        # Pengembalian nilai fungsi
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