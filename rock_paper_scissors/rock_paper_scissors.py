import random
from typing import Dict, List, Set

class InvalidInputError(Exception):
    pass

def get_computer_choice(options: List[str]) -> str:
    """
    Випадково обирає варіант із заданих, який обирає комп'ютер

    Parameters:
        options (List[str]): список допустимих варіантів

    Returns:
        str: один обраний варіант
    """
    return random.choice(options)


def compute_beats(options: List[str]) -> Dict[str, Set[str]]:
    """
    Функція визначає які варіанти будуть побиті для окремого варіанту
    Наприклад, для папіру таким варіантом буде камінь

    Parameters:
        options (List[str]): список варіантів гри у порядку, заданому користувачем

    Returns:
        Dict[str, Set[str]]: відображення програшних варіантів для одного окремого варіанту
    """
    beats = {}
    n = len(options)
    for i, opt in enumerate(options):
        ordered = options[i + 1:] + options[:i]
        half = len(ordered) // 2
        beats[opt] = set(ordered[half:])
    return beats


def determine_winner(user_choice: str, computer_choice: str, beats: Dict[str, Set[str]]) -> str:
    """
    Функція визначає результат гри за допомогою минулих розрахунків варіантів

    Parameters:
        user_choice (str): вибір користувача
        computer_choice (str): вибір комп'ютера
        beats (Dict[str, Set[str]]): словник з інформацією про те, які варіанти перемагають інші

    Returns:
        str: результат гри - win, lose або draw
    """
    if user_choice == computer_choice:
        return "draw"
    if computer_choice in beats[user_choice]:
        return "win"
    return "lose"


def display_result(result: str, computer_choice: str) -> None:
    """
    Функція виводить повідомлення про результат гри

    Parameters:
        result (str): результат - win, lose або draw
        computer_choice (str): вибір комп'ютера
    """
    if result == "win":
        print(f"Well done. The computer chose {computer_choice} and failed")
    elif result == "lose":
        print(f"Sorry, but the computer chose {computer_choice}")
    elif result == "draw":
        print(f"There is a draw ({computer_choice})")
    else:
        print("Unexpected result.")


def get_name() -> str:
    """
    Просить користувача ввести ім'я

    Returns:
        str: введене ім'я без пробілів
    """
    name = input("Enter your name: ").strip()
    return name


def load_rating(name: str) -> int:
    """
    Завантажує початковий рейтинг з файлу rating.txt
    Якщо файлу не існує або в ньому не записано ім'я користувача, початковий рейтинг залишається 0

    Parameters:
        name (str): ім'я користувача

    Returns:
        int: початковий рейтинг
    """
    try:
        with open("rating.txt") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == name:
                    return int(parts[1])
    except FileNotFoundError:
        pass
    return 0


def update_rating(rating: int, result: str) -> int:
    """
    Оновлює рейтинг відповідно до результату

    Parameters:
        rating (int): рейтинг на час початку гри
        result (str): результат гри

    Returns:
        int: новий рейтинг
    """
    if result == "win":
        return rating + 100
    if result == "draw":
        return rating + 50
    return rating


def get_options() -> List[str]:
    """
    Запитує у користувача список параметрів гри через кому
    Якщо нічого не введено, запускається базова гра - камінь, ножиці, папір

    Returns:
        List[str]: список можливих варіантів для гри
    """
    user_input = input("> ").strip()
    if user_input == "":
        return ["rock", "paper", "scissors"]
    options = [opt.strip().lower() for opt in user_input.split(",")]
    return options


def main() -> None:
    """
    Функція, що запускає повну версію практичної роботи
    """
    name = get_name()
    print(f"Hello, {name}")

    rating = load_rating(name)

    print("Enter a list of options:")
    options = get_options()
    beats = compute_beats(options)
    print("Okay, let's start")

    while True:
        user_input = input("> ").strip().lower()

        if user_input == "!exit":
            print("Bye!")
            break
        if user_input == "!rating":
            print(f"Your rating: {rating}")
            continue

        if user_input not in options:
            print("Invalid input")
            continue

        computer_choice = get_computer_choice(options)
        result = determine_winner(user_input, computer_choice, beats)
        display_result(result, computer_choice)
        rating = update_rating(rating, result)

#Головна функція для запуску програми
if __name__ == "__main__":
    main()