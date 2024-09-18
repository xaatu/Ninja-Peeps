import pygame
import sys
from ninjapeeps import  level_one, level_two, level_three, level_four, level_five

# INITIALISE
pygame.init() 

# DISPLAY
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

# DEFINE COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FONTS
font = pygame.font.SysFont(None, 48)

# MENU OPTIONS
menu_items = ['Start Game', 'HiScore', 'Level Select']
selected_item = 0

level_options = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']
selected_level = 1  # DEFAULT LEVEL

def draw_menu():
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        text_color = WHITE if index == selected_item else (100, 100, 100)
        text_surf = font.render(item, True, text_color)
        text_rect = text_surf.get_rect(center=(screen_width//2, 150 + index * 60))
        screen.blit(text_surf, text_rect)
    pygame.display.flip()

def draw_level_menu(selected_level):
    screen.fill(BLACK)
    
    for index, option in enumerate(level_options):
        text_color = WHITE if index + 1 == selected_level else (100, 100, 100)
        text_surf = font.render(option, True, text_color)
        text_rect = text_surf.get_rect(center=(screen_width//2, 150 + index * 60))
        screen.blit(text_surf, text_rect)
    pygame.display.flip()

def main_menu():
    global selected_item
    global selected_level
    running = True
    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu_items[selected_item] == 'Start Game':
                        level_one()
                    elif menu_items[selected_item] == 'HiScore':
                        print("HiScore")  
                    elif menu_items[selected_item] == 'Level Select':
                        level_selection(selected_level)

def level_selection(selected_level):
    level_selected = False
    while not level_selected:
        draw_level_menu(selected_level)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = max(1, selected_level - 1)
                elif event.key == pygame.K_DOWN:
                    selected_level = min(len(level_options), selected_level + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if selected_level == 1:
                        level_one()
                    elif selected_level == 2:
                        level_two()
                    elif selected_level == 3:
                        level_three()
                    elif selected_level == 4:
                        level_four()
                    elif selected_level == 5:
                        level_five()
                    level_selected = True

if __name__ == '__main__':
    main_menu()

