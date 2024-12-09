'''
--- Day 8: Resonant Collinearity ---

You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............

The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........

Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........

Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........

The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.

Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
Your puzzle answer was 254.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........

In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##

Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?

'''
import numpy as np
from itertools import combinations
from math import sqrt
from tqdm import tqdm
#------------------------Functions and classes:
def check_antinodes2(antena:str, antena_positions:dict, limits:list[int,int]) -> list[list[int,int]]:
    '''This checks for each antena possible antinodes within town and provides a list of locations. 
    Does not care for other antenas.'''
    list_positions = antena_positions[antena]
    antena_pairs = list(combinations(list_positions,2))
    antinodes_for_this_antena = []
    for pair in tqdm(antena_pairs):
        antinodes_for_this_antena += __colinear_positions_all(pair[0], pair[1], limits)
    return antinodes_for_this_antena


def __colinear_positions_all(pointa:list[int,int], pointb:list[int,int], limits:list[int,int]) -> list[list[int,int]]:
    '''Mark the positions in line whose distance is double the distance of other point.'''
    points_in_map = []
    slope = (pointb[1]-pointa[1])/(pointb[0]-pointa[0])
    constant = pointb[1] - slope*pointb[0]
    print(f'{pointa} and {pointb} -----> y = {slope}*x + {constant} producing points: ', end='')
    for x_coord in range(limits[0]):
        y_coord = slope*x_coord + constant
        y_coord_int = int(round(y_coord,0))
        if abs(round((y_coord-float(y_coord_int))*1000,0)) < 1:
            if (y_coord_int < limits[1]) and (y_coord_int>=0):
                points_in_map.append([x_coord, y_coord_int])
    unique_antinode_locations = []
    for antinode_pos in points_in_map:
        if not antinode_pos in unique_antinode_locations:
            unique_antinode_locations.append(antinode_pos)
    print(unique_antinode_locations)
    return unique_antinode_locations

def check_antinodes(antena:str, antena_positions:dict, limits:list[int,int]) -> list[list[int,int]]:
    '''This checks for each antena possible antinodes within town and provides a list of locations. 
    Does not care for other antenas.'''
    list_positions = antena_positions[antena]
    antena_pairs = list(combinations(list_positions,2))
    antinodes_for_this_antena = []
    for pair in tqdm(antena_pairs):
        antinodes_for_this_antena += __colinear_positions_1x_2x(pair[0], pair[1], limits)
    return antinodes_for_this_antena


def __colinear_positions_1x_2x(pointa:list[int,int], pointb:list[int,int], limits:list[int,int]) -> list[list[int,int]]:
    '''Mark the positions in line whose distance is double the distance of other point.'''
    points_in_map = []
    antinode_locations = []
    slope = (pointb[1]-pointa[1])/(pointb[0]-pointa[0])
    constant = pointa[1] - slope*pointa[0]
    for x_coord in range(limits[0]):
        y_coord = slope*x_coord + constant
        y_coord_int = int(round(y_coord,0))
        if (y_coord_int < limits[1]) and (y_coord_int>=0):
            points_in_map.append([x_coord, y_coord_int])
    for node in points_in_map:
        dist_point_a = dist_two_points(node, pointa)
        dist_point_b = dist_two_points(node,pointb)
        ratio_distances = dist_point_a/(dist_point_b + np.finfo(np.float32).eps)
        if ratio_distances <1: ratio_distances = 1/(ratio_distances+ np.finfo(np.float32).eps)
        ratio_distances_round = int(round(ratio_distances*1000,0))
        if ratio_distances_round in range(1999,2001):
            antinode_locations.append(node)
    unique_antinode_locations = []
    for antinode_pos in antinode_locations:
        if not antinode_pos in unique_antinode_locations:
            unique_antinode_locations.append(antinode_pos)
    print(f'For antenas at {pointa} and {pointb}, we find {len(unique_antinode_locations)} valid points at: {unique_antinode_locations}.')
    return unique_antinode_locations

        
def dist_two_points(pointa:list[float,float], pointb:list[int,int]) -> float:
    '''Returns the distance between two points.'''
    del_x = pointa[0] - pointb[0]
    del_y = pointa[1] - pointb[1]
    distance = sqrt((del_x*del_x) + (del_y*del_y))
    return distance

def print_results(limits:list[int,int], antenas_reversed:dict, antinodes:list[list[int,int]]) -> None:
    '''Prints results as shown in example.'''
    for line in range(limits[0]):
        line_string = ''
        for column in range(limits[1]):
            position = [column, line]
            if str(position) in antena_reversed.keys():
                line_string += antena_reversed[str(position)]
            elif position in antinodes:
                line_string += '#'
            else:
                line_string += '•'
        print(line_string)
    return None
                

#---------------------------------------------------------------
if __name__ == '__main__':

    #Read the map explains the map:
    with open('Day 8\map_antenas.txt', 'r') as antena_map:
        raw_mapping = antena_map.readlines()
    raw_mapping = [line.replace('\n','') for line in raw_mapping]

    #Set limits of "city":
    lim_x = len(raw_mapping[0])
    lim_y = len(raw_mapping)
    city_limits = [lim_x, lim_y]

    occupied_positions = []
    antena_list = []
    antena_names = []
    for index_y, line in enumerate(raw_mapping):
        for index_x, char in enumerate(line):
            if not char == '.':
                occupied_positions.append([index_x, index_y])
                antena_names.append(char)
                antena_list.append([char, [index_x, index_y]])
    antena_names = list(set(antena_names))

    #Now we create a dict for each antena type containing all their positions:
    antena_locations = {}
    for antena in antena_names:
        locations = []
        for marking in antena_list:
            if marking[0] == antena:
                locations.append(marking[1])
        antena_locations[antena] = locations
    
    #Reversing for easier printing:
    antena_reversed = {}
    for key, value in antena_locations.items():
        for location in value:
            antena_reversed[str(location)] = key

    antinodes_global = []
    for antena in tqdm(antena_names):
        antinodes_global += check_antinodes2(antena, antena_locations, city_limits)
    
    active_antinodes = []
    for antinode_position in antinodes_global:
        if not antinode_position in active_antinodes:
            active_antinodes.append(antinode_position)
    print(city_limits)
    # print('Ocuppied positions ----> ', occupied_positions)
    # print('----------------------------------\nActive nodes----> ', active_antinodes)
    print(f'There are {len(active_antinodes)} active nodes currently.')
    print('-------------------------------------------------------')
    print_results(city_limits, antena_reversed, active_antinodes)