def read_matrix():
    """
    Функція зчитує матрицю, яку ввів користувач, та переводить її в список
    Перший рядок - розмір, далі - сама матриця

    Parameters:
        input: матриця, що ввів користувач

    Returns:
        list: матрицю у вигляді двовимірного списку
    """
    rows, cols = map(int, input().split())
    matrix = []
    for _ in range(rows):
        row = list(map(float, input().split()))
        matrix.append(row)
    return matrix

def read_without_size(rows, cols):
    """
    Зчитує матрицю без розмірів (вже відомих)

    Parameters:
        rows (int): кількість рядків
        cols (int): кількість стовпців

    Returns:
        list: матрицю у вигляді двовимірного списку
    """
    matrix = []
    for _ in range(rows):
        row = list(map(float, input().split()))
        matrix.append(row)
    return matrix


def add_matrix(matrix_a, matrix_b):
    """
    Додає дві матриці, якщо вони однакового розміру

    Parameters:
        matrix_a (list): перша матриця
        matrix_b (list): пруга матриця

    Returns:
        list/None: сумарна матриця, якщо розміри співпадають або None, якщо не співпадають
    """
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        return None

    result = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_a[0])):
            row.append(matrix_a[i][j] + matrix_b[i][j])
        result.append(row)
    return result


def multiply_by_constant(matrix, constant):
    """
    Функція помножує матрицю, що ввів користувач, на константу

    Parameters:
        matrix (list): вхідна матриця, що ввів користувач
        constant (float): константа для множення (число, може бути з плаваючою крапкою)

    Returns:
        list: результат розрахунків
    """
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(matrix[i][j] * constant)
        result.append(row)
    return result


def multiply_matrix(matrix_a, matrix_b):
    """
    Помножує дві матриці, що ввів користувач, одна на одну

    Parameters:
        matrix_a (list): перша матриця
        matrix_b (list): друга матриця

    Returns:
        list/None: результат розрахунків або None, якщо матриці не можна перемножити
    """
    rows_a, cols_a = len(matrix_a), len(matrix_a[0])
    rows_b, cols_b = len(matrix_b), len(matrix_b[0])

    if cols_a != rows_b:
        return None

    result = []
    for i in range(rows_a):
        row = []
        for j in range(cols_b):
            sum = 0
            for k in range(cols_a):
                sum += matrix_a[i][k] * matrix_b[k][j]
            row.append(sum)
        result.append(row)

    return result


def transpose_main(matrix):
    """
    Транспонує матрицю за головною діагоналлю

    Parameters:
        matrix (list): вхідна матриця, що ввів користувач

    Returns:
        list: транспонована матриця
    """
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(matrix[i][j])
        result.append(row)
    return result


def transpose_side(matrix):
    """
    Транспонує матрицю за побічною діагоналлю

    Parameters:
        matrix (list): вхідна матриця

    Returns:
        list: транспонована матриця
    """
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    for j in range(cols - 1, -1, -1):
        row = []
        for i in range(rows - 1, -1, -1):
            row.append(matrix[i][j])
        result.append(row)
    return result


def transpose_vertical(matrix):
    """
    Транспонує матрицю за вертикаллю

    Parameters:
        matrix (list): вхідна матриця

    Returns:
        list: транспонована матриця
    """
    result = []
    for row in matrix:
        result.append(row[::-1])
    return result


def transpose_horizontal(matrix):
    """
    Транспонує матрицю за горизонталлю

    Parameters:
        matrix (list): вхідна матриця

    Returns:
        list: транспонована матриця
    """
    return matrix[::-1]


def determinant(matrix):
    """
    Обчислює визначник квадратної матриці

    Parameters:
        matrix (list): квадратна матриця, яку ввів користувач

    Returns:
        float: визначник матриці
    """
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for j in range(n):
        minor = []
        for i in range(1, n):
            row = []
            for k in range(n):
                if k != j:
                    row.append(matrix[i][k])
            minor.append(row)

        sign = 1 if j % 2 == 0 else -1
        det += sign * matrix[0][j] * determinant(minor)

    return det


def get_minor(matrix, i, j):
    """
    Обчислює мінор матриці без i рядка та j стовпця.

    Parameters:
        matrix (list): вхідна матриця
        i (int): індекс рядка для виключення
        j (int): індекс стовпця для виключення

    Returns:
        list: мінор матриці
    """
    return [row[:j] + row[j + 1:] for row_idx, row in enumerate(matrix) if row_idx != i]


def inverse_matrix(matrix):
    """
    Обчислює обернену матрицю

    Parameters:
        matrix (list): квадратна матриця, яку ввів користувач

    Returns:
        list/None: обернена матриця, якщо визначник не дорівнює нулю або None, якщо матриця не має оберненої
    """
    n = len(matrix)
    det = determinant(matrix)

    if det == 0:
        return None

    if n == 1:
        return [[1 / matrix[0][0]]]

    if n == 2:
        a, b = matrix[0][0], matrix[0][1]
        c, d = matrix[1][0], matrix[1][1]
        return [[d / det, -b / det], [-c / det, a / det]]

    cofactors = []
    for i in range(n):
        cofactor_row = []
        for j in range(n):
            minor = get_minor(matrix, i, j)
            sign = 1 if (i + j) % 2 == 0 else -1
            cofactor_row.append(sign * determinant(minor))
        cofactors.append(cofactor_row)

    adj = transpose_main(cofactors)

    inverse = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(adj[i][j] / det)
        inverse.append(row)

    return inverse


def format_number(num):
    """
    Функція форматує числа для виводу
    Ціле число без точки, дробове — з двома знаками після коми

    Parameters:
        num (float): число для форматування

    Returns:
        str: форматований рядок
    """
    if abs(num) < 1e-10:
        return "0"

    if abs(num - int(num)) < 1e-10:
        return str(int(num))

    return f"{num:.2f}".rstrip('0').rstrip('.')


def print_matrix(matrix):
    """
    Виводить матрицю без розмірів

    Parameters:
        matrix (list): матриця для виводу
    """
    for row in matrix:
        format_row = [format_number(x) for x in row]
        print(' '.join(format_row))


def menu():
    """
    Головне меню програми для вибору операцій з всіх етапів практичної роботи
    """
    while True:
        print("1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")

        choice = input("Your choice: > ")

        if choice == "1":
            print("Enter size of first matrix: > ", end="")
            rows_a, cols_a = map(int, input().split())
            print("Enter first matrix:")
            matrix_a = read_without_size(rows_a, cols_a)

            print("Enter size of second matrix: > ", end="")
            rows_b, cols_b = map(int, input().split())
            print("Enter second matrix:")
            matrix_b = read_without_size(rows_b, cols_b)

            result = add_matrix(matrix_a, matrix_b)

            print("The result is:")
            if result is None:
                print("The operation cannot be performed.")
            else:
                print_matrix(result)

        elif choice == "2":
            print("Enter size of matrix: > ", end="")
            rows, cols = map(int, input().split())
            print("Enter matrix:")
            matrix = read_without_size(rows, cols)

            constant = float(input("Enter constant: > "))

            result = multiply_by_constant(matrix, constant)

            print("The result is:")
            print_matrix(result)

        elif choice == "3":
            print("Enter size of first matrix: > ", end="")
            rows_a, cols_a = map(int, input().split())
            print("Enter first matrix:")
            matrix_a = read_without_size(rows_a, cols_a)

            print("Enter size of second matrix: > ", end="")
            rows_b, cols_b = map(int, input().split())
            print("Enter second matrix:")
            matrix_b = read_without_size(rows_b, cols_b)

            result = multiply_matrix(matrix_a, matrix_b)

            print("The result is:")
            if result is None:
                print("The operation cannot be performed.")
            else:
                print_matrix(result)

        elif choice == "4":
            print("1. Main diagonal")
            print("2. Side diagonal")
            print("3. Vertical line")
            print("4. Horizontal line")

            transpose_choice = input("Your choice: > ")

            print("Enter matrix size: > ", end="")
            rows, cols = map(int, input().split())
            print("Enter matrix:")
            matrix = read_without_size(rows, cols)

            if transpose_choice == "1":
                result = transpose_main(matrix)
            elif transpose_choice == "2":
                result = transpose_side(matrix)
            elif transpose_choice == "3":
                result = transpose_vertical(matrix)
            elif transpose_choice == "4":
                result = transpose_horizontal(matrix)
            else:
                print("Invalid choice.")
                print()
                continue

            print("The result is:")
            print_matrix(result)

        elif choice == "5":
            print("Enter matrix size: > ", end="")
            rows, cols = map(int, input().split())

            if rows != cols:
                print("Determinant can only be calculated for square matrix")
                print()
                continue

            print("Enter matrix:")
            matrix = read_without_size(rows, cols)

            result = determinant(matrix)

            print("The result is:")
            print(format_number(result))

        elif choice == "6":
            print("Enter matrix size: > ", end="")
            rows, cols = map(int, input().split())

            if rows != cols:
                print("Error: Inverse matrix can only be calculated for square matrices.")
                print()
                continue

            print("Enter matrix:")
            matrix = read_without_size(rows, cols)
            result = inverse_matrix(matrix)

            print("The result is:")
            if result is None:
                print("This matrix doesn't have an inverse.")
            else:
                print_matrix(result)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")

        print()

#Головна функція для запуску програми
if __name__ == "__main__":
    menu()
