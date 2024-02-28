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

pygame.init()
pygame.display.set_caption("slime")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# กำหนดภาพพื้นหลัง
sky_img = pygame.image.load('images/background/bg_1.png').convert_alpha()
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

ROWS = 15
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1




# กำหนด font
font = pygame.font.Font(None, 36)



# ตัวแปรสำหรับเก็บเวลาล่าสุดที่สร้างศัตรู
last_enemy_spawn_time = 0
enemy_spawn_interval = 1000  # 1 วินาที

def draw_bg():
    screen.fill(green)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img,((x * width)-scroll, 0))
# ฟังก์ชันสำหรับสร้างปุ่ม
def draw_button(screen, x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

def draw_grid():
    for c in range(MAX_COLS+1):
        pygame.draw.line(screen, white, (c * TILE_SIZE, 0),(c * TILE_SIZE,SCREEN_HEIGHT))
    for c in range(ROWS+1):
        pygame.draw.line(screen, white, (0, c * TILE_SIZE),(SCREEN_WIDTH, c * TILE_SIZE))

        
class Player(pygame.sprite.Sprite) :
    ACTIONS = [ 'Idle', 'Attack', 'Move', 'Jump',]
    GRAVITY = 0.5

    def __init__(self,action = 'Idle', x = 0, y = 720 , hp = 100 ,max_hp = 100, dmg = 25, speed = 5, attack_de_cooldown = 30,frame = 0):
        super().__init__()
        self.action = action # ท่าทาง
        self.image =pygame.image.load(f'images/character/{self.action}.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//4 , self.image.get_height() //4))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.jump_power = -10  # แรงกระโดด
        self.gravity = 0.5  # แรงโน้มถ่วง
        self.x = x #ต่ำแหน่ง
        self.y = y #ต่ำแหน่ง
        self.hp = hp # เลือด
        self.max_hp = max_hp # maxเลือด
        self.dmg = dmg 
        self.speed = speed
        self.velocity_y = 0
        self.attack_de_cooldown = attack_de_cooldown
        self.attack_cooldown = attack_de_cooldown 
        self.frame = frame
        self.deltatime = 0
        self.direction = 1
        self.rate = 0

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

    def update(self,):
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, hp, max_hp, speed=2, attack_cooldown =80, *groups):
        super().__init__(*groups)
        self.player = player
        self.hp = hp
        self.max_hp = max_hp
        self.image = pygame.image.load('images/character/e1.png')  
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//2 , self.image.get_height() //2))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = speed
        self.attack_cooldown = attack_cooldown  # เพิ่มตัวแปรคูลดาวน์การโจมตี

    def update(self):
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed
        if scroll_left == True:
            self.rect.x += 5
        if scroll_right == True:
            self.rect.x -= 5
        # ตรวจสอบคูลดาวน์การโจมตี
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

                # ตรวจสอบการชนของ player กับ enemy
        if pygame.sprite.collide_rect(self.player, self) and self.attack_cooldown == 0:
            self.player.hp -= 10  # ค่าความเสียหายจากการโจมตี
            self.attack_cooldown = 60  # รีเซ็ตคูลดาวน์หลังจากโจมตี 


def mode_game(screen):
    global back_button_rect, easy_button_rect, hard_button_rect
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

        screen.blit(sky_img, (0, 0))

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

        screen.blit(sky_img, (0, 0))

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

        screen.blit(sky_img, (0, 0))

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
                    return  # Return to the main_game function
                elif main_button_rect.collidepoint(mouse_pos):
                    print("to Main menu")
                    main_menu(screen)
                elif fullscreen_button_rect.collidepoint(mouse_pos):
                    print('fullscreen')
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                elif window_button_rect.collidepoint(mouse_pos):
                    print('window')
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                    
        screen.blit(sky_img, (0, 0))

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
    global enemy, player, clock, scroll, scroll_left, scroll_right

    pygame.init()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    # สร้างรายการภาพพื้นหลังตามลำดับที่กำหนด
    player = Player()
    all_sprites.add(player)

    enemy_spawn_timer = 0  # เพิ่มตัวแปรสำหรับจับเวลาสำหรับการสุ่ม spawn enemy


    # ลูปหลัก
    running = True
    while running:
        draw_bg()

        if scroll_left == True:
            scroll -= 5
        if scroll_right == True:
            scroll += 5 

        # ลดค่าของ enemy_spawn_timer ทุกๆ 1 วินาที
        if enemy_spawn_timer > 0:
            enemy_spawn_timer -= 1
        if player.attack_cooldown < player.attack_de_cooldown:
            player.attack_cooldown += 1
        # สุ่ม spawn enemy ทุกๆ 1 วินาที
        if enemy_spawn_timer == 0:
            new_enemy = Enemy(player, 40, 40, 2)
            all_sprites.add(new_enemy)
            enemy_spawn_timer = 300  # รีเซ็ตค่าของ enemy_spawn_timer เพื่อสุ่ม spawn ใหม่ในอีก 1 วินาที
        # ตรวจสอบการชนกันระหว่าง enemy และ player
        hits = pygame.sprite.spritecollide(player, all_sprites, False)
        for hit in hits:
            if isinstance(hit, Enemy) and player.attack_cooldown == 30 :
                # player.hp -= 10  # ลด HP ของ player เมื่อโดน enemy โจมตี
                hit.hp -= 10
                player.attack_cooldown = 0
                player.action = 'Attack'
                if hit.hp < 1:    
                    hit.kill() # ทำลาย enemy ที่โดนโจมตี player


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    scroll_left = True
                elif event.key == pygame.K_d:
                    scroll_right = True
                elif event.key == pygame.K_r:
                    player.hp = 100
                elif event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_f and player.attack_cooldown == 30:
                    player.attack()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and scroll_left == True:
                    scroll_left = False
                elif event.key == pygame.K_d and scroll_right == True:
                    scroll_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button_rect.collidepoint(mouse_pos):
                    if game_setting_menu(screen):  # Check the return value
                        return  # Exit the main_game loop and return to the main_menu
 

        width = sky_img.get_width()
        for x in range(4):
            screen.blit(sky_img, ((x * width) - scroll, 0))
        screen.blit(sky_img, (0 - scroll, 0))
        pause_button_rect = pygame.Rect(1100, 30, 50, button_height)
        draw_button(screen, pause_button_rect.x, pause_button_rect.y, 50, button_height, "ll", gray)
        
        if not player.hp == player.max_hp:
            red_hp_bar = pygame.Rect(player.rect.x +20 , player.rect.y - 35, 50,button_height)
            draw_button(screen, red_hp_bar.x, red_hp_bar.y, 100, 20, "", red)
            hp_bar = pygame.Rect(player.rect.x  +20 , player.rect.y - 35, player.hp, 50)
            draw_button(screen, hp_bar.x, hp_bar.y,player.hp , 20, "", green)
        if not hit.hp < 0 :
            redenemy_hp_bar = pygame.Rect(hit.rect.x +20 , hit.rect.y - 35, 50,button_height)
            draw_button(screen, redenemy_hp_bar.x, redenemy_hp_bar.y, hit.max_hp, 20, "", red)
            ehp_bar = pygame.Rect(hit.rect.x  +20 , hit.rect.y - 35, hit.hp, 50)
            draw_button(screen, ehp_bar.x, ehp_bar.y,hit.hp , 20, "", green)



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
