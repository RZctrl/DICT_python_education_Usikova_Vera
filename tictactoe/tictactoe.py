def print_grid(cells: str):
    """
    Функція виводить ігрове поле 3x3 з гранями

    Parameters:
        cells (str): строка з 9 символів, всього три варіанти - 'X', 'O' або '_'.
                    символи заповнюють поле згідно до рядків зверху вниз, зліва направо

    Returns:
        None: функція виводить результат на екран
    """
    print("---------")
    print(f"| {cells[0]} {cells[1]} {cells[2]} |")
    print(f"| {cells[3]} {cells[4]} {cells[5]} |")
    print(f"| {cells[6]} {cells[7]} {cells[8]} |")
    print("---------")


def get_coordinates():
    """
    Отримує координати від користувача та перевіряє їхню коректність
    Одразу перетворює отримані коректні координати на індекси рядка, 0-8 (як і можливих координат на полі)

    Returns:
        int: індекс у рядку, 0-8 (всього 9 значень)
    """
    while True:
        coords = input("Enter the coordinates: ").strip()

        if not coords:
            print("Input cannot be empty")
            continue

        parts = coords.split()

        if len(parts) != 2:
            print("Coordinates must be separated by spaces")
            continue

        try:
            row = int(parts[0])
            col = int(parts[1])
        except ValueError:
            print("You should enter numbers!")
            continue

        if not (1 <= row <= 3 and 1 <= col <= 3):
            print("Coordinates should be from 1 to 3")
            continue

        return (row - 1) * 3 + (col - 1)

def make_move(cells: str, index: int, symbol: str):
    """
    Функція виконує хід на ігровому полі

    Parameters:
        cells (str): поточний стан ігрового поля
        index (int): індекс місця на полі, 0-8
        symbol (str): символ для встановлення ('X' за замовчуванням)

    Returns:
        str: новий стан ігрового поля після ходу
    """
    if index < 0 or index >= 9:
        print("Invalid index")
        return cells

    if cells[index] != '_':
        print("This cell is occupied! Choose another one!")
        return cells

    new_cells = cells[:index] + symbol + cells[index + 1:]
    return new_cells


def analyze_game_state(cells: str):
    """
    Аналізує стан гри та повертає результат

    Parameters:
        cells (str): рядок з 9 символів, що представляє собою ігрове поле

    Returns:
        str: результат аналізу:
        X/О wins - якщо X/О виграв відповідно
        Draw - якщо нічия
        Game not finished - якщо гра не завершена
        Impossible - якщо перемога неможлива
    """

    count_x = cells.count('X')
    count_o = cells.count('O')

    diff = abs(count_x - count_o)

    if diff > 1:
        return "Impossible"

    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    x_wins = False
    o_wins = False

    for line in win_lines:
        a, b, c = line
        if cells[a] == cells[b] == cells[c] != '_':
            if cells[a] == 'X':
                x_wins = True
            elif cells[a] == 'O':
                o_wins = True

    if x_wins and o_wins:
        return "Impossible"

    if x_wins:
        return "X wins"
    elif o_wins:
        return "O wins"
    elif '_' in cells:
        return "Game not finished"
    else:
        return "Draw"


def get_current_player(cells: str):
    """
    Визначає, чий зараз час ходити за полі

    Parameters:
        cells (str): поточний стан ігрового поля

    Returns:
        str: 'X' якщо хід X, 'О' якщо хід O
    """
    count_x = cells.count('X')
    count_o = cells.count('O')

    if count_x <= count_o:
        return 'X'
    else:
        return 'O'

def main():
    """
    Основна функція для цього етапу, запускає повну версію всієї практичної роботи для двох гравців
    Запитує у гравця строку та виводить ігрове поле
    Запитує координати на полі для того, щоб виконати хід, та оновлює поле
    """
    cells = "_________"

    while True:
        print_grid(cells)

        player = get_current_player(cells)
        print(f"Player's turn {player}")

        while True:
            index = get_coordinates()
            if index is None:
                continue

            new_cells = make_move(cells, index, player)

            if new_cells != cells:
                cells = new_cells
                break

        game_state = analyze_game_state(cells)

        if game_state in ["X wins", "O wins", "Draw"]:
            print_grid(cells)
            print(game_state)
            break

        if game_state == "Impossible":
            print("Impossible game state!")
            break

#Головна функція для запуску програми
if __name__ == "__main__":
    main()
