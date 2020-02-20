import pygame
import random
tail_color=(254,128,80)
head_color=(255,251,0)
food_color=(255, 255, 255)
background_color=(65,179,128)
top_bar_color=(103, 72, 129)
square_size=15
displaySize=990,495
max_speed=20
genereal_border=100
top_bar_size=displaySize[0],45
way_list={"North":0,"South":1,"West":2,"East":3}
pygame.init()
myDisplay=pygame.display.set_mode((displaySize[0],displaySize[1]))
pygame.display.set_caption('Snake Game')
font_style = pygame.font.SysFont("bahnschrift", 25)
clock = pygame.time.Clock()

def draw_top_bar(tail_size,game_speed):

    pygame.draw.rect(myDisplay, top_bar_color, [0,0, top_bar_size[0],top_bar_color[1]])
    score = font_style.render("Score: " + str(tail_size), True, tail_color)
    myDisplay.blit(score, [genereal_border, top_bar_size[1]/2])
    speed=font_style.render("Speed: " + str(game_speed), True, tail_color)
    myDisplay.blit(speed, [displaySize[0]-2*genereal_border, top_bar_size[1]/2])


def draw_snake(snake_list):
    counter=0
    for x in snake_list:
        if counter==0:
            pygame.draw.rect(myDisplay, head_color, [x[0], x[1], square_size, square_size])
            counter += 1
        else:
            pygame.draw.rect(myDisplay, tail_color, [x[0], x[1], square_size, square_size])

def get_random_food_position(snake_point_list):
    food_x,food_y=get_random_pos()
    while check_rnd_point_in_snake(snake_point_list,food_x,food_y):
        food_x,food_y=get_random_pos()
    return food_x,food_y
def get_random_pos():
    food_x=random.randint(0,displaySize[0])
    food_x=food_x-(food_x % square_size)
    food_y=random.randint(top_bar_size[1]+2*square_size,displaySize[1])
    food_y=food_y-(food_y % square_size)
    return food_x,food_y
def check_rnd_point_in_snake(snake_point_list,food_x,food_y):
    for x in snake_point_list:
        if x[0]== food_x and x[1] == food_y:
            return True
        else:
            return False
def check_game_over(head_x,head_y,snake_point_list):
    if head_x < 0 or head_x >= displaySize[0] or head_y < top_bar_size[1]+2*square_size or head_y >= displaySize[1]:
        return True
    for x in snake_point_list:
        if x[0]== head_x and x[1] == head_y:
            return True
    return False
def show_message(msg, color):
    mesg = font_style.render(msg, True, color)
    myDisplay.blit(mesg, [displaySize[0] / 4, displaySize[1] /2])
def game_loop():
    game_over=False
    tail_size = 0
    game_speed = 1
    tick_speed = 8
    add_x=0
    add_y=0
    head_x=displaySize[0]/2-(displaySize[0]/2%square_size)
    head_y=displaySize[1]/2-(displaySize[1]/2%square_size)
    current_way=None
    snake_start_point=[head_x,head_y]
    snake_point_list=[]
    snake_point_list.append(snake_start_point)
    food_x,food_y=get_random_food_position(snake_point_list)
    myDisplay.fill(background_color)
    pygame.draw.rect(myDisplay, food_color, [food_x, food_y, square_size, square_size])
    draw_top_bar(tail_size, game_speed)
    draw_snake(snake_point_list)
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not current_way == way_list["East"]:
                    current_way=way_list["West"]
                    add_x = -square_size
                    add_y = 0
                elif event.key == pygame.K_RIGHT and not current_way == way_list["West"]:
                    current_way = way_list["East"]
                    add_x=square_size
                    add_y=0
                elif event.key == pygame.K_UP and not current_way == way_list["South"]:
                    current_way = way_list["North"]
                    add_x=0
                    add_y=-square_size
                elif event.key == pygame.K_DOWN and not current_way == way_list["North"]:
                    current_way = way_list["South"]
                    add_x=0
                    add_y=square_size
        if not current_way == None:
            head_x+=add_x
            head_y+=add_y
            if check_game_over(head_x,head_y,snake_point_list):
                myDisplay.fill(background_color)
                show_message("Score : %d  Press R - Play Again or Q - Quit" %(tail_size),tail_color)
                game_over=True
                pygame.display.update()
                break
            snake_point_list.insert(0,[head_x,head_y])
            if food_x == head_x and food_y == head_y:
                food_x, food_y = get_random_food_position(snake_point_list)
                tail_size+=1
                if tail_size %3 == 0 and game_speed < max_speed:
                    tick_speed+=1
                    game_speed+=1
            else:
                snake_point_list.remove(snake_point_list.__getitem__(snake_point_list.__len__()-1))
            myDisplay.fill(background_color)
            pygame.draw.rect(myDisplay,food_color,[food_x,food_y,square_size,square_size])
            draw_top_bar(tail_size, game_speed)
            draw_snake(snake_point_list)
            pygame.display.update()
            clock.tick(tick_speed)
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    game_loop()

game_loop()
