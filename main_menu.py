import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Font settings
font = pygame.font.Font(None, 36)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to create buttons
def draw_button(screen, color, x, y, width, height, text, text_color, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, font, text_color, screen, x + 10, y + 10)
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, GRAY, (x, y, width, height))
        draw_text(text, font, BLACK, screen, x + 10, y + 10)
        if mouse_click[0] == 1 and action is not None:
            return action

# Main menu loop
def main_menu():
    while True:
        screen.fill(WHITE)
        
        draw_text("Main Menu", font, BLACK, screen, 300, 50)
        
        action = draw_button(screen, GREEN, 300, 200, 200, 50, "Play", BLACK, "play")
        if action == "play":
            print("Starting the game...")
        
        action = draw_button(screen, GREEN, 300, 300, 200, 50, "Settings", BLACK, "settings")
        if action == "settings":
            settings_menu()
        
        action = draw_button(screen, GREEN, 300, 400, 200, 50, "Quit", BLACK, "quit")
        if action == "quit":
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Settings menu loop
def settings_menu():
    global screen  # Declare screen as global
    fullscreen = False
    while True:
        screen.fill(WHITE)
        
        draw_text("Settings", font, BLACK, screen, 350, 50)     
        # Toggle fullscreen button
        action = draw_button(screen, GREEN, 300, 200, 200, 50, "Fullscreen: " + ("On" if fullscreen else "Off"), BLACK, "fullscreen_toggle")
        if action == "fullscreen_toggle":
            fullscreen = not fullscreen
            if fullscreen:
           
                screen = pygame.display.set_mode((1980, 1080), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Start the main menu
main_menu()
