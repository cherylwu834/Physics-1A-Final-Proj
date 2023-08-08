#working simulation, no image

import pygame #this is a graphics library to help animate the bike
import math

pygame.font.init() #initialize font

pygame.init() #initialize pygame


#PARAMETERS
INIT_BIKE_VELOCITY = 30 #initial velocity of the bike in m/s
WIND_VELOCITY = 0 #velocity of the wind in m/s
BIKE_MASS = 9 #mass of the bike in kg
PERSON_MASS = 58 #mass of the person in kg

#other constants
AIR_DENSITY = 1.22 #kg/m^3
DRAG_COEFFICIENT_TIMES_AREA = 0.31 #m^2
SCALE = 1/4  #4 meters = 1 pixel
FPS = 60 #frames per second
TIMESTEP = 1/6 # The number*60 (b/c 60 FPS) = 1 second in real life, j makes it go faster/slower
WIDTH, HEIGHT = 800, 500 #set the width and height of the screen
GROUND_Y = 400 #height of the ground in pixels
RADIUS = 100 #height of the bike circle in pixels
text_font = pygame.font.SysFont('monospace', 15) #font for text
#zero_velocity_font = pygame.font.SysFont('monospace', 50) #font for when velocity is 0

#colors
GREEN = (0, 100, 0)
BACKGROUND = (255, 255, 240) #ivory

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #set the screen
pygame.display.set_caption("Bike Simulation with Air Resistance") #set the title of the screen

class Bike:
    def __init__(self, x, y, velocity, mass):
        self.x = x*(1/SCALE) #position in meters
        self.y = y*(1/SCALE)
        self.velocity = velocity #this is the velocity of the biker, not the wind
        self.mass = mass
        self.time_elapsed = 0.0 #should stop incrementing when velocity = 0
        self.radius = RADIUS

        self.velocity_history = []  #[] means it's a list, roughly equivalent to an array
        self.accleration_history = []
        self.position_history = []


    def draw (self, screen):
        x = self.x * SCALE
        y = self.y * SCALE
        pygame.draw.circle(screen, (0, 0, 0), (x, y), self.radius) #draw the bike as a circle

    def air_resistance_accel(self):
        v = self.velocity + WIND_VELOCITY
        air_resistance = -0.5 * AIR_DENSITY * DRAG_COEFFICIENT_TIMES_AREA * v** 2
        accel = air_resistance / self.mass
        return accel
    
    def update_position(self):
        accel = self.air_resistance_accel()
        self.velocity += accel * TIMESTEP #update velocity
        self.x += self.velocity * TIMESTEP  #update position
        
        #updating my logs
        self.time_elapsed += TIMESTEP #increment time elapsed
        self.accleration_history.append((self.time_elapsed, accel)) #add the current acceleration to the acceleration history list
        self.velocity_history.append((self.time_elapsed,self.velocity)) #add the current velocity to the velocity history list
        self.position_history.append((self.time_elapsed, self.x)) #add the current position to the position history list


def main ():
    run = True
    clock = pygame.time.Clock() #to sync speed/regulate frame rate

    bike1 = Bike(100, GROUND_Y - RADIUS, INIT_BIKE_VELOCITY, BIKE_MASS+PERSON_MASS) #create a bike object

    while run:
        clock.tick(FPS) #60 frames per second
        screen.fill(BACKGROUND) #fill the screen with ivory
        pygame.draw.rect(screen, GREEN, pygame.Rect((0, GROUND_Y), (WIDTH, HEIGHT - GROUND_Y))) #draw the ground

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bike1.update_position() #update position of bike

        bike1.draw(screen) #draw the bike

        time_text = text_font.render("Time Elapsed: " + str(bike1.time_elapsed) + " seconds", 1, (0, 0, 0)) #shows time passed
        screen.blit(time_text, (10, 10)) #draws the actual text
        velocity_text = text_font.render("Velocity: " + str(bike1.velocity) + " m/s", 1, (0, 0, 0)) #shows velocity
        screen.blit(velocity_text, (10, 30)) #draws the actual text

        pygame.display.update() #update the screen

    pygame.quit()


main()