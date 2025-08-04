import random
import string
from hashlib import md5, sha256
from pprint import pprint


def xor(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

DEPTH = 10
NODES = 2**(DEPTH) - 1

def generate_flag(flag):
    prefix = b'COMPFEST17{'
    suffix = b'}'
    flag_bytes = flag.encode()
    flag_hash = sha256(flag_bytes).hexdigest()[:10].encode()
    return prefix + flag_bytes + b'_' + flag_hash + suffix


FLAG = generate_flag("i5n7_i7_fUn_wh3n_7h3_r3v_ch4ll_i5_actu4lly_4_c0mppr0g_problem?")
SOL_PWD_BYTES = ''.join(map(chr, [ord(random.choice(string.ascii_letters + string.digits)) for _ in range(len(FLAG))])).encode()
SOL_PWD = list(SOL_PWD_BYTES) 


class Expr:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"((int)inp[{self.x}] == {self.y})"

class FuncNode:
    def __init__(self, idx):
        self.id = idx
        self.value = random.randint(-2**7, 2**15)
        self.expr1: list[Expr] = []
        self.expr2: list[Expr] = []
        self.left_child_id = 2 * idx + 1 if (2 * idx + 1) < NODES else -1
        self.right_child_id = 2 * idx + 2 if (2 * idx + 2) < NODES else -1


true_idxs = list(range(len(FLAG)))
def pick_idxs(num):
    chosen = []
    for _ in range(num):
        if len(true_idxs) == 0:
            return [random.choice(range(len(FLAG))) for _ in range(num)]
        rand_choice = random.choice(true_idxs)
        chosen.append(rand_choice)
        true_idxs.remove(rand_choice)
    return chosen
     
def generate_expr_simple(is_correct_path):
    num_conds = random.randint(3, 8)
    chosen_idxs = pick_idxs(num_conds)
    expressions = []

    for i, idx in enumerate(chosen_idxs):
        offset = 0 if is_correct_path else (random.randint(0, 1) if i != 0 else 2)
        
        # v[x] == y
        y = SOL_PWD[idx] + offset
        x = idx
        expressions.append(Expr(x=x, y=y))
            
    return expressions


def generate_tree():
    nodes = [FuncNode(i) for i in range(NODES)]

    solution_moves = [random.choice(['l', 'r']) for _ in range(DEPTH - 3)]
    print(f"// Solution Path: {''.join(solution_moves).upper()}")

    current_node_idx = 0
    final_checksum = nodes[current_node_idx].value
    path_node_indices = {0}

    for move in solution_moves:
        if current_node_idx == -1: break
        node = nodes[current_node_idx]
        
        if move == 'l':
            node.expr1 = generate_expr_simple(True) # Correct path
            node.expr2 = generate_expr_simple(False) # Incorrect path
            current_node_idx = node.left_child_id
        else: # move == 'r'
            node.expr1 = generate_expr_simple(False) # Incorrect path
            node.expr2 = generate_expr_simple(True) # Correct path
            current_node_idx = node.right_child_id
        
        if current_node_idx != -1:
            final_checksum += nodes[current_node_idx].value
            path_node_indices.add(current_node_idx)

    for node in nodes:
        if node.id not in path_node_indices:
            node.expr1 = generate_expr_simple(False)
            node.expr2 = generate_expr_simple(False)
    
    return nodes, final_checksum

def generate_goofy_dict():
    res = {}
    GOOFY = ["COMPFEST17", "fl4g", "C0mpf3st", "flag_check", "cool_function", "Encrypt_decrypt", "free", "reverse", "wow"]
    for i in range(NODES):
        if i == 0:
            res[i] = "check"
            continue
        rand_str = '_'.join(random.sample(GOOFY, 2) + [md5(str(i).encode()).hexdigest()[:6]])
        res[i] = rand_str
    return res

FUNC_DICT = generate_goofy_dict()

def generate_func(node: FuncNode):
    res = f"void {FUNC_DICT[node.id]} (const std::string& inp, long long* checksum) {{"
    res += f"\n\t*checksum += {node.value};"
    
    def bundle_exprs(exprs):
        return " && ".join([f"({e})" for e in exprs])

    has_left = node.left_child_id != -1 and node.expr1
    has_right = node.right_child_id != -1 and node.expr2
    
    if has_left:
        res += f"\n\tif ({bundle_exprs(node.expr1)}) {{"
        res += f"\n\t\t{FUNC_DICT[node.left_child_id]}(inp, checksum);"
        res += f"\n\t}}"
    
    if has_right:
        clause = "else if" if has_left else "if"
        res += f"\n\t{clause} ({bundle_exprs(node.expr2)}) {{"
        res += f"\n\t\t{FUNC_DICT[node.right_child_id]}(inp, checksum);"
        res += f"\n\t}}"

    res += "\n}\n"
    return res

def vectorize_ints(lst):
    return '{' + ','.join(list(map(str, lst))) + '}'


SOL_KEY = xor(SOL_PWD_BYTES, FLAG)
print(f"// Secret Password: {SOL_PWD_BYTES.decode()}")

with open('./password', 'w') as f:
    f.write(SOL_PWD_BYTES.decode())

print(f'// Flag: {FLAG.decode()}' )
nodes, final_checksum = generate_tree()
print(f"// Checksum: {final_checksum}")


headers = "#include <iostream>\n#include <string>\n#include <vector>\n\nusing namespace std;\n"

# Forward declarations for all functions
forward_declarations = ""
for i in range(NODES):
    forward_declarations += f"void {FUNC_DICT[i]}(const std::string&, long long*);\n"

# Main C++ function
main_func = f"""
void print_flag(const std::string& input){{
    vector<int> xor_key = {vectorize_ints(SOL_KEY)};
    for ( int i = 0; i < input.length(); i++){{
        cout << (char)(xor_key[i] ^ (int) input[i] ) ;
    }}
    cout << endl;
}}

int main(){{
    string input;
    long long checksum = 0;
    cout << "Enter the password: ";
    cin >> input;
    if (input.length() != {len(FLAG)}) {{
        cout << "Incorrect." << endl;
        return 1;
    }}
    check(input, &checksum);
    if (checksum == {final_checksum}LL){{
        cout << "Correct! Here is your flag: ";
        print_flag(input);
    }} else {{
        cout << "Incorrect." << endl;
    }}
    return 0;
}}
"""

function_definitions = ""
node_indices = list(range(NODES))
random.shuffle(node_indices)
for i in node_indices:
    function_definitions += generate_func(nodes[i])

final_code = headers + "\n" + forward_declarations + "\n" + function_definitions + "\n" + main_func

with open("challenge.cpp", "w") as f:
    f.write(final_code)

print("\nSuccessfully generated 'challenge.cpp'")