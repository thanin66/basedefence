import pygame

pygame.init

    clock = pygame.time.Clock()
    fps = 60
    #หน้าต่าง เกม
    bottom_panel = 150 

    screen_width = 800
    screen_height = 400 + bottom_panel
    screen = pygame.display.set_mode((screen_width, screen_height))


    #โหลด ภาพ

    #ภาพ พื้นหลัง
    background_img = pygame.image.load('ภาพ/background.png').convert_alpha()
    # panel image
    panel_img = pygame.image.load('ภาพ/panel.png').convert_alpha()


    #ฟังชั่นเพื่อใส่ภาพพื่นหลัง
    def draw_bg():
        screen.blit(background_img, (0, 0))

    #ฟังชั่นเพื่อใส่ภาพ panel
    def draw_panel():
        screen.blit(panel_img, (0, screen_height - bottom_panel))


    # คลาส ตัวละคร 
    class Fighter():
        def __init__(self, x, y, name, max_hp, strangth, potions):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strangth = strangth
            self.start_potions = potions
            self.alive = True 
            self.animation_list = [] 
            self.frame_index = 0
            self.action = 0 
            self.update_time = pygame.time.get_ticks()
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3 , img.get_height() * 3 ))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            animation_cooldown = 100
            #ทำให้เกิดภาพเคลื่อนไหว
            #อัพเกรดภาพ
            self.image = self.animation_list[self.action][self.frame_index]
            #เช็คว่าถึงเวลาอัพเดตภาพหรือยัง
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            
            #ถ้าอนิเมชันหมด ให้เริ่มใหม่
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            

        def draw(self):
            screen.blit(self.image, self.rect)

    #ออปเจค ตัวละคร
    knight = Fighter(200, 260 ,'Knight', 30, 10, 3 )
    bandit1 = Fighter(550, 270 ,'Bandit', 20, 6, 1 )
    bandit2 = Fighter(700, 270 ,'Bandit', 20, 6, 1 )

    bandit_list = []
    bandit_list.append(bandit1)
    bandit_list.append(bandit2)

    run = True
    while run == True:

        clock.tick(fps)

        #วาด พื้นหลัง
        draw_bg()

        #วาด panel
        draw_panel()

        #วาด ตัวละคร
        knight.update()
        knight.draw()
        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()

