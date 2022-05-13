import math
import pygame
import pygame.gfxdraw
import random



def createCircleImage(imagelocation, shifting_range, modify_range, gradient_range, do_colorschwift, do_lightschwift, do_gradientshift, min_radius, max_radius, iterations, use_bw, filename, color1, color2, background_color):
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    dark_grey = (50, 50, 50, 255)

    background_color = list(background_color)
    background_color.append(255)
    background_color = tuple(background_color)

    display_size = 900
    outer_radius = display_size/2
    (width, height) = (display_size, display_size)
    middle = (width/2, height/2)
    screen = pygame.display.set_mode((width, height))
    screen.fill(background_color)
    schablone = pygame.image.load(imagelocation)
    schablone_size = schablone.get_size()

    scaling_factor_x = schablone_size[0]/width
    scaling_factor_y = schablone_size[1]/height

    Matrix = [[[] for y in range((height//(2*max_radius)) + 2)] for x in range((width//(2*max_radius) + 2))]
  
    def colorschwift(color, intervall):
        color = list(color)
        for i in range(3):
            shifted_color = random.randint(color[i] - intervall, color[i] + intervall)
            color[i] = int(max(min(255, shifted_color), 0))
        return tuple(color)


    def lightschwift(color, modifier):
        color = list(color)
        if modifier < 1:
            modifier = 1/modifier
        modifier = random.uniform(1/modifier, modifier)
        for i in range(3):
            color[i] = int(min(255, color[i] * modifier))
        return tuple(color)


    def gradientshift(first_color, second_color, gradient_range):  # how much one color changes into the other, only works with b/w
        first_color = list(first_color)
        second_color = list(second_color)
        gradient_change = random.uniform(0, gradient_range)

        for i in range(3):
            difference = first_color[i] - second_color[i]
            first_color[i] = int(first_color[i] - (difference * gradient_change))

        return tuple(first_color)


    class Circle(object):
        def __init__(self, x, y, radius, state):
            self.x = x
            self.y = y
            self.radius = radius
            self.state = state # only useful for b/w drawing

    # idk, weird draw function so that every possible combination of modifiers can be possible
        def draw(self, surface):
            if use_bw:
                if self.state:
                    farbe = color1
                    farbe2 = color2
                else:
                    farbe = color2
                    farbe2 = color1
                if do_gradientshift:
                    farbe = gradientshift(farbe, farbe2, gradient_range)
            else:
                farbe = schablonenfarbe
            if do_colorschwift:
                farbe = colorschwift(farbe, shifting_range)
            if do_lightschwift:
                farbe = lightschwift(farbe, modify_range)
            pygame.gfxdraw.aacircle(surface, self.x, self.y, self.radius, farbe)
            pygame.gfxdraw.filled_circle(surface, self.x, self.y, self.radius, farbe)


    circles = []

    screen.fill(background_color)

    for i in range(iterations):
        x_places = []
        y_places = []
        # random value of the original picture to pick the color of the to be drawn circle
        random_x = random.randint(0, schablone_size[0]-1)
        random_y = random.randint(0, schablone_size[1]-1)

        #get the accoriding coordinates for the endimage
        resize_x = int(random_x / scaling_factor_x)
        resize_y = int(random_y / scaling_factor_y)
        schablonenfarbe = schablone.get_at((random_x, random_y))
        if schablonenfarbe == black:
            state = True
        else:
            state = False

        # checks, if theres already been drawn on this pixel
        if not((screen.get_at((resize_x, resize_y))) == background_color):
            continue

        # checks, if the circle can be drawn inside the bounds of the outer circle
        # also beginst to calculate the biggest possible radius for the circle
        #this variable will be reduced throughout the process
        distance_to_origin = math.dist((resize_x, resize_y), middle)
        biggest_possible_radius = outer_radius - distance_to_origin
        if not(biggest_possible_radius > min_radius):
            continue

        # checks for collision with other circles so they dont overlap
        x_places.append((resize_x) // (2 * max_radius) + 1)
        x_places.append((resize_x) // (2 * max_radius) - 1)
        x_places.append((resize_x) // (2 * max_radius))

        y_places.append((resize_y) // (2 * max_radius) + 1)
        y_places.append((resize_y) // (2 * max_radius) - 1)
        y_places.append((resize_y) // (2 * max_radius))

        for x_element in x_places:
            for y_element in y_places:
                currentsquare = Matrix[x_element][y_element]
                for circle in currentsquare:
                    current_radius = math.dist((resize_x, resize_y), (circle.x, circle.y)) - circle.radius
                    # makes sure, that the biggest possible radius is always the smallest, so no circle can overlap
                    if current_radius < biggest_possible_radius:
                        biggest_possible_radius = current_radius
                        if biggest_possible_radius < min_radius:
                            break

        if biggest_possible_radius >= min_radius:
            biggest_possible_radius = int(biggest_possible_radius)
            biggest_possible_radius = min(biggest_possible_radius, max_radius)
            myCircle = Circle(resize_x, resize_y, biggest_possible_radius, state)
            place = Matrix[resize_x//(2*max_radius)][resize_y//(2*max_radius)]
            place.append(myCircle)
            myCircle.draw(screen)

    pygame.image.save(screen, filename)
    pygame.quit()
    return filename   
        
def createCustomImage(number):
    pygame.font.init()
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    background_colour = black

    (width, height) = (900, 900)
    screen = pygame.display.set_mode((width, height))
    myFont = pygame.font.SysFont('DejaVu Sans', 520)
    text = myFont.render(str(number), True, white)
    fontsize = myFont.size(str(number))

    screen.fill(background_colour)
    screen.blit(text,(450 - (fontsize[0]/2),450 -(fontsize[1]/2)))
    pygame.display.update()
    filename = "Number" + str(number) + ".png"
    pygame.image.save(screen, filename)
    pygame.quit()
    return filename