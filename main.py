import pygame, sys
import data
import math
from pygame.locals import QUIT

pygame.init()
w = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Hexagonal Rating')

# categories
# Auto balance points
# Cone auto points
# Cone teleop points
# Cube teleop points
# Cube auto points
# Cycle time

# Draws circle around the hexagon
w.fill((255, 255, 255))
pygame.draw.circle(w, (211, 219, 232), (200, 200), 175)

# Calculate the side length of the hexagon
hexagon_side = 350 / math.sqrt(3)

# Calculate the points of the hexagon
hexagon_points = []
for i in range(6):
    angle_deg = 60 * i
    angle_rad = math.radians(angle_deg)
    x = 200 + 175 * math.cos(angle_rad)
    y = 200 + 175 * math.sin(angle_rad)
    hexagon_points.append((x, y))

# Draw the hexagon
pygame.draw.polygon(w, (169, 176, 171), hexagon_points)

# Draws lines inside the hexagon that extend 175px from the center to each vertex
pygame.draw.line(w, (0, 0, 0), (25, 200), (375, 200))
pygame.draw.line(w, (0, 0, 0), (112.50000000000004, 351.55444566227675), (287.5, 48.44555433772325))
pygame.draw.line(w, (0, 0, 0), (287.5, 351.55444566227675), (112.49999999999993, 48.44555433772328))

teams = data.get_csv_data("dummydata2")
team_index = list(teams.keys())
viewing_number = 0

# Finds max values
auto_cone_max = data.findMaxStat(0,teams) # highest auto balance points
teleop_cone_max = data.findMaxStat(1,teams) # highest auto balance points
cycle_time_min = data.findMaxStat(2,teams) # highest auto balance points
auto_cube_max = data.findMaxStat(3,teams) # highest auto balance points
teleop_cube_max = data.findMaxStat(4,teams) # highest auto balance points
auto_balance_max = data.findMaxStat(5,teams) # highest auto balance points
# debug: print(auto_cone_max,teleop_cone_max,cycle_time_min,auto_cube_max,teleop_cone_max,auto_balance_max)

def update_values():
    # Chooses active team
    team = team_index[viewing_number]
    values = teams[team]
    print(team)

    # Redraw the hexagon
    ## Calculate the points of the hexagon
    hexagon_points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = 200 + 175 * math.cos(angle_rad)
        y = 200 + 175 * math.sin(angle_rad)
        hexagon_points.append((x, y))

    ## Draw the hexagon
    pygame.draw.polygon(w, (169, 176, 171), hexagon_points)

    ## Draws lines inside the hexagon that extend 175px from the center to each vertex
    pygame.draw.line(w, (0, 0, 0), (25, 200), (375, 200))
    pygame.draw.line(w, (0, 0, 0), (112.50000000000004, 351.55444566227675), (287.5, 48.44555433772325))
    pygame.draw.line(w, (0, 0, 0), (287.5, 351.55444566227675), (112.49999999999993, 48.44555433772328))
    
    # AUTO CONE
    length = 175 #155.520905479
    percentage = (float(values[0]) / auto_cone_max)
    newLength = length * percentage
    auto_cone_coord = ((200 - math.cos(1.0472) * newLength), (200 - math.sin(1.0472) * newLength))

    # TELEOP CONE
    percentage = (float(values[1]) / teleop_cone_max)
    newLength = length * percentage
    teleop_cone_coord = ((200 + math.cos(1.0472) * newLength), (200 - math.sin(1.0472) * newLength))

    # CYCLE TIME
    percentage = (cycle_time_min / float(values[2]))
    newLength = length * percentage
    cycle_time_coord = (200 + newLength, 200)

    # AUTO CUBE
    percentage = (float(values[3]) / auto_cube_max)
    newLength = length * percentage
    auto_cube_coord = ((200 + math.cos(1.0472) * newLength), (200 + math.sin(1.0472) * newLength))

    # TELEOP CUBE
    percentage = (float(values[4]) / teleop_cube_max)
    newLength = length * percentage
    teleop_cube_coord = ((200 - math.cos(1.0472) * newLength), (200 + math.sin(1.0472) * newLength))

    # AUTO BALANCE
    percentage = (float(values[5]) / auto_balance_max)
    newLength = length * percentage
    auto_balance_coord = (200 - newLength, 200)

    coords = [auto_cone_coord, teleop_cone_coord, cycle_time_coord, auto_cube_coord, teleop_cube_coord, auto_balance_coord]

    #for i in coords:
        #pygame.draw.circle(w, (0, 0, 0), i, 10)

    pygame.draw.polygon(w, (0, 0, 0), coords)
    pygame.display.update()
update_values()
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                viewing_number -= 1
                if viewing_number < 0:
                    viewing_number = 0
                else:
                    update_values()
            if event.key == pygame.K_RIGHT:
                viewing_number += 1
                try:
                    update_values()
                except:
                    viewing_number -= 1
    