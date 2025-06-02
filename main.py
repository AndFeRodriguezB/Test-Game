import pygame
import constants
from characters import Characters
from weapon import Weapon
from texts import DamageText
from items import Item
from world import World
import csv
import os

# Functions
# Scale images
def escalar_img(image,scale):
    w = image.get_width()
    h = image.get_height()
    new_image = pygame.transform.scale(image,(w*scale, h*scale))
    return new_image

# Function to count elements
def count_elements(directorio):
    return len(os.listdir(directorio))

# Function to list element names
def names_folders(directorio):
    return os.listdir(directorio)

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH_SCREEN,
                                  constants.HEIGHT_SCREEN))
pygame.display.set_caption("Games")

# Variables
position_screen = [0,0]
level = 1

# Fonts
font = pygame.font.Font("assets//fonts//antiquity.ttf", 25)
font_game_over = pygame.font.Font("assets//fonts//antiquity.ttf", 100)
font_restart = pygame.font.Font("assets//fonts//antiquity.ttf", 25)
font_start = pygame.font.Font("assets//fonts//antiquity.ttf", 25)
font_title = pygame.font.Font("assets//fonts//antiquity.ttf", 75)


game_over_text = font_game_over.render('Game over', True, constants.WHITE)
restart_text = font_restart.render("Restart", True, constants.BLACK)

# Start bottoms
button_play = pygame.Rect(constants.WIDTH_SCREEN / 2 - 100,
                          constants.HEIGHT_SCREEN / 2 - 50, 150, 50)
button_exit = pygame.Rect(constants.WIDTH_SCREEN / 2 - 100,
                          constants.HEIGHT_SCREEN / 2 + 50, 150, 50)
play_text = font_start.render("Play", True, constants.BLACK)
exit_text = font_start.render("Exit", True, constants.BLACK)

# Start screen
def start_screen():
    screen.fill(constants.PURPLE)
    draw_text("Test Game", font_title, constants.WHITE,
              constants.WIDTH_SCREEN / 2 - 250,
              constants.HEIGHT_SCREEN / 2  - 200)
    pygame.draw.rect(screen, constants.YELLOW, button_play)
    pygame.draw.rect(screen, constants.YELLOW, button_exit)
    screen.blit(play_text, (button_play.x + 40, button_play.y + 8))
    screen.blit(exit_text, (button_exit.x + 40, button_exit.y + 8))
    pygame.display.update()

# Import Images
# Energy
heart_empty = pygame.image.load("assets/images/items/heart_empty.png")
heart_empty = escalar_img(heart_empty, constants.SCALA_HEART)
heart_half = pygame.image.load("assets/images/items/heart_half.png")
heart_half = escalar_img(heart_half, constants.SCALA_HEART)
heart_full = pygame.image.load("assets/images/items/heart_full.png")
heart_full = escalar_img(heart_full, constants.SCALA_HEART)

# Character
animations = []
for i in range(10):
    img = pygame.image.load(f"assets//images//characters//player//run{i}.png")
    img = escalar_img(img, constants.SCALE_CHARACTER)
    animations.append(img)

# Enemies
directory_enemies = "assets/images/characters/enemies"
type_enemies = names_folders(directory_enemies)
animations_enemies = []
for eni in type_enemies:
    list_temp = []
    ruta_temp = f"assets/images/characters/enemies//{eni}"
    num_animations = count_elements(ruta_temp)
    for i in range(num_animations):
        img_enemy = pygame.image.load(f"{ruta_temp}//{eni}{i}.png")
        img_enemy = escalar_img(img_enemy,constants.SCALE_ENEMIES)
        list_temp.append(img_enemy)
    animations_enemies.append(list_temp)

# Weapon
image_gun = pygame.image.load("assets//images//weapons//gun.png")
image_gun = escalar_img(image_gun, constants.SCALE_GUN)

# Bullet
image_bullet = pygame.image.load("assets//images//weapons//bullet.png")
image_bullet = escalar_img(image_bullet, constants.SCALE_BULLET)

# Upload images of the world
tile_list = []
for x in range(constants.TILE_TYPE):
    tile_image = pygame.image.load(f"assets//images//tiles//tile ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# Upload images of the items
potions = pygame.image.load("assets//images//items//potion.png")
potions = escalar_img(potions, constants.SCALA_POTION)

coin_images = []
ruta_img = "assets//images//items//coin"
num_coin_images = count_elements(ruta_img)
for i in range(num_coin_images):
    img = pygame.image.load(f"assets//images//items//coin//coin_{i+1}.png")
    img = escalar_img(img, 1)
    coin_images.append(img)

item_images = [coin_images, [potions]]

def draw_text(texto, fuente, color, x ,y):
    img = fuente.render(texto, True, color)
    screen.blit(img, (x,y))

def life_player():
    h_half_printed = False
    for i in range(4):
        if player.energy >= ((i+1)*25):
            screen.blit(heart_full, (i*50, 5))
        elif player.energy % 25 > 0 and h_half_printed == False:
            screen.blit(heart_half, (i*50, 5))
            h_half_printed = True
        else:
            screen.blit(heart_empty, (i*50,5))

def reset_world():
    group_damage_text.empty()
    group_bullets.empty()
    group_items.empty()

    # Create a tile list empty
    data = []
    for row in range(constants.ROWS):
        rows = [2] * constants.COLUMNS
        data.append(rows)
    return data

world_data = []

for row in range(constants.ROWS):
    rows = [19] * constants.COLUMNS
    world_data.append(rows)

# Upload level's file
with open("levels/level_1.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, column in enumerate(row):
            world_data[x][y] = int(column)

world = World()
world.process_data(world_data, tile_list, item_images, animations_enemies)


def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZES, 0),(x * constants.TILE_SIZES, constants.HEIGHT_SCREEN))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZES), (constants.WIDTH_SCREEN, x * constants.TILE_SIZES))

# Create a player from the character class
player = Characters(80,80, animations, 100, 1)

# Create an enemies list
list_enemies = []
for ene in world.list_enemy:
    list_enemies.append(ene)

# Create a weapon from the weapon class
gun = Weapon(image_gun, image_bullet)

# Create a group of sprites
group_damage_text = pygame.sprite.Group()
group_bullets = pygame.sprite.Group()
group_items = pygame.sprite.Group()

# Add items from the level's data
for item in world.lista_item:
    group_items.add(item)

coin = Item(380, 300, 0 , coin_images)
potion = Item(380, 200, 1, [potions])

group_items.add(coin)
#group_items.add(potion)


# Define the player's movement variables
move_up = False
move_down = False
move_left = False
move_right = False

# Check the frame rate
clock = pygame.time.Clock()

# Restart bottom
bottom_restart = pygame.Rect(constants.WIDTH_SCREEN / 2 - 100,
                             constants.HEIGHT_SCREEN / 2 + 150, 200, 50)

show_start = True

running = True
while running:
    if show_start:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    show_start = False
                if button_exit.collidepoint(event.pos):
                    running = False
    else:
        # That goes at 60 FPS
        clock.tick(constants.FPS)
        screen.fill(constants.PURPLE)

        if player.life:
            # Calculate the player's movement
            delta_x = 0
            delta_y = 0

            if move_right == True:
                delta_x = constants.SPEED
            if move_left == True:
                delta_x = -constants.SPEED
            if move_up == True:
                delta_y = -constants.SPEED
            if move_down == True:
                delta_y = constants.SPEED

            # Player movement
            position_screen, level_completed = player.movement(delta_x, delta_y, world.obstacles_tiles,
                                              world.exit_tile)

            # Update map
            world.update(position_screen)

            # Update player status
            player.update()

            # Update enemy status
            for ene in list_enemies:
                ene.update()

            # Update weapon status
            bullet = gun.update(player)
            if bullet:
                group_bullets.add(bullet)
            for bullet in group_bullets:
                damage, pos_damage = bullet.update(list_enemies, world.obstacles_tiles)
                if damage:
                    damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constants.RED)
                    group_damage_text.add(damage_text)

            # Update damage
            group_damage_text.update(position_screen)

            # Update items
            group_items.update(position_screen, player)

        # Draw world
        world.draw(screen)

        # Draw the player
        player.draw(screen)

        # Draw the enemy
        for ene in list_enemies:
            if ene.energy == 0:
                list_enemies.remove(ene)
            if ene.energy > 0:
                ene.enemies(player, world.obstacles_tiles, position_screen,
                            world.exit_tile)
                ene.draw(screen)

        # Draw the weapon
        gun.draw(screen)

        # Draw bullet
        for bullet in group_bullets:
            bullet.draw(screen)

        # Draw hearts
        life_player()
        # Draw texts
        group_damage_text.draw(screen)
        draw_text(f"score: {player.score}", font, (255,255,0), 665, 5)
        # Level
        draw_text(f" Level: " + str(level), font, constants.WHITE, constants.WIDTH_SCREEN/2, 5)

        # Draw Items
        group_items.draw(screen)

        # Check if the level is completed
        if level_completed == True:
            if level < constants.MAX_LEVEL:
                level += 1
                world_data = reset_world()

                # Upload level's file
                with open(f"levels/level_{level}.csv", newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, column in enumerate(row):
                            world_data[x][y] = int(column)
                world = World()
                world.process_data(world_data, tile_list, item_images, animations_enemies)
                player.update_coordinates(constants.COORDINATES[str(level)])

                # Create an enemies list
                list_enemies = []
                for ene in world.list_enemy:
                    list_enemies.append(ene)

                # Add items from the level's data
                for item in world.lista_item:
                    group_items.add(item)

        if player.life == False:
            screen.fill(constants.DARK_RED)
            text_rect = game_over_text.get_rect(center=(constants.WIDTH_SCREEN / 2,
                                                        constants.HEIGHT_SCREEN / 2))
            screen.blit(game_over_text, text_rect)

            pygame.draw.rect(screen, constants.YELLOW, bottom_restart)
            screen.blit(restart_text, (bottom_restart.x + 40, bottom_restart.y + 8))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_w:
                    move_up = True
                if event.key == pygame.K_s:
                    move_down = True
                if event.key == pygame.K_e:
                    if world.change_door(player, tile_list):
                        print("puerta cambiada")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_s:
                    move_down = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bottom_restart.collidepoint(event.pos) and not player.life:
                    player.life = True
                    player.energy = 100
                    player.score = 0
                    level = 1
                    world_data = reset_world()
                    with open(f"levels/level_{level}.csv", newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, column in enumerate(row):
                                world_data[x][y] = int(column)
                    world = World()
                    world.process_data(world_data, tile_list, item_images, animations_enemies)
                    player.update_coordinates(constants.COORDINATES[str(level)])

                    list_enemies = []
                    for ene in world.list_enemy:
                        list_enemies.append(ene)

                    for item in world.lista_item:
                        group_items.add(item)

        pygame.display.update()
pygame.quit()