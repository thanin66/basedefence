import pygame
import sys



# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

# Colors
white = (255, 255, 255)
gray = (150, 150, 150) 
green = (0, 255, 0)
red =  (255, 0, 0)
magen = (255, 0, 255)
black = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("base def")

# Font settings
font = pygame.font.Font(None, 50)
# กำหนดขนาดปุ่ม
button_width = 200
button_height = 50

bg = pygame.image.load('images/clouds/cloud_2.png').convert()
bg_rect = bg.get_rect()

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    
# Function to create buttons
def draw_button(screen, color, x, y, width, height, text, text_color, action=None):     
    pygame.draw.rect(screen, color, (x, y, width, height))


    # Main menu loop
def main_menu():
    while True:
        screen.fill(white)            
        draw_text("Main Menu", font, black, screen, (SCREEN_WIDTH // 2 ), 50)        
        action = draw_button(screen, green, (SCREEN_WIDTH // 2 ), 200, 200, 50, "Play", black, "play")
        if action == "play":
            print('start') 
        action = draw_button(screen, green, (SCREEN_WIDTH // 2 ), 300, 200, 50, "Settings", black, "settings")
        if action == "settings":
            settings_menu()  
        action = draw_button(screen, green, (SCREEN_WIDTH // 2 ), 400, 200, 50, "Quit", black, "quit")
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
    fullscreen = False
    while True:
        screen.fill(white)
        
        draw_text("Settings", font, black, screen, (SCREEN_WIDTH // 2 ), 50)
        #back button
        action = draw_button(screen, green, 20, 50, 200, 50, "back", black, "go_back")
        if action == "go_back": 
            main_menu()
        # Toggle fullscreen button
        action = draw_button(screen, green, (SCREEN_WIDTH // 2 ), 200, 200, 50, "Fullscreen: " + ("On" if fullscreen else "Off"), black, "fullscreen_toggle")
        if action == "fullscreen_toggle":
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def mode_game(screen):
    global back_button_rect, easy_button_rect, hard_button_rect
    bg = pygame.image.load('images/background/bg_1_p.png')
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    print("back")
                    main_menu(screen)
                elif easy_button_rect.collidepoint(mouse_pos):
                    print("easy Button Clicked")
                    pass
                elif hard_button_rect.collidepoint(mouse_pos):
                    print("hard Button Clicked")

        screen.blit(bg, (0, 0))

        back_button_rect = pygame.Rect(10, 40, button_width, button_height)
        draw_button(screen, back_button_rect.x, back_button_rect.y, button_width, button_height, "Back", gray)

        easy_button_rect = pygame.Rect(360, 300, button_width, button_height)
        draw_button(screen, easy_button_rect.x, easy_button_rect.y, button_width, button_height, "easy", green)

        hard_button_rect = pygame.Rect(700, 300, button_width, button_height)
        draw_button(screen, hard_button_rect.x, hard_button_rect.y, button_width, button_height, "hard", red)


        pygame.display.flip()
def game_setting_menu(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    print("back to game")
                    return  
                elif main_button_rect.collidepoint(mouse_pos):
                    print("to Main menu")
                    main_menu(screen)
                elif fullscreen_button_rect.collidepoint(mouse_pos):
                    print('fullscreen')
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

                elif window_button_rect.collidepoint(mouse_pos):
                    print('fullscreen')
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    return

        screen.blit(bg, (0, 0))

        # สร้างปุ่ม Back
        back_button_rect = pygame.Rect(700, 500, button_width, button_height)
        draw_button(screen, back_button_rect.x, back_button_rect.y, button_width, button_height, "back to game", gray)

        main_button_rect = pygame.Rect(360, 500, button_width, button_height)
        draw_button(screen, main_button_rect.x, main_button_rect.y, button_width, button_height, "to Main menu", gray)

        fullscreen_button_rect = pygame.Rect(360, 200, button_width, button_height)
        draw_button(screen, fullscreen_button_rect.x, fullscreen_button_rect.y, button_width, button_height, "fullscreen", gray)

        window_button_rect = pygame.Rect(700, 200, button_width, button_height)
        draw_button(screen, window_button_rect.x, window_button_rect.y, button_width, button_height, "window", gray)

        pygame.display.flip()
