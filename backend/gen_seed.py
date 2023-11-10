import time
import traceback

from random import Random
from hashlib import sha256
from pymongo import MongoClient


class GenerateSeed:
    def __init__(self, bet_pool_queue, bet_pool_lock, bet_pool_event, pool_number):
        # Connect to MongoDB
        self.CLIENT = MongoClient('mongodb://localhost:27017/')
        self.DB = self.CLIENT['roulette']
        self.SEEDS_COLLECTION = self.DB['seeds']

        # queues, events and locks

        self.bet_pool_queue = bet_pool_queue
        self.bet_pool_lock = bet_pool_lock
        self.bet_pool_event = bet_pool_event

        # Shared variable pool name to update the flask the other processes that the pool has changed
        self.POOL_NUMBER = pool_number

        # Drop the seeds collection on startup to clean the older entries on docker 10 min restart. This is needed as
        # the older seeds are useless once the new self.PERSISTENT object is created.
        self.SEEDS_COLLECTION.drop()

        self.PERSISTENT = Random()

    def generate_seed(self):

        while True:
            # Update the pool name after a new number is released
            try:
                print("Enqueuing message to PA queue!")

                # lock and enqueue

                print("Acquiring lock on pool shared var and enque the message!")

                self.bet_pool_lock.acquire()

                # self.pa_queue.put(json_msg, timeout=2)
                try:
                    self.POOL_NUMBER.value += 1

                except:
                    print("ERROR: Couldn't update the pool number")
                    traceback.print_exc()

                print("Process successful! Releasing lock!")
                self.bet_pool_lock.release()

                # Signaling PA process

                # print("Signalling PA process!")

                # self.bet_pool_event.set()
            except:
                print("Failed to update the processes with pool change!")
                traceback.print_exc()

            txt = ""
            for i in range(2048 // 32):
                # Generate a random 32-bit number
                random_number = self.PERSISTENT.getrandbits(32)
                # convert to hash and append
                txt += hex(random_number)[2:].zfill(8)

            hashed_seed = sha256(txt.encode()).hexdigest()
            rand_no_from_hash = Random(int(txt, 16)).randrange(38)

            # Create a new seed document
            new_seed_details = {
                'hashed_seed': hashed_seed,
                'number': rand_no_from_hash
            }

            print(new_seed_details)
            # Insert the new seed into the collection
            self.SEEDS_COLLECTION.insert_one(new_seed_details)

            # Check and clean database if there are >1000 seeds else it piles up which is not required
            all_seeds = self.SEEDS_COLLECTION.count_documents({})

            if all_seeds > 1000:
                oldest_entries = self.SEEDS_COLLECTION.find().sort("_id", 1).limit(100)
                for entry in oldest_entries:
                    self.SEEDS_COLLECTION.delete_one({"_id": entry["_id"]})

            # Sleep for 20 sec as a new number is generated every 15 seconds
            time.sleep(20)
