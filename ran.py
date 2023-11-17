import random
import database


def generator_cod() -> str:
    while True:
        a = random.randint(1, 1000)
        l = database.tes.get_cod()
        if not (str(a) in l):
            return str(a)
            break
        else:
            continue
