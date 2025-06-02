import pygame
import constants
from items import Item
from characters import Characters

obstacles = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 66, 67]
door_close = [36, 37, 66, 67]

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacles_tiles = []
        self.lista_item = []
        self.list_enemy = []
        self.door_close_tiles = []
        self.exit_tile = None

    def process_data(self,data,tile_list, item_images, animations_enemies):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x,image_y)
                tile_data = [image, image_rect, image_x, image_y, tile]
                # Add tiles to obstacles
                if tile in obstacles:
                    self.obstacles_tiles.append(tile_data)
                    #self.exit_tile = None

                #
                if tile in door_close:
                    self.door_close_tiles.append(tile_data)
                # Exit's tile
                elif tile == 84:
                    self.exit_tile = tile_data

                # Create coins
                elif tile == 86:
                    coin = Item(image_x, image_y, 0, item_images[0])
                    self.lista_item.append(coin)
                    tile_data[0] = tile_list[22]

                # Create potion
                elif tile == 89:
                    posion = Item(image_x, image_y, 1, item_images[1])
                    self.lista_item.append(posion)
                    tile_data[0] = tile_list[22]

                # Create enemies
                elif tile == 75:
                    globi = Characters(image_x, image_y, animations_enemies[0], 60, 2)
                    tile_data[0] = tile_list[22]
                    self.list_enemy.append(globi)
                elif tile == 77:
                    orc = Characters(image_x, image_y, animations_enemies[1], 80, 2)
                    tile_data[0] = tile_list[22]
                    self.list_enemy.append(orc)
                self.map_tiles.append(tile_data)

    def change_door(self, player, tile_list):
        buffer = 50
        proximity_rect = pygame.Rect(player.shape.x - buffer, player.shape.y - buffer,
                                     player.shape.width + 2 * buffer, player.shape.height + 2 * buffer)
        for tile_data in self.map_tiles:
            image, rect, x, y, tile_type = tile_data
            if proximity_rect.colliderect(rect):
                if tile_type in door_close:
                    if tile_type == 36 or tile_type == 66:
                        new_tile_type = 57
                    elif tile_type == 37 or tile_type == 67:
                        new_tile_type = 58

                    tile_data[-1] = new_tile_type
                    tile_data[0] = tile_list[new_tile_type]

                    # Delete the tile from  the collision list
                    if tile_data in self.obstacles_tiles:
                        self.obstacles_tiles.remove(tile_data)


                    return True
        return False

    def update(self, position_screen):
        for tile in self.map_tiles:
            tile[2] += position_screen[0]
            tile[3] += position_screen[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])