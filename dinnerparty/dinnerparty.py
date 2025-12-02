import random

def get_valid_count():
    """
    Description: Отримує та перевіряє кількість людей на вечірці
    значення має бути строго більше 0
    повернеться 0 якщо введення некоректне

    Returns:
        int: кількість людей, включаючи користувача
    """
    try:
        count = int(input("Enter the number of friends joining (including you):\n> "))
        return count if count > 0 else 0
    except ValueError:
        return 0




def get_name_dict(count):
    """
    Description: Збирає імена людей, які приєдналися до вечірки
    створює з ними словник, де імена - ключі, а значення - баланс = 0

    Parameters:
        count (int): кількість людей, що приєднались до вечірки

    Returns:
        dict: словник з іменами як ключами та 0 як значеннями
    """
    print("Enter the name of every friend (including you), each on a new line:")
    friends_dict = {}
    for _ in range(count):
        name = input("> ")
        friends_dict[name] = 0
    return friends_dict


def get_total_amount():
    """
    Description: Отримує загальну суму рахунку від користувача

    Returns:
        float: загальна сума рахунку, що може бути з комою(дробна частина)
    """
    try:
        amount = float(input("Enter the total amount:\n> "))
        return amount if amount > 0 else 0
    except ValueError:
        return 0


def calculate_share(total_amount, friends_count, lucky_friend=None):
    """
    Description: Розраховує частку, яку повинна сплатити кожен

    Parameters:
        total_amount (float): загальна сума рахунку
        friends_count (int): кількість людей
        lucky_friend (str, опціонально): ім'я щасливчика, який не платить (тільки якщо було обрано "yes")


    Returns:
        float: частка кожного, округлена до 2 знаків після коми
        при наявності щасливчика його частка = 0
    """
    if lucky_friend:
        share = total_amount / (friends_count - 1)
    else:
        share = total_amount / friends_count

    return round(share, 2)


def update_dict(friends_dict, share, lucky_friend=None):
    """
    Description: Оновлює значення в словнику друзів

    Parameters:
        friends_dict (dict): словник людей(їх ім'я) та їхні баланси
        share (float): сума, яку кожен має сплатити
        lucky_friend (str, опціонально): ім'я щасливчика (за його наявності)

    Returns:
        dict: оновлений словник друзів
    """
    for friend in friends_dict:
        if friend == lucky_friend:
            friends_dict[friend] = 0
        else:
            friends_dict[friend] = share
    return friends_dict




def choose_lucky(friends_dict):
    """
    Description: Запитує користувача, чи хоче він використати функцію вибору щасливчика

    Parameters:
        friends_dict (dict): словник друзів

    Returns:
        bool: True, якщо користувач обирає "yes", False якщо "no".
    """
    response = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')

    use_lucky = response.strip().lower() == 'yes'

    if use_lucky:
        lucky_friend = random.choice(list(friends_dict.keys()))
        print(f"{lucky_friend} is the lucky one!")
        return True, lucky_friend
    else:
        return False, None







def run_party():
    """Основна функція для запуску програми

    Ця функція обробляє всі функції програми, викликаючи їх та обробляючи весь процес роботи
    (з'єднала тут всі стейджи в цій програмі, як і деякі функції до цього злила разом)
    """

    friends_count = get_valid_count()

    if friends_count == 0:
        print("No one is joining for the party")
        return

    friends_dict = get_name_dict(friends_count)
    print(friends_dict)

    total_amount = get_total_amount()




    if total_amount <= 0:
        print("Invalid total amount")
        return

    share_per_person = calculate_share(total_amount, len(friends_dict))
    friends_dict = update_dict(friends_dict, share_per_person)
    print(friends_dict)




    use_lucky, lucky_friend = choose_lucky(friends_dict)

    if use_lucky:
        updated_share = calculate_share(total_amount, len(friends_dict), lucky_friend)
        friends_dict = update_dict(friends_dict, updated_share, lucky_friend)

    else:
        print("No one is going to be lucky")

    print(friends_dict)


#Запуск виконання коду
if __name__ == "__main__":
    run_party()
