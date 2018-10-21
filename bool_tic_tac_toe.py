from random import randint

def get_binary_string(binary):
    binary = format(binary, '0b')
    return '0'*(9-len(binary))+binary

def print_scoreboard(table, mask):
    row, mask, table = "", get_binary_string(mask), get_binary_string(table)
    
    for i, v in enumerate(table):
        row += '-' if mask[i]=='0'else ('X' if v == '1' else 'O')
    
        if (i+1)% 3 == 0:
            print(row)
            row = ""
            
def get_random_index(l):
    p = randint(0, len(l)-1)
    return l[p], l[:p]+l[p+1:]

def winner(table, a):
    masks = [0b111000000, 0b000111000, 0b000000111,
             0b100100100, 0b010010010, 0b001001001,
             0b100010001, 0b001010100]
    
    for m in masks:
        if  a & (table & m == m):
            return 1
        if ~a & ((~table & 0b111111111) & m == m):
            return 0
    return -1

def simulation_tic_tac_toe(M, debug=True):
    prob = dict()
    prob.update({'X': 0, 'O': 0, 'DRAW': 0})
    
    for i in range(M):
        base, mask, number, actual = list(range(9)), 0, 0, 1 
        
        while len(base) > 0:
            p, base = get_random_index(base)
            mask |= 1 << p
            number = number | 1 << p if actual else number
            update = winner(number & mask if actual else number | (~mask & 0b111111111), actual)
            
            if debug:
                print_scoreboard(number, mask)
                print("")
                        
            if update == 1:
                    if debug: 
                        print("X WINS!")
                    prob['X'] += 1
                    break
            
            if update == 0:
                    if debug:
                        print("O WINS!")
                    prob['O'] += 1
                    break
                
            actual = int(not(actual))
        
        if winner(number & mask if actual else number | (~mask & 0b111111111), actual) == -1:
            prob['DRAW'] += 1
            if debug:
                print("DRAW")
    return prob

M = 2
probs = simulation_tic_tac_toe(M, debug = True)

for k, prob in probs.items():
    print("P(Y="+str(k)+")="+str(prob)+"/"+str(M)+"="+"%.2f"%(1.0*prob/M))