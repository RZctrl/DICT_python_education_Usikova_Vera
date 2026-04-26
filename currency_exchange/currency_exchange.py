import json
import urllib.request
import urllib.error
from typing import Dict, Optional

class NegativeAmountError(Exception):
    pass

class CurrencyNotFoundError(Exception):
    pass

class NetworkError(Exception):
    pass

class EmptyInputError(Exception):
    pass

def get_positive_float(prompt: str) -> float:
    """
    Запитує у користувача додатнє число з комою

    Parameters:
        prompt (str): текст

    Returns:
        float: введене додатнє число
    """
    user_input = input(prompt).strip()
    if not user_input:
        raise ValueError("No data entered")
    try:
        value = float(user_input)
    except ValueError:
        raise ValueError("It is necessary to enter a number")
    if value < 0:
        raise NegativeAmountError("The amount cannot be negative")
    return value

def get_currency_code(prompt: str, allow_empty: bool = False) -> str:
    """
    Запитує у користувача код валюти

    Parameters:
        prompt (str): текст
        allow_empty (bool): якщо True, порожній рядок не викликає помилку

    Returns:
        str: введений код валюти у верхньому регістрі
    """
    code = input(prompt).strip()
    if not code and not allow_empty:
        raise EmptyInputError("Currency code cannot be empty")
    return code.upper()

def fetch_rate(base_currency: str, target_currency: str) -> float:
    """
    Отримує обмінний курс з FloatRates API

    Parameters:
        base_currency (str): код базової валюти
        target_currency (str): код валюти, в яку потрібно перевести обмін

    Returns:
        float: курс валют на даний момент
    """
    if target_currency == base_currency:
        return 1.0

    url = f"http://www.floatrates.com/daily/{base_currency.lower()}.json"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise NetworkError(f"HTTP status: {response.status}")
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        raise NetworkError(f"Network error: {e.reason}")
    except json.JSONDecodeError as e:
        raise NetworkError(f"JSON decoding error: {e}")

    target_key = target_currency.lower()
    if target_key not in data:
        raise CurrencyNotFoundError(f"Rate for {target_currency} not found")
    return data[target_key]["rate"]

def initialize_cache(base_currency: str) -> Dict[str, float]:
    """
    Завантажує курси USD та EUR для базової валюти та повертає словник-кеш

    Parameters:
        base_currency (str): код базової валюти

    Returns:
        Dict[str, float]: словник з курсами
    """
    cache = {}
    for curr in ("USD", "EUR"):
        rate = fetch_rate(base_currency, curr)
        cache[curr] = rate
    return cache

def main() -> None:
    """
    Функція, що запускає повну версію практичної роботи
    Запитує базову валюту, кешує курси USD та EUR, у циклі запитує цільову валюту та суму, виконує конвертацію.
    При новій цільовій валюті робить запит до API та кешує курс. Завершується при порожньому введенні цільової валюти.
    """
    try:
        base_currency = get_currency_code("Enter your currency code: ")

        cache = initialize_cache(base_currency)

        while True:
            print()
            try:
                target_currency = get_currency_code("Enter the code of the currency you want to exchange "
                                                    "(Enter for exit): ", allow_empty=True)
                if not target_currency:
                    break

                amount = get_positive_float("Enter the amount: ")

                print("Checking the cache...")
                if target_currency in cache:
                    print("It is in the cache!")
                    rate = cache[target_currency]
                else:
                    print("Sorry, but it is not in the cache!")
                    rate = fetch_rate(base_currency, target_currency)
                    cache[target_currency] = rate

                result = amount * rate
                print(f"You received {result:.2f} {target_currency}.")

            except EmptyInputError:
                break
            except (ValueError, NegativeAmountError, EmptyInputError) as e:
                print(f"Data entry error: {e}.")
                continue
            except (NetworkError, CurrencyNotFoundError) as e:
                print(f"Error receiving exchange rate: {e}.")
                continue

    except (EmptyInputError, NetworkError, CurrencyNotFoundError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

#Головна функція для запуску програми
if __name__ == "__main__":
    main()