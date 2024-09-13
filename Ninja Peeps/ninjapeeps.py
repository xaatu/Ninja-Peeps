import pygame
import random
import multiprocessing

# INITIALISE
pygame.init()


# SET UP SCREEN
screen_width = 800 
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ninja Peeps")

# DEFINE COLOURS
LIGHT_BLUE = (135, 206, 250) 
DARK_GREY = (100, 100, 100)
WHITE = (255, 255, 255)

# LOAD IMAGES
floor_image = pygame.image.load("images/floor2.png").convert_alpha()
floor_width = 100
floor_height = 100
floor_image = pygame.transform.scale(floor_image, (floor_width, floor_height))  # Set fixed width for tiling
peeps_images = [
    pygame.image.load("images/peeps1.png").convert_alpha(),
    pygame.image.load("images/peeps2.png").convert_alpha() 
    
]
peeps_width, peeps_height = 40, 100
peeps_images = [pygame.transform.scale(img, (peeps_width, peeps_height)) for img in peeps_images]

# LOAD WALKING WITH RIGHT AND LEFT ANIMATION
peeps_walk_right_images = [
    pygame.image.load("images/peepswalkright1.png").convert_alpha(),
    pygame.image.load("images/peepswalkright2.png").convert_alpha(),
    pygame.image.load("images/peepswalkright3.png").convert_alpha()
]
peeps_walk_left_images = [
    pygame.image.load("images/peepswalkleft1.png").convert_alpha(),
    pygame.image.load("images/peepswalkleft2.png").convert_alpha(),
    pygame.image.load("images/peepswalkleft3.png").convert_alpha()
]

# SCALE IMAGES
peeps_walk_right_images = [pygame.transform.scale(img, (peeps_width * 1.2, peeps_height)) for img in peeps_walk_right_images]
peeps_walk_left_images = [pygame.transform.scale(img, (peeps_width * 1.2, peeps_height)) for img in peeps_walk_left_images]

coin_images = [
    pygame.image.load("images/coin1.png").convert_alpha(),
    pygame.image.load("images/coin2.png").convert_alpha(),
    pygame.image.load("images/coin3.png").convert_alpha()
]
coin_width, coin_height = 30, 30
coin_images = [pygame.transform.scale(img, (coin_width, coin_height)) for img in coin_images]

catflap_images = [
    pygame.image.load("images/catflap1.png").convert_alpha(),
    pygame.image.load("images/catflap2.png").convert_alpha(),
    pygame.image.load("images/catflap3.png").convert_alpha(),
    pygame.image.load("images/catflap4.png").convert_alpha(),
    pygame.image.load("images/catflap5.png").convert_alpha(),
    pygame.image.load("images/catflap6.png").convert_alpha(),
    pygame.image.load("images/catflap7.png").convert_alpha(),
    pygame.image.load("images/catflap8.png").convert_alpha(),
    pygame.image.load("images/catflap9.png").convert_alpha()
]
catflap_width, catflap_height = 100, 100
catflap_images = [pygame.transform.scale(img, (catflap_width, catflap_height)) for img in catflap_images]

# LOAD CLOUD IMAGES
cloud_images = [
    pygame.image.load("images/cloud1.png").convert_alpha(),
    pygame.image.load("images/cloud2.png").convert_alpha(),
    pygame.image.load("images/cloud3.png").convert_alpha(),
    pygame.image.load("images/cloud4.png").convert_alpha()
]
cloud_width, cloud_height = 150, 100  
cloud_images = [pygame.transform.scale(img, (cloud_width, cloud_height)) for img in cloud_images]

# INIT LIST FOR CLOUDS
clouds = []





# PEEPS ATTRIBUTES
player_x = 100
player_y = screen_height - floor_height - peeps_height
player_velocity_y = 0
player_speed = 5
jump_strength = 16
gravity = 0.8
can_jump = True


score_font = pygame.font.SysFont(None, 30)

# GAME STATE
game_over = False
level_complete = False

# CAMERA POSITION
camera_x = 0

# GAME VARIABLES
score = 0

# FRAME RATE
clock = pygame.time.Clock()
FPS = 60

# COIN ANIMATION
coin_animation_speed = 12  # FPS
coin_frame_count = 0
coin_current_frame = 0

# CATFLAP ANIMATION
catflap_animation_speed = 12  # FPS
catflap_frame_count = 0
catflap_current_frame = 0

# PEEPS ANIMATION
peeps_animation_speed = 12  # FPS
peeps_frame_count = 0
peeps_current_frame = 0

coins = []  # INIT LIST FOR COINS
# LOAD COIN ANIMATION
coin_anim_images = [
    pygame.image.load("images/coin1.png").convert_alpha(),
    pygame.image.load("images/coin2.png").convert_alpha(),
    pygame.image.load("images/coin3.png").convert_alpha()
]
coin_anim_width, coin_anim_height = 30, 30
coin_anim_images = [pygame.transform.scale(img, (coin_anim_width, coin_anim_height)) for img in coin_anim_images]

# COIN ANIMATION VARIABLES
coin_anim_speed = 12  # FPS
coin_anim_frame_count = 0
coin_anim_current_frame = 0

# JUMPING ANIMATION IMAGES
peeps_jump_images = [
    pygame.image.load("images/peepjump1.png").convert_alpha(),
    pygame.image.load("images/peepjump2.png").convert_alpha(),
    pygame.image.load("images/peepjump3.png").convert_alpha(),
    pygame.image.load("images/peepjump4.png").convert_alpha(),
    pygame.image.load("images/peepjump5.png").convert_alpha(),
    pygame.image.load("images/peepjump6.png").convert_alpha(),
    pygame.image.load("images/peepjump7.png").convert_alpha(),
    pygame.image.load("images/peepjump8.png").convert_alpha(),
    pygame.image.load("images/peepjump9.png").convert_alpha(),
    pygame.image.load("images/peepjump10.png").convert_alpha()
]

# SCALING IMAGES
peeps_jump_images = [pygame.transform.scale(img, (peeps_width, peeps_height)) for img in peeps_jump_images]




# DEFINE LEVEL WIDTH
total_level_width = screen_width * 3
catflap_x = total_level_width - catflap_width



# COIN STARTING POINT AND SPACING
coin_start_x = player_x + 100  # START GENERATING 100PX TO RIGHT OF PEEPS

num_coins = 10

# DEFINE GAME STATE
game_over = False
level_complete = False
catflap_activated = False  # TRACK IF PLAYER HAS ENOUGH COINS TO GET THROUGH CATFLAP/START ANIMATION

# INIT VARIABLES FOR WALK TRACKING
walk_frame_count = 0
walk_current_frame = 0
walking_animation_speed = 12  # FPS
last_walk_update_time = pygame.time.get_ticks()
walk_frame_duration = 1000 // walking_animation_speed

# INIT VARIABLES FOR JUMP TRACKING
jump_frame_count = 0
jump_current_frame = 0
jumping_animation_speed = 12  # FPS
last_jump_update_time = pygame.time.get_ticks()
jump_frame_duration = 1000 // jumping_animation_speed

# LOAD PRESS SPACE IMAGES
press_space_images = [
    pygame.image.load("images/pressspace1.png").convert_alpha(),
    pygame.image.load("images/pressspace2.png").convert_alpha()
]
press_space_width, press_space_height = 300, 100  
press_space_images = [pygame.transform.scale(img, (press_space_width, press_space_height)) for img in press_space_images]



def level_one():
    
    global on_ground, player_velocity_y, camera_x, coin_frame_count, coin_current_frame, catflap_frame_count, catflap_current_frame, peeps_frame_count, peeps_current_frame, score, coins, level_complete, walk_frame_count, walk_current_frame, last_walk_update_time, jump_frame_count, jump_current_frame, last_jump_update_time, jumping  # Add 'jumping' to global variables

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ninja Peeps - Level 1")

    # INIT PLAYER POSITION AND SCORE
    player_x = 100  
    player_y = screen_height - floor_height - peeps_height  # MAKE SURE HE STARTS ON THE FLOOR
    score = 0  # INIT SCORE
    can_jump = True  # FROM LEVEL 2 PLAYER CAN JUMP FROM THE START (DOESN'T NEED TO GET UNLOCKED)

    # ANIMATION TIMING
    frame_rate = 12
    frame_duration = 1000 // frame_rate  


 

# SPACE TO JUMP
    def display_press_space_animation(screen, images, x, y):
        current_frame = 0
        frame_count = 0
        frame_rate = 12  
        frame_duration = 1000 // frame_rate
        last_update_time = pygame.time.get_ticks()

        running = True
        while running:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > frame_duration:
                last_update_time = current_time
                current_frame = (current_frame + 1) % len(images)
                screen.blit(images[current_frame], (x, y))
                pygame.display.flip()
                frame_count += 1
                if frame_count > frame_rate * 2:  
                    running = False

    # MAIN GAME LOOP
    running = True
    last_update_time = pygame.time.get_ticks()  

    walking_right = False
    walking_left = False
    jumping = False

    # LOAD PLATFORM IMAGE
    platform_image = pygame.image.load("images/platform.png").convert_alpha()
    platform_width, platform_height = 76 , 42  # PLATFORM DIMENSIONS
    platform_image = pygame.transform.scale(platform_image, (platform_width, platform_height))

    # DEFINE PLATFORMS (LEVEL 1)
    platforms = [
        (0, screen_height - 0),
      
    ]

    # DEFINE FISH (LEVEL 1)
    coins = [
        (325, screen_height - 150),
        (525, screen_height - 150),
        (725, screen_height - 150),
        (925, screen_height - 150),
        (1125, screen_height - 150),
        (1325, screen_height - 250),
        (1525, screen_height - 250),
        (1725, screen_height - 250),
        (1925, screen_height - 250),
        (2125, screen_height - 250)
    ]

    press_space_displayed = False  # PRESS SPACE ANIMATION FLAG

    while running:
        current_time = pygame.time.get_ticks()
        frame_time_elapsed = current_time - last_update_time
        walk_time_elapsed = current_time - last_walk_update_time
        jump_time_elapsed = current_time - last_jump_update_time

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        # KEY PRESS HANDLER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x = max(player_x - player_speed, camera_x)
            walking_left = True
            walking_right = False
        elif keys[pygame.K_RIGHT]:
            player_x = min(player_x + player_speed, camera_x + screen_width - peeps_width)
            walking_right = True
            walking_left = False
        else:
            walking_right = walking_left = False

        if keys[pygame.K_SPACE] and on_ground and can_jump:
            player_velocity_y = -jump_strength
            on_ground = False
            jumping = True
            jump_current_frame = 0  # RESET JUMP ANIMATION AT START OF JUMP

        # PLATFORM COLLISION DETECT
        player_rect = pygame.Rect(player_x, player_y, peeps_width * 0.5, peeps_height)
        on_ground = False  # ASSUME PLAYER IS NOT ON THE GROUND UNLESS ON PLATFORM
        for platform_x, platform_y in platforms:
            platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
            if player_rect.colliderect(platform_rect):
                # CHECK IF PLAYER IS COMING DOWN ONTO PLATFORM
                if player_velocity_y > 0 and player_y + peeps_height <= platform_y + platform_height:
                    # CORRECT PLAYER TO BE ON TOP OF PALTFORM
                    player_y = platform_y - peeps_height
                    on_ground = True
                    player_velocity_y = 0
                    jumping = False  # STOP JUMPING IF ON PLATFORM
                    jump_current_frame = 0  # RESET JUMP ANIMATION

        # IF PLAYER WALKS OF PLATFORM THEY FALL
        if not on_ground:
            player_velocity_y += gravity
            player_y += player_velocity_y

        # CHECK PLAYER COLLIDES WITH GROUND
        if player_y >= screen_height - floor_height - peeps_height:
            player_y = screen_height - floor_height - peeps_height
            on_ground = True
            player_velocity_y = 0
            jumping = False  # RESET JUMP WHEN LANDING

        # UPDATE CAMERA TO FOLLOW PLAYER BUT STOP AT END OF LEVEL
        camera_x = max(0, min(player_x - screen_width // 2, total_level_width - screen_width))

        # DISPLAY PRESS SPACE FLAG WHEN PLAYER REACHES HALFWAY
        if player_x >= total_level_width / 2 and not press_space_displayed:
            display_press_space_animation(screen, press_space_images, screen_width // 2 - press_space_width // 2, screen_height // 2 - press_space_height // 2)
            press_space_displayed = True  # ONLY TRIGGER ONCE

        # CHECK FOR COIN COLLECTION
        player_rect = pygame.Rect(player_x, player_y, peeps_width * 0.5, peeps_height)
        new_coins = [coin for coin in coins if not player_rect.colliderect(pygame.Rect(coin[0], coin[1], coin_width, coin_height))]
        coins = new_coins  # UPDATE COIN LIST 
        score = num_coins - len(coins)  # UPDATE SCORE WHEN COINS COLLECTED

        # CHECK PLAYER IS CLOSE ENOUGH TO END OF LEVEL AND HAS 10 POINTS SO THEY CAN MOVE ON
        if player_x >= total_level_width - 150 and score >= 10:
            level_two()  # START LEVEL 2
            running = False  # EXIT CURRENT GAME LOOP

        # ANIMATION UPDATES
        if frame_time_elapsed >= frame_duration:
            last_update_time = current_time
            coin_current_frame = (coin_current_frame + 1) % len(coin_images)
            if score >= 10:
                catflap_current_frame = (catflap_current_frame + 1) % len(catflap_images)
            peeps_current_frame = (peeps_current_frame + 1) % len(peeps_images)

        # UPDATE WALKING ANIMATION FRAME
        if walking_right or walking_left:
            if walk_time_elapsed >= walk_frame_duration:
                last_walk_update_time = current_time
                walk_current_frame = (walk_current_frame + 1) % len(peeps_walk_right_images)

        # UPDATE JUMPING ANIMATION FRAME
        if jumping:
            if jump_time_elapsed >= jump_frame_duration:
                last_jump_update_time = current_time
                jump_current_frame = (jump_current_frame + 2) % len(peeps_jump_images)

        # CLEAR SCREEN
        screen.fill(DARK_GREY)
        # DRAW ALL CLOUDS
        for cloud in clouds:
            screen.blit(cloud[2], (cloud[0] - camera_x, cloud[1]))

        # DRAW FLOOR
        for i in range(0, total_level_width, floor_width):
            screen.blit(floor_image, (i - camera_x, screen_height - floor_height))

        # DRAW COINS
        for coin in coins:
            screen.blit(coin_images[coin_current_frame], (coin[0] - camera_x, coin[1]))

        # DRAW CATFLAP
        screen.blit(catflap_images[catflap_current_frame], (total_level_width - catflap_width - camera_x, screen_height - floor_height - catflap_height))

        # COLLISION DETECTION
        catflap_rect = pygame.Rect(total_level_width - catflap_width - camera_x, screen_height - floor_height - catflap_height, catflap_width, catflap_height)
        if player_rect.colliderect(catflap_rect) and score >= 10:
            level_complete = True  # LEVEL COMPLETE
            running = False  # EXIT GAME LOOP

        # DRAW PLAYER WITH RIGHT ANIMATION
        if jumping:
            player_image = peeps_jump_images[jump_current_frame]
        elif walking_right:
            player_image = peeps_walk_right_images[walk_current_frame]
        elif walking_left:
            player_image = peeps_walk_left_images[walk_current_frame]
        else:
            player_image = peeps_images[peeps_current_frame]  # STANDING IMAGE

        screen.blit(player_image, (player_x - camera_x, player_y))

        # DRAW HUD (COINS)
        font = pygame.font.Font(None, 36)
        coin_text = font.render(f'Fish: {score}', True, WHITE)
        screen.blit(coin_text, (10, 10))

        # UPDATE DISPLAY
        pygame.display.flip()

        # FRAME RATE CAP
        clock.tick(60)

    pygame.quit()

def level_two():
    
    floor_image = pygame.image.load("images/floor.png").convert_alpha()
    floor_image = pygame.transform.scale(floor_image, (floor_width, floor_height))
    
    global on_ground, player_velocity_y, camera_x, coin_frame_count, coin_current_frame, catflap_frame_count, catflap_current_frame, peeps_frame_count, peeps_current_frame, score, coins, level_complete, walk_frame_count, walk_current_frame, last_walk_update_time, jump_frame_count, jump_current_frame, last_jump_update_time, jumping  # Add 'jumping' to global variables

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ninja Peeps - Level 2")

    # INIT PLAYER POSITION AND SCORE
    player_x = 100  # SET INIT POSITION
    player_y = screen_height - floor_height - peeps_height  # MAKE SURE PLAYER STARTS ON FLOOR!!
    score = 0  # INIT SCORE
    can_jump = True  # PLAYER CAN JUMP FROM START OF LEVEL 2

    # ANIMATION TIMING
    frame_rate = 12
    frame_duration = 1000 // frame_rate  

    # MAIN GAME LOOP
    running = True
    last_update_time = pygame.time.get_ticks()  

    walking_right = False
    walking_left = False
    jumping = False

    # LOAD PLATFORM IMAGE
    platform_image = pygame.image.load("images/platform.png").convert_alpha()
    platform_width, platform_height = 96 , 53  # Set platform dimensions
    platform_image = pygame.transform.scale(platform_image, (platform_width, platform_height))

    # DEFINE PLATFORMS FOR LEVEL 2
    platforms = [
        (300, screen_height - 200),
        (500, screen_height - 200),
        (700, screen_height - 200),
        (900, screen_height - 200),
        (1100, screen_height - 200),
        (1300, screen_height - 200),
        (1500, screen_height - 200),
        (1700, screen_height - 200),
        (1900, screen_height - 200),
        (2100, screen_height - 200)
    ]

    # DEFINE FISH FOR LEVEL 2
    coins = [
        (325, screen_height - 240),
        (525, screen_height - 240),
        (725, screen_height - 240),
        (925, screen_height - 240),
        (1125, screen_height - 240),
        (1325, screen_height - 240),
        (1525, screen_height - 240),
        (1725, screen_height - 240),
        (1925, screen_height - 240),
        (2125, screen_height - 240)
    ]

    press_space_displayed = False  

    while running:
        current_time = pygame.time.get_ticks()
        frame_time_elapsed = current_time - last_update_time
        walk_time_elapsed = current_time - last_walk_update_time
        jump_time_elapsed = current_time - last_jump_update_time

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        # KEY PRESS HANDLING
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x = max(player_x - player_speed, camera_x)
            walking_left = True
            walking_right = False
        elif keys[pygame.K_RIGHT]:
            player_x = min(player_x + player_speed, camera_x + screen_width - peeps_width)
            walking_right = True
            walking_left = False
        else:
            walking_right = walking_left = False

        if keys[pygame.K_SPACE] and on_ground and can_jump:
            player_velocity_y = -jump_strength
            on_ground = False
            jumping = True
            jump_current_frame = 0  # JUMP ANIMATION RESET

        # PLATFORM COLLISION DETECTION
        player_rect = pygame.Rect(player_x, player_y, peeps_width * 0.5, peeps_height)
        on_ground = False  # ASSUME PLAYER NOT ON GROUND UNLESS ON PLATFORM
        for platform_x, platform_y in platforms:
            platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
            if player_rect.colliderect(platform_rect):
                # CHECK IF PLAYER IS COMING DOWN ONTO PLATFORM
                if player_velocity_y > 0 and player_y + peeps_height <= platform_y + platform_height:
                    # CORRECT PLAYERS POSITION TO BE ONTOP OF PLATFORM
                    player_y = platform_y - peeps_height
                    on_ground = True
                    player_velocity_y = 0
                    jumping = False  # STOP JUMPING STATE IF PLAYER LANDS ON PLATFORM 
                    jump_current_frame = 0  # RESET JUMP ANIMATION FRAME

        # PLAYER WALK OFF PLATFORM
        if not on_ground:
            player_velocity_y += gravity
            player_y += player_velocity_y

        # PLAYER HITS FLOOR
        if player_y >= screen_height - floor_height - peeps_height:
            player_y = screen_height - floor_height - peeps_height
            on_ground = True
            player_velocity_y = 0
            jumping = False  # RRESET JUMP STATE

        # CAMERA FOLLOWS PLAYER BUT STOPS AT END OF LEVEL
        camera_x = max(0, min(player_x - screen_width // 2, total_level_width - screen_width))

        # COIN COLLECTION CHECK
        player_rect = pygame.Rect(player_x, player_y, peeps_width * 0.5, peeps_height)
        new_coins = [coin for coin in coins if not player_rect.colliderect(pygame.Rect(coin[0], coin[1], coin_width, coin_height))]
        coins = new_coins  
        score = num_coins - len(coins)  # UPDATE SCORE 

        # CHECK PLAYER HAS ENOUGH COINS AND IS IN RIGHT POSITION TO START LEVEL 3
        if player_x >= total_level_width - 150 and score >= 10 :
            level_three()  # START LEVEL 3
            running = False  # EXIT CURRENT GAME LOOP

        # ANIMATION UPDATES
        if frame_time_elapsed >= frame_duration:
            last_update_time = current_time
            coin_current_frame = (coin_current_frame + 1) % len(coin_images)
            if score >= 10:
                catflap_current_frame = (catflap_current_frame + 1) % len(catflap_images)
            peeps_current_frame = (peeps_current_frame + 1) % len(peeps_images)

        # UPDATE WALKING ANIMATION
        if walking_right or walking_left:
            if walk_time_elapsed >= walk_frame_duration:
                last_walk_update_time = current_time
                walk_current_frame = (walk_current_frame + 1) % len(peeps_walk_right_images)

        # UPDATE JUMPING ANIMATION
        if jumping:
            if jump_time_elapsed >= jump_frame_duration:
                last_jump_update_time = current_time
                jump_current_frame = (jump_current_frame + 2) % len(peeps_jump_images)

        # CLEAR SCREEN
        screen.fill(LIGHT_BLUE)

        # DRAW CLOUDS
        for cloud in clouds:
            screen.blit(cloud[2], (cloud[0] - camera_x, cloud[1]))

        # DRAW FLOOR
        for i in range(0, total_level_width, floor_width):
            screen.blit(floor_image, (i - camera_x, screen_height - floor_height))

        # DRAW COINS
        for coin in coins:
            screen.blit(coin_images[coin_current_frame], (coin[0] - camera_x, coin[1]))

        # DRAW CATFLAP
        screen.blit(catflap_images[catflap_current_frame], (total_level_width - catflap_width - camera_x, screen_height - floor_height - catflap_height))

        # DRAW PLATFORMS
        for platform in platforms:
            screen.blit(platform_image, (platform[0] - camera_x, platform[1]))

        # DRAW PLAYER WITH RIGHT ANIMATION
        if jumping:
            player_image = peeps_jump_images[jump_current_frame]
        elif walking_right:
            player_image = peeps_walk_right_images[walk_current_frame]
        elif walking_left:
            player_image = peeps_walk_left_images[walk_current_frame]
        else:
            player_image = peeps_images[peeps_current_frame]  # STANDING

        screen.blit(player_image, (player_x - camera_x, player_y))

        # DRAW HUD FOR COINS
        font = pygame.font.Font(None, 36)
        coin_text = font.render(f'Fish: {score}', True, WHITE)
        screen.blit(coin_text, (10, 10))

        # UPDATE DISPLAY
        pygame.display.flip()

        # FRAMERATE CAP
        clock.tick(60)

    pygame.quit()

def level_three():



    floor_image = pygame.image.load("images/floor.png").convert_alpha()
    floor_image = pygame.transform.scale(floor_image, (floor_width, floor_height))
    
    global on_ground, player_velocity_y, camera_x, coin_frame_count, coin_current_frame, catflap_frame_count, catflap_current_frame, peeps_frame_count, peeps_current_frame, score, coins, level_complete, walk_frame_count, walk_current_frame, last_walk_update_time, jump_frame_count, jump_current_frame, last_jump_update_time, jumping  # Add 'jumping' to global variables

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ninja Peeps - Level 3")

    # INIT PLAYER POSITION AND SCORE
    player_x = 100  # SET INIT POSITION
    player_y = screen_height - floor_height - peeps_height  # MAKE SURE PLAYER STARTS ON FLOOR
    score = 0  # INIT SCORE
    can_jump = True  # PLAYER CAN JUMP FROM START

    # ANIMATION TIMING
    frame_rate = 12
    frame_duration = 1000 // frame_rate  # Duration of each frame in milliseconds

    # MAIN GAME LOOP
    running = True
    last_update_time = pygame.time.get_ticks()  

    walking_right = False
    walking_left = False
    jumping = False

    # PLATFORM IMAGES
    platform_image = pygame.image.load("images/platform.png").convert_alpha()
    platform_width, platform_height = 96 , 53  # Set platform dimensions
    platform_image = pygame.transform.scale(platform_image, (platform_width, platform_height))

    # DEFINE PLATFORMS LEVEL 3
    platforms = [
        (300, screen_height - 170),
        (500, screen_height - 190),
        (700, screen_height - 210),
        (900, screen_height - 230),
        (1100, screen_height - 250),
        (1300, screen_height - 270),
        (1500, screen_height - 290),
        (1700, screen_height - 310),
        (1900, screen_height - 330),
        (2100, screen_height - 350),
        (2300, screen_height - 370)
        
    ]

    # DEFINE FISH LEVEL 3
    coins = [
        (325, screen_height - 210),
        (525, screen_height - 230),
        (725, screen_height - 250),
        (925, screen_height - 270),
        (1125, screen_height - 290),
        (1325, screen_height - 310),
        (1525, screen_height - 330),
        (1725, screen_height - 350),
        (1925, screen_height - 370),
        (2125, screen_height - 390)
    ]

    press_space_displayed = False  

    while running:
        current_time = pygame.time.get_ticks()
        frame_time_elapsed = current_time - last_update_time
        walk_time_elapsed = current_time - last_walk_update_time
        jump_time_elapsed = current_time - last_jump_update_time

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        # KEY PRESS HANDLER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x = max(player_x - player_speed, camera_x)
            walking_left = True
            walking_right = False
        elif keys[pygame.K_RIGHT]:
            player_x = min(player_x + player_speed, camera_x + screen_width - peeps_width)
            walking_right = True
            walking_left = False
        else:
            walking_right = walking_left = False

        if keys[pygame.K_SPACE] and on_ground and can_jump:
            player_velocity_y = -jump_strength
            on_ground = False
            jumping = True
            jump_current_frame = 0  # RESET JUMP ANIMATION WHEN STARTING JUMP

        # PLATFORM COLLISION
        player_rect = pygame.Rect(player_x, player_y, peeps_width * 0.5, peeps_height)
        on_ground = False  
        for platform_x, platform_y in platforms:
            platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
            if player_rect.colliderect(platform_rect):
                
                if player_velocity_y > 0 and player_y + peeps_height <= platform_y + platform_height:
                    
                    player_y = platform_y - peeps_height
                    on_ground = True
                    player_velocity_y = 0
                    jumping = False  
                    jump_current_frame = 0  

        # WALK OFF PLATFORM
        if not on_ground:
            player_velocity_y += gravity
            player_y += player_velocity_y

        # CHECK IF PLAYER HITS GROUND
        if player_y >= screen_height - floor_height - peeps_height:
            player_y = screen_height - floor_height - peeps_height
            on_ground = True
            player_velocity_y = 0
            jumping = False  # RESET JUMP WHEN LANDING

        # CAMERA FOLLOWS PLAYER BUT NOT PAST END OF LEVEL
        camera_x = max(0, min(player_x - screen_width // 2, total_level_width - screen_width))

        # COIN COLLECTION CHECK
        player_rect = pygame.Rect(player_x, player_y, peeps_width * 0.5, peeps_height)
        new_coins = [coin for coin in coins if not player_rect.colliderect(pygame.Rect(coin[0], coin[1], coin_width, coin_height))]
        coins = new_coins  
        score = num_coins - len(coins)  



        # ANIMATION UPDATES
        if frame_time_elapsed >= frame_duration:
            last_update_time = current_time
            coin_current_frame = (coin_current_frame + 1) % len(coin_images)
            if score >= 10:
                catflap_current_frame = (catflap_current_frame + 1) % len(catflap_images)
            peeps_current_frame = (peeps_current_frame + 1) % len(peeps_images)

        # UPDATE WALKING ANIMATION
        if walking_right or walking_left:
            if walk_time_elapsed >= walk_frame_duration:
                last_walk_update_time = current_time
                walk_current_frame = (walk_current_frame + 1) % len(peeps_walk_right_images)

        # UPDATE JUMPING ANIMATION
        if jumping:
            if jump_time_elapsed >= jump_frame_duration:
                last_jump_update_time = current_time
                jump_current_frame = (jump_current_frame + 2) % len(peeps_jump_images)

        # CLEAR SCREEN
        screen.fill(WHITE)

        # DRAW CLOUDS
        for cloud in clouds:
            screen.blit(cloud[2], (cloud[0] - camera_x, cloud[1]))

        # DRAW FLOOR
        for i in range(0, total_level_width, floor_width):
            screen.blit(floor_image, (i - camera_x, screen_height - floor_height))

        # DRAW COINS
        for coin in coins:
            screen.blit(coin_images[coin_current_frame], (coin[0] - camera_x, coin[1]))

        # DRAW CATFLAP
        screen.blit(catflap_images[catflap_current_frame], (2300 - camera_x, screen_height - 470))

        # END OF LEVEL CHECK
        if player_x >= total_level_width - 150 and screen_height * 0.5 and score >= 10:
            level_four()  # START LEVEL FOUR
            running = False  # EXIT CURRENT GAME LOOP

        # DRAW PLATFORMS
        for platform in platforms:
            screen.blit(platform_image, (platform[0] - camera_x, platform[1]))

        # DRAW PLAYER ANIMATION
        if jumping:
            player_image = peeps_jump_images[jump_current_frame]
        elif walking_right:
            player_image = peeps_walk_right_images[walk_current_frame]
        elif walking_left:
            player_image = peeps_walk_left_images[walk_current_frame]
        else:
            player_image = peeps_images[peeps_current_frame]  # STANDING

        screen.blit(player_image, (player_x - camera_x, player_y))

        # DRAW HUD FOR COINS
        font = pygame.font.Font(None, 36)
        coin_text = font.render(f'Fish: {score}', True, WHITE)
        screen.blit(coin_text, (10, 10))

        # UPDATE DISPLAY
        pygame.display.flip()

        # CAP FRAMERATE
        clock.tick(60)

def level_four():
    pygame.quit()
        

    pygame.quit()

    

    def main_game():
    # Existing main_game code...
        level_complete = False
    while not level_complete:
        # Existing game loop code...
        pass

pygame.quit() 

if __name__ == '__main__':
    main_game_process = multiprocessing.Process(target=level_one)
    main_game_process.start()
    main_game_process.join()  # Wait for the main game to finish before exiting the script
