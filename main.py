import math
import pygame

from utils import blit_rotate_center, scale_img

GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)

TRACK = scale_img(pygame.image.load("imgs/track.png"),0.9)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (130,250)

RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"),0.55)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"),0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Racing Game!")
# -------------------------------------------------------------------------------------

FPS = 60
PATH = [(177, 112), (103, 62), (56, 148), (58, 448), (321, 741), (410, 659),
(412, 519), (554, 473), (596, 670), (676, 752), (746, 646),
 (739, 393), (422, 349), (454, 254), (728, 258), (722, 89), (301, 108),
 (285, 388), (172, 369), (167, 250)]
################## Classes #################
class AbstractCar:
    def __init__(self, max_vel, rotation_vel, start_pos):
        self.START_POS = start_pos
        self.img = pygame.Surface((10,10))
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = start_pos
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel+self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel-self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x), int(self.y-y))
        poi = mask.overlap(car_mask, offset)

        return poi

    def reset(self):
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS


class PlayerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, start_pos):
        super().__init__(max_vel, rotation_vel,start_pos)
        self.img = RED_CAR
        

    def reduce_speed(self):
        self.vel= max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel/2
        self.move()

class ComputerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel,start_pos, path=[]):
        super().__init__(max_vel, rotation_vel, start_pos)
        self.img = GREEN_CAR
       
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self,win):
        for point in self.path:
            pygame.draw.circle(win, (255,0,0), point, 5)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle >0:
            self.angle -=  min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle +=  min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point  >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()
    

################# FUNCTIONS ####################

def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    computer_car.draw(win)

    pygame.display.update()

def move_player(player_car: PlayerCar):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car: PlayerCar, computer_car: ComputerCar):
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POS)
    if computer_finish_poi_collide is not None:
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
    if player_finish_poi_collide is not None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()
            
#################################################

################ MAIN APP ####################

clock = pygame.time.Clock()

images=[(GRASS, (0,0)),(TRACK, (0,0)), (FINISH, FINISH_POS), (TRACK_BORDER, (0,0))]
run = True
player_car = PlayerCar(6,5,(180,200))
computer_car = ComputerCar(4,4, (150,200),PATH)



while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            break

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path .append(pos)
    
    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car)

print(computer_car.path)
pygame.quit()