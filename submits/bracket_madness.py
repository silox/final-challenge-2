def bracket_checker(string):
    stack = []
    for char in string:
        if stack:
            if char == ')' and stack[-1] == '(':
                stack.pop()
            elif char == ']' and stack[-1] == '[':
                stack.pop()
            elif char in '([':
                stack.append(char)
            else:
                return False
        elif char in ')]':
            return False
        else:
            stack.append(char)

    return not stack


print('hotkao' if bracket_checker(input()) else 'kahoot')
