import os

DELIMITER = '==========================='

def clear_cls():
    os.system('cls')

def menu(lines, header='', footer='', input_text=''):
    print(DELIMITER)
    menu_items = [f"{index + 1}) {lines[index]}" for index in range(len(lines))]
    if header != '':
        print(header)
    print('\n'.join(menu_items))
    if footer != '':
        print(footer)
    print(DELIMITER)
    try:
        return int(input(input_text)) or -1
    except:
        return -1
