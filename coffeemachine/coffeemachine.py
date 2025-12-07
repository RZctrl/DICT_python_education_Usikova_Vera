class CoffeeMachine:
    """
    Клас, що представляє кавоварку цієї практичної роботи

    Parameters:
        water (int): кількість води (мл)
        milk (int): кількість молока (мл)
        coffee_beans (int): кількість кавових зерен гр)
        cups (int): кількість одноразових стаканчиків (шт)
        money (int): кількість грошей (грн)
        state (str): стан кавомашини
    """

    RECIPES = {
        '1': {'name': 'espresso', 'water': 250, 'milk': 0, 'coffee': 16, 'price': 4},
        '2': {'name': 'latte', 'water': 350, 'milk': 75, 'coffee': 20, 'price': 7},
        '3': {'name': 'cappuccino', 'water': 200, 'milk': 100, 'coffee': 12, 'price': 6}
    }

    def __init__(self):
        """
        Запускає машину з визначеними початковими значеннями
        """
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.cups = 9
        self.money = 550
        self.state = "choos_action"

    def print_state(self):
        """
        Ця функція виводить початкові значення на екран користувача
        """
        print("\nThe coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.coffee_beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"{self.money} of money\n")

    def can_make(self, coffee_type):
        """
        Перевіряє чи достатньо розхідників для обраного користувачем типу кави

        Parameters:
            coffee_type (str): тип кави ('1', '2', '3')

        Returns:
            tuple: (bool, str): значення так/ні після перевірки кількості ресурсів, достатньо/недостатньо
        """
        recipe = self.RECIPES[coffee_type]

        if self.water < recipe['water']:
            return False, "water"
        if self.milk < recipe['milk']:
            return False, "milk"
        if self.coffee_beans < recipe['coffee']:
            return False, "coffee beans"
        if self.cups < 1:
            return False, "disposable cups"

        return True, ""

    def make_coffee(self, coffee_type):
        """
        Функція вже після перевірки та підтвердження кількості ресурсів, готує каву та оновлює
        кількість ресурсів, мінусуючи використані ресурси

        Parameters:
            coffee_type (str): тип кави (1, 2, 3)
        """
        recipe = self.RECIPES[coffee_type]

        self.water -= recipe['water']
        self.milk -= recipe['milk']
        self.coffee_beans -= recipe['coffee']
        self.cups -= 1
        self.money += recipe['price']

    def process_inp(self, inp):
        """
        Обробляє введення користувача відповідно до станом кавомашини

        Parameters:
            inp (str): введення користувача

        Returns:
            bool: True/False - продовжити/завершити роботу
        """
        if self.state == "choos_action":
            return self._handle_action(inp)
        elif self.state == "choos_coffee":
            return self._handle_coffee_choice(inp)
        elif self.state == "fill_water":
            return self._handle_fill_water(inp)
        elif self.state == "fill_milk":
            return self._handle_fill_milk(inp)
        elif self.state == "fill_coffee":
            return self._handle_fill_coffee(inp)
        elif self.state == "fill_cups":
            return self._handle_fill_cups(inp)

        return True

    def _handle_action(self, inp):
        """
        Обробляє вибір основної дії

        Parameters:
            inp (str): обрана дія

        Returns:
            bool: True - продовжити роботу
        """
        if inp == "buy":
            self.state = "choos_coffee"
            print("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back -- to main menu:")
        elif inp == "fill":
            self.state = "fill_water"
            print("\nWrite how many ml of water do you want to add:")
        elif inp == "take":
            self._take_money()
            self.state = "choos_action"
            print("\nWrite action (buy, fill, take, remaining, exit):")
        elif inp == "remaining":
            self.print_state()
            print("Write action (buy, fill, take, remaining, exit):")
        elif inp == "exit":
            return False
        else:
            print("Invalid action")
            print("Write action (buy, fill, take, remaining, exit):")

        return True

    def _handle_coffee_choice(self, inp):
        """
        Обробляє вибір типу кави (1, 2, 3)

        Parameters:
            inp (str): обраний тип кави

        Returns:
            bool: True - продовжити роботу
        """
        if inp == "back":
            self.state = "choos_action"
            print("\nWrite action (buy, fill, take, remaining, exit):")
            return True

        if inp not in self.RECIPES:
            print("Invalid choice! Please try again.")
            print("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back -- to main menu:")
            return True

        can_make, missing = self.can_make(inp)

        if can_make:
            self.make_coffee(inp)
            print("I have enough resources, making you a coffee!")
        else:
            print(f"Sorry, not enough {missing}!")

        self.state = "choos_action"
        print("\nWrite action (buy, fill, take, remaining, exit):")
        return True

    def _handle_fill_water(self, inp):
        """
        Функція оброблює введення кількості води для поповнення

        Parameters:
            inp (str): кількість води

        Returns:
            bool: True - продовжити роботу
        """
        try:
            self.water += int(inp)
            self.state = "fill_milk"
            print("Write how many ml of milk do you want to add:")
        except ValueError:
            print("Please enter a valid number")
            print("Write how many ml of water do you want to add:")

        return True

    def _handle_fill_milk(self, inp):
        """
        Оброблює введення кількості молока

        Parameters:
            inp (str): кількість молока

        Returns:
            bool: True - продовжити роботу
        """
        try:
            self.milk += int(inp)
            self.state = "fill_coffee"
            print("Write how many grams of coffee beans do you want to add:")
        except ValueError:
            print("Please enter a valid number")
            print("Write how many ml of milk do you want to add:")

        return True

    def _handle_fill_coffee(self, inp):
        """
        Оброблює введення кількості кавових зерен

        Parameters:
            inp (str): кількість кавових зерен

        Returns:
            bool: True - продовжити роботу
        """
        try:
            self.coffee_beans += int(inp)
            self.state = "fill_cups"
            print("Write how many disposable cups of coffee do you want to add:")
        except ValueError:
            print("Please enter a valid number")
            print("Write how many grams of coffee beans do you want to add:")

        return True

    def _handle_fill_cups(self, inp):
        """
        Оброблює введення кількості стаканчиків

        Parameters:
            inp (str): кількість стаканчиків

        Returns:
            bool: True - продовжити роботу
        """
        try:
            self.cups += int(inp)
            print("Resources added successfully!")
            self.state = "choos_action"
            print("\nWrite action (buy, fill, take, remaining, exit):")
        except ValueError:
            print("Please enter a valid number")
            print("Write how many disposable cups of coffee do you want to add:")

        return True

    def _take_money(self):
        """
        Видає гроші з кавомашини
        """
        print(f"\nI gave you {self.money}")
        self.money = 0





def main():
    """
    Основна функція для цього етапу, запускає повну версію всієї практичної роботи
    Буде працювати у циклі, поки користувач не обере опцію "exit"
    """
    machine = CoffeeMachine()

    print("Write action (buy, fill, take, remaining, exit):")

    while True:
        inp = input("> ").strip().lower()

        if not machine.process_inp(inp):
            break


#Головна функція для запуску програми
if __name__ == "__main__":
    main()