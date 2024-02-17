import pygame
from pygame import mixer

import sys

# Initialize pygame font module
pygame.font.init()
mixer.init()
# กำหนดขนาดหน้าจอ
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# กำหนดสี RGB
WHITE = (255, 255, 255)

# กำหนดภาพพื้นหลัง
bg = pygame.image.load('images/background/bg_1.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# กำหนดภาพปุ่ม
button_img = pygame.image.load('images/button/button.png')
# กำหนดเสียงของปุ่ม

# กำหนดขนาดปุ่ม
button_width = 200
button_height = 50

# กำหนดสีของปุ่มเมื่อไม่กด
button_color_white = (255, 255, 255)
button_color = (150, 150, 150) 
button_color_green = (0, 255, 0)
button_color_red =  (255, 0, 0)
button_color_magen = (255, 0, 255)
button_color_black = (0, 0, 0)
button_color_active = (255, 255, 255)

# เสียงปุ่ม




# กำหนด font
font = pygame.font.Font(None, 36)

# ฟังก์ชันสำหรับสร้างปุ่ม
def draw_button(screen, x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)



class Player :
    ACTIONS = [ 'Idle', 'Attack', 'Move', 'Jump',]
    GRAVITY = 0.5

    def __init__(self,action = None, x = 640, y = 200 , hp = 100, dmg = 11, speed = 2,):
        self.action = action
        self.x = x
        self.y = y
        self.hp = hp
        self.dmg = dmg
        self.speed = speed
        self.velocity_y = 0
        

    def move_left(self):
        self.x += self.speed
    def move_right(self):
        self.x -= self.speed

    def apply_gravity(self):
        # ในแต่ละเฟรม ความเร็วในแนวตั้งจะเพิ่มขึ้นตามค่าแรงโน้มถ่วง
        self.velocity_y += Player.GRAVITY
        self.y += self.velocity_y

    def jump(self, jump_strength):
        # เมื่อกระโดด ความเร็วในแนวตั้งจะถูกเซ็ตให้เป็นค่าของ jump_strength
        self.velocity_y = -jump_strength


class inventory :
    ()

def mode_game(screen):
    global back_button_rect, easy_button_rect, hard_button_rect
    bg = pygame.image.load('images/background/bg_2.png')
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
                elif hard_button_rect.collidepoint(mouse_pos):
                    print("hard Button Clicked")

        screen.blit(bg, (0, 0))

        back_button_rect = pygame.Rect(10, 40, button_width, button_height)
        draw_button(screen, back_button_rect.x, back_button_rect.y, button_width, button_height, "Back", button_color)

        easy_button_rect = pygame.Rect(360, 300, button_width, button_height)
        draw_button(screen, easy_button_rect.x, easy_button_rect.y, button_width, button_height, "easy", button_color_green)

        hard_button_rect = pygame.Rect(700, 300, button_width, button_height)
        draw_button(screen, hard_button_rect.x, hard_button_rect.y, button_width, button_height, "hard", button_color_red)


        pygame.display.flip()









# ฟังก์ชันสำหรับแสดงเมนูหลัก
def main_menu(screen):
    global start_button_rect, setting_button_rect, quit_button_rect
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    # ทำสิ่งที่ต้องการเมื่อคลิกที่ปุ่ม start
                    print("Start Button Clicked")
                    mode_game(screen)
                elif setting_button_rect.collidepoint(mouse_pos):
                    # ทำสิ่งที่ต้องการเมื่อคลิกที่ปุม setting
                    print("Setting Button Clicked")
                    setting_menu(screen)
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(bg, (0, 0))

        # สร้างปุ่ม start
        start_button_rect = pygame.Rect(540, 200, button_width, button_height)
        draw_button(screen, start_button_rect.x, start_button_rect.y, button_width, button_height, "Start", button_color)

        # สร้างปุ่ม setting
        setting_button_rect = pygame.Rect(540, 300, button_width, button_height)
        draw_button(screen, setting_button_rect.x, setting_button_rect.y, button_width, button_height, "Setting", button_color)

        # สร้างปุ่ม quit
        quit_button_rect = pygame.Rect(540, 400, button_width, button_height)
        draw_button(screen, quit_button_rect.x, quit_button_rect.y, button_width, button_height, "Quit", button_color)

        pygame.display.flip()

# ฟังก์ชันสำหรับแสดงเมนูตั้งค่า
def setting_menu(screen):
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
                elif fullscreen_button_rect.collidepoint(mouse_pos):
                    print('fullscreen')
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

                elif window_button_rect.collidepoint(mouse_pos):
                    print('fullscreen')
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    return

        screen.blit(bg, (0, 0))

        # สร้างปุ่ม Back
        back_button_rect = pygame.Rect(540, 500, button_width, button_height)
        draw_button(screen, back_button_rect.x, back_button_rect.y, button_width, button_height, "Back", button_color_magen)

        fullscreen_button_rect = pygame.Rect(360, 200, button_width, button_height)
        draw_button(screen, fullscreen_button_rect.x, fullscreen_button_rect.y, button_width, button_height, "fullscreen", button_color)

        window_button_rect = pygame.Rect(700, 200, button_width, button_height)
        draw_button(screen, window_button_rect.x, window_button_rect.y, button_width, button_height, "window", button_color)

        pygame.display.flip()




# กำหนดหน้าจอ
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# เรียกใช้เมนูหลัก
main_menu(screen)
