'''
--- Day 12: Garden Groups ---

Why not search for the Chief Historian near the gardener and his massive farm? There's plenty of food, so The Historians grab something to eat while they search.

You're about to settle near a complex arrangement of garden plots when some Elves ask if you can lend a hand. They'd like to set up fences around each region of garden plots, but they can't figure out how much fence they need to order or how much it will cost. They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:

AAAA
BBCD
BBCC
EEEC

This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.

In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.

The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.

Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not tou
Your puzzle answer was 1381056.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC

The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of 436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE

The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA

It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

    A region of R plants with price 12 * 10 = 120.
    A region of I plants with price 4 * 4 = 16.
    A region of C plants with price 14 * 22 = 308.
    A region of F plants with price 10 * 12 = 120.
    A region of V plants with price 13 * 10 = 130.
    A region of J plants with price 11 * 12 = 132.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 8 = 104.
    A region of I plants with price 14 * 16 = 224.
    A region of M plants with price 5 * 6 = 30.
    A region of S plants with price 3 * 6 = 18.

Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?
'''
import math
import numpy as np
from numpy import array as vect
from tqdm import tqdm

#-------------Functions and properties
class LandPlot():
    '''This emulates one land plot 1m x 1m.'''
    def __init__(self, crop:str, pos:vect) -> None:

        self.crop = crop
        self.pos = pos
        self.in_region = False
        self.shape_coordinates = []
        for i in range(2):
            self.shape_coordinates.append(self.pos+vect([((-1)**i)*0.5,((-1)**(i+1))*0.5]))
        for i in range(2):
            self.shape_coordinates.append(self.pos+vect([((-1)**i)*0.5,((-1)**(i))*0.5]))
        # self.shape_coordinates = list(map(tuple, self.shape_coordinates))

class CropRegion():

    def __init__(self, crop:str) -> None:
        self.crop_type = crop
        self.plots = []
        self.coverture = []

    def add_plot(self, plot:LandPlot) -> bool:
        '''This adds a landplot to crop region. Returns true if successfull.'''
        if plot.in_region:
            return False
        elif plot.crop == self.crop_type:
            if not self.coverture:
                self.plots.append(plot)
                self.coverture.append(plot.pos)
                plot.in_region = True
                return True
            else:
                veredict = False #To check if this plot belongs to the group
                for position in self.coverture:
                    veredict = veredict or ((abs(position-plot.pos)==1).any() and (position==plot.pos).any())
                if veredict:
                    self.plots.append(plot)
                    self.coverture.append(plot.pos)
                    plot.in_region = True
                    return True
                else:
                    return False
        else:
            return False
        
    def __set_area(self) -> None:
        '''Sets area atribute for group.'''
        self.area = len(self.coverture)
        return None
    
    def __set_perimeter(self) -> None:
        '''Calculates the perimeter of group.'''
        total_perim = 0
        for plot in self.coverture:
            sides = []
            sides.append(plot - vect([0,-1]))
            sides.append(plot - vect([0,1]))
            sides.append(plot - vect([-1,0]))
            sides.append(plot - vect([1,0]))
            for side in sides:
                veredict = False
                for other_plot in self.coverture:
                    veredict = veredict or (side == other_plot).all()
                if not veredict:
                    total_perim += 1
                    

            # print(plot, (plot - vect([-1,0])))
            # if not ((plot - vect([-1,0])) in self.coverture):
            #     total_perim +=1
            # if not (plot - vect([ 1,0])) in self.coverture:
            #     total_perim +=1
            # if not (plot - vect([0,-1])) in self.coverture:
            #     total_perim +=1
            # if not (plot - vect([0, 1])) in self.coverture:
            #     total_perim +=1

        self.perimeter = total_perim

    def __count_sides(self) -> None:
        '''This counts all the sides from the area.'''
        buffer = []
        self.polygon_vertices = []
        self.singularities = 0 #Singularities: poits where two blocks kiss.
        for plot in self.plots:
            buffer += plot.shape_coordinates
        for point in buffer:
            if (self.count(point, buffer) == 1) or (self.count(point, buffer) == 3): #3 occurences imply an identation.
                self.polygon_vertices.append(point)
            elif (self.count(point, buffer)==2): #2 occurences means either it is on a vertice, or two lots kiss each other.
                if not self.__check_if_point_on_side(point, self.coverture):
                    self.polygon_vertices.append(point)
                    self.singularities +=0.5
        self.reduced_polygon_vertices = self.unique(self.polygon_vertices)           
        self.sides = len(self.reduced_polygon_vertices) + int(self.singularities)

    def unique(self, group:list[vect]) -> list[vect]:
        '''Returns a unique list of vectors'''
        reduced = []
        for item in group:
            present = False
            for comp_vect in reduced:
                present = present or (item == comp_vect).all()
            if not present:
                reduced.append(item)
        return reduced

    def __check_if_point_on_side(self, point_to_test:vect, group:list[vect]) -> bool:
        '''Returns true if on the side'''
        colinear_possibilities = []
        colinear_possibilities.append([(point_to_test+vect([0.5,-0.5])),(point_to_test+vect([0.5,0.5]))]) #Horizontal colinear possibility
        colinear_possibilities.append([(point_to_test+vect([-0.5,-0.5])),(point_to_test+vect([-0.5,0.5]))]) #Horizontal colinear possibility 2
        colinear_possibilities.append([(point_to_test+vect([-0.5,-0.5])),(point_to_test+vect([0.5,-0.5]))]) #Vertical colinear possibility
        colinear_possibilities.append([(point_to_test+vect([-0.5,0.5])),(point_to_test+vect([0.5,0.5]))]) #Vertical colinear possibility 2
        on_side = False
        for axis in colinear_possibilities:
            on_side = on_side or (self.__check_vect_in_list(axis[0], group) and self.__check_vect_in_list(axis[1], group))

        return on_side


    def __redundant_point(self, point_to_test:vect, group:list[vect]) -> bool:
        '''[DEPRECATED]Checks if point is between two other points in a side.'''
        colinear_possibilities = []
        colinear_possibilities.append([(point_to_test+vect([0,-1])),(point_to_test+vect([0,1]))]) #Horizontal colinear possibility
        colinear_possibilities.append([(point_to_test+vect([1,0])),(point_to_test+vect([-1,0]))]) #Vertical colinear possibility
        veredict = False
        for axis in colinear_possibilities:
            veredict = veredict or (self.__check_vect_in_list(axis[0], group) and self.__check_vect_in_list(axis[1], group))
        return veredict
    
    def __simplify_polygon(self) -> None:
        '''[DEPRECATED]This reduces the vertices removing vertices on sides.'''
        reduced_list = []
        for vertice in self.polygon_vertices:
            if not self.__redundant_point(vertice):
                reduced_list.append(vertice)
        self.reduced_polygon_vertices = reduced_list

    def count(self, vector:vect, group:list[vect]) -> int:
        '''Count how many times vector is in group.'''
        counted = 0
        for comp_vector in group:
            if (comp_vector == vector).all():
                counted +=1
        return counted

    def __check_vect_in_list(self, vector:vect, group:list[vect]) -> bool:
        '''Handy function to do checks.'''
        veredict = False
        for comp_vector in group:
            veredict = veredict or (vector == comp_vector).all()
        return veredict

    def reevaluate(self) -> None:
        '''Recalculates area and perim, and sets score.'''
        self.__set_area()
        self.__set_perimeter()
        self.__count_sides()
        self.score = self.area*self.perimeter
        self.price = self.area*self.sides



#---------------Main program
if __name__ == '__main__':

    #Reading the information:
    with open('Day12\crop_map.txt','r') as crop_map_txt:
        crop_map = crop_map_txt.read().splitlines()
    
    crop_land_plots = []
    for pos_y, line in enumerate(crop_map):
        for pos_x, crop_type in enumerate(line):
            crop_land_plots.append(LandPlot(crop_type, vect([int(pos_x),int(pos_y)])))

    crop_regions = []
    for plot_land in tqdm(crop_land_plots):
        if not plot_land.in_region:
            crop_regions.append(CropRegion(plot_land.crop))
            crop_regions[-1].add_plot(plot_land)
            scan_further = True
            while scan_further:
                scan_further = False
                for other_plot_land in crop_land_plots:
                    scan_further = scan_further or crop_regions[-1].add_plot(other_plot_land)
                    # if crop_regions[-1].add_plot(other_plot_land):
                    #     scan_further = True
                    #     crop_land_plots.remove(other_plot_land)


    total_score = 0
    total_price = 0
    for index, region in enumerate(crop_regions):
        region.reevaluate()
        total_score += region.score
        total_price += region.price
        print(f'Region {index+1} of {region.crop_type}:  (a x p) {region.area} x {region.perimeter} = {region.score} and (a x s) {region.area} x {region.sides} = {region.price}')

    print(f'The total score for this arrangement is {total_score} and price is {total_price}.')
