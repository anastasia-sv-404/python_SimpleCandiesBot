total = 150
new_game = False


def get_total():
    global total
    return total


def take_candies(taken_candies: int):
    global total
    total -= taken_candies


def start_new_game():
    global new_game
    global total
    if new_game:
        new_game = False
    else:
        new_game = True
        total = 150


def game():
    global new_game
    return new_game
