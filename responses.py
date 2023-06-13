from random import random


def random_string(strings):
    return strings[int(random() * strings.__len__())]


def greet():
    greetings = ["hi!", "hello!", "welcome!", "greetings!"]
    return random_string(greetings)


def ask_q_help():
    questions = ["how can I help you?", "what can I do for you?", "what do you need?"]
    return random_string(questions)


def sorry():
    apologies = ["I don't think i can do that...", "Sorry, I can't do that..", "I don't know how to do that...", "I'm sorry but I won't be able to do that", "I don't think I can help you"]
    return random_string(apologies)


def become_impatient():
    response = ["LOOK, WILL YOU PLEASE TELL ME TO DO SOMETHING I CAN??", "STOP ASKING ME TO DO THINGS I CAN'T!!", "LOOK, I CAN'T DO THAT, OK???", "WHY DO YOU ASK ME TO DO THINGS I CAN'T???"]
    return random_string(response)