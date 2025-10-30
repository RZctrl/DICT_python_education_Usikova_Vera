bot_name = "Botbot"
birth_year = 2025

print(f"Hello! My name's {bot_name}.")
print(f"I was created in {birth_year}.")
print("Hey, what's your name?")


ur_name = input("> ")
print(f"What a great name, {ur_name}!")

print("Lemme guess your age.")
print("Enter remainders of dividing your age by 3, 5 and 7.")



rem3 = int(input("> "))
rem5 = int(input("> "))
rem7 = int(input("> "))

age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105
print(f"Your age is {age}; that's a good time to take a nap!")




print("Now I'll prove that I can count to any number you want.")
num = int(input("> "))

for i in range(num + 1):
    print(f"{i} !")

print("Complete, I can do it just as I say!")




print("Ok, and the last thing! Let's test your programming knowledge just with one question")
print("Why do we use methods?")
print("1. To repeat a statement multiple times.")
print("2. To decompose a program into several small subroutines.")
print("3. To determine the execution time of a program.")
print("4. To interrupt the execution of a program.")

while True:
    answer = input("> ")
    if answer == "2":
        break
    print("Nope, not that answer.")

print("Congratulations! That's all, have a nice day!")