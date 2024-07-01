from utils import *
from constants import *

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.blocks = TETROMINOES[shape]
        self.color = COLORS[shape]
        self.start_position = [[5,0]] # start in the middle of the top of the play area
        self.pivot_position = add_lists(self.start_position,PIVOT_POINTS[shape])
        self.position = add_lists(self.start_position,self.blocks)
        self.min_x = min(block[0] for block in self.position)
        self.max_x = max(block[0] for block in self.position)
        self.max_y = max(block[1] for block in self.position)
        self.collision = False
        self.hard_collision = False

    def move(self, direction, placed_tetrominos):
        self.min_x = min(block[0] for block in self.position)
        self.max_x = max(block[0] for block in self.position)
        self.max_y = max(block[1] for block in self.position)
        self.collision = False

        new_position = []

        if direction == "left":
            if self.min_x>0:
                new_position = add_lists([[-1,0]],self.position)
                new_pivot_position =  add_lists([[-1,0]],self.pivot_position)
            else:
                new_position = self.position
                new_pivot_position = self.pivot_position

        elif direction == "right":
            if self.max_x<9:
                new_position = add_lists([[1,0]],self.position)
                new_pivot_position =  add_lists([[1,0]],self.pivot_position)
            else:
                new_position = self.position
                new_pivot_position = self.pivot_position

        elif direction == "down":
            new_position = add_lists([[0,1]],self.position)
            new_pivot_position =  add_lists([[0,1]],self.pivot_position)


        if max(block[1] for block in new_position) <= 19:
            #collision detection
            if len(placed_tetrominos) != 0:
                for x,y in new_position:
                    if self.collision:
                        break
                    for i in range(len(placed_tetrominos)):
                        for u,v in placed_tetrominos[i]:
                            if y == v and x==u:
                                self.collision = True
                                break
                        if self.collision:
                            break   

            if len(placed_tetrominos) != 0:
                for x,y in new_position:
                    if self.hard_collision:
                        break
                    for i in range(len(placed_tetrominos)):
                        for u,v in placed_tetrominos[i]:
                            if y == v and x==u and direction == "down":
                                self.hard_collision = True
                                break
                        if self.hard_collision:
                            break  

            if self.collision == False:
                self.position = new_position
                self.pivot_position = new_pivot_position


        else:
            self.collision = True
            self.hard_collision = True

 
            
    def check_collision(self, new_position, placed_tetrominos):
        for x, y in new_position:
            if x < 0 or x > 9 or y > 19:
                return True
            for tetromino in placed_tetrominos:
                if [x, y] in tetromino:
                    return True
        return False
    
    def rotate(self, placed_tetrominoes):
        new_blocks = [(-y, x) for x, y in substract_lists(self.pivot_position,self.position)]  # 90 degree rotation around the pivot point
        new_position = add_lists(self.pivot_position,new_blocks)
        min_x = min(block[0] for block in new_position)
        max_x = max(block[0] for block in new_position)
        max_y = max(block[1] for block in new_position)
        if  min_x < 0:
            self.position = add_lists([[(-1)* min_x,0]],new_position)
            self.pivot_position = add_lists([[(-1)* min_x,0]],self.pivot_position)
        elif  max_x > 9:
            self.position = add_lists([[9-max_x,0]],new_position)
            self.pivot_position = add_lists([[9-max_x,0]],self.pivot_position)
        elif max_y > 19:
            self.position = add_lists([[0,19-max_y]],new_position)
            self.pivot_position = add_lists([[0,19-max_y]],self.pivot_position)
        
        else: self.position = new_position

        for i in range(len(self.position)):
            for tetromino in placed_tetrominoes:
                for placed_block in tetromino:
                    while placed_block == self.position[i]:
                        self.position = add_lists([[0,-1]], self.position)
                        self.pivot_position = add_lists([[0,-1]], self.pivot_position)
                        print("felmozgatva")
