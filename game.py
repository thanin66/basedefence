import pygame,sys,random
from pygame import mixer
# Initialize pygame font module
pygame.font.init()
mixer.init()
# กำหนดขนาดหน้าจอ
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# กำหนดสี RGB
WHITE = (255, 255, 255)

# กำหนดภาพพื้นหลัง
bg = pygame.image.load('images/background/bg_1_p.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


# กำหนดเสียงของปุ่ม

# กำหนดขนาดปุ่ม
button_width = 200
button_height = 50

# กำหนดสีของปุ่มเมื่อไม่กด
white = (255, 255, 255)
gray = (150, 150, 150) 
green = (0, 255, 0)
red =  (255, 0, 0)
magen = (255, 0, 255)
black = (0, 0, 0)

# เสียงปุ่ม




# กำหนด font
font = pygame.font.Font(None, 36)

# ฟังก์ชันสำหรับสร้างปุ่ม
def draw_button(screen, x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player,hp, speed, *groups):
        super().__init__(*groups)
        self.player = player
        self.hp = hp
        self.image = pygame.image.load('images/character/e1.png')  # กำหนดภาพของ Enemy
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//2 , self.image.get_height() //2))
        self.rect = self.image.get_rect(center=(random.randint(0, 1280),560 ))  # กำหนดตำแหน่งเริ่มต้นของ Enemy
        self.speed = speed
    def update(self):
        # เคลื่อนที่ไปทางซ้ายหรือขวาเพื่อเข้าหา Player
        if self.rect.x < self.player.rect.x:  # ถ้า Enemy อยู่ซ้ายของ Player
            self.rect.x += self.speed  # เคลื่อนที่ไปทางขวา
        elif self.rect.x > self.player.rect.x:  # ถ้า Enemy อยู่ขวาของ Player
            self.rect.x -= self.speed  # เคลื่อนที่ไปทางซ้าย


class Player(pygame.sprite.Sprite) :
    ACTIONS = [ 'Idle', 'Attack', 'Move', 'Jump',]
    GRAVITY = 0.5

    def __init__(self,action = None, x = 0, y = 720 , hp = 100 ,max_hp = 100, dmg = 11, speed = 5,):
        super().__init__()
        self.image =pygame.image.load(f'images/character/001.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//4 , self.image.get_height() //4))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.jump_power = -10  # แรงกระโดด
        self.gravity = 0.5  # แรงโน้มถ่วง
        self.action = action # ท่าทาง
        self.x = x #ต่ำแหน่ง
        self.y = y #ต่ำแหน่ง
        self.hp = hp # เลือด
        self.max_hp = max_hp # maxเลือด
        self.dmg = dmg 
        self.speed = speed
        self.velocity_y = 0

    def apply_gravity(self):
        # ในแต่ละเฟรม ความเร็วในแนวตั้งจะเพิ่มขึ้นตามค่าแรงโน้มถ่วง
        self.velocity_y += Player.GRAVITY
        self.y += self.velocity_y

    def jump(self, jump_strength):
        # เมื่อกระโดด ความเร็วในแนวตั้งจะถูกเซ็ตให้เป็นค่าของ jump_strength
        self.velocity_y = -jump_strength
    def jump(self):
        # กระโดดเฉพาะเมื่ออยู่บนพื้น
        if self.rect.bottom >= SCREEN_HEIGHT - 100:
            self.y = self.jump_power
    def update(self):
        # อัพเดทตำแหน่งของผู้เล่น
        self.rect.x += self.x
        self.rect.y += self.y

        # ฟิสิกส์: ใช้แรงโน้มถ่วง
        self.y += self.gravity

        # ฟิสิกส์: เบรกหลังถ้าชนขอบหน้าต่าง
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT-100:
            self.rect.bottom = SCREEN_HEIGHT - 100

class Envor():
    ()
  
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
                    main_game(screen)
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
        draw_button(screen, start_button_rect.x, start_button_rect.y, button_width, button_height, "Start", gray)

        # สร้างปุ่ม setting
        setting_button_rect = pygame.Rect(540, 300, button_width, button_height)
        draw_button(screen, setting_button_rect.x, setting_button_rect.y, button_width, button_height, "Setting", gray)

        # สร้างปุ่ม quit
        quit_button_rect = pygame.Rect(540, 400, button_width, button_height)
        draw_button(screen, quit_button_rect.x, quit_button_rect.y, button_width, button_height, "Quit", gray)

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
        draw_button(screen, back_button_rect.x, back_button_rect.y, button_width, button_height, "Back", gray)

        fullscreen_button_rect = pygame.Rect(360, 200, button_width, button_height)
        draw_button(screen, fullscreen_button_rect.x, fullscreen_button_rect.y, button_width, button_height, "fullscreen", gray)

        window_button_rect = pygame.Rect(700, 200, button_width, button_height)
        draw_button(screen, window_button_rect.x, window_button_rect.y, button_width, button_height, "window", gray)

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


def main_game(screen):
    pygame.init()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    # สร้างรายการภาพพื้นหลังตามลำดับที่กำหนด
    bg = pygame.image.load('images/background/bg_main.png')
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_scenes = ['block', 'bg_3_left', 'bg_2_left', 'bg_1_left', 'bg_main', 'bg_1_right', 'bg_2_right', 'bg_3_right','block']
    current_scene_index = 4  # กำหนดให้ภาพเริ่มต้นที่ index 3 คือ 'bg_1'


    player = Player()
    all_sprites.add(player)
    
    enemy = Enemy(player,20,1)
    enemy.rect.x = -50
    all_sprites.add(enemy)



    # ลูปหลัก
    running = True
    while running:
        # ตรวจสอบการคลิกปิด
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button_rect.collidepoint(mouse_pos):
                    print("pause")
                    game_setting_menu(screen)

            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_a:
                   player.x = -10
               elif event.key == pygame.K_d:
                   player.x = 10
               elif event.key == pygame.K_SPACE:  # เมื่อกด Spacebar ให้กระโดด
                   player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.x < 0:
                   player.x = 0
                elif event.key == pygame.K_d and player.x > 0:
                   player.x = 0
        
        if background_scenes[current_scene_index] == 'bg_3_left':
            if player.rect.left <= 20:  # ถ้าผู้เล่นอยู่ที่ขอบซ้ายของหน้าจอ
                player.x = 1
                player.jump()
        if background_scenes[current_scene_index] == 'bg_3_right':
            if player.rect.right >= SCREEN_WIDTH - 20 :  # ถ้าผู้เล่นอยู่ที่ขอบขวาของหน้าจอ
                player.x = -1
                player.jump()
        if abs(enemy.rect.x - player.rect.x) < 50 : 
            print('Ahhhhhh')       
            player.hp -= 1
        if player.hp == 0 :
            print('dead')
            main_menu(screen)

            
        if player.rect.right >= SCREEN_WIDTH:  # ถ้าผู้เล่นอยู่ที่ขอบขวาของหน้าจอ
            current_scene_index = (current_scene_index + 1) % len(background_scenes)# เปลี่ยนไปฉากถัดไปในรายการ
            # โหลดภาพพื้นหลังของฉากใหม่
            bg = pygame.image.load(f'images/background/{background_scenes[current_scene_index]}.png')
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # อัพเดทตำแหน่งของผู้เล่นให้เริ่มต้นที่ขอบซ้ายของหน้าจอ
            enemy.kill()
            player.rect.left = 0
            enemy = Enemy(player,20,1)
            enemy.rect.x = random.randint(400,1280)
            all_sprites.add(enemy)
        elif player.rect.left <= 0:  # ถ้าผู้เล่นอยู่ที่ขอบซ้ายของหน้าจอ
            current_scene_index = (current_scene_index - 1) % len(background_scenes)  # เปลี่ยนไปฉากถัดไปในรายการa
            # โหลดภาพพื้นหลังของฉากใหม่
            bg = pygame.image.load(f'images/background/{background_scenes[current_scene_index]}.png')
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            enemy.kill()
            # อัพเดทตำแหน่งของผู้เล่นให้เริ่มต้นที่ขอบขวาของหน้าจอ
            player.rect.right = SCREEN_WIDTH
            enemy = Enemy(player,20,1)
            enemy.rect.x = random.randint(1,600)
            all_sprites.add(enemy)

        if background_scenes[current_scene_index] == 'bg_main':
            enemy.kill()

        screen.blit(bg, (0, 0))
        pause_button_rect = pygame.Rect(1100, 30, 50, button_height)
        draw_button(screen, pause_button_rect.x, pause_button_rect.y, 50, button_height, "ll", gray)
        
        if not player.hp == player.max_hp:
            red_hp_bar = pygame.Rect(player.rect.x +20 , player.rect.y - 35, 50,button_height)
            draw_button(screen, red_hp_bar.x, red_hp_bar.y, 100, 20, "", red)
            hp_bar = pygame.Rect(player.rect.x  +20 , player.rect.y - 35, player.hp, 50)
            draw_button(screen, hp_bar.x, hp_bar.y,player.hp , 20, "", green)

        all_sprites.update()

        # วาด
        all_sprites.draw(screen)
        pygame.display.flip()

        # จำกัดเฟรมเรต
        clock.tick(60)
    pygame.quit()
    sys.exit()
# กำหนดหน้าจอ
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# เรียกใช้เมนูหลัก
main_menu(screen)
