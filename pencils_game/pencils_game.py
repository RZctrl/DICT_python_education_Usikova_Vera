import random

def get_pencil_count():
    """
    Функція запитує у користувача кількість олівців для подальшої гри

    Returns:
        int: кількість олівців для гри
    """
    while True:
        pencil_input = input("How many pencils would you like to use:\n")

        if not pencil_input.lstrip('-').isdigit():
            print("The number of pencils should be numeric")
            continue

        pencils = int(pencil_input)
        if pencils <= 0:
            print("The number of pencils should be positive")
            continue

        return pencils


def get_first_player(player1: str, bot: str):
    """
    Запитує у гравця хто буде ходити першим - він/людина або бот

    Parameters:
        player1 (str): ім'я гравця/людини
        bot (str): ім'я бота

    Returns:
        str: ім'я того, хто буде ходити першим
    """
    while True:
        first_player = input(f"Who will be the first ({player1}, {bot}):\n")
        if first_player == player1 or first_player == bot:
            return first_player
        print(f"Choose between '{player1}' and '{bot}'")


def get_human_turn(current_pencils: int):
    """
    Запитує у людини скільки саме олівців людина хоче взяти

    Parameters:
        current_pencils (int): поточна кількість олівців, що залишилась

    Returns:
        int: кількість олівців, які гравець/людина взяв
    """
    while True:
        taken_inp = input()

        if not taken_inp.isdigit():
            print("Possible values: '1', '2' or '3'")
            continue

        taken = int(taken_inp)

        if taken not in [1, 2, 3]:
            print("Possible values: '1', '2' or '3'")
            continue

        if taken > current_pencils:
            print("Too many pencils were taken")
            continue

        return taken


def get_bot_turn(current_pencils: int):
    """
    Функція визначає хід бота за допомогою імпортованого модуля random,
    відповідно до виграшної стратегії

    Parameters:
        current_pencils (int): поточна кількість олівців у грі

    Returns:
        int: кількість олівців, які бот бере відповідно до стратегії виграшу
    """
    if current_pencils % 4 == 1:
        if current_pencils == 1:
            return 1
        else:
            return random.randint(1, min(3, current_pencils))

    remainder = current_pencils % 4

    if remainder == 0:
        return 3
    elif remainder == 3:
        return 2
    elif remainder == 2:
        return 1
    else:
        return random.randint(1, min(3, current_pencils))



def print_pencils(pencils: int):
    """
    Виводить поточну кількість олівців у вигляді вертикальних рис, тобто відображає їх на столі

    Parameters:
        pencils (int): кількість олівців для відображення
    """
    print("|" * pencils)


def play_game(pencils: int, first_player: str, player1: str, bot: str):
    """
    Основна логіка гри, де виконується запуск всього коду та всі по черзі беруть олівці

    Parameters:
        pencils (int): початкова кількість олівців
        first_player (str): ім'я гравця, який ходить першим
        player1 (str): ім'я гравця/людини
        bot (str): ім'я бота
    """
    current_player = first_player
    current_pencils = pencils

    print_pencils(current_pencils)

    while True:
        print(f"{current_player}'s turn:")

        if current_player == player1:
            taken = get_human_turn(current_pencils)
        else:
            taken = get_bot_turn(current_pencils)
            print(taken)

        current_pencils -= taken

        if current_pencils == 0:
            winner = bot if current_player == player1 else player1
            print(f"{winner} won!")
            break

        print_pencils(current_pencils)

        current_player = bot if current_player == player1 else player1


def main():
    """
    Основна функція для цього етапу, запускає повну версію всієї практичної роботи
    """
    player1 = "John"
    bot = "Jack"

    pencils = get_pencil_count()
    first_player = get_first_player(player1, bot)

    play_game(pencils, first_player, player1, bot)

#Головна функція для запуску програми
if __name__ == "__main__":
    main()
