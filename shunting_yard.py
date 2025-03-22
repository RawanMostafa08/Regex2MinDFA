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

        

def preprocessing(infix:str):
    if not validate(infix):
        print('Invalid regex')
        return
    
    infix = infix.replace(' ', '')
    infix = replace_dot(infix)
    infix = handle_ranges(infix)
    infix = add_ors(infix)
    return infix

print(preprocessing('[a-z]'))


        