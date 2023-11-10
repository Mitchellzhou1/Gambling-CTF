from pymongo import MongoClient


class ProcessPool:
    def __init__(self, bet_pool_queue, bet_pool_lock, bet_pool_event, pool_name):
        # Connect to MongoDB
        self.CLIENT = MongoClient('mongodb://localhost:27017/')
        self.DB = self.CLIENT['roulette']
        self.SEEDS_COLLECTION = self.DB['seeds']

        # queues, events and locks

        self.bet_pool_queue = bet_pool_queue
        self.bet_pool_queue = bet_pool_lock
        self.bet_pool_event = bet_pool_event

        print("Successfully initiated process bets process!")

    def update_pool(self):
        pass
