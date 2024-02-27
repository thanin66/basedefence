import pygame,sys,random
from pygame import mixer

# Initialize pygame font module
pygame.font.init()
mixer.init()
# กำหนดขนาดหน้าจอ
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# กำหนดหน้าจอ
pygame.init()
pygame.display.set_caption("slime")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# กำหนดภาพพื้นหลัง
sky_img = pygame.image.load('images/background/bg_1.png').convert_alpha()


# กำหนดเสียงของปุ่ม

# กำหนดขนาดปุ่ม
button_width = 200
button_height = 50

# กำหนดสี RGB
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
def draw_bg():
    screen.fill(green)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img,((x * width)-scroll, 0))

def draw_grid():
    for c in range(MAX_COLS+1):
        pygame.draw.line(screen, white, (c * TILE_SIZE, 0),(c * TILE_SIZE,SCREEN_HEIGHT))
    for c in range(ROWS+1):
        pygame.draw.line(screen, white, (0, c * TILE_SIZE),(SCREEN_WIDTH, c * TILE_SIZE))
    

# ฟังก์ชันสำหรับสร้างปุ่ม
def draw_button(screen, x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite) :
    ACTIONS = [ 'Idle', 'Attack', 'Move', 'Jump',]
    GRAVITY = 0.5

    def __init__(self,action = 'Idle', x = 0, y = 720 , hp = 100 ,max_hp = 100, dmg = 25, speed = 5, attack_de_cooldown = 30,):
        super().__init__()
        self.action = action # ท่าทาง
        self.image =pygame.image.load(f'images/character/{self.action}.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//4 , self.image.get_height() //4))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.frame = clock
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

    def attack(self):
        print("AT")
        self.action = 'Attack'
        if abs((self.rect.x - (enemy.rect.x + 50))) < 200:
            enemy.hp -= self.dmg  # ค่าความเสียหายจากการโจมตี
            self.attack_cooldown = 0
        else:
            self.attack_cooldown = 0



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

        # หากคูลดาวน์การโจมตีลดลงถึง 0 ให้โจมตีผู้เล่น
        if self.attack_cooldown == 0:
            if abs(self.rect.x - self.player.rect.x) < 50:
                self.player.hp -= 10  # ค่าความเสียหายจากการโจมตี
                self.attack_cooldown = 60  # รีเซ็ตคูลดาวน์หลังจากโจมตี


pygame.init()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
# สร้างรายการภาพพื้นหลังตามลำดับที่กำหนด
player = Player()
all_sprites.add(player)
for i in range(5):
    enemy = Enemy(player,40,40,2)
    all_sprites.add(enemy)

# ลูปหลัก
running = True
while running:
    draw_bg()
    draw_grid()

    if scroll_left == True:
        scroll -= 5
    if scroll_right == True:
        scroll += 5 
    if player.attack_cooldown < player.attack_de_cooldown:
        player.attack_cooldown += 1

    # ตรวจสอบการคลิกปิด
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
               enemy.hp = enemy.max_hp
           elif event.key == pygame.K_SPACE:  # เมื่อกด Spacebar ให้กระโดด
               player.jump()
           elif event.key == pygame.K_f and player.attack_cooldown == 30: 
                player.attack()
        elif event.type == pygame.KEYUP:
           if event.key == pygame.K_a and scroll_left == True:
               scroll_left = False
           elif event.key == pygame.K_d and scroll_right == True:
               scroll_right = False

        
    if not player.hp == player.max_hp:
        red_hp_bar = pygame.Rect(player.rect.x +20 , player.rect.y - 35, 50,button_height)
        draw_button(screen, red_hp_bar.x, red_hp_bar.y, 100, 20, "", red)
        hp_bar = pygame.Rect(player.rect.x  +20 , player.rect.y - 35, player.hp, 50)
        draw_button(screen, hp_bar.x, hp_bar.y,player.hp , 20, "", green)
    if not enemy.hp < 0 and not enemy.hp == enemy.max_hp  :
        redenemy_hp_bar = pygame.Rect(enemy.rect.x +20 , enemy.rect.y - 35, 50,button_height)
        draw_button(screen, redenemy_hp_bar.x, redenemy_hp_bar.y, enemy.max_hp, 20, "", red)
        ehp_bar = pygame.Rect(enemy.rect.x  +20 , enemy.rect.y - 35, enemy.hp, 50)
        draw_button(screen, ehp_bar.x, ehp_bar.y,enemy.hp , 20, "", green)
    if enemy.hp < 0:
        enemy.kill()
    all_sprites.update()
    # วาด
    all_sprites.draw(screen)
    pygame.display.flip()
    # จำกัดเฟรมเรต
    clock.tick(60)
pygame.quit()
sys.exit()

