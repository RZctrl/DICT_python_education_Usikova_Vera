import random #імпортування модулю для виконання роботи

def announce():
    """
    Модифікований перший етап практичної роботи.
    Базово виводив заголовок і прописане повідомлення "The game will be available soon."
    Зараз виводить тільки заголовок гри при запуску коду через функцію print().
    """
    print("HANGMAN")


def random_word():
    """
    Функція третього етапу практичної роботи.
    При викликанні повертає випадкове слово з заданого списку ['python', 'java', 'javascript', 'php'].
    Слово обирається випадково за допомогою функції random.
    """
    words = ['python', 'java', 'javascript', 'php']
    return random.choice(words)





def word_state(word, guess_letter):
    """
    Функція п'ятого етапу практичної роботи. Відображає поточний стан слова
    з вже вгаданими літерами.

    Функція отримує: word - задане з списку слово, що вказано в функції random_word(),
    guess_letter - множина всіх вже вгаданих літер;

    Повертає строку, що відображає вгадані та скриті літери, зберігаючи правильний порядок у слові.
    """
    display = ''
    for letter in word:
        if letter in guess_letter:
            display += letter
        else:
            display += '-'
    return display




def valid_input(guess, all_guess_letter):
    """
    Функція сьомого етапу.
    Перевіряє коректність введеної літери.

    Функція отримує: guess - введена гравцем строка з літерою,
    guess_letter - множина всіх вже вгаданих літер;

    Повертає валідність введених даних, перевірка їх на коректність
    """
    if len(guess) != 1:
        return False, "You should input a single letter"

    if not guess.isalpha() or not guess.islower():
        return False, "Please enter a lowercase English letter"

    if guess in all_guess_letter:
        return False, "You've already guessed this letter"

    return True, ""








def play_game():
    """
    Модифікований другий етап практичної роботи.
    Запускає варіант гри с заздалегідь прописаним списком рандомних слів та валідацією введених даних.
    Слово відображається у вигляді дефісів, ховаючи під ними літери, та просить гравця вгадати його.
    Гравець має фіксовану кількість спроб виграти - 8.
    Функція перевіряє чи введена 1 літера, чи строчна англійска вона, чи не вводилась ця літаре раніше.
    Такі помилки не зменшують кількість спроб.

    Повертає результат гри - програв/виграв, - за допомогою функції print().
    """
    word = random_word()
    guess_letter = set()
    all_guess_letter = set()
    attempts = 8


    announce()
    while attempts > 0:
        display_now = word_state(word, guess_letter)
        print(display_now)

        if '-' not in display_now:
            print("You guessed the word!")
            print("You survived!")
            return

        guess = input("Input a letter: > ")

        is_valid, error_message = valid_input(guess, all_guess_letter)
        if not is_valid:
            print(error_message)
            continue

        all_guess_letter.add(guess)

        if guess in word:
            guess_letter.add(guess)
        else:
            print("That letter doesn't appear in the word")
            attempts -= 1

    print("You lost!")



def menu():
    """
    Функція восьмого етапу.
    Відображає меню гри та обробляє вибір користувача.

    Отримує: choice - введені значення гравця з вибором почати гру/закінчити

    Повертає виклик необхідної опції циклу while True.
    """
    while True:
        choice = input('Type "play" to play the game, "exit" to quit: > ')
        if choice == "play":
            play_game()
            print()
        elif choice == "exit":
            break
        else:
            continue



def main():
    """Головна функція для запуску кожного з етапів гри.
    Викликає функцію з викликом меню для початку гри."""
    menu()


if __name__ == "__main__":
    main()