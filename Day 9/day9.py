'''
--- Day 9: Disk Fragmenter ---

Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402

The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

0..111....22222

The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899

The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......

The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............

The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)

Your puzzle answer was 6448989155953.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..

The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?

'''
from tqdm import tqdm

#---------------Functions and classes
class MemorySpace():
    '''This simulates a memory space that can decide how to act.'''
    def __init__(self, pos:int, information:str='.', strip_id:int = 0):
        self.content = information
        self.occupied = False
        if not self.content == '.': self.occupied = True
        self.pos = pos
        self.strip_id = strip_id

class MemoryCard():
    '''This simulates the complete memory of the system.'''
    def __init__(self):
        self.memory_bits = []

    def load(self, disk_map:list[str]) -> None:
        '''This loads the memory into memory card.'''
        info_ID = 0
        strip_ID = 0
        for index in range(len(disk_map)):
            if index%2 == 0:
                for _ in range(int(disk_map[index])):
                    position = len(self.memory_bits)
                    self.memory_bits.append(MemorySpace(position, information=info_ID, strip_id=strip_ID))
                info_ID +=1
            else:
                for _ in range(int(disk_map[index])):
                    position = len(self.memory_bits)
                    self.memory_bits.append(MemorySpace(position, strip_id=strip_ID))
            strip_ID +=1        
            
    
    def print_out_loaded_memory(self,max_digits:int = None) -> None:
        '''Prints out loaded memory.'''
        if max_digits == None:
            range_print = len(self.memory_bits)
        else:
            range_print = max_digits
        for index in range(range_print):
            print(self.memory_bits[index].content, end='')
        return None
    
    def fragment_disk(self) -> None:
        '''This cycles the fragment disk steps.'''
        frag_flag = True
        while frag_flag:
            frag_flag = self.__fragment_disk_step()

    def __fragment_disk_step(self) -> bool:
        '''This emulates the disk fragment algorythim described.'''
        empty_bits = []
        information_bits = []
        for memory_bit in self.memory_bits:
            if memory_bit.occupied:
                information_bits.append(memory_bit)
            else:
                empty_bits.append(memory_bit)
        
        first_free_space = empty_bits[0].pos
        if first_free_space >= len(information_bits): return False #This exits without changing
        fragmentable_information = information_bits[first_free_space:]
        fragmentable_information.reverse()
        free_space = len(empty_bits)
        movable_memory = len(fragmentable_information)
        
        range_fragmentation = min(free_space, movable_memory)
        for index in range(range_fragmentation):
            empty_bits[index].content = fragmentable_information[index].content
            empty_bits[index].occupied = True
            fragmentable_information[index].content = '.'
            fragmentable_information[index].occupied = False
        return True

    def checksum(self) -> int:
        '''This calculates the checksum of the memory'''
        checksum = 0
        for memory_bit in self.memory_bits:
            if memory_bit.content == '.':
                value = 0
            else:
                value = int(memory_bit.content)
            checksum += value*memory_bit.pos
        return checksum

    def __file_stripper(self) -> None:
        '''Using the second method mentioned.'''
        self.empty_strips = {}
        self.used_strips = {}
        for memory_bit in self.memory_bits:
            if memory_bit.occupied:
                target_list = self.used_strips
            else:
                target_list = self.empty_strips

            if memory_bit.strip_id in target_list.keys():
                target_list[memory_bit.strip_id] += [memory_bit.pos]
            else:
                target_list[memory_bit.strip_id] = [memory_bit.pos]

        self.empty_slots = list(self.empty_strips.values())
        self.movable_blocks = list(self.used_strips.values())[1:]
        self.movable_blocks.reverse()
    
    def __memory_switcher(self, memory_strip:list[str], empty_memory:list[str]) -> bool:
        '''Switches position memory, returns True if succeeds.'''
        if not len(memory_strip) <= len(empty_memory):
            return False
        for index in range(len(memory_strip)):
            self.memory_bits[empty_memory[index]].content = self.memory_bits[memory_strip[index]].content
            self.memory_bits[memory_strip[index]].content = '.'
            self.memory_bits[memory_strip[index]].occupied = False
            self.memory_bits[empty_memory[index]].occupied = True
        return True

    def defragment_special(self) -> bool:
        '''Runs one round of special defragmentation. Part2 of problem.'''
        self.__file_stripper()
        flag_change_possible = False
        change_wave = self.movable_blocks
        for movable_bloc in tqdm(change_wave):
            for slot in self.empty_slots:
                if movable_bloc[0] > slot[0]:
                    if self.__memory_switcher(movable_bloc,slot):
                        self.__file_stripper()
                        break
        return flag_change_possible
    
    # def defragment_special(self):
    #     '''Loops fragmentation step.'''
    #     should_continue = True
    #     while should_continue:
    #         self.print_out_loaded_memory()
    #         should_continue = self.__defragment_special()


#---------------Program
if __name__ == '__main__':

    #Read the map:
    with open('Day 9\disk_map.txt', 'r') as disk_map_file:
        disk_map = disk_map_file.read()
    disk_map = str(disk_map)
    memory_disk = MemoryCard()
    memory_disk.load(disk_map)
    # memory_disk.print_out_loaded_memory()
    # memory_disk.fragment_disk()
    # print('\n---------------------------')
    # memory_disk.print_out_loaded_memory()
    memory_disk.defragment_special()
    print(f'\nThe checksum is: {memory_disk.checksum()}.')


