import pygame #initiate pygame library

#"SETUP" SECTION ======================================================================

#Size of the screen
SCREEN_TITLE = "CROSSY RPG - Marcel :)"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
            #  RED GREEN BLUE  
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)

clock = pygame.time.Clock() #clock used to update game events and frames
pygame.font.init()
font = pygame.font.SysFont('cambria', 75)
font2 = pygame.font.SysFont('cambria', 60)
levelfont = pygame.font.SysFont('comicsans', 50)
#pygame.font.Font() is used mainly when you’ve included an actual ttf Font file with
#your code. For example, if you have a ttf file for the font arial in the same directory
#as your python file, you can use it with the following code.
#pygame.font.Font("arial.ttf", 20)

#======================================================================================

class Game:

    
    TICK_RATE = 60 #(typical rate of 60, equivalent to FPS)
     #tick rate and is game over do not need initiators
    
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        #fill the game screen with white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):

        is_game_over = False
        did_win = False
        #main game loop (for update all gameplay, such as movement, checks, graphics)
        direction = 0
        level_text = levelfont.render('Level ' '%.1f' % (level_speed), True, WHITE_COLOR)
        
        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('enemy.png', 20, 600, 50, 50)
        enemy_0.SPEED *= level_speed

        enemy_1 = NonPlayerCharacter('enemy.png', self.width - 40, 400, 50, 50)
        enemy_1.SPEED *= level_speed

        enemy_2 = NonPlayerCharacter('enemy.png', 20, 200, 50, 50)
        enemy_2.SPEED *= level_speed
        
        treasure = GameObject('treasure.png', 375, 50, 50, 50)
        
        while not is_game_over: #runs until the game is over

            #loop to get all of the events occuring at any given time (mouse movement, mouse and
            #button clicks, or exit events)
            for event in pygame.event.get():
                #if the user produces a 'quit' type of event
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    #move up if up key is pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        direction = 1
                    #move down if down key is pressed
                    elif event.key  == pygame.K_DOWN or event.key  == pygame.K_s:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key  == pygame.K_s or event.key == pygame.K_w:
                        direction = 0

                print(event) #monitors every event in the game

            self.game_screen.fill(WHITE_COLOR)
            
            self.game_screen.blit(self.image, (0, 0))
            #surface variable     color    coordinates  rect. size
            pygame.draw.rect(self.game_screen, BLACK_COLOR, [615, 10, 165, 50])

            self.game_screen.blit(level_text, (625, 20))
            
            # draw the treasure
            treasure.draw(self.game_screen)
            
            # Update the player position
            player_character.move(direction, self.height)
            
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            # Moving the enemy and then drawing it on the screen
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 3:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)
                
            #detect collision
            # Return False (no collision) if y positions and x positions do not overlap
            # Return True (collision) if y positions and x positions overlap
            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('YOU LOSE :(', True, RED_COLOR)
                text2 = font2.render('Better Luck Next Time !', True, WHITE_COLOR)
                self.game_screen.blit(text, (230, 300))
                self.game_screen.blit(text2, (120, 400))
                pygame.display.update()
                pygame.time.delay(2000)
                clock.tick(1)
                break
            
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('YOU WIN :)', True, BLACK_COLOR)
                text2 = font.render('Next Level !', True, WHITE_COLOR)
                self.game_screen.blit(text, (210, 300))
                self.game_screen.blit(text2, (200, 400))
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update() #update all game graphics 
            clock.tick(self.TICK_RATE) #makes the clock tick to run the game
            #TICK_RATE variable is within the class[needs .self]!

        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return
                    
class GameObject:

    def __init__(self, image_path, x, y, width, height):
        #Load player image from the file directory
        object_image = pygame.image.load(image_path)
        #image scaling (in this case = upscale)
        self.image = pygame.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

#class which represents the controllable character (player)    
class PlayerCharacter(GameObject):

    #how many tiles the character moves per second
    SPEED = 5
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #move function will move character up if direction > 0 and down if < 0
    def move(self, direction, max_height): #-Y = UP +Y=DOWN [i know, it's weird!]
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        # making sure that the character never goes past the bottom of the screen
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True
            
class NonPlayerCharacter(GameObject):

    #how many tiles the character moves per second
    SPEED = 3.5
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        if self.x_pos <= 20 :
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

        
pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

#quit pygame
pygame.quit()
quit()



