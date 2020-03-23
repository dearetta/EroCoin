import hashlib
import json
from time import time
import ecdsa
from ecdsa import NIST256p
from hashlib import sha256

class Blockchain:
    """
    {
        // Block
        "index": index of a block in the chain
        "previous_hash": hash of previous block
        "timestamp": when the block was mined
        "nonce": proof-of-work mining result
        "transactions": transactions (2) in the block
    }

    { //Transaction
     "id": random 64-bytes id
     "type": transfer or fee/reward?
     "sender": address (public key) of the sender, reward-type has no sender
     "signature": signature derived from private key
     "unspent": amount of leftover from last unspent transaction
     "previous_hash": hash of the previous transaction with leftover corresponding to the sender's address
     "recipient": address of the recipient
     "amount": amount to be transferred
     "leftover": unspent - amount - fee
     }
    """

    def __init__(self):
        self.chain = []  # chains of block
        self.difficulty = 1  # difficulty of finding nonce
        self.diff_adjust_interval = 10  # difficulty adjusted per x block created
        self.block_generation_interval = 5  # expected minutes for one block creation
        self.mempool = []
        self.reward = 69
        self.fee = 1

    def new_transfer(self, id, sender, recipient, amount, signature):
        # create new transfer-type transaction
        print(self.chain)
        unspent = 0
        for block in self.chain:
            transactions = block['transactions']
            for transaction in transactions:
                print(type(transaction))
                if transaction['sender'] == sender:
                    unspent = transaction['leftover']
                elif transaction['recipient'] == sender:
                    unspent += transaction['amount']
                else:
                    pass

        times = time()
        leftover = unspent - amount - self.fee

        transaction = {
            "id": id,
            "type": "transfer",
            "timestamp": times,
            "sender": sender,
            "signature": signature,
            "unspent": unspent,
            "recipient": recipient,
            "amount": amount,
            "leftover": leftover
        }
        if self.validate_transaction(transaction):
            self.mempool.append(transaction)
            return transaction
        else:
            return 403

    @staticmethod
    def get_transact_id(sender, amount, recipient):
        dk = hashlib.sha256()
        bamount = str(amount).encode()
        dk.update(bamount)
        dk.update(sender.encode())
        dk.update(recipient.encode())
        return dk.hexdigest()

    def new_reward(self, id, miner, signature):
        transaction = {
            "id": id,
            "type": "reward",
            "timestamp": time(),
            "sender": "None",
            "signature": signature,
            "unspent": self.reward,
            "recipient": miner,
            "amount": self.reward,
            "leftover": 0
        }
        if self.validate_transaction(transaction):
            print(type(transaction))
            return transaction
        else:
            return False

    def new_fee(self, miner, signature):
        transaction = {
            "id": "miner",
            "type": "fee",
            "timestamp": time(),
            "sender": "None",
            "signature": signature,
            "unspent": self.fee,
            "recipient": miner,
            "amount": self.fee,
            "leftover": 0
        }
        return transaction

    def validate_transaction(self, transaction):
        times = transaction['timestamp']
        sender = transaction['sender']
        unspent = transaction['unspent']
        recipient = transaction['recipient']
        amount = transaction['amount']
        leftover = transaction['leftover']
        # check if id is valid
        if self.get_transact_id(sender, amount, recipient) != transaction['id']:
            print("line 126")
            return False
        else:
            pass
        # check if signature is verified
        message = transaction['id'].encode()
        public_key = sender
        sig = transaction['signature']
        if sender == "None":
            pass
        else:
            verify_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST256p)
            if not verify_key.verify(bytes.fromhex(sig), message):
                print("line 139")
                return False
            else:
                pass
        # check if unspent is enough
        if sender == "None":
            pass
        else:
            if unspent - amount < self.fee:
                print("line 149")
                return False
            else:
                pass
        # check if leftover is true
        if sender == "None":
            return True
        else:
            print(unspent, amount, leftover)
            if unspent - amount != leftover+self.fee:
                print("line 156")
                return False
            else:
                return True

    def new_block(self, nonce, transaction, previous_hash):
        # creates new block and append them
        transactions = []
        transactions.append(transaction)
        block = {
            "index": len(self.chain)+1,
            "previous_hash": previous_hash,
            "timestamp": time(),
            "nonce": nonce,
            "transactions": transactions
        }
        self.chain.append(block)
        return block

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def genesis_block(self):
        # returns the genesis block
        return self.chain[0]

    def initiate_genesis_block(self):
        genesis = {
            "index": 0,
            "previous_hash": "8132eb35f965fe190a9e903b1c392909579a816d9bcf18dfda3e942ed39be2d7",
            "timestamp": time(),
            "nonce": 69,
            "transactions": [
                {
                    "id": "Corvus_Rex",
                    "type": "genesis",
                    "timestamp": 0,
                    "sender": "None",
                    "signature": "Yeet",
                    "unspent": 1,
                    "recipient": "None",
                    "amount": 0,
                    "leftover": 0
                }
            ]
        }
        self.chain.append(genesis)

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_nonce):
        # hash of nonce*last nonce in string
        # if hash string starts with 0 * difficulty, return the nonce
        nonce = 0
        while self.nonce_matches_difficulty(last_nonce, nonce) is False:
            nonce += 1
        return nonce

    def nonce_matches_difficulty(self, last_nonce, nonce):
        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0"*self.difficulty

    @staticmethod
    def multi_hash(transactions, nonce):
        dk = hashlib.sha256()
        btransactions = str(transactions).encode()
        bnonce = str(nonce).encode()
        dk.update(btransactions)
        dk.update(bnonce)
        return dk.hexdigest()

    def adjust_difficulty(self):
        # adjust the difficulty every interval, pass if difficulty is already the lowest at 1
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
