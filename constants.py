import pygame

pygame.mixer.init()
pygame.font.init()

width, height = 700, 800
play_area_width = 350
play_area_height = 700
work_transform_x = width / 2 - play_area_width / 2
work_transform_y = height - 50 - play_area_height
block_dim = play_area_width / 10

next_tetrominoes_x0 = 609
next_tetrominoes_y0 = 130

held_center_x = 91
held_center_y = 150

level_center_x = 616
level_center_y = 632

font_style = "Dubai"
font = pygame.font.SysFont(font_style, 36)
font.set_bold(True)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")
background = pygame.transform.scale(pygame.image.load("Assets/bg.png"), (width, height))
row_clear_sound = pygame.mixer.Sound("Assets/row_clear.mp3")
row_clear_sound.set_volume(0.6)
tetris_row_clear_sound = pygame.mixer.Sound("Assets/tetris_row_clear.mp3")
background_music = "Assets/Tetris.mp3"
place_object_sound = pygame.mixer.Sound("Assets/place_object_sound.mp3")
hard_drop_sound = pygame.mixer.Sound("Assets/hard_drop_sound.mp3")
hard_drop_sound.set_volume(0.8)
movement_tick_sound = pygame.mixer.Sound("Assets/movement_tick_sound.mp3")
movement_tick_sound.set_volume(0.6)
hold_sound = pygame.mixer.Sound("Assets/hold_sound.mp3")
hold_sound.set_volume(0.6)
rotate_sound = pygame.mixer.Sound("Assets/rotate_sound.mp3")
rotate_sound.set_volume(0.6)

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (-1, -1), (1, 0)],
    'L': [(0, 0), (1, 0), (1, -1), (-1, 0)],
    'I': [(0, 0), (-1, 0), (1, 0), (2, 0)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}

PIVOT_POINTS = {
    'T': [[0, 0]],
    'O': [[0.5, -0.5]],
    'J': [[0, 0]],
    'L': [[0, 0]],
    'I': [[0.5, 0.5]],
    'S': [[0, 0]],
    'Z': [[0, 0]]
}

COLORS = {
    'T': (165, 63, 155),
    'O': (179, 154, 51),
    'J': (82, 57, 206),
    'L': (180, 100, 50),
    'I': (49, 178, 131),
    'S': (130, 178, 49),
    'Z': (180, 51, 58)
}