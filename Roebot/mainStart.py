from concurrent.futures import ThreadPoolExecutor
import threading
from Roebot import RoebotMachine



def main():


    threadpool = ThreadPoolExecutor(max_workers=3)

    roebot = RoebotMachine.roebot(threadpool)
    roebot.switch_case(0)





if __name__ == '__main__':
    main()