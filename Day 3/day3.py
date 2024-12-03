'''Day 3 of the advent of code 2025'''

#Functions
def dos_and_donts(raw_data: str, verbose: bool = False) -> (str, str):
    '''This function snips the dos and donts according to the instructions'''
    active_instruction = ''
    inactive_instruction = ''
    donts_bits = raw_data.split('don\'t()')
    active_instruction += donts_bits[0]
    for split_bit in donts_bits[1:]:
        try:
            ignore, activate = split_bit.split('do()', 1)
            active_instruction += activate
            inactive_instruction += ignore
        except:
            inactive_instruction += split_bit
            continue
    if verbose: print(f'Original size = {len(raw_data)}, split size = {len(active_instruction)}')
    return (active_instruction, inactive_instruction)


def select_valid_inputs(raw_data: str, verbose:bool = False) -> list:
    '''This reads the inputs and gives back valid mul pairs'''
    discrete_input = raw_data.split('mul(')
    valid_inputs = []
    for i in range(len(discrete_input)):
        
        try:
            new_entryA, rest = discrete_input[i].split(',',1)
        except:
            if verbose: print(f'{discrete_input[i]}---> Not considered because only one number')
            continue
        if len(new_entryA)>3:
            if verbose: print(f'{discrete_input[i]}---> Not considered because too large')
            continue #→ Max 3 digit numbers
        if not len(new_entryA) == len(new_entryA.replace(" ","")): 
            if verbose: print(f'{discrete_input[i]}---> Not considered because white spaces')
            continue #→ No white spaces allowed inside brackets
        try:
            new_entryB, _ = rest.split(')',1)
        except:
            new_entryB = rest.replace(')','')
            if len(rest) == len(new_entryB):
                if verbose: print(f'{discrete_input[i]}---> Not considered because no closing brackets')
                continue
        if len(new_entryB)>3: 
            if verbose: print(f'{discrete_input[i]}---> Not considered because too large')
            continue
        if not len(new_entryB) == len(new_entryB.replace(" ","")): 
            if verbose: print(f'{discrete_input[i]}---> Not considered because white spaces')
            continue
        try:
            new_entryA = int(new_entryA)
            new_entryB = int(new_entryB)
        except:
            if verbose: print(f'{new_entryA, new_entryB}---> Not considered because cannot convert')
            continue
        entry = [new_entryA, new_entryB]
        valid_inputs.append(entry)
    return valid_inputs
            
def mul(entries: list) -> int:
    '''Multiply pairs in a list and then return sum.'''
    result = 0
    for entry in entries:
        result += entry[0]*entry[1]
    
    return result

#Main code
if __name__ == '__main__':

    #Reading the input
    with open('Day 3\mul_input.txt') as file:
        raw_input = file.read()

    print(f'Original result = {mul(select_valid_inputs(raw_input))}')
    new_input, refused_input = dos_and_donts(raw_input)
    print(len(new_input), len(refused_input))
    print(f'Filtered does and donts result = {mul(select_valid_inputs(new_input))}')
    print(f'Filtered does and donts result that was ignored = {mul(select_valid_inputs(refused_input))}')
