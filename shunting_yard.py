import re
alphanumerics = '.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
def add_ors(infix: str):
    preprocessed_infix = infix
    i = 0
    while i < len(preprocessed_infix):
        if preprocessed_infix[i] == '[':
            j = i
            while preprocessed_infix[j] != ']':
                if preprocessed_infix[j] in alphanumerics and preprocessed_infix[j+1] in alphanumerics:
                    preprocessed_infix = preprocessed_infix[:j+1] + '|' + preprocessed_infix[j+1:]
                    j += 1
                j += 1
        i += 1
    return preprocessed_infix


def validate(infix:str):
    stack = []
    opertators = ["*+?|"]
    prev = None
    inside_bracket = False

    i = 0
    while i < len(infix):
        char = infix[i]

        # unmatched parentheses
        if char in "([":
            stack.append(char)
            if char == "[":
                inside_bracket = True

        elif char in ")]":
            if not stack or (char == ")" and stack[-1] != "(") or (char == "]" and stack[-1] != "["):
                return False
            stack.pop()

            if char == "]":
                inside_bracket = False

        if char in opertators:
            if prev is None or prev in "([|":
                return False

            if char == "|" and (i + 1 == len(infix) or infix[i + 1] in "|)"):
                return False

        if char == "[" and i + 1 < len(infix) and infix[i + 1] == "]":
            return False

        if char == "(" and i + 1 < len(infix) and infix[i + 1] == ")":
            return False

        prev = char
        i += 1

    return not stack

def validate_using_re(infix:str):
    try:
        re.compile(infix)
    except re.error:
        return False
    return True


def add_concatenation(infix: str):
    preprocessed_infix = ""
    for i, char in enumerate(infix):
        preprocessed_infix += char

        if i < len(infix) - 1:
            if char in '*+?)]' and infix[i+1] not in '*+?)]&|' or \
                (char in alphanumerics and (infix[i+1] in alphanumerics or infix[i+1] in '([')):
                preprocessed_infix += '&'

    return preprocessed_infix

def preprocessing(infix:str):
    if not validate(infix):
        print('Invalid regex caught by manual validation')
        return

    if not validate_using_re(infix):
        print('Invalid regex caught by re.compile')
        return
    infix = infix.replace(' ', '')

    infix = add_ors(infix)
    infix = add_concatenation(infix)

    return infix


def shunting_yard(infix:str):
    temp_stack = []
    postfix = []
    precedence = {'*': 5, '+': 4, '?': 3,'&':2, '|': 1, '(': 0 , ')': 0, '[': 0, ']': 0}
    operators = '*+?|&'
    for i,char in enumerate(infix):
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
        elif char in alphanumerics and i == 0 or i == len(infix) - 1:
            postfix.append(char)
        elif char in alphanumerics and infix[i+1] != '-' and infix[i-1] != '-':
            postfix.append(char)
        elif char == '-':
            start_char = infix[i-1]
            end_char = infix[i+1]
            new_symbol = start_char+"-"+end_char
            postfix.append(new_symbol)

    while len(temp_stack) != 0:
        postfix.append(temp_stack.pop())

    return ''.join(postfix)


def infix2postfix(infix:str):
    infix = preprocessing(infix)
    postfix = shunting_yard(infix)
    return postfix