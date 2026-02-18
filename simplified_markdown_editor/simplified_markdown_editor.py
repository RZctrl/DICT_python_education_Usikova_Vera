def show_menu():
    """
    Відображає список доступних форматів та спец. команд help та done
    """

    formatters = (
        "plain bold italic header link inline-code ordered-list "
        "unordered-list new-line"
    )
    special = "!help !done"
    print(f"Available formatters: {formatters}")
    print(f"Special commands: {special}")


def is_valid_formatter(user_input: str):
    """
    Перевіряє введені дані на коректність форматувальником

    Args:
        user_input (str): рядок, що вводить користувач

    Returns:
        bool: True - якщо дані відповідають одному з форматувальників
        False - якщо ні
    """


    valid_formatters = {
        "plain", "bold", "italic", "header", "link",
        "inline-code", "ordered-list", "unordered-list", "new-line"
    }
    return user_input in valid_formatters


def format_plain(document: list):
    """Додає звичайний текст"""
    text = input("Text: ")
    document.append(text)
    return True


def format_bold(document: list):
    """Додає жирний текст"""
    text = input("Text: ")
    document.append(f"**{text}**")
    return True


def format_italic(document: list):
    """Додає курсив"""
    text = input("Text: ")
    document.append(f"*{text}*")
    return True


def format_inline_code(document: list):
    """Додає текст як код"""
    text = input("Text: ")
    document.append(f"`{text}`")
    return True


def format_header(document: list):
    """Додає заголовок (рівень 1-6)"""
    try:
        level_input = input("Level: ").strip()
        level = int(level_input)
        if level < 1 or level > 6:
            print("The level should be within the range of 1-6.")
            return False
    except ValueError:
        print("The level should be within the range of 1-6.")
        return False

    text = input("Text: ")
    document.append("#" * level + " " + text)
    return True


def format_link(document: list):
    """Додає посилання"""
    label = input("Label: ")
    url = input("URL: ")
    document.append(f"[{label}]({url})")
    return True


def format_new_line(document: list):
    """Додає порожній рядок"""
    document.append("")
    return True

def format_list(document: list, list_type: str):
    """
    Функція для створення списків

    Args:
        document (list): документ у вигляді списку
        list_type (str): тип списку

    Returns:
        bool: True - якщо список створено успішно, False - якщо виникла помилка
    """
    try:
        rows_input = input("Number of rows: ").strip()
        rows = int(rows_input)
        if rows <= 0:
            print("The number of rows should be greater than zero")
            return False
    except ValueError:
        print("The number of rows should be greater than zero")
        return False

    for i in range(1, rows + 1):
        row_text = input(f"Row #{i}: ")
        if list_type == "ordered":
            document.append(f"{i}. {row_text}")
        else:
            document.append(f"* {row_text}")
    return True




def apply_formatter(formatter: str, document: list):
    """
    Функція застосовує обраний користувачем форматтер та оновлює документ

    Args:
        formatter (str): тип форматування, що було застосовано до даних
        document (list): оновлений документ у вигляді списку

    Returns:
        bool: True - якщо все було застосовано вірно, False - якщо виникла помилка
    """

    formatter_map = {
        "plain": format_plain,
        "bold": format_bold,
        "italic": format_italic,
        "inline-code": format_inline_code,
        "header": format_header,
        "link": format_link,
        "new-line": format_new_line,
        "ordered-list": lambda doc: format_list(doc, "ordered"),
        "unordered-list": lambda doc: format_list(doc, "unordered"),
    }

    func = formatter_map.get(formatter)
    if func:
        return func(document)
    return False





def save_file(document: list):
    """
    Зберігає документ з всіма даними в output.md.

    Args:
        document (list): рядки для збереження до документа
    """

    try:
        with open("output.md", "w", encoding="utf-8") as f:
            f.write("\n".join(document))
    except OSError as e:
        print(f"Помилка при збереженні файлу: {e}")


def main():
    """
    Функція, що запускає повну версію практичної роботи
    """

    document = []
    while True:
        user_input = input("Choose a formatter: ").strip()

        if user_input == "!help":
            show_menu()
        elif user_input == "!done":
            save_file(document)
            break
        elif is_valid_formatter(user_input):
            success = apply_formatter(user_input, document)
            if success:
                print("\n".join(document))
        else:
            print("Unknown formatting type or command")

#Головна функція для запуску програми
if __name__ == "__main__":
    main()