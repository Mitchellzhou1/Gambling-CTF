import multiprocessing

from app import *
from gen_seed import *


def main():
    try:
        # initiating roulette process
        print("Initiating roulette backend processes!")

        print("Initiating flask process!")
        flask_process = multiprocessing.Process(name="flask_process", target=run_flask)

        # initiating gen seed process

        print("Initiating the gen seed process!")
        gen_seed_process = multiprocessing.Process(name="gen_seed_process", target=generate_seed)

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

    except:
        print("ERROR: Failed to initiate roulette backend processes!")


if __name__ == "__main__":
    main()
