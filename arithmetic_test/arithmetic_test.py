import random

class InvalidInputError(Exception):
    """
    Свій створений виняток для даних невірного формату, введених користувачем
    Виникає, коли введені дані неможливо перетворити на ціле число
    """
    pass


def gen_question_level1() -> tuple[int, int, str, int]:
    """
    Функція створює випадкове арифметичне завдання для рівня складності 1

    Returns:
        tuple[int, int, str, int]: кортеж, що містить перше та друге число (int) у діапазоні 2-9,
            оператор (str) та правильну відповідь (int)
    """
    num1 = random.randint(2, 9)
    num2 = random.randint(2, 9)
    operator = random.choice(['+', '-', '*'])

    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    else:
        result = num1 * num2

    return num1, num2, operator, result


def gen_question_level2() -> tuple[int, int]:
    """
    Функція створює випадкове арифметичне завдання для рівня складності 2 (квадрат числа)

    Returns:
        tuple[int, int]: кортеж, що містить число (int) у діапазоні 11-29 та його квадрат (int)
    """
    num = random.randint(11, 29)
    return num, num ** 2


def get_user_answer() -> int:
    """
    Функція, що просить користувача ввести відповідь та повертає її у вигляді цілого числа

    Raises:
        InvalidInputError: якщо введені дані неможливо перетворити на ціле число

    Returns:
        int: відповідь користувача у вигляді цілого числа
    """
    user_input = input('> ').strip()
    try:
        return int(user_input)
    except ValueError:
        raise InvalidInputError('Input is not a valid integer.') from None


def check_answer(user_answer: int, correct_answer: int) -> bool:
    """
    Порівнює відповідь користувача з правильною

    Parameters:
        user_answer (int): відповідь, що ввів користувач
        correct_answer (int): правильна відповіль

    Returns:
        bool: True - якщо відповіді збігаються, False - якщо ні
    """
    return user_answer == correct_answer


def get_level() -> int:
    """
    Функція запитує складність рівня

    Returns:
        int: обраний рівень складності 1 або 2
    """
    while True:
        print("Which level do you want? Enter a number:")
        print("1 - simple operations with numbers 2-9")
        print("2 - integral squares of 11-29")
        try:
            level = get_user_answer()
            if level in (1, 2):
                return level
            else:
                print("Incorrect format.")
        except InvalidInputError:
            print("Incorrect format.")


def run_level(level: int) -> int:
    """
    Функція запускає тест з 5 питань після обрання складності

    Parameters:
        level (int): обраний рівень складності - 1 або 2

    Returns:
        int: кількість вірних відповідей, максимум 5
    """
    correct_count = 0
    total_questions = 5

    for _ in range(total_questions):
        if level == 1:
            num1, num2, op, correct = gen_question_level1()
            print(f"{num1} {op} {num2}")
        else:
            num, correct = gen_question_level2()
            print(num)

        while True:
            try:
                user_ans = get_user_answer()
                break
            except InvalidInputError:
                print("Incorrect format.")

        if check_answer(user_ans, correct):
            print("Right!")
            correct_count += 1
        else:
            print("Wrong!")

    return correct_count


def save_results(name: str, results: list[tuple[int, int]]) -> None:
    """
    Зберігає результат користувача в файлі results.txt
    Кожен результат записується окремим рядком

    Parameters:
        name (str): ім'я користувача
        results (list[tuple[int, int]]): список кортежів
    """
    level_desc = {
        1: "simple operations with numbers 2-9",
        2: "integral squares of 11-29"
    }
    with open("results.txt", "a", encoding="utf-8") as file:
        for score, level in results:
            file.write(f"{name}: {score}/5 in level {level} ({level_desc[level]}).\n")
    print('The results are saved in "results.txt".')


def get_yes_no(prompt: str) -> bool:
    """
    Запитує у користувача так або ні і повертає логічне значення
    Повторює запит, доки не отримано коректну відповідь

    Parameters:
        prompt (str): повідомлення для виведення

    Returns:
        bool: True якщо відповідь 'yes', False якщо 'no'
    """
    while True:
        answer = input(prompt + "\n> ").strip().lower()
        if answer == "yes":
            return True
        elif answer == "no":
            return False
        else:
            print("Incorrect format.")




def ask_save(results: list[tuple[int, int]], name: str | None = None) -> str | None:
    """
    Функція запитує користувача хоче він зберегти результат чи ні

    Parameters:
        results (list[tuple[int, int]]): список результатів
        name (str | None): ім'я користувача
    """
    if not results:
        return name

    if get_yes_no("Would you like to save your result to the file? Enter yes or no."):
        if name is None:
            name = input("What is your name?\n> ").strip()
        save_results(name, results)
        return name
    return name


def main() -> None:
    """
    Функція, що запускає повну версію практичної роботи
    """
    initial_level = get_level()
    results = []
    user_name = None

    if initial_level == 2:
        score = run_level(2)
        print(f"Your mark is {score}/5.")
        results.append((score, 2))
        user_name = ask_save(results, user_name)
    else:
        score1 = run_level(1)
        print(f"Your mark is {score1}/5.")
        results.append((score1, 1))



        # додаткова функція, яку пропонували зробити у файлі до практичної роботи
        # при проходженні першого рівня складності буде запитувати, чи хоче користувач спробувати другий
        if get_yes_no("Would you like to try level 2? Enter yes or no."):
            score2 = run_level(2)
            print(f"Your mark is {score2}/5.")
            results.append((score2, 2))

        user_name = ask_save(results, user_name)


#Головна функція для запуску програми
if __name__ == "__main__":
    main()
