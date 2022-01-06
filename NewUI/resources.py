# people counting flags
import time
from random import random
import globals

def main():



    globals.temperature = random() * 100
    globals.humidity = random() * 55
    globals.moisture = random() * 60
    globals.enter_Counter = random() * 5
        # Enter_Counter = randint(0,5)
        # if Enter_Counter
        # Exit_Counter = randint(0,5)
    globals.exit_Counter = random() * 5
    print(globals.temperature, globals.humidity, globals.moisture, globals.enter_Counter, globals.exit_Counter)
    time.sleep(2)


if __name__ == '__main__':
    main()
