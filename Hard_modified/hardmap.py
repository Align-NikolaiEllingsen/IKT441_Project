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
width = 1920
height = 1080
fps = 9999
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
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

        # Hide display        
        self.show_sensors = not display_hidden
        self.draw_screen = not display_hidden

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., 0.)

        # Create the car.
        self.create_car(150, coordfix(600), 1.57)

        # This is all a mess of markers
        o1 = self.create_marker(100, coordfix(500), 10, THECOLORS["blue"])
        o2 = self.create_marker(200, coordfix(200), 10, THECOLORS["blue"])
        o3 = self.create_marker(400, coordfix(100), 10, THECOLORS["blue"])
        o4 = self.create_marker(600, coordfix(200), 10, THECOLORS["blue"])
        o5 = self.create_marker(700, coordfix(500), 10, THECOLORS["blue"])
        o6 = self.create_marker(950, coordfix(500), 10, THECOLORS["blue"])
        o7 = self.create_marker(1000, coordfix(200), 10, THECOLORS["blue"])
        o8 = self.create_marker(1400, coordfix(100), 10, THECOLORS["blue"])
        o9 = self.create_marker(1800, coordfix(200), 10, THECOLORS["blue"])
        o10 = self.create_marker(1800, coordfix(900), 10, THECOLORS["blue"])
        o11 = self.create_marker(1650, coordfix(1000), 10, THECOLORS["blue"])
        o12 = self.create_marker(1500, coordfix(900), 10, THECOLORS["blue"])
        o13 = self.create_marker(1500, coordfix(500), 10, THECOLORS["blue"])
        o14 = self.create_marker(1400, coordfix(400), 10, THECOLORS["blue"])
        o15 = self.create_marker(1300, coordfix(500), 10, THECOLORS["blue"])
        o16 = self.create_marker(1300, coordfix(700), 10, THECOLORS["blue"])
        o17 = self.create_marker(1100, coordfix(800), 10, THECOLORS["blue"])
        o18 = self.create_marker(825, coordfix(850), 10, THECOLORS["blue"])
        o19 = self.create_marker(500, coordfix(850), 10, THECOLORS["blue"])
        o20 = self.create_marker(100, coordfix(900), 10, THECOLORS["blue"])

        i1 = self.create_marker(500, coordfix(700), 10, THECOLORS["yellow"])
        i2 = self.create_marker(250, coordfix(700), 10, THECOLORS["yellow"])
        i3 = self.create_marker(250, coordfix(500), 10, THECOLORS["yellow"])
        i4 = self.create_marker(300, coordfix(300), 10, THECOLORS["yellow"])
        i5 = self.create_marker(400, coordfix(250), 10, THECOLORS["yellow"])
        i6 = self.create_marker(500, coordfix(300), 10, THECOLORS["yellow"])
        i7 = self.create_marker(550, coordfix(600), 10, THECOLORS["yellow"])
        i8 = self.create_marker(825, coordfix(700), 10, THECOLORS["yellow"])
        i9 = self.create_marker(1150, coordfix(600), 10, THECOLORS["yellow"])
        i10 = self.create_marker(1150, coordfix(300), 10, THECOLORS["yellow"])
        i11 = self.create_marker(1400, coordfix(250), 10, THECOLORS["yellow"])
        i12 = self.create_marker(1650, coordfix(300), 10, THECOLORS["yellow"])
        i13 = self.create_marker(1650, coordfix(800), 10, THECOLORS["yellow"])

        # Create lines
        self.static = [
            # Walls
            pymunk.Segment(self.space.static_body,(0, 1), (0, height), 1),
            pymunk.Segment(self.space.static_body,(1, height), (width, height), 1),
            pymunk.Segment(self.space.static_body,(width-1, height), (width-1, 1), 1),
            pymunk.Segment(self.space.static_body,(1, 1), (width, 1), 1),

            # Outer boundary
            pymunk.Segment(self.space.static_body,(o1.position), (o2.position), 6),
            pymunk.Segment(self.space.static_body,(o2.position), (o3.position),6),
            pymunk.Segment(self.space.static_body,(o3.position), (o4.position),6),
            pymunk.Segment(self.space.static_body,(o4.position), (o5.position),6),
            pymunk.Segment(self.space.static_body,(o5.position), (o6.position),6),
            pymunk.Segment(self.space.static_body,(o6.position), (o7.position),6),
            pymunk.Segment(self.space.static_body,(o7.position), (o8.position),6),
            pymunk.Segment(self.space.static_body,(o8.position), (o9.position),6),
            pymunk.Segment(self.space.static_body,(o9.position), (o10.position),6),
            pymunk.Segment(self.space.static_body,(o10.position), (o11.position),6),
            pymunk.Segment(self.space.static_body,(o11.position), (o12.position),6),
            pymunk.Segment(self.space.static_body,(o12.position), (o13.position),6),
            pymunk.Segment(self.space.static_body,(o13.position), (o14.position),6),
            pymunk.Segment(self.space.static_body,(o14.position), (o15.position),6),
            pymunk.Segment(self.space.static_body,(o15.position), (o16.position),6),
            pymunk.Segment(self.space.static_body,(o16.position), (o17.position),6),
            pymunk.Segment(self.space.static_body,(o17.position), (o18.position),6),
            pymunk.Segment(self.space.static_body,(o18.position), (o19.position),6),
            pymunk.Segment(self.space.static_body,(o19.position), (o20.position),6),
            pymunk.Segment(self.space.static_body,(o20.position), (o1.position),6),

            # Inner boundary
            pymunk.Segment(self.space.static_body,(i1.position), (i2.position),6),
            pymunk.Segment(self.space.static_body,(i2.position), (i3.position),6),
            pymunk.Segment(self.space.static_body,(i3.position), (i4.position),6),
            pymunk.Segment(self.space.static_body,(i4.position), (i5.position),6),
            pymunk.Segment(self.space.static_body,(i5.position), (i6.position),6),
            pymunk.Segment(self.space.static_body,(i6.position), (i7.position),6),
            pymunk.Segment(self.space.static_body,(i7.position), (i8.position),6),
            pymunk.Segment(self.space.static_body,(i8.position), (i9.position),6),
            pymunk.Segment(self.space.static_body,(i9.position), (i10.position),6),
            pymunk.Segment(self.space.static_body,(i10.position), (i11.position),6),
            pymunk.Segment(self.space.static_body,(i11.position), (i12.position),6),
            pymunk.Segment(self.space.static_body,(i12.position), (i13.position),6),
            pymunk.Segment(self.space.static_body,(i1.position), (i8.position),6),
        ]
        for s in self.static:
            #s.sensor = 1
            s.friction = 1
            s.collision_type = 1
            s.color = THECOLORS['red']
        self.space.add(self.static)

        # Create checkpoints for scoring
        self.checkpoint = [
            pymunk.Segment(self.space.static_body,(o1.position), (i3.position), 5),
            pymunk.Segment(self.space.static_body,(o2.position), (i4.position), 5),
            pymunk.Segment(self.space.static_body,(o3.position), (i5.position), 5),
            pymunk.Segment(self.space.static_body,(o4.position), (i6.position), 5),
            pymunk.Segment(self.space.static_body,(o5.position), (i7.position), 5),
            pymunk.Segment(self.space.static_body,(o6.position), (i9.position), 5),
            pymunk.Segment(self.space.static_body,(o7.position), (i10.position), 5),
            pymunk.Segment(self.space.static_body,(o8.position), (i11.position), 5),
            pymunk.Segment(self.space.static_body,(o9.position), (i12.position), 5),
            pymunk.Segment(self.space.static_body,(o10.position), (i13.position), 5),
            pymunk.Segment(self.space.static_body,(o11.position), (i13.position), 5),
            pymunk.Segment(self.space.static_body,(o12.position), (i13.position), 5),
            pymunk.Segment(self.space.static_body,(o13.position), (i12.position), 5),
            pymunk.Segment(self.space.static_body,(o14.position), (i11.position), 5),
            pymunk.Segment(self.space.static_body,(o15.position), (i10.position), 5),
            pymunk.Segment(self.space.static_body,(o16.position), (i9.position), 5),
            pymunk.Segment(self.space.static_body,(o18.position), (i8.position), 5),
            pymunk.Segment(self.space.static_body,(o19.position), (i1.position), 5),
            pymunk.Segment(self.space.static_body,(o20.position), (i2.position), 5),

            ]

        for c in self.checkpoint:
            c.sensor = 1
            c.collision_type = 4
            c.color = THECOLORS['green']
        self.space.add(self.checkpoint[0])

        self.score = 0
        self.counter = 0
        def checkpoint_hit(space, arbiter, data): # Do this if called by collision handler
            if self.counter < 18: # If less than 18, remove current and place next checkpoint
                self.space.remove(self.checkpoint[self.counter])
                self.score += 1
                self.counter += 1
                self.space.add(self.checkpoint[self.counter])
            else: # If less than 18, remove current and place next checkpoint
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
        pygame.draw.polygon(screen, (100,10,10), [[250, 700],[250, 500],[300, 300],[400, 250],[500, 300],[550, 600],[825, 700],[500, 700]], 0)
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
        self.car_body.position = 150, coordfix(600) # Restart coordinates

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
