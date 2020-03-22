import hashlib
import json
from time import time


class Blockchain:
    """
    {
        // Block
        "index": index of a block in the chain
        "previous_hash": hash of previous block
        "timestamp": when the block was mined
        "nonce": proof-of-work mining result
        "transaction": transactions (2) in the block
        "hash": Hash of this block
    }
    """

    def __init__(self):
        self.chain = []
        self.difficulty = 1
        self.diff_adjust_interval = 10
        self.block_generation_interval = 5

    def new_block(self, nonce, previous_hash, transaction):
        # creates a new Block and appends the created block
        pass

    def append_block(self, block):
        #  into the chain after proof-of-work
        pass

    @staticmethod
    def hash(*args):
        # hashes a block
        pass

    @property
    def genesis_block(self):
        # returns the genesis block
        return self.chain[0]

    @genesis_block.setter
    def genesis_block(self):
        # initiate a genesis block
        pass

    def blockbyaddress(self, address):
        # returns a list of blocks corresponding to an address
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

    def proof(self, last_nonce):
        nonce = 0
        while True:
            temp_hash = hashlib.sha256(f'{nonce*last_nonce}'.encode()).hexdigest()
            if temp_hash[:self.difficulty] == "0"*self.difficulty:
                return nonce
            else:
                nonce += 1

    def adjust_difficulty(self):
        if self.difficulty == 1:
            pass

        elif (self.last_block['index'] % self.diff_adjust_interval == 0) and (self.last_block['index'] != 0):
            pass

        else:
            prev_adjustment = self.chain[-1 - self.diff_adjust_interval]
            avg_time_expected = self.diff_adjust_interval * self.block_generation_interval
            time_taken = self.last_block['timestamp'] - prev_adjustment['timestamp']
            if avg_time_expected > time_taken:
                self.difficulty += 1
            elif avg_time_expected < time_taken:
                self.difficulty -= 1
            else:
                pass


class Transactions:
    """
    { //Transaction
     "id": random 64-bytes id
     "type": transfer or fee/reward?
     "sender": address of the sender, reward-type has no sender
     "unspent": amount of leftover from last unspent transaction
     "previous_hash": hash of the previous transaction with leftover corresponding to the sender's address
     "recipient": address of the recipient
     "amount": amount to be transferred
     "leftover": unspent - amount - fee
     }
    """

    def __init__(self):
        self.list = []
        self.reward = 69

    def new_transfer(self, sender, recipient, amount):
        # create new transfer-type transaction
        pass

    def new_reward(self, miner):
        # create new reward-type transaction
        pass
