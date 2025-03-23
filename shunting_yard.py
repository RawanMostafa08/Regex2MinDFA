import re
alphanumerics = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def replace_dot(infix:str):
    infix = infix.replace('.', '[a-zA-Z0-9]')
    return infix

#d-i --> d|e|f|g|h|i
#D-I --> A|B|C|D|E|F|G|H|I
#[d-iD-I]
def handle_ranges(infix: str):
    preprocessed_infix = ''
    for i,char in enumerate(infix):
        if char == '-':
            start_char = infix[i-1]
            end_char = infix[i+1]
            start_idx = alphanumerics.index(start_char)
            end_idx = alphanumerics.index(end_char)
            ored_str = ''
            for j in range(start_idx+1, end_idx):
                ored_str += '|' 
                ored_str += alphanumerics[j]
            preprocessed_infix += ored_str
            preprocessed_infix += '|'
        else:
            preprocessed_infix += char
    return preprocessed_infix

#[d|e|f|g|h|iD|E|F|G|H|I]
def add_ors(infix: str):
    preprocessed_infix = infix
    for i,char in enumerate(infix):
        if char == '[':
            j = i
            while preprocessed_infix[j] != ']':
                if preprocessed_infix[j] in alphanumerics and preprocessed_infix[j+1] in alphanumerics:
                    preprocessed_infix = preprocessed_infix[:j+1] + '|' + preprocessed_infix[j+1:]
                j = j+1
    return preprocessed_infix

def validate(infix:str):
    try: 
        re.compile(infix)
    except re.error:
        return False
    return True


#(abc + bcd).a.x
#ax
#a(bx)
def add_concatenation(infix: str):
    preprocessed_infix = ""
    for i, char in enumerate(infix):
        preprocessed_infix += char 
        
        if i < len(infix) - 1:
            if char in '*+?)]' and infix[i+1] not in '*+?)].|' or \
                (char in alphanumerics and (infix[i+1] in alphanumerics or infix[i+1] in '([')):
                preprocessed_infix += '.'
    
    return preprocessed_infix

def preprocessing(infix:str):
    if not validate(infix):
        print('Invalid regex')
        return
    
    infix = infix.replace(' ', '')
    infix = replace_dot(infix)
    infix = add_concatenation(infix)
    infix = handle_ranges(infix)
    infix = add_ors(infix)
    return infix


def shunting_yard(infix:str):
    temp_stack = []
    postfix = []
    precedence = {'*': 5, '+': 4, '?': 3,'.':2, '|': 1, '(': 0 , ')': 0, '[': 0, ']': 0}
    operators = '*+?|.'
    for char in infix:
        if char == '(' or char == '[':
            temp_stack.append(char)
        elif char == ')':
            while temp_stack[-1] != '(':
                postfix.append(temp_stack.pop())
            temp_stack.pop()
        elif char == ']':
            while temp_stack[-1] != '[':
                postfix.append(temp_stack.pop())
            temp_stack.pop()
        elif char in operators: 
            while len(temp_stack) !=0 and precedence[temp_stack[-1]] >= precedence[char]:
                postfix.append(temp_stack.pop())
            temp_stack.append(char)
        elif char in alphanumerics:
            postfix.append(char)
        
    while len(temp_stack) != 0:
        postfix.append(temp_stack.pop())

    return ''.join(postfix)


def infix2postfix(infix:str):
    infix = preprocessing(infix)
    postfix = shunting_yard(infix)
    return postfix

        
print(infix2postfix('(A+B*)?(C|D)'))
print(infix2postfix('(02)+|CD'))
# 
# stack   : ? ( | 
# postfix : A B * + C 