import pygame, sys ,time, random
from button import Button

pygame.init()
window_x = 600
window_y = 400 
SCREEN = pygame.display.set_mode((window_x,window_y))
pygame.display.set_caption("MiniGames")

#General things 
#colors
main_color = "#b68f40"
secondary_color = "#d1caca"

#background image
BG = pygame.image.load("assets/Background.png")

#for background sound
pygame.mixer.init()
BGMUSIC = pygame.mixer.Sound("assets/bgmusic3.mp3")
BGMUSIC.set_volume(.3)
HITSOUND = pygame.mixer.Sound("assets/hit.wav")
FOODSOUND = pygame.mixer.Sound("assets/food.wav")
SNAKEBGSOUND = pygame.mixer.Sound("assets/bg_music_1.mp3")

##This is for the font and size
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

#For the Snake Game colors
foodColor = pygame.Color(238, 238, 238)
bgColor = pygame.Color(19, 75, 112)
snakeColor = pygame.Color(80, 140, 155)
fps = pygame.time.Clock()

#for snake properties
snake_speed = 15
snake_position = [100,50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

#Define food properties
food_position = [random.randrange(1,(window_x // 10))*10,random.randrange(1,(window_y // 10))*10]
food_spawn = True

#Set initial direction
direction = 'RIGHT'
change_to = direction

#Initial Score
score = 0

#Function to display score
def showScore_for_snake (choice,color,font,size):
    score_font = pygame.font.SysFont(font,size)
    score_surface = score_font.render('Score : '+str(score),True,color)
    score_rect = score_surface.get_rect()
    SCREEN.blit(score_surface, score_rect)

#Game_over function with play again features
def game_over_for_snake():
    pygame.display.set_caption("GAME OVER")
    SNAKEBGSOUND.stop()
    HITSOUND.play()
    game_over_surface = get_font(40).render('GAME OVER',True,"#b68f40")
    game_over_surface1 =  get_font(25).render(f'Your score is : {score}',True,"#b68f40")
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (300,150)
    game_over_rect1 = game_over_surface1.get_rect()
    game_over_rect1.midtop = (300,210)
    SCREEN.blit(game_over_surface,game_over_rect)
    SCREEN.blit(game_over_surface1,game_over_rect1)
    pygame.display.flip()
    time.sleep(2)
    playagain_or_quit_for_snake()

#Playagain or back to main menu or quit
def playagain_or_quit_for_snake():
    pygame.display.set_caption("Play Again or Quit")
    BGMUSIC.play()

    #Ask the user if they want to play again or quit
    while True:
        CHOOSE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(bgColor)
        SCREEN.blit(BG, (0, 0))
        
        PLAY_AGAIN_BUTTON = Button(image=None, pos=(300, 170),text_input="Play Again", font=get_font(20), base_color="White", hovering_color="#b68f40")
        MENU_BUTTON = Button(image=None, pos=(300, 220),text_input="Back to MENU", font=get_font(20), base_color="White", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=None, pos=(300, 270),text_input="Quit", font=get_font(20), base_color="White", hovering_color="#b68f40")

        for button in [PLAY_AGAIN_BUTTON, QUIT_BUTTON,MENU_BUTTON]:
            button.changeColor(CHOOSE_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                    play_snake()
                if MENU_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                    BGMUSIC.stop()
                    main_menu()
                if QUIT_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

#main play snake game function
def play_snake():
    pygame.display.set_caption("SNAKE GAME")
    BGMUSIC.stop()
    SNAKEBGSOUND.play()
    global snake_position,snake_body,food_position,food_spawn,direction,change_to,score
    
    #Reset game variables
    snake_position = [100,50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    food_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not direction == 'DOWN':
                        direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    if not direction == 'UP':
                        direction = 'DOWN'
                elif event.key == pygame.K_RIGHT:
                    if not direction == 'LEFT':
                        direction = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    if not direction == 'RIGHT':
                        direction = 'LEFT'  

        #if snake is moving in the direction, change to that direction
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10
        
        #snake body growing mechanism
        snake_body.insert(0,list(snake_position))
        if snake_position == food_position:
            score += 1
            FOODSOUND.play()
            food_spawn = False
        else:
            snake_body.pop()
        
        if not food_spawn:
            food_position = [random.randrange(1,(window_x//10))*10,random.randrange(1,(window_y//10))*10]
        food_spawn = True

        #background
        SCREEN.fill(bgColor)
        SCREEN.blit(BG, (0, 0))

        #Draw snake
        for pos in snake_body:
            pygame.draw.rect(SCREEN,snakeColor,pygame.Rect(pos[0],pos[1],10,10))
        
        #Draw food 
        pygame.draw.rect(SCREEN,foodColor,pygame.Rect(food_position[0],food_position[1],10,10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            return game_over_for_snake()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            return game_over_for_snake()

        for block in snake_body[1:]:
            if snake_position == block:
                return game_over_for_snake()

        # Display score
        showScore_for_snake(1, "white", 'assets/font.tff', 20)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)
        
#For tic tac toe game
#Board setup
RED = pygame.Color(255,0,0)
board = [' ' for _ in range(9)]
player = 'X'
computer = 'O'
current_turn = player
computer_move_time = None  # Timer for computer's move   

# Draw the grid
def draw_grid():
    SCREEN.fill("WHITE")
    SCREEN.blit(BG,(0,0))
    pygame.draw.line(SCREEN, main_color, (200, 0), (200, 400), 5)
    pygame.draw.line(SCREEN, main_color, (400, 0), (400, 400), 5)
    pygame.draw.line(SCREEN, main_color, (0, 133), (600, 133), 5)
    pygame.draw.line(SCREEN, main_color, (0, 266), (600, 266), 5)

# Draw the marks (X and O)
def draw_marks():
    for i in range(9):
        x = (i % 3) * 200 + 100
        y = (i // 3) * 133 + 66
        if board[i] == 'X':
            pygame.draw.line(SCREEN, RED, (x - 50, y - 50), (x + 50, y + 50), 10)
            pygame.draw.line(SCREEN, RED, (x + 50, y - 50), (x - 50, y + 50), 10)
        elif board[i] == 'O':
            pygame.draw.circle(SCREEN, secondary_color, (x, y), 50, 10)

# Check for a win or draw
def check_winner():
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

# Computer makes a move (random for simplicity)
def computer_move():
    empty_cells = [i for i, mark in enumerate(board) if mark == ' ']
    if empty_cells:
        move = random.choice(empty_cells)
        board[move] = computer

# Display the result
def display_winner(winner):
    SCREEN.fill("white")
    SCREEN.blit(BG,(0,0))
    if winner == 'X':
        text = get_font(25).render("Player Wins!", True, RED)
    elif winner == 'O':
        text = get_font(25).render("Computer Wins!", True, secondary_color)
    else:
        text = get_font(25).render("It's a Draw!", True, "White")
    SCREEN.blit(text, (window_x // 2 - text.get_width() // 2, window_y // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Get the cell index based on mouse position
def get_cell_index(pos):
    x, y = pos
    row = y // 133
    col = x // 200
    return row * 3 + col

def play_tic_tac():
    pygame.display.set_caption("Tic tac toe game")
    BGMUSIC.stop()
    SNAKEBGSOUND.play()
    global current_turn, computer_move_time
    game_over = False

    while True:
        draw_grid()
        draw_marks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_turn == player:
                pos = pygame.mouse.get_pos()
                cell_index = get_cell_index(pos)
                if board[cell_index] == ' ':
                    board[cell_index] = player
                    FOODSOUND.play()
                    current_turn = computer
                    computer_move_time = pygame.time.get_ticks()  # Start the 2-second timer

        # Handle computer's move with a 2-second delay
        if current_turn == computer and not game_over:
            if computer_move_time and pygame.time.get_ticks() - computer_move_time >= 2000:  # 2 seconds delay
                computer_move()
                current_turn = player
                computer_move_time = None  # Reset the timer

        winner = check_winner()
        if winner:
            SNAKEBGSOUND.stop()
            display_winner(winner)
            board[:] = [' ' for _ in range(9)]  # Reset board
            current_turn = player
            game_over = True
            playagain_or_quit_for_tic_tac_toe()
        pygame.display.update()

#play again or quit function
def playagain_or_quit_for_tic_tac_toe ():
    pygame.display.set_caption("Play Again or Quit")
    BGMUSIC.play()
    #Ask the user if they want to play again or quit
    while True:
        CHOOSE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(bgColor)
        SCREEN.blit(BG, (0, 0))
        
        PLAY_AGAIN_BUTTON = Button(image=None, pos=(300, 170),text_input="Play Again", font=get_font(20), base_color="White", hovering_color="#b68f40")
        MENU_BUTTON = Button(image=None, pos=(300, 220),text_input="Back to MENU", font=get_font(20), base_color="White", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=None, pos=(300, 270),text_input="Quit", font=get_font(20), base_color="White", hovering_color="#b68f40")

        for button in [PLAY_AGAIN_BUTTON, QUIT_BUTTON,MENU_BUTTON]:
            button.changeColor(CHOOSE_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                    play_tic_tac()
                if MENU_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                    BGMUSIC.stop()
                    main_menu()
                if QUIT_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

#The Main Function of two games
def main_menu():
    pygame.display.set_caption("Main Menu")

    while True:
        SCREEN.fill("black")
        SCREEN.blit(BG, (0, 0))
        BGMUSIC.play()
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 80))

        PLAY_SNAKE_BUTTON = Button(image=None, pos=(300, 180), text_input="PLAY SNAKE GAME", font=get_font(20), base_color="#d7fcd4", hovering_color="#b68f40")
        PLAY_TICTAC_BUTTON = Button(image=None, pos=(300, 230), text_input="PLAY TIC TAC TOE", font=get_font(20), base_color="#d7fcd4", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=None, pos=(300, 280), text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="#b68f40")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_SNAKE_BUTTON, PLAY_TICTAC_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_SNAKE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_snake()
                if PLAY_TICTAC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_tic_tac()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
