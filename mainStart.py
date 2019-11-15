from concurrent.futures import ThreadPoolExecutor
import threading
from Roebot.RoebotMachine2 import roebot



def main():


    threadpool = ThreadPoolExecutor(max_workers=3)

    roebotmachine = roebot(threadpool)
    roebotmachine.switch_case(0)





if __name__ == '__main__':
    main()