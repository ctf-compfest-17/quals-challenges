import os
from pprint import pprint
import re

def extract_index(expression: str):
    match = re.search(r'std::string::operator\[\]\(\(?[^\),]*, *(\d+)\)', expression)
    if match:
        return int(match.group(1))
    return None

DUMP_PATH = "./func_dumps/functions"

def is_user_func(func_name):
    return 'COMPFEST17' in func_name or 'flag' in func_name or 'fl4g' in func_name or 'pico' in func_name or 'reverse' in func_name or 'C0mp' in func_name or 'cool' in func_name or 'check' in func_name
 
def read_contents(path):
    with open(DUMP_PATH + '/' + path, 'r') as f:
        return f.read()
    
def scrape_sum(func_name):
    contents = read_contents(func_name)
    try:
        checksum = contents.split('*checksum += ')[1].split(';')[0]
        return int(checksum)
    except:
        try:
            checksum = contents.split('*checksum -= ')[1].split(';')[0]
            return -int(checksum)
        except:
            checksum = 0 if '--' not in contents else 1
            return -checksum

def scrape_expressions(func_name):
    contents = read_contents(func_name)
    lines = contents.split('\n')

    
def scrape_calls(func_name):
    contents = read_contents(func_name)
    lines = contents.split('\n')
    calls = []
    for l in lines:
        if 'inp, checksum' in l:
            calls.append(l.strip().removesuffix("(inp, checksum);"))
    return tuple(calls)
    
def strip_details(func_name):
    # if '_Z' not in func_name:
    #     return func_name
    # func_name = func_name[len('_ZXX'):]
    # func_name = func_name.replace('RKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEPx','')
    return func_name


def find_path_recursive(node, current_sum, target_sum, checksums, children_map):
    new_sum = current_sum + checksums[node]

    if new_sum == target_sum:
        return [node]

    if not children_map.get(node):
        return None

    for child in children_map[node]:
        path = find_path_recursive(child, new_sum, target_sum, checksums, children_map)
        if path:
            return [node] + path
            
    return None

paths = os.listdir(DUMP_PATH)
func_paths = list(filter(is_user_func, paths))

# TREEE
func_checksums = {}
func_children = {}
target = 210487

for path in func_paths:
    checksum = scrape_sum(path)
    func_checksums[strip_details(path)] = checksum
    func_children[strip_details(path)] = scrape_calls(path)

# pprint(func_children)
from json import dumps

json_tree = open("tree.json", "w")
json_checksum = open("checksum.json", "w")
json_tree.write(dumps(func_children))
json_checksum.write(dumps(func_checksums))



solution = find_path_recursive('check', 0, target, func_checksums, func_children)


# Testing apakah solution exist
checksum_test = 0

for k, func in enumerate(solution):
    calls = scrape_calls(func)
    checksum_test += scrape_sum(func)
    if k == len(solution)-1:
        break
    assert solution[k+1] in calls

assert checksum_test == target

constraint_dump = open("constraint_dump", "w")
good_constraints = open('z3_constraints', 'w')

def safe_exit():
    print('EXITING:')
    good_constraints.close()
    exit()


for k, func in enumerate(solution):
    calls = scrape_calls(func)
    if k == len(solution)-1:
        break
    left_or_right = 0 if solution[k+1] == calls[0] else 1
    contents = read_contents(func)
    constraint_dump.write(f'\n\n##### FUNCTION {func} GOES TO {solution[k+1]} ({left_or_right}) #######\n')
    if left_or_right == 0:
        shit_exprs = contents[:contents.index(calls[0]) ]
        constraint_dump.write(shit_exprs)
        
    else:
        shit_exprs = contents[contents.index(calls[0]) + len(calls[0]):contents.index(calls[1]) + len(calls[1])]
        constraint_dump.write(shit_exprs)
    shit_lines = shit_exprs.splitlines()
    filter_the_non_shits = lambda x: x.startswith('  ') and '}' not in x and '//' not in x and len(x) > 2
    
    good_lines = list(filter(filter_the_non_shits, shit_lines))
    pprint(good_lines)
    line_num = 0
    while line_num < len(good_lines)-4:
        block = good_lines[line_num:line_num+5]

        # case 1: EQ (inverse)
        if 'goto LABEL' in block[1]:
            print('eq ops')

            first = block[0].replace(') != ', ' ').replace(')', '').split()[-2]
            second = block[0].replace(') != ', ' ').replace(')', '').split()[-1]
            good_constraints.write(f'# case 1\n')
            good_constraints.write(f'solver.add(inp[{first}] == {second})\n')
            print('wrote constraints')
            line_num += 2
        # case 2: XOR (invers)
        elif 'goto LABEL' in block[-1]:
            print('xor ops')
            first = block[0].replace(');', '').split('inp, ')[-1]
            second = block[1].replace('));', '').split('inp, ')[-1]
            res = block[3].replace(' )', '').split('!= ')[-1]
            operator = block[3].split()[3]
            v8 = f'inp[{first}]'
            if operator.strip() == '-':
                operator2 = '&'
                v9 = f'{v8} | inp[{second}]'
            else:
                operator2 = '|'
                v9 = f'{v8} & inp[{second}]'
            v10 = f'inp[{first}]'
       
            good_constraints.write(f'solver.add_soft( (({v9}) {operator if '-' in operator or '+' in operator else 'ERROR'} ({v10}  {operator2} inp[{second}])) == {res})\n')
            line_num += 5
        # case 3: IDFK
        elif 'if ( ' in block[0]:
            print('fuck ops')
            
            # equality
            if '==' in block[0] and 'if' in block[0] and ' | *' not in block[0] and '- (c' not in block[0]:
                print('IM HERE 1')
                res = block[0].replace(') ==', '').split()[-1]
                idx = block[0].replace(') ==', '').split()[-2]
                good_constraints.write(f'# case 2\n')

                good_constraints.write(f'solver.add(inp[{idx}] == {res})\n')

            # 2 cases, xornya bisa terhadap char dengan nilai yang sama (di IDA decompilenya beda)

            # stupid case:
            if '== (' in block[4] :
                print('IM HERE 2')
                first = block[1].replace('),', '').split()[-1]
                second = block[4].replace(')))', ' ').split()[-1]
                good_constraints.write(f'solver.add(inp[{first}] == inp[{second}])\n')

            if '- (char)' in block[4]:
                assert '| *(_BYTE' in block[2]
                first = extract_index(block[1])
                second =extract_index(block[2])
                res = block[4].replace(') )', '').split()[-1]
                v66 = f'inp[{first}]'
                v67 = f'{v66} | inp[{second}]'
                v68 = f'inp[{first}]'
                good_constraints.write(f'solver.add_soft( (({v67}) - ({v68} & inp[{second}])) == {res})\n')

            elif '+ (char)' in block[4]:
                assert '& *(_BYTE' in block[2]
                first = extract_index(block[1])
                second =extract_index(block[2])
                res = block[4].replace(') )', '').split()[-1]
                v66 = f'inp[{first}]'
                v67 = f'{v66} & inp[{second}]'
                v68 = f'inp[{first}]'
                good_constraints.write(f'solver.add_soft( (({v67}) + ({v68} | inp[{second}])) == {res})\n')


            first = block[0].replace('),', '').replace('(inp,','').split()[-1]
            line_num += 4
        else:
            line_num += 1

    print(func)
    # print('\n'.join(good_lines))
