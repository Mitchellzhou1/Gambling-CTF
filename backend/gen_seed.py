import time

from random import Random
from hashlib import sha256
from pymongo import MongoClient

# Connect to MongoDB
CLIENT = MongoClient('mongodb://localhost:27017/')
DB = CLIENT['roulette']
SEEDS_COLLECTION = DB['seeds']


# Drop the seeds collection on startup to clean the older entries on docker 10 min restart. This is needed as the older
# seeds are useless once the new PERSISTENT object is created.
SEEDS_COLLECTION.drop()

PERSISTENT = Random()

def generate_seed():

    while True:
                 #### import random
        txt = ""  ##################
        for i in range(2048 // 32):
            # Generate a random 32-bit number
            random_number = PERSISTENT.getrandbits(32)
            # convert to hash and append
            txt += hex(random_number)[2:]

        hashed_seed = sha256(txt.encode()).hexdigest()
        rand_no_from_hash = Random(int(txt, 16)).randrange(38) ######################

        # Create a new seed document
        new_seed_details = {
            'hashed_seed': hashed_seed,
            'number': rand_no_from_hash
        }
        print(rand_no_from_hash)

        # Insert the new seed into the collection
        SEEDS_COLLECTION.insert_one(new_seed_details)

        # Check and clean database if there are >1000 seeds else it piles up which is not required
        all_seeds = SEEDS_COLLECTION.count_documents({})

        if all_seeds > 1000:
            oldest_entries = SEEDS_COLLECTION.find().sort("_id", 1).limit(100)
            for entry in oldest_entries:
                SEEDS_COLLECTION.delete_one({"_id": entry["_id"]})

        # Sleep for 15sec as a new number is generated every 15 seconds
        time.sleep(8)
