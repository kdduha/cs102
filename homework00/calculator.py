import typing as tp
import math


def check_num_type(num: tp.Any) -> bool:
    return isinstance(num, float)


def input_numbers(command: str) -> tuple[float, float]:
    if command in ['-', '+', '/', '*', '^', 'convert']:
        try:
            num_1 = float(input('Введите число 1 > '))
        except ValueError:
            print('Введите число')
            return input_numbers(command)
        try:
            num_2 = float(input('Введите число 2 > '))
        except ValueError:
            print('Введите число')
            return input_numbers(command)
    else:
        try:
            num_1 = num_2 = float(input('Введите число > '))
        except ValueError:
            print('Введите число')
            return input_numbers(command)
    return num_1, num_2


def convert(num: int, new_base: int) -> str:
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num < new_base:
        return symbols[num]
    return convert(num // new_base, new_base) + symbols[num % new_base]


def check_brackets(string: str) -> bool:
    array = ''.join([i for i in string if i in '()'])
    count = 0
    while '()' in array:
        array = array.replace('()', '')
        count += 1
    return bool(len(array))


def logic(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    match command:
        case "+":
            return num_1 + num_2
        case "-":
            return num_1 - num_2
        case "/":
            if num_2 != 0:
                return num_1 / num_2
            return "На ноль делить нельзя"
        case "*":
            return num_1 * num_2
        case "^":
            return num_2 ** num_1
        case "^2":
            return num_1 ** 2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tg":
            return math.tan(num_1)
        case "ctg":
            if math.tan(num_1) != 0:
                return 1 / math.tan(num_1)
            return 'Котангенс не определен'
        case "ln":
            if num_1 > 0:
                return math.log(num_1)
            return 'Аргумент должен быть положительным'
        case "log":
            if num_1 > 0:
                return math.log10(num_1)
            return 'Аргумент должен быть положительным'
        case 'convert':
            if num_2 > 9:
                return 'База новой системы счисления не должна быть больше 9'
            if (num_1 > 0 and num_2 > 0) and (int(num_1) == num_1 and int(num_2) == num_2):
                return convert(int(num_1), int(num_2))
            return 'Для перевода в другую систему счисления введите натуральные числа'
        case _:
            return f"Неизвестный оператор: {command!r}."


def calc_string(string: str) -> tp.Union[float, str]:
    if not check_brackets(string):
        print('Скобки расставлены неверно, давайте еще раз')
    elif string == 'end':
        return 'Выход из режима строки'
    else:
        array = string.split()
    pass



if __name__ == "__main__":
    while True:
        COMMAND = input("Введите операцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if COMMAND == 'string':
            print('Введите строку выражения:')
            STRING = input()
            ANSWER = calc_string(STRING)
        else:
            NUM_1, NUM_2 = input_numbers(COMMAND)
            ANSWER = logic(NUM_1, NUM_2, COMMAND)
        print(ANSWER)
    print('До скорых встреч!')
