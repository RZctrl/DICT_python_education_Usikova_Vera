import argparse
import math
import sys
from typing import Optional, List, Tuple, Union


class InvalidParametersError(Exception):
    """Виникає, коли аргументи командного рядка недійсні"""
    pass


class CalculationError(Exception):
    """Виникає, коли обчислення не вдається через недійсні вхідні значення"""
    pass


def parse_arguments() -> argparse.Namespace:
    """
    Функція розбирає та перевіряє аргументи командного рядка

    Returns:
        argparse.Namespace: розібрані аргументи з атрибутами type, principal, payment, periods, interest

    Raises:
        InvalidParametersError: якщо аргументи відсутні або недійсні
    """
    parser = argparse.ArgumentParser(description="Credit Calculator")
    parser.add_argument("--type", required=True, choices=["annuity", "diff"],
                        help="Type of payment: 'annuity' or 'diff'")
    parser.add_argument("--principal", type=float,
                        help="Loan principal (positive number)")
    parser.add_argument("--payment", type=float,
                        help="Monthly payment amount (positive number)")
    parser.add_argument("--periods", type=int,
                        help="Number of monthly payments (positive integer)")
    parser.add_argument("--interest", type=float, required=True,
                        help="Annual interest rate in percent (positive number)")

    args = parser.parse_args()

    if args.type == "diff" and args.payment is not None:
        raise InvalidParametersError("Incorrect parameters")

    numer_args = ["principal", "payment", "periods", "interest"]
    for arg_name in numer_args:
        value = getattr(args, arg_name)
        if value is not None and value <= 0:
            raise InvalidParametersError("Incorrect parameters")

    if args.type == "annuity":
        provide = sum(1 for a in ["principal", "payment", "periods"] if getattr(args, a) is not None)
        if provide != 2:
            raise InvalidParametersError("Incorrect parameters")

    if args.type == "diff":
        if args.principal is None or args.periods is None:
            raise InvalidParametersError("Incorrect parameters")

    return args


def calculate_annuity_payment(principal: float, annual_rate: float, periods: int) -> int:
    """
    Функція розраховує щомісячний платіж, округлений в більшу сторону

    Parameters:
        principal (float): основна сума кредиту
        annual_rate (float): процентна ставка у відсотках
        periods (int): кількість щомісячних платежів

    Returns:
        int: щомісячний платіж, округлений в більшу сторону

    Raises:
        CalculationError: якщо знаменник - нуль або від'ємне число
    """
    i = annual_rate / 100 / 12
    if i == 0:
        return math.ceil(principal / periods)

    power = math.pow(1 + i, periods)
    denom = power - 1
    if denom <= 0:
        raise CalculationError("Invalid parameters: denominator non-positive.")
    payment = principal * i * power / denom
    return math.ceil(payment)


def calculate_annuity_periods(principal: float, payment: float, annual_rate: float) -> int:
    """
    Обчислює кількість щомісячних платежів, округлених у більшу сторону

    Parameters:
        principal (float): основна сума кредиту
        payment (float): щомісячний платіж
        annual_rate (float): процентна ставка у відсотках

    Returns:
        int: кількість місяців, округлена в більшу сторону

    Raises:
        CalculationError: якщо платіж занадто малий, щоб покрити відсотки
    """
    i = annual_rate / 100 / 12
    if i == 0:
        return math.ceil(principal / payment)

    if payment <= i * principal:
        raise CalculationError("Monthly payment is too low to cover interest.")

    argument = payment / (payment - i * principal)
    try:
        months = math.log(argument, 1 + i)
    except ValueError:
        raise CalculationError("Logarithm calculation failed.")
    return math.ceil(months)


def calculate_annuity_principal(payment: float, annual_rate: float, periods: int) -> int:
    """
    Розраховує основну суму кредиту

    Parameters:
        payment (float): щомісячний платіж
        annual_rate (float): процентна ставка у відсотках
        periods (int): кількість щомісячних платежів

    Returns:
        int: основна сума кредиту, округлена до цілого числа

    Raises:
        CalculationError: якщо знаменник дорівнює нулю або від'ємний
    """
    i = annual_rate / 100 / 12
    if i == 0:
        return round(payment * periods)

    power = math.pow(1 + i, periods)
    denom = power - 1
    if denom <= 0:
        raise CalculationError("Invalid parameters: denominator non-positive.")
    annuity_factor = i * power / denom
    principal = payment / annuity_factor
    return round(principal)


def calculate_diff_payments(principal: float, annual_rate: float, periods: int) -> List[int]:
    """
    Розраховує всі щомісячні платежі

    Parameters:
        principal (float): основна сума кредиту
        annual_rate (float): процентна ставка у відсотках
        periods (int): кількість місяців

    Returns:
        List[int]: список щомісячних платежів, округлених до більшого числа
    """
    i = annual_rate / 100 / 12
    monthly_principal = principal / periods
    payments = []
    for m in range(1, periods + 1):
        remain = principal - monthly_principal * (m - 1)
        payment = monthly_principal + i * remain
        payments.append(math.ceil(payment))
    return payments


def format_periods(months: int) -> str:
    """
    Розраховує та виводить місяці у вигляді рядка з роками та місяцями

    Parameters:
        months (int): загальна кількість місяців

    Returns:
        str: рядок, у якому представлено введені місяці у вигляді років та решти місяців
    """
    years = months // 12
    remain_months = months % 12

    if years == 0:
        return f"{remain_months} month{'s' if remain_months != 1 else ''}"
    elif remain_months == 0:
        return f"{years} year{'s' if years != 1 else ''}"
    else:
        return (f"{years} year{'s' if years != 1 else ''} and {remain_months} month"
                f"{'s' if remain_months != 1 else ''}")


def compute_overpay(total_paid: Union[float, int], principal: float) -> int:
    """
    Обчислює переплату як загальну сплачену суму мінус основна сума

    Parameters:
        total_paid (Union[float, int]): загальна сплачена сума
        principal (float): основна сума кредиту

    Returns:
        int: переплата, округлена до цілого числа
    """
    return round(total_paid - principal)


def main() -> None:
    """
    Функція для запуску розбору аргументів, виконання обчислень та виведення результатів
    """
    try:
        args = parse_arguments()

        if args.type == "diff":
            principal = args.principal
            periods = args.periods
            interest = args.interest

            payments = calculate_diff_payments(principal, interest, periods)

            for idx, payment in enumerate(payments, start=1):
                print(f"Month {idx}: payment is {payment}")

            total_paid = sum(payments)
            overpayment = compute_overpay(total_paid, principal)
            print(f"\nOverpayment = {overpayment}")

        else:
            unknown = None
            if args.principal is None:
                unknown = "principal"
            elif args.payment is None:
                unknown = "payment"
            elif args.periods is None:
                unknown = "periods"

            if unknown == "principal":
                principal = calculate_annuity_principal(args.payment, args.interest, args.periods)
                total_paid = args.payment * args.periods
                overpayment = compute_overpay(total_paid, principal)
                print(f"Your loan principal = {principal}!")
                print(f"Overpayment = {overpayment}")

            elif unknown == "payment":
                payment = calculate_annuity_payment(args.principal, args.interest, args.periods)
                total_paid = payment * args.periods
                overpayment = compute_overpay(total_paid, args.principal)
                print(f"Your monthly payment = {payment}!")
                print(f"Overpayment = {overpayment}")

            elif unknown == "periods":
                months = calculate_annuity_periods(args.principal, args.payment, args.interest)
                total_paid = args.payment * months
                overpayment = compute_overpay(total_paid, args.principal)
                formatted = format_periods(months)
                print(f"It will take {formatted} to repay this loan!")
                print(f"Overpayment = {overpayment}")

    except (InvalidParametersError, CalculationError):
        print("Incorrect parameters")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


#Головна функція для запуску програми
if __name__ == "__main__":
    main()