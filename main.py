import pygame
import random
from tetromino import Tetromino
from utils import *
from constants import *

#--------------------------------
# TO DO:
#--------------------------------

pygame.font.init()
pygame.mixer.init()
pygame.init()

def music():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.65)
    pygame.mixer.music.play(loops=-1)

def draw_grid():
    window.blit(background, (0, 0))
    pygame.draw.rect(window, (10, 10, 10), (work_transform_x, work_transform_y, play_area_width, play_area_height))

def draw_tetromino(tetromino, placed_tetrominos, placed_tetromino_colors):
    for block in tetromino.position:
        x = work_transform_x + block[0] * block_dim
        y = work_transform_y + block[1] * block_dim
        pygame.draw.rect(window, tetromino.color, (x, y, block_dim, block_dim))

    for i in range(len(placed_tetrominos)):
        for block in placed_tetrominos[i]:
            x = work_transform_x + block[0] * block_dim
            y = work_transform_y + block[1] * block_dim
            pygame.draw.rect(window, placed_tetromino_colors[i], (x, y, block_dim, block_dim))
        
    for i in range(11):
        pygame.draw.line(window, (200, 200, 200), [work_transform_x + i * block_dim, work_transform_y], [work_transform_x + i * block_dim, work_transform_y + play_area_height], 1)
    for i in range(21):
        pygame.draw.line(window, (200, 200, 200), [work_transform_x, work_transform_y + i * block_dim], [work_transform_x + play_area_width, work_transform_y + i * block_dim], 1)

def draw_shadow_tetromino(shadow_tetromino):
    for block in shadow_tetromino.position:
        x = work_transform_x + block[0] * block_dim
        y = work_transform_y + block[1] * block_dim

        temp_surface = pygame.Surface((block_dim, block_dim), pygame.SRCALPHA)
        temp_surface.fill((156,156,156, 90))
        window.blit(temp_surface, (x,y))

def draw_next_tetrominoes(next_tetrominoes):
    for i, tetromino in enumerate(next_tetrominoes):

        x_offset = next_tetrominoes_x0 - ((tetromino.max_x - tetromino.min_x + 1)*block_dim) / 2

        block_x_min = min(block[0] for block in tetromino.blocks)

        tetromino_blocks = add_lists([[ - block_x_min, 0]], tetromino.blocks)

        for block in tetromino_blocks:
            x = x_offset + block[0] * block_dim
            y = next_tetrominoes_y0 + i * 3 * block_dim + block[1] * block_dim
            pygame.draw.rect(window, tetromino.color, (x, y, block_dim, block_dim))

def draw_held_tetromino(held_tetromino_shape):
        held_tetromino = Tetromino(held_tetromino_shape)
        x_offset = held_center_x - ((held_tetromino.max_x - held_tetromino.min_x + 1)*block_dim) / 2
        y_offset = held_center_y - ((held_tetromino.max_y - held_tetromino.min_y + 1)*block_dim) / 2
        
        block_x_min = min(block[0] for block in held_tetromino.blocks)
        block_y_min = min(block[1] for block in held_tetromino.blocks)

        tetromino_to_show = add_lists([[- block_x_min, - block_y_min]], held_tetromino.blocks)

        for block in tetromino_to_show:
            x = x_offset + block[0] * block_dim
            y = y_offset + block[1] * block_dim
            pygame.draw.rect(window, held_tetromino.color, (x, y, block_dim, block_dim))


def check_finished_rows(placed_tetrominoes):
    row_to_clear = list()
    for i in range(21):
        block_counter_in_row = 0    
        for tetromino in placed_tetrominoes:
            for block in tetromino:
                if block[1]==i-1:
                    block_counter_in_row += 1
            if block_counter_in_row == 10:
                row_to_clear.append(i-1)
    return row_to_clear

def clear_and_shift_rows(placed_tetrominos, rows_to_clear):
    for row in rows_to_clear:
        # Remove blocks in the current row and shift blocks above it
        placed_tetrominos = [
            [
                [x, y + 1] if y < row else [x, y] 
                for x, y in tetromino if y != row
            ]
            for tetromino in placed_tetrominos
        ]
    if len(rows_to_clear) > 0:
      row_cleared_sound.play()
    return placed_tetrominos

def random_tetromino(tetromino):

    tetromino_shapes = list(TETROMINOES.keys())
    last_tetromino_shape = tetromino.shape
    reroll_value = 8

    roll = random.randint(1, reroll_value)

    if roll == reroll_value or tetromino_shapes[roll - 1] == last_tetromino_shape:
        # Second roll: 7-sided die
        roll = random.randint(1, 7)

    return Tetromino(tetromino_shapes[roll - 1])

def place_tetromino(tetromino, placed_tetrominos, placed_tetromino_colors, key_timers, next_tetrominoes):

    placed_tetrominos.append(tetromino.position)
    placed_tetromino_colors.append(tetromino.color)

    new_tetromino = next_tetrominoes[0]

    
    for item in key_timers:
        key_timers[item]['pressed'] = False

    return new_tetromino




def main():
    run = True
    clock = pygame.time.Clock()
    tetromino = Tetromino(random.choice(list(TETROMINOES.keys())))
    auto_move_down = pygame.USEREVENT + 1
    pygame.time.set_timer(auto_move_down, 800)  # move down every 500ms

    placed_tetrominos = list()
    placed_tetromino_colors = list()
    held_tetromino_shape = 10 # dummy number to initialize
    changed = False

    key_delay = 300  # Initial delay before continuous movement (in milliseconds)
    key_interval = 20  # Interval for continuous movement (in milliseconds)

    key_timers = {
        pygame.K_LEFT: {'pressed': False, 'timer': 0},
        pygame.K_RIGHT: {'pressed': False, 'timer': 0},
        pygame.K_DOWN: {'pressed': False, 'timer': 0}
    }

    next_tetrominoes = []
    for i in range(4):
        next_tetrominoes.append(random_tetromino(tetromino))


    while run:
        current_time = pygame.time.get_ticks()

        shadow_tetromino = Tetromino(tetromino.shape)
        shadow_tetromino.position = tetromino.position

        while shadow_tetromino.collision == False:
            shadow_tetromino.move("down", placed_tetrominos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in key_timers:
                    key_timers[event.key]['pressed'] = True
                    key_timers[event.key]['timer'] = current_time + key_delay
                    if event.key == pygame.K_LEFT:
                        tetromino.move("left",placed_tetrominos)
                    elif event.key == pygame.K_RIGHT:
                        tetromino.move("right", placed_tetrominos)
                    elif event.key == pygame.K_DOWN:
                        tetromino.move("down", placed_tetrominos)
                elif event.key == pygame.K_SPACE:
                    while tetromino.hard_collision == False:
                        tetromino.move("down", placed_tetrominos)
                    tetromino = place_tetromino(tetromino, placed_tetrominos, placed_tetromino_colors, key_timers, next_tetrominoes)
                    next_tetrominoes.pop(0)
                    next_tetrominoes.append(random_tetromino(next_tetrominoes[-1]))
                    changed = False
                    

                if event.key == pygame.K_UP:
                    tetromino.rotate(placed_tetrominos) # Rotate the tetromino clockwise

                if event.key == pygame.K_LCTRL:
                    for i in range(3):
                        tetromino.rotate(placed_tetrominos) # Rotate the tetromino counterclockwise

                if event.key == pygame.K_a:
                    for i in range(2):
                        tetromino.rotate(placed_tetrominos) # Flip the tetromino
                    
                if event.key == pygame.K_LSHIFT:
                    if changed == False:
                        if isinstance(held_tetromino_shape, str):
                            tetromino_change_buffer = held_tetromino_shape
                            held_tetromino_shape = tetromino.shape
                            tetromino = Tetromino(tetromino_change_buffer)
                            changed = True

                        else:
                            held_tetromino_shape = tetromino.shape
                            tetromino = next_tetrominoes[0]
                            next_tetrominoes.pop(0)
                            next_tetrominoes.append(random_tetromino(next_tetrominoes[-1]))
                            changed = True


            if event.type == pygame.KEYUP:
                if event.key in key_timers:
                    key_timers[event.key]['pressed'] = False

            if event.type == auto_move_down:       
                tetromino.move("down", placed_tetrominos) 

                if tetromino.collision == True:
                     #Place tetromino
                    if tetromino.hard_collision == True:
                        tetromino = place_tetromino(tetromino, placed_tetrominos, placed_tetromino_colors, key_timers, next_tetrominoes)
                        next_tetrominoes.pop(0)
                        next_tetrominoes.append(random_tetromino(next_tetrominoes[-1]))
                        changed = False

        for key, value in key_timers.items():
            if value['pressed']:
                if current_time >= value['timer']:
                    if key == pygame.K_LEFT:
                        tetromino.move("left", placed_tetrominos)
                    elif key == pygame.K_RIGHT:
                        tetromino.move("right", placed_tetrominos)
                    elif key == pygame.K_DOWN:
                        tetromino.move("down", placed_tetrominos)
                    value['timer'] = current_time + key_interval
            
        #clear rows
        placed_tetrominos = clear_and_shift_rows(placed_tetrominos, check_finished_rows(placed_tetrominos))


        if len(placed_tetromino_colors)>200:
            placed_tetromino_colors.pop(0)

        draw_grid()
        draw_shadow_tetromino(shadow_tetromino)
        draw_tetromino(tetromino,placed_tetrominos, placed_tetromino_colors)
        draw_next_tetrominoes(next_tetrominoes)
        if isinstance(held_tetromino_shape, str):
            draw_held_tetromino(held_tetromino_shape)
        pygame.display.update()
        clock.tick(60)  # control the frame rate

    pygame.quit()

if __name__ == "__main__":
    music()
    main()
