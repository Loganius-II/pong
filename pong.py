import pygame
from pygame.locals import *
import threading
import random
import time

SCREEN = (500,500)
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("Pong")

def fnt(fontsize) -> pygame.font.Font:
    try:
        return pygame.font.SysFont("Times New Roman", fontsize)
    except pygame.error:
        return
def ball(ball_x, ball_y, ball_dir, ball_up_or_down, ball_up_or_down_int) -> tuple[int, int, str, str, str]:
    global game_time, player1_score, player2_score, prev_game_time
    ball_attr = pygame.Rect(ball_x, ball_y, 30, 30)
    pygame.draw.rect(screen, (250, 0, 0), ball_attr, border_radius=50)
    set_new_dir = ball_dir  



    if ball_y <= 0:
        ball_up_or_down = 'down'
    elif ball_y >= SCREEN[0] -30:
        ball_up_or_down = 'up'
    elif ball_x >= 500:
        player1_score += 10
        if game_time > prev_game_time:
            prev_game_time = game_time
        game_time = 0
        ball_x = 250
        ball_y = 250
        pygame.time.delay(1000)
    elif ball_x <= 0:
        player2_score += 10
        if game_time > prev_game_time:
            prev_game_time = game_time
        game_time = 0
        ball_x = 250
        ball_y = 250
        pygame.time.delay(1000)
    if ball_dir == 'left':
        if ball_attr.colliderect(player1_attr):
            set_new_dir = 'right'  

        else:
            try:
                if game_time >= 5:
                    ball_x -= game_time
                else:
                    ball_x -= 4
            except:
                ball_x -= 4
            if ball_up_or_down == 'up':
                ball_y -= ball_up_or_down_int
            else:
                ball_y += ball_up_or_down_int

    elif ball_dir == 'right':
        if ball_attr.colliderect(player2_attr):
            set_new_dir = 'left'  
        else:
            try:
                if game_time >= 5:
                    ball_x += game_time
                else:    
                    ball_x += 4  
            except:
                ball_x += 4
            if ball_up_or_down == 'up':
                ball_y -= ball_up_or_down_int
            else:    
                ball_y += ball_up_or_down_int
    player_f = fnt(10)
    p1s = player_f.render(f"Player 1 Score: {player1_score}", True, (1,14,202))
    p2s = player_f.render(f"Player 2 Score: {player2_score}", True, (255,11,11))
    screen.blit(p1s, (50 - p1s.get_width() / 2, 20))
    screen.blit(p2s, (460 - p2s.get_width() / 2, 20))
    return ball_x, ball_y, set_new_dir, ball_attr, ball_up_or_down

    
def game_clock() -> str:
    global game_time
    game_time = 0
    while True:
        time.sleep(1)
        game_time += 1

        

def player_movement() -> None:
    p1y = 250
    p2y = 250
    ballx = 250
    bally = 250
    global player1_score, player2_score, prev_game_time
    prev_game_time = 0
    player1_score = 0
    player2_score = 0
    ball_up_or_down = random.choice(['up','down'])
    ball_up_or_down_int = random.randint(0,10)
    ball_directions = ['left', 'right']
    rand_direc = random.choice(ball_directions)
    loops = 0
    game_clock_thread = threading.Thread(target=game_clock, args=())
    game_clock_thread.start()
    while True:
        loops += 1
        clock.tick(60)
        try:
            screen.fill((255,255,255))
        except pygame.error:
            return
        global player2_attr, player1_attr
        player2_attr = pygame.Rect(470, p2y, 10,50)
        player1_attr = pygame.Rect(10, p1y, 10, 50 )
        pygame.draw.rect(
                    screen,
                    (0,0,0),
                    player2_attr,
                    border_radius=10
        )
        pygame.draw.rect(
                    screen,
                    (0,0,0),
                    player1_attr,
                    border_radius=10
        )
        if_pressed = pygame.key.get_pressed()
        if if_pressed[K_UP]:
            if p2y <= 0:
                pass
            else:
                p2y -= 10
        elif if_pressed[K_DOWN]:
            if p2y >= 445:
                pass
            else:
                p2y += 10
        if if_pressed[K_w]:
            
            if  p1y <= 0:
                pass
            else:
                p1y -= 10
        elif if_pressed[K_s]:
            if p1y >= 445:
                pass
            else:
                p1y += 10
        if loops != 1:
            if rand_direc2 == recent_direc:
                pass
            else:
                ball_up_or_down = random.choice(['up','down'])
                ball_up_or_down_int = random.randint(0,10)
            ballx, bally, rand_direc2, ball_attr, ball_up_or_down = ball(ballx, bally, rand_direc2, ball_up_or_down, ball_up_or_down_int)
            recent_direc = rand_direc2
        else:
            ballx, bally, rand_direc2, ball_attr, ball_up_or_down = ball(ballx, bally, rand_direc, ball_up_or_down, ball_up_or_down_int)
            recent_direc = rand_direc2
        game_clock_font = fnt(20)
        try:
            game_clock_surface = game_clock_font.render(f"{game_time}", True, (20,0,0))
        except:
            game_clock_surface = game_clock_font.render("Null", True, (0,0,0))
        screen.blit(game_clock_surface, (250 - game_clock_surface.get_width() / 2, 20))
        pygame.display.update()
        

def start_game() -> None:
    global player1_score, player2_score, prev_game_time
    with open('highscore.txt', 'r') as f:
        list = f.readlines()
        p1_high = list[1]
        p2_high = list[3]
        time_high = list[5]
    pygame.time.delay(500)
    big_font = fnt(50)
    not_as_big_font = fnt(25)
    screen.fill((0,0,0))
    text_surface = big_font.render("PONG", True, (255,255,255))
    screen.blit(text_surface, (250 - text_surface.get_width()/2, 50))
    pygame.display.update()
    pygame.time.delay(500)
    by_tag = not_as_big_font.render("By: Logan McDermott", True, (255,255,255))
    screen.blit(by_tag, (250 - by_tag.get_width()/2, 120))
    pygame.display.update()
    pygame.time.delay(500)
    scores_surface = big_font.render("Highest...", True, (255,255,255))
    scores_surface2 = not_as_big_font.render("Player 1 Score: " + p1_high, True, (1,172,202))
    scores_surface3 = not_as_big_font.render(f"Player 2 Score: " + p2_high, True, (1, 172,202))
    scores_surface4 = not_as_big_font.render(f"Longest Round " + time_high, True, (1,172,202))
    screen.blit(scores_surface, (250 - scores_surface.get_width() / 2, 150))
    screen.blit(scores_surface2, (250 - scores_surface2.get_width() / 2, 200))
    screen.blit(scores_surface3, (250 - scores_surface3.get_width() / 2, 250) )
    screen.blit(scores_surface4, (250 - scores_surface4.get_width() / 2, 300))
    pygame.display.update()
    pygame.time.delay(3000)
    player_thread = threading.Thread(target=player_movement, args=())
    player_thread.start()

    while True:
        for event in pygame.event.get():
                   
            if event.type == pygame.QUIT:
                
                with open('highscore.txt', 'r') as f:
                    lines = f.readlines()
                    high_p1s = int(lines[1])
                    high_p2s = int(lines[3])
                    highest_time = int(lines[5])

            
                if prev_game_time > highest_time:
                    highest_time = prev_game_time
                    if player1_score > high_p1s:
                        high_p1s = player1_score
                    if player2_score > high_p2s:
                        high_p2s = player2_score

                
                    with open('highscore.txt', 'w') as f:
                        f.write(f"player 1:\n{high_p1s}\nplayer 2:\n{high_p2s}\ntime:\n{highest_time}")
                pygame.quit()
                return

if __name__ == '__main__':
    start_game()