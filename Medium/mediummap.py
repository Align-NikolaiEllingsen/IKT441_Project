import random
import math
import numpy as np

import pygame
from pygame.color import THECOLORS

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions

import os

#os.environ["SDL_VIDEODRIVER"] = "dummy" # Used when training on server since there is no "screen"

# PyGame init
width = 1000
height = 700
fps = 9999
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
screen.set_alpha(None)

# Small hack to convert chipmunk physics to pygame coordinates
def coordfix(y):
    return -y+height

def draw(screen, space):
    space.debug_draw(DrawOptions(screen))

class GameState:
    def __init__(self, display_hidden=False):

        # Load sprite
        sprite = pygame.image.load("../ar19_q.png")
        self.sprite_img = pygame.transform.scale(sprite, (50,50))
        self.sprites = []
        
        self.show_sensors = not display_hidden
        self.draw_screen = not display_hidden

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)

        # Create the car.
        self.create_car(125, coordfix(500), 1.57)

        # Create some markers

        # u-upper, l-lower, r-right, l-left, o-outer, i-inner
        uro = self.create_marker(900, 600, 10, THECOLORS["blue"])
        ulo = self.create_marker(100, 600, 10, THECOLORS["blue"])
        lro = self.create_marker(900, 100, 10, THECOLORS["blue"])
        llo = self.create_marker(100, 100, 10, THECOLORS["blue"])
        mro = self.create_marker(990, 350, 10, THECOLORS["blue"])
        lmo = self.create_marker(10, 350, 10, THECOLORS["blue"])
        muo2 = self.create_marker(300, 600, 10, THECOLORS["blue"])
        muo22 = self.create_marker(350, 350, 10, THECOLORS["blue"])
        muo = self.create_marker(500, 650, 10, THECOLORS["blue"])
        mlo = self.create_marker(500, 50, 10, THECOLORS["blue"])

        uri = self.create_marker(800, 500, 10, THECOLORS["yellow"])
        uli = self.create_marker(200, 500, 10, THECOLORS["yellow"])
        lri = self.create_marker(800, 200, 10, THECOLORS["yellow"])
        lli = self.create_marker(200, 200, 10, THECOLORS["yellow"])
        mri = self.create_marker(850, 350, 10, THECOLORS["yellow"])
        lmi = self.create_marker(150, 350, 10, THECOLORS["yellow"])
        mui2 = self.create_marker(250, 250, 10, THECOLORS["yellow"])
        mui22 = self.create_marker(450, 250, 10, THECOLORS["yellow"])
        mui = self.create_marker(600, 525, 10, THECOLORS["yellow"])
        mli = self.create_marker(500, 150, 10, THECOLORS["yellow"])

        # Create lines
        self.static = [
            # Walls
            pymunk.Segment(self.space.static_body,(0, 1), (0, height), 1),
            pymunk.Segment(self.space.static_body,(1, height), (width, height), 1),
            pymunk.Segment(self.space.static_body,(width-1, height), (width-1, 1), 1),
            pymunk.Segment(self.space.static_body,(1, 1), (width, 1), 1),

            # Outer boundary
            pymunk.Segment(self.space.static_body,(uro.position), (muo.position), 2),
            pymunk.Segment(self.space.static_body,(ulo.position), (lmo.position), 2),
            pymunk.Segment(self.space.static_body,(lmo.position), (llo.position), 2),
            pymunk.Segment(self.space.static_body,(llo.position), (mlo.position), 2),
            pymunk.Segment(self.space.static_body,(mlo.position), (lro.position), 2),
            pymunk.Segment(self.space.static_body,(lro.position), (mro.position), 2),
            pymunk.Segment(self.space.static_body,(mro.position), (uro.position), 2),
            pymunk.Segment(self.space.static_body,(ulo.position), (muo2.position), 2),
            pymunk.Segment(self.space.static_body,(muo2.position), (muo22.position), 2),
            pymunk.Segment(self.space.static_body,(muo22.position), (muo.position), 2),
            
            #Inner boundary
            pymunk.Segment(self.space.static_body,(uri.position), (mui.position), 2),
            pymunk.Segment(self.space.static_body,(uli.position), (lmi.position), 2),
            pymunk.Segment(self.space.static_body,(lmi.position), (lli.position), 2),
            pymunk.Segment(self.space.static_body,(lli.position), (mli.position), 2),
            pymunk.Segment(self.space.static_body,(mli.position), (lri.position), 2),
            pymunk.Segment(self.space.static_body,(lri.position), (mri.position), 2),
            pymunk.Segment(self.space.static_body,(mri.position), (uri.position), 2),  
            pymunk.Segment(self.space.static_body,(uli.position), (mui2.position), 2),  
            pymunk.Segment(self.space.static_body,(mui2.position), (mui22.position), 2),  
            pymunk.Segment(self.space.static_body,(mui22.position), (mui.position), 2),  
        ]
        for s in self.static:
            #s.sensor = 1
            s.friction = 1
            s.collision_type = 1
            s.color = THECOLORS['red']
        self.space.add(self.static)

        self.checkpoint = [
            pymunk.Segment(self.space.static_body,(lmo.position), (lmi.position), 5),
            pymunk.Segment(self.space.static_body,(ulo.position), (uli.position), 5),
            pymunk.Segment(self.space.static_body,(uli.position), (muo2.position), 5),
            pymunk.Segment(self.space.static_body,(muo22.position), (mui2.position), 5),
            pymunk.Segment(self.space.static_body,(muo22.position), (mui22.position), 5),
            pymunk.Segment(self.space.static_body,(muo.position), (mui.position), 5),
            pymunk.Segment(self.space.static_body,(uro.position), (uri.position), 5),
            pymunk.Segment(self.space.static_body,(mro.position), (mri.position), 5),
            pymunk.Segment(self.space.static_body,(lro.position), (lri.position), 5),
            pymunk.Segment(self.space.static_body,(mlo.position), (mli.position), 5),
            pymunk.Segment(self.space.static_body,(llo.position), (lli.position), 5),
            ]

        for c in self.checkpoint:
            c.sensor = 1
            c.collision_type = 4
            c.color = THECOLORS['green']
        self.space.add(self.checkpoint[0])

        self.score = 0
        self.counter = 0
        def checkpoint_hit(space, arbiter, data): # Do this if called by collision handler
            if self.counter < 10: # If less than 10, remove current and place next checkpoint
                self.space.remove(self.checkpoint[self.counter])
                self.score += 1
                self.counter += 1
                self.space.add(self.checkpoint[self.counter])
            else: # If more than 10, remove current checkpoint and add checkpoint 0 again
                self.space.remove(self.checkpoint[self.counter])
                self.counter = 0
                self.space.add(self.checkpoint[self.counter])
            return True

        # Pymunk collision for car and checkpoints
        ht = self.space.add_collision_handler(2,4) 
        ht.pre_solve = checkpoint_hit

    def create_marker(self, x, y, r, c):
        o_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        o_shape = pymunk.Circle(o_body, r)
        o_shape.elasticity = 1.0
        o_body.position = x, y
        o_shape.color = c
        self.space.add(o_body, o_shape)
        return o_body

    # Create the car in pymunk
    # Need to use car parameters again, so "self" a lot
    def create_car(self, x, y, r):     
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        self.car_body.angle = r
        self.car_shape = pymunk.Circle(self.car_body, 20)
        self.car_shape.color = THECOLORS["gray15"]
        self.car_shape.elasticity = 1.0
        self.space.add(self.car_body, self.car_shape)
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_shape.collision_type = 2
        self.sprites.append(self.car_shape)
    # Advance the game one frame and input actions
    def frame_step(self, action):
        pygame.event.get()
        if action == 0:  # Turn left.
            self.car_body.angle -= .2
        elif action == 1:  # Turn right.
            self.car_body.angle += .2
        elif action == 2: # Do nothing
            None

        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 100 * driving_direction

        # Fill background, draw screen, advance game
        screen.fill(THECOLORS["gray15"])
        pygame.draw.polygon(screen, (100,10,10), [[200, coordfix(500)],[150, coordfix(350)],[200, coordfix(200)],[250, coordfix(250)]], 0)
        pygame.draw.polygon(screen, (100,10,10), [[250, coordfix(250)],[450, coordfix(250)],[500, coordfix(150)],[200, coordfix(200)]], 0)
        pygame.draw.polygon(screen, (100,10,10), [[500, coordfix(150)],[450, coordfix(250)],[850, coordfix(350)],[800, coordfix(200)]], 0)
        pygame.draw.polygon(screen, (100,10,10), [[600, coordfix(525)],[800, coordfix(500)],[850, coordfix(350)],[450, coordfix(250)]], 0)
        draw(screen, self.space)
        self.space.step(1./10)
        clock.tick(fps)

        for sprite_shape in self.sprites:
            p = sprite_shape.body.position
            p = Vec2d(p.x, (coordfix(p.y)))   
            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(sprite_shape.body.angle) + 180
            rotated_sprite_img = pygame.transform.rotate(self.sprite_img, angle_degrees) 
            offset = Vec2d(rotated_sprite_img.get_size()) / 2.
            p = p - offset
            screen.blit(rotated_sprite_img, p) # Use blit since we only need a minor update


        if self.draw_screen:
            pygame.display.flip() # Can use flip here for very minor performance gain compared to pygame.draw

        # Get the current location and the readings there.
        x, y = self.car_body.position
        readings = self.get_lidar_readings(x, y, self.car_body.angle)
        normalized_readings = [(x-20.0)/20.0 for x in readings] 
        state = np.array([normalized_readings])

        if self.lidar_check(readings):
            # If crashed reward = -500 if not do score * 100 to get reward
            reward = -500 
            self.handle_crash(driving_direction)
        else:
            # If not crashed, set reward to score * 100
            reward = self.score * 100
        return reward, state

    # Check if the distance from sensor 1-5 is equal to 1, which pretty much means it crashed
    def lidar_check(self, readings):
        if readings[0] == 1 or readings[1] == 1 or readings[2] == 1 or readings[3] == 1 or readings[4] == 1:
            return True
        else:
            return False

    def handle_crash(self, driving_direction):
       # Reset game 
        self.space.remove(self.checkpoint[self.counter])
        self.counter = 0
        self.score = 0
        self.space.add(self.checkpoint[self.counter])
           
        # Reset car
        self.car_body.angle = 1.57 # Restart angle
        self.car_body.position = 125, coordfix(500) # Restart coordinates

    def sum_readings(self, readings):
        # Sum the number of non-zero readings
        tot = 0
        for i in readings:
            tot += i
        return tot

    def get_lidar_readings(self, x, y, angle):
        readings = []
        """
        Instead of using a grid of boolean(ish) sensors, lidar readings
        simply return N "distance" readings, one for each lidar
        we're simulating. The distance is a count of the first non-zero
        reading starting at the object. For instance, if the fifth sensor
        in a lidar "arm" is non-zero, then that arm returns a distance of 5.
        """
        # Make lidar arms with "rear sensor"
        arms = [(self.make_lidar_arm(x, y), i) for i in [0,
            math.pi/4, -math.pi/4, math.pi/2, -math.pi/2]]

        # Rotate them and get readings.
        for arm, a in arms:
            distance = self.get_arm_distance(arm, x, y, angle, a)
            readings.append(distance)

        if self.show_sensors:
            pygame.display.update()

        return readings

    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return i  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    return i

            if self.show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)

        # Return the distance for the arm.
        return i

    def make_lidar_arm(self, x, y):
        spread = 10  # Default spread.
        distance = 20  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        if reading == THECOLORS['gray15'] or reading == THECOLORS['green']:
            return 0
        else:
            return 1

if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step((random.randint(0, 2)))
