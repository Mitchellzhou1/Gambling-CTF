import multiprocessing
import traceback

from multiprocessing import Value

from app import *
from gen_seed import *
from process_bets import *


def main():
    try:
        # initiating roulette process
        print("Initiating roulette backend processes!")

        # multiprocessing queues
        bet_pool_queue = multiprocessing.Queue()

        # multiprocessing locks
        bet_pool_lock = multiprocessing.Lock()

        # multiprocessing events
        bet_pool_event = multiprocessing.Event()

        bet_pool_number = Value("i", 0)

        print("Initiating flask process!")
        flask_process = multiprocessing.Process(name="flask_process", target=run_flask, args=(bet_pool_number,))

        # initiating gen seed process

        print("Initiating the gen seed process!")
        gen_seed_process = multiprocessing.Process(name="gen_seed_process",
                                                   target=GenerateSeed(bet_pool_queue, bet_pool_lock, bet_pool_event,
                                                                       bet_pool_number).generate_seed)

        try:
            # Starting the processes
            flask_process.start()
            gen_seed_process.start()

            # Waiting for all the processes to be complete
            flask_process.join()
            gen_seed_process.join()

        except KeyboardInterrupt:
            flask_process.terminate()
            gen_seed_process.terminate()
            flask_process.join()
            gen_seed_process.join()
            traceback.print_exc()

    except:
        print("ERROR: Failed to initiate roulette backend processes!")
        traceback.print_exc()


if __name__ == "__main__":
    main()
