'''
--- Day 10: Hoof It ---

You all arrive at a Lava Production Facility on a floating island in the sky. As the others begin to search the massive industrial complex, you feel a small nose boop your leg and look down to discover a reindeer wearing a hard hat.

The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly.

Perhaps you can help fill in the missing hiking trails?

The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest). For example:

0123
1234
8765
9876

Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).

You look up from the map and notice that the reindeer has helpfully begun to construct a small pile of pencils, markers, rulers, compasses, stickers, and other equipment you might need to update the map with hiking trails.

A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail. In the above example, the single trailhead in the top left corner has a score of 1 because it can reach a single 9 (the one in the bottom left).

This trailhead has a score of 2:

...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9

(The positions marked . are impassable tiles to simplify these examples; they do not appear on your actual topographic map.)

This trailhead has a score of 4 because every 9 is reachable via a hiking trail except the one immediately to the left of the trailhead:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This topographic map contains two trailheads; the trailhead at the top has a score of 1, while the trailhead at the bottom has a score of 2:

10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01

Here's a larger example:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

This larger example has 9 trailheads. Considering the trailheads in reading order, they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of all trailheads is 36.

The reindeer gleefully carries over a protractor and adds it to the pile. What is the sum of the scores of all trailheads on your topographic map?

Your puzzle answer was 674.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.

The paper describes a second way to measure a trailhead called its rating. A trailhead's rating is the number of distinct hiking trails which begin at that trailhead. For example:

.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....

The above map has a single trailhead; its rating is 3 because there are exactly three distinct hiking trails which begin at that position:

.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....

Here is a map containing a single trailhead with rating 13:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This map contains a single trailhead with rating 227 (because there are 121 distinct hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on the bottom edge):

012345
123456
234567
345678
4.6789
56789.

Here's the larger example from before:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic map is 81.

You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. What is the sum of the ratings of all trailheads?
'''
from tqdm import tqdm

#------------ Classes and functions

class MapPoint():
    '''This class manages all information on a node to make it easier to process.'''

    def __init__(self, pos:tuple, altitude:int) -> None:
        '''Position in (row,line), altitude number in [0,9].'''
        self.position = pos
        self.height = altitude
        self.destinations = []
        if self.height == 0: 
            self.head_of_trail = True
            self.tail_of_trail = False
            self.finish_points = []
        elif self.height == 9:
            self.head_of_trail = False
            self.tail_of_trail = True
        else:
            self.head_of_trail = False
            self.tail_of_trail = False

class TrailMap():
    '''This class is able to read a topographic map and return the information requested in the problem.'''

    def __init__(self, topographic_map:list[str]) -> None:
        self.__load_map(topographic_map)

    def __load_map(self, topographic_map:list[str]) -> None:
        '''This loads the map as MapPoints.'''
        self.map = []
        dim_x = len(topographic_map[0])
        dim_y = len(topographic_map)
        self.map_size = [dim_x,dim_y]
        self.point_locator = {}

        for index_y, line in enumerate(topographic_map):
            for index_x, altitude in enumerate(line):
                self.map.append(MapPoint((index_x, index_y), int(altitude)))
                self.point_locator[(index_x, index_y)] = self.map[-1]

        self.__define_possible_nodes()
        return None
    
    def print_map(self) -> None:
        draw_map = [[] for _ in range(self.map_size[1])] #Creates an empty list per row
        for point in self.map:
            draw_map[point.position[1]].append(point.height)

        for line in draw_map:
            printable = ''
            for char in line:
                printable += str(char)
            print(printable)
        return None

    def __define_possible_nodes(self) -> None:
        '''This function checks if point can be considered.'''
        for index_y in range(self.map_size[1]):
            for index_x in range(self.map_size[0]):
                location = (index_x, index_y)
                neighbour_nodes = []
                if index_x < self.map_size[0]-1:
                    neighbour_nodes.append((index_x +1, index_y))
                if index_x > 0:
                    neighbour_nodes.append((index_x -1, index_y))
                if index_y < self.map_size[1]-1:
                    neighbour_nodes.append((index_x, index_y +1))
                if index_y > 0:
                    neighbour_nodes.append((index_x, index_y -1))
                veredict = False
                for node in neighbour_nodes:
                    veredict = (
                        (self.point_locator[location].height - self.point_locator[node].height) == -1
                    )
                    if veredict:
                        self.point_locator[location].destinations.append(node)

    def trailblaze(self) -> None:
        '''This checks if you can move foward from a point.'''
        for location in tqdm(self.map):
            if location.height == 0:
                self.__advance(location.position, [location.position])
        pass

    def __advance(self,origin:tuple, curent_pos:list[tuple]) -> bool:
        '''This function makes steps until it finds a 9'''
        if curent_pos == []:
            return True
        for location in curent_pos:
            # print(location)
            if self.point_locator[location].height == 9:
                self.point_locator[origin].finish_points.append(location)
                # print(f'{origin} ----> {location}')
            else:
                self.__advance(origin,self.point_locator[location].destinations)
        return False
    
    def score_trails(self) -> list[int]:
        '''This score all trails and return sum'''
        map_score = 0
        map_rating = 0        
        for location in self.map:
            if location.head_of_trail:
                unique_trails = []
                for finish in location.finish_points:
                    if finish not in unique_trails:
                        unique_trails.append(finish)
                # print(f'{location.position} ---> {[self.point_locator[point].height for point in unique_trails]} Total: {len(unique_trails)}.')
                map_score += len(unique_trails)
                map_rating += len(location.finish_points)
        return [map_score, map_rating]


#----------------- Program
if __name__ == '__main__':

    #Reading the map
    with open('Day 10\\topographic_map.txt', 'r') as blank_map:
        topo_map = blank_map.readlines()
    topo_map = [line.replace('\n','') for line in topo_map]

    island = TrailMap(topo_map)
    island.trailblaze()
    scoring = island.score_trails()
    print(f'This map has a trailhead score of {scoring[0]} and a rating of {scoring[1]}.')

        