import pygame

class Fighter():

    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player

        #Image size and rendering onto the screen
        self.image_scale = data[2]
        self.size = data[:2]  # Create a list for the first 2 items
        self.offset = data[3]

        #Drawing rect and gravity
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0

        #Movement and actions
        self.running = False
        self.jump = [False, False] #First Jump, Second Jump
        self.attacking = False
        self.normal_attack = False
        self.strong_attack = False
        self.special_attack = False
        self.health = 100
        self.flip = flip
        self.hit = False
        self.dead = False

        #Animations
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 2  #0 - Attack #1 - Death #2 - Idle #3 - Attack #4
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

        #Clock
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0
        self.update_hit_cooldown = pygame.time.get_ticks()
        self.hit_cooldown = 800


    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spreadsheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1], self.size[0], self.size[1])
                scaled_image = pygame.transform.scale(temp_img, (self.size[0] * self.image_scale, self.size[1] * self.image_scale))
                temp_img_list.append(scaled_image)
            animation_list.append(temp_img_list)
        return animation_list


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.normal_attack = False
        self.strong_attack = False
        self.special_attack = False

        #Get key presses
        key = pygame.key.get_pressed()

        if not(self.dead):
            if self.player == 1:

                #If you attack then you can't perfrom another action - gonna change
                if self.attacking == False:
                    #MOVEMENT
                    if key[pygame.K_a]:
                        dx -= SPEED
                        self.running = True
                    if key[pygame.K_d]:
                        dx += SPEED
                        self.running = True

                    #JUMPING
                    # Make sure to try it using pygame.key.get_pressed() and delay the continous presses

                    #ATTACKS
                    if key[pygame.K_j] or key[pygame.K_u] or key[pygame.K_i]:
                        self.attacking = True
                        self.attack(surface, target)

                        if key[pygame.K_j]:
                            self.normal_attack = True
                        if key[pygame.K_u]:
                            self.strong_attack = True
                        if key[pygame.K_i]:
                            self.special_attack = True

            if self.player == 2:

                # If you attack then you can't perfrom another action - gonna change
                if self.attacking == False:
                    # MOVEMENT
                    if key[pygame.K_LEFT]:
                        dx -= SPEED
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx += SPEED
                        self.running = True

                    # JUMPING
                    # Make sure to try it using pygame.key.get_pressed() and delay the continous presses


                    # ATTACKS
                    if key[pygame.K_v] or key[pygame.K_f] or key[pygame.K_g]:
                        self.attacking = True
                        self.attack(surface, target)

                        if key[pygame.K_v]:
                            self.normal_attack = True
                        if key[pygame.K_f]:
                            self.strong_attack = True
                        if key[pygame.K_g]:
                            self.special_attack = True


    # Apply PHYSICS - NOTE: DON'T FORGET TO EXPERIMENT
        self.vel_y += GRAVITY
        dy += self.vel_y

    #Setting up borders
        #For x Variable
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #For Y Variable
        if self.rect.bottom + dy > 550:
            self.vel_y = 0
            dy = 550 - self.rect.bottom
            self.jump[0], self.jump[1] = False, False



        if not(self.dead):
            #Ensure players face each other
            if self.rect.centerx <= target.rect.centerx:
                self.flip = False
            else:
                self.flip = True


    #UPDATE POSITION OF RECTANGLE
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):

        attacking_rectangle = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rectangle.colliderect(target.rect):
            target.health -= 10
            target.hit = True


    #Update the timer and sprite aniamtions
    def update(self):
        #check what animation the player is performing
        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(1)
        elif self.hit == True:
            self.update_action(10)
        elif self.attacking == True:
            if self.normal_attack == True:
                self.update_action(0)
            elif self.strong_attack == True:
                self.update_action(4)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(7)
        elif self.running == True:
            self.update_action(3)
        else:
            self.update_action(2)  # IDLE

        animation_cooldown = 40

        #update image
        self.image = self.animation_list[self.action][self.frame_index]

        #check if half a second has passed --> make sure to experiment with the if statement below
        if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        #If the end of the animation is reached
        if self.frame_index >= len(self.animation_list[self.action]):

            if self.dead:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

                #if the attack animation is finished
                if self.attacking:
                    self.attacking = False
                    self.normal_attack = False
                    self.strong_attack = False
                    self.special_attack = False

                #if the hit animation is finished
                if self.hit:
                    if pygame.time.get_ticks() - self.update_hit_cooldown > self.hit_cooldown:
                        self.update_hit_cooldown = pygame.time.get_ticks()
                        self.hit = False
                    #If the opponent is attacking but hit at the same time :
                    self.attacking = False
                    self.normal_attack = False
                    self.strong_attack = False
                    self.special_attack = False


    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            # update the animation settings
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
