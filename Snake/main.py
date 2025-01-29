from ast import excepthandler
import sys
import random
import pickle
import pygame
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.x = random.randint(0, 14)
        self.y = random.randint(0, 14)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 140), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, 14)
        self.y = random.randint(0, 14)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        # importing snake graphics
        self.head_up = pygame.image.load('./Snake/graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('./Snake/graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('./Snake/graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('./Snake/graphics/head_left.png').convert_alpha()

        self.tail_down = pygame.image.load('./Snake/graphics/tail_up.png').convert_alpha()
        self.tail_up = pygame.image.load('./Snake/graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('./Snake/graphics/tail_right.png').convert_alpha() 
        self.tail_right = pygame.image.load('./Snake/graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('./Snake/graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('./Snake/graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('./Snake/graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('./Snake/graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('./Snake/graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('./Snake/graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # we need  a rect for postitioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # what direction is the head facing
            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else:
                # to get relation
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rect)


    def update_head_graphics(self):
        head_relation = self.body[0]- self.body[1]
        # head direction to the right
        if head_relation == Vector2(1, 0): self.head = self.head_right         
        # head direction to the left
        elif head_relation == Vector2(-1, 0): self.head = self.head_left 
        # head direction to the up
        elif head_relation == Vector2(0, -1): self.head = self.head_up 
        # head direction to the down    
        elif head_relation == Vector2(0, 1): self.head = self.head_down 
        
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1, 0): self.tail = self.tail_right
        if tail_relation == Vector2(-1, 0): self.tail = self.tail_left
        if tail_relation == Vector2(0, -1): self.tail = self.tail_up
        if tail_relation == Vector2(0, 1): self.tail = self.tail_down

        # for block in self.body:
        #     x_pos = int(block.x * cell_size)
        #     y_pos = int(block.y * cell_size)
        #     snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        #     pygame.draw.rect(screen, (183, 111, 122), snake_rect)

    def move_snake(self):
        if self.new_block:          # if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:                       # elif self.new_block == False:
            body_copy = self.body[:-1]

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_block(self):
        self.new_block = True
       

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.check_overlap()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            print("snek munch:>")
            self.fruit.randomize()
            self.snake.add_block()

    def check_overlap(self):
        if self.fruit.pos in self.snake.body:
            self.fruit.randomize()
                
    def draw_grass(self):
        grass_color = (167, 209, 61)

        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

            else:
                for row in range(cell_number):
                    if row % 2 != 0:
                        for column in range(cell_number):
                            if column % 2 != 0:
                                grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                                pygame.draw.rect(screen, grass_color, grass_rect)

    def check_fail(self):
            # check if snake hits the boundary:
            # if below conditions are True then snake is inside the boundary(these conditions return True)
            # but if they are False then the snake is outside(these conditions return False)
            x_condition = 0 <= self.snake.body[0].x < cell_number
            y_condition = 0 <= self.snake.body[0].y < cell_number
            
            # not True => False ,, not False => True
            if not x_condition or not y_condition:
                print("You hit a wall!")
                self.game_over()
                

            # check if snake hits itself:
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    print("You hit yourself ;-;")
                    self.game_over()

    def game_over(self):
        print("GAME OVER")
        self.save_score()
        pygame.quit()
        sys.exit()

    def save_score(self):
        self.score = len(self.snake.body) -3
        try:
            with open('score.txt', 'r') as f:
                self.highScore = f.read()
        except:
            print(f"\nScore: {self.score}\n")
            with open('score.txt', 'w') as f:
                f.write(str(self.score))
        else:
            if self.score > int(self.highScore):
                print("\n You beat the highscore!")
                print(f"New high score: {self.score}\n")
                with open('score.txt', 'w') as f:
                    f.write(str(self.score))
            
            else:
                print(f"Score: {self.score}")
        # try:
        #     with open('score.dat', 'rb') as f:
        #         self.highScore = pickle.load(f)
        #         print("High score loaded")
        # except:
        #     print(f"\nScore: {self.score}\n")
        #     with open('score.dat', 'wb') as f:
        #         pickle.dump(self.score, f)
        # else:
        #     if self.score > self.highScore:
        #         print("\nYou beat the highscore!")
        #         print(f"New high score: {self.score}\n")
        #         with open('score.dat', 'wb') as f:
        #             pickle.dump(self.score, f)
        #     else:
                #   print(f"Score: {self.score}")


pygame.init()

cell_size = 40
cell_number = 17
# screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('./Snake/graphics/apple.png').convert_alpha()

# creating custom event
SCREEN_UPDATE = pygame.USEREVENT
# timer; SCREEN_UPDATE works every 150 ms
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # pygame.quit() is not enough bc some parts of the program might still be running, so we use sys.exit() too
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)