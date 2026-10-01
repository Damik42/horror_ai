import pygame
import math
class HidingSpot:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.color = (0, 200, 0)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.x, self.y, self.width, self.height])
class Monster:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.state = "patrol"
        self.speed = 2
        self.waypoints = [(100, 100), (700, 100), (700, 500), (100, 500)]
        self.current_point_index = 0
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
    def update(self, player):
        dist_x = self.x - player.x
        dist_y = self.y - player.y
        distance = math.hypot(dist_x, dist_y)
        if self.state == "patrol":
            target_x, target_y = self.waypoints[self.current_point_index]
            if self.x < target_x:
                self.x += self.speed
            elif self.x > target_x:
                self.x -= self.speed
            if self.y < target_y:
                self.y += self.speed
            elif self.y > target_y:
                self.y -= self.speed
            if self.x == target_x and self.y == target_y:
                print("I am moving to the next point")
                self.current_point_index += 1
            if self.current_point_index >= len(self.waypoints):
                self.current_point_index = 0
            if distance < 150 and not player.is_hiding:
                print("I found you!")
                self.state = "chase"
                self.speed = 4
            else:
                self.state = "patrol"
        if self.state == "chase":
            if distance > 250 or player.is_hiding:
                print("I lost you!")
                self.state = "patrol"
                self.speed = 2
            if self.x < player.x:
                self.x += self.speed
            elif self.x > player.x:
                self.x -= self.speed
            if self.y < player.y:
                self.y += self.speed
            elif self.y > player.y:
                self.y -= self.speed



class Player:
    def __init__(self):
        self.is_hiding = False
        self.x = 400
        self.y = 300
        self.width = 40
        self.height = 40
        self.color = (0, 0, 255)
        self.speed = 5
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
    def toggle_hiding(self, hiding_spots):
        if self.is_hiding:
            self.is_hiding = False
            print("Игрок вышел из укрытия")
        else:
            for spot in hiding_spots:
                if (self.x < spot.x + spot.width and 
                    self.x + self.width > spot.x and 
                    self.y < spot.y + spot.height and 
                    self.y + self.height > spot.y):
                    
                    self.is_hiding = True
                    print("Игрок спрятался в укрытие!")
                    break
    def update(self,):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        elif keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        elif keys[pygame.K_d]:
            self.x += self.speed

                
spot1 = HidingSpot(200, 200, 60)
spots = [spot1]
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
clock = pygame.time.Clock()
hunter = Monster()
player = Player()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.toggle_hiding(spots)
    screen.fill((30, 30, 30))
    for spot in spots:
        spot.draw(screen)
    hunter.update(player)
    player.update()
    hunter.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
