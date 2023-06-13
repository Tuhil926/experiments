from myprojects.experiments.calc import calculator
from myprojects.experiments import responses
from myprojects.experiments import triangle
from myprojects.experiments import compound_interest
from time import sleep

print(responses.greet())
sleep(.75)
error_counter = 0

while True:
    sleep(.75)
    words = input(responses.ask_q_help() + "\n")
    if "calculator" in words.lower():
        sleep(.4)
        print("Here is the calculator:")
        sleep(.5)
        calculator()

    elif "compound interest" in words.lower():
        sleep(.4)
        print("here is the program to calculate compound interest:")
        sleep(.5)
        compound_interest.ci()

    elif "exit" in words.lower():
        sleep(.4)
        break

    elif "thank you" in words.lower():
        sleep(.4)
        print("You,re welcome")

    elif "hi" in words.lower():
        sleep(.4)
        print("hi")

    elif "bye" in words.lower():
        print("bye")
        sleep(.8)
        break

    elif "because" in words.lower():
        sleep(.4)
        print("ok.")
        error_counter = 0

    elif "ok" in words.lower():
        sleep(.4)
        print("GOOD!")
        error_counter = 0

    elif "no" in words.lower():
        sleep(.4)
        print("WELL, BYE THEN!")
        sleep(.4)
        break

    elif "triangle" in words.lower():
        sleep(.4)
        print("here is the triangle checker:")
        sleep(.5)
        triangle.tri_checker()

    else:
        error_counter += 1
        if error_counter > 3:
            sleep(.4)
            print(responses.become_impatient())
        else:
            sleep(.4)
            print(responses.sorry())

