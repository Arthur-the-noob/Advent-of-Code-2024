'''
--- Day 5: Print Queue ---

Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47

The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

    75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
    47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
    61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
    53 is correctly fourth because it is before page number 29 (53|29).
    29 is the only page left and so is correctly last.

Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13

These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?
--- Part Two ---

While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.

After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

Your puzzle answer was 4260.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your Advent calendar and try another puzzle.

If you still want to see it, you can get your puzzle input.

You can also [Shareon Bluesky Twitter Mastodon] this puzzle.


'''
#-----------Base class and functions--------------------------------
def sorter_with_rules(rules:dict, instruction:list) -> list:
    '''This storts a list of str based on given rules'''
    sort_pool = instruction.copy()
    sorted_list = []
    tail = []
    while len(sort_pool) > 0:
        for element in sort_pool:
            #If not in rule, should go to the end
            if not element in rules.keys():
                tail.append(element)
                sort_pool.remove(element)
            #If no element is after this one by rules, than it is the last one in order
            elif not (set(sort_pool) & set(rules[str(element)])):
                sorted_list.append(element)
                sort_pool.remove(element)
                break
    full_list = tail+sorted_list
    full_list.reverse() #Because we started with last to first.
    return full_list

#-----------Main program itself----------------------------
if __name__ == '__main__':

    #Read input:
    with open('Day 5\instruction_maual.txt', 'r') as manual:
        full_manual = manual.readlines()
    full_manual = [line.replace('\n','') for line in full_manual]

    #-----------------------------
    instructions = []
    rules = []

    for line in full_manual:
        if len(line) == 0:
            continue
        elif (len(line) -len(line.replace('|',''))) == 0:
            instructions.append(line)
        else:
            rules.append(line)

    rules_digested = [[line.split('|')[0],line.split('|')[1]] for line in rules]
    keys_for_dict = [rule[0] for rule in rules_digested]

    #I prefere to complie the list of all pages after page X so it is easier to evaluate
    before_than_dict = {}
    for key in keys_for_dict:
        comes_before_than = []
        for line in rules_digested:
            if line[0] == key:
                comes_before_than.append(line[1])
        before_than_dict[key] = comes_before_than
    
    instructions_digested = []
    for line in instructions:
        instructions_digested.append([x for x in line.split(',')])

    #Now calculating what was asked of us
    total_of_middle_pages = 0
    for line in instructions_digested:
        answer = sorter_with_rules(before_than_dict, line)
        if not answer == line: # "not" for second part only
            pos = int((len(answer)-1)/2)
            total_of_middle_pages += int(answer[pos])
    
    print(total_of_middle_pages)