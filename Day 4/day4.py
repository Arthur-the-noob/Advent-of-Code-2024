'''
--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?

'''
#Creating a class for the letter
class Letter():
    '''This allows us to check if letters are active, set their position and value'''
    def __init__(self, value:str, pos:tuple):

        self.value = value
        self.display_value = value
        self.pos = tuple
        self.part_of_solution = False #This is set FALSE by default

    def toggle_solution(self, mode:str) -> None:
        '''Can toggle solution ON or OFF. ON: Shows only part of answer.'''
        if mode.lower() == 'on':
            if self.part_of_solution: self.display_value = self.display_value
            else: self.display_value = '-'
        if mode.lower() == 'off':
            self.display_value = self.value

class Puzzle():
    '''This helps managing the letters.'''
    def __init__(self, puzzle_source:str):
        '''This class scans the puzzle from a TXT file.'''
        self.__read(puzzle_source)
    
    def __read(self, address) -> None:
        '''This function creates the puzzle from a TXT file'''
        self.puzzle = []
        with open(address, 'r') as source:
            puzzle_lines = source.readlines()
        for i, line in enumerate(puzzle_lines):
            line = line.replace('\n','')
            self.puzzle.append([])
            for j,letter in enumerate(line):
                self.puzzle[i].append(Letter(letter,(i,j)))
    
    def __evaluate_list(self, letter_list:list) -> str:
        '''This evaluates word in list of (line,row) direct and reverse order and returns a pair.'''
        word_output = ''
        for address in letter_list:
            word_output += self.puzzle[address[0]][address[1]].value
        return word_output, word_output[::-1]
    
    def __flag_as_solution_list(self, letter_list:list) -> None:
        '''This evaluates word in list of (line,row) direct and reverse order and returns a pair.'''
        word_output = ''
        for address in letter_list:
            self.puzzle[address[0]][address[1]].part_of_solution = True
        return None

    def solve_cross_3letter(self, search_word:str) -> int:
        '''This solves for word and returns # of occurences. Pallindromes count only as 1 hit every time. Needs odd numbered word.'''
        #Set up
        #Set up:
        word_count = 0
        word_len = 3
        mid_point = 1
        anchor = search_word[mid_point]
        tentacle = search_word[0]+ search_word[2]
        for line in range(mid_point, len(self.puzzle)-1):
            for row in range(mid_point, len(self.puzzle[line])-1):
                if self.__evaluate_list([(line,row)])[0] == anchor:
                    investigate_tentacles = []
                    investigate_tentacles.append([(line-1, row-1),(line+1, row+1)])
                    investigate_tentacles.append([(line+1, row-1),(line-1, row+1)])
                    investicate_tentacles_values = [self.__evaluate_list(tentaclex) for tentaclex in investigate_tentacles]
                    evaluation_tentacle = [((test_value[0] == tentacle)|(test_value[1] == tentacle)) for test_value in investicate_tentacles_values]
                    if evaluation_tentacle[0] and evaluation_tentacle[1]:
                        word_count +=1
                        self.__flag_as_solution_list([(line,row)])
                        for tentacle_list in investigate_tentacles:
                            self.__flag_as_solution_list(tentacle_list)
        
        self.toggle_puzzle('on')
        return word_count



    def solve(self, search_word:str) -> int:
        '''This solves for word and returns # of occurences. Pallindromes count only as 1 hit every time.'''
        #Set up:
        word_count = 0
        word_len = len(search_word)
        word_limit = word_len -1
        #Horizontal search:
        for line in range(len(self.puzzle)):
            for row in range(len(self.puzzle[line])-word_limit):
                word_list = [(line, x) for x in range(row, row+word_len)]
                combinations = self.__evaluate_list(word_list)
                if (combinations[0] == search_word) | (combinations[1] == search_word):
                    word_count +=1
                    self.__flag_as_solution_list(word_list)
        #Vertical search:
        for row in range(len(self.puzzle[0])):
            for line in range(len(self.puzzle)-word_limit):
                word_list = [(x, row) for x in range(line, line+word_len)]
                combinations = self.__evaluate_list(word_list)
                if (combinations[0] == search_word) | (combinations[1] == search_word):
                    word_count +=1
                    self.__flag_as_solution_list(word_list)

        #Obtouse diagonals
        for line in range(word_limit, len(self.puzzle)):
            for row in range(len(self.puzzle[line])-word_limit):
                word_list = [(line-x, row+x) for x in range(word_len)]
                combinations = self.__evaluate_list(word_list)
                if (combinations[0] == search_word) | (combinations[1] == search_word):
                    word_count +=1
                    self.__flag_as_solution_list(word_list)
        
        #Obliquous diagonals
        for line in range(len(self.puzzle)-word_limit):
            for row in range(len(self.puzzle[line])-word_limit):
                word_list = [(line+x, row+x) for x in range(word_len)]
                combinations = self.__evaluate_list(word_list)
                if (combinations[0] == search_word) | (combinations[1] == search_word):
                    word_count +=1
                    self.__flag_as_solution_list(word_list)

        self.toggle_puzzle('on')
        return word_count

    def toggle_puzzle(self, mode:str):
        '''Toggles puzzle on or of based on searched words.'''
        for line in self.puzzle:
            for letter in line:
                letter.toggle_solution(mode)

    def show(self, save = False):
        '''This prints the puzzle on the console.'''
        
        output_string =''
        for line in self.puzzle:
            for letter in line:
                print(letter.display_value, end="")
                output_string +=letter.display_value
            print('\n')
            output_string +='\n'
        if save:
            path = 'Day 4\\result.py'
            with open(path, 'w') as output_file:
                output_file.write(output_string)



if __name__ == '__main__':

    puzzle_source = 'Day 4\word_search_puzzle.txt'
    puzzle = Puzzle(puzzle_source)
    # result = puzzle.solve(search_word='XMAS')
    result = puzzle.solve_cross_3letter(search_word='MAS')
    puzzle.show(save=True)
    print(f'The word XMAS was found {result} times.')