import hashlib
import json
from time import time
import ecdsa
from ecdsa import NIST256p
from hashlib import sha256
from urllib.parse import urlparse
import requests

class Blockchain:
    """
    {
        // Block
        "index": index of a block in the chain
        "previous_hash": hash of previous block
        "timestamp": when the block was mined
        "nonce": proof-of-work mining result
        "transactions": a list of transactions in the block (see Transaction below)
        "difficulty": Difficulty on mining this block (hash rate * time)
    }

    { //Transaction
     "id": SHA256 hashed values of 'sender', 'recipient' and 'amount'
     "type": transfer, fee or reward?
     "sender": address (public key) of the sender, reward-type and fee-type has no sender
     "signature": signature derived from private key
     "unspent": amount of leftover from last unspent transaction (TxOut)
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
        self.nodes = set()  # an empty set (no duplicate) of nodes
        self.mempool = []  # mempool contains a list of transactions not added to the chain yet
                           # miner can mine the mempool to add them to the valid block
        self.reward = 5  # reward for mining an empty block
        self.fee = 5  # fee for conducting transaction (transfer from sender to recipient/receiver)

    def register_node(self, address):  # add new address to the set of nodes
        #  address argument is a string formatted as "http://xxx.xxx.xxx.xxx:<port>"
        parsed_url = urlparse(address)   # parse the string as a url scheme
        self.nodes.add(parsed_url.netloc)  # add the netloc of the url to the set

    def new_transfer(self, id, sender, recipient, amount, signature):  # create new transfer-type transaction
        print(self.chain)  # debug statement
        unspent = self.current_balance(sender=sender)  # call current_balance function to get the amount of the latest unspent Erocoin
        timenow = time()  # current timestamp
        leftover = unspent - amount - self.fee  # leftover Erocoin after deducting amount to be sent and fee
        transaction = {
            "id": id,
            "type": "transfer",
            "timestamp": timenow,
            "sender": sender,
            "signature": signature,
            "unspent": unspent,
            "recipient": recipient,
            "amount": amount,
            "leftover": leftover
        }
        if self.validate_transaction(transaction):  # validate the transaction
            self.mempool.append(transaction)  # add transaction to the mempool
            return transaction
        else:
            return 403

    def current_balance(self, sender):  # get the latest balance in this Blockchain
        unspent = 0
        for block in self.chain:
            transactions = block['transactions']
            for transaction in transactions:
                print(type(transaction))  # debug statement
                if transaction['sender'] == sender:  # if the sender in transaction is same as the sender
                    # balance is always equal to the last leftover if the last transaction involving the sender is a
                    # transaction in which the sender is the actual sender
                    unspent = transaction['leftover']
                elif transaction['recipient'] == sender:  # if the receiver in transaction is same as the sender
                    # balance is ADDED to the last leftover if the last transaction involving the sender is a
                    # transaction in which the sender is the receiver
                    unspent += transaction['amount']
                else:
                    pass  # if this is a new transaction by the sender, pass and return 0 as the balance
        return unspent  # return current balance

    @staticmethod
    def get_transact_id(sender, amount, recipient):  # get transaction id by hashing arguments
        dk = hashlib.sha256()  # new empty sha256 hash
        bamount = str(amount).encode()  # transform amount to string then encode it
        dk.update(bamount)  # hash the encoded amount, add it to the empty hash
        dk.update(sender.encode())  # hash the encoded sender, add it to the empty hash
        dk.update(recipient.encode())  # hash the encoded recipient, add it to the empty hash
        return dk.hexdigest()  # return the hash as a string as transaction id

    def new_reward(self, id, miner, signature):  # create a new reward-type transaction (when miner mine an empty block)
        # empty block has no sender but mining reward is given to the miner
        transaction = {
            "id": id,
            "type": "reward",
            "timestamp": time(),
            "sender": "None",  # reward has no sender
            "signature": signature,
            "unspent": self.reward,
            "recipient": miner,  # rewarded to the miner
            "amount": self.reward,
            "leftover": 0
        }
        if self.validate_transaction(transaction):  # validate the transaction
            print(type(transaction))  # debug statement
            return transaction
        else:
            return False

    def new_fee(self, id, miner, signature):  # create a new fee-type transaction (when miner mine their mempool)
        # a fee is always instantiated everytime a mempool is mined and thus added to the chain
        transaction = {
            "id": id,
            "type": "fee",
            "timestamp": time(),
            "sender": "None",  # fee has no sender
            "signature": signature,
            "unspent": self.fee,
            "recipient": miner,  # rewarded to the miner
            "amount": self.fee,
            "leftover": 0
        }
        return transaction

    def validate_transaction(self, transaction):  # validate the transaction to check if any of the record has been tampered
        times = transaction['timestamp']
        sender = transaction['sender']
        unspent = transaction['unspent']
        recipient = transaction['recipient']
        amount = transaction['amount']
        leftover = transaction['leftover']
        # check if id is valid
        if self.get_transact_id(sender, amount, recipient) != transaction['id']:  # hash arguments to check if it matches
            print("line 126")
            return False  # id is not valid
        else:
            pass  # id is valid
        # check if signature is verified
        message = transaction['id'].encode()  # encode the transaction id
        public_key = sender
        sig = transaction['signature']
        if sender == "None":
            pass  # if this is a reward or fee-type automatically pass the check
        else:
            # real key is verified with ECDSA
            verify_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST256p)
            if not verify_key.verify(bytes.fromhex(sig), message):
                print("line 139")  # debug statement
                return False  # real key does not match signature
            else:
                pass  # real key match
        # check if unspent (current balance) is enough
        if sender == "None":
            pass  # if this is a reward or fee-type automatically pass the check
        else:
            if unspent - amount < self.fee:
                print("line 149")  # debug statement
                return False  # sender does not have enough balance
            else:
                pass  # sender has enough balance
        # check if leftover is true
        if sender == "None":
            return True  # if this is a reward or fee-type automatically pass the check
        else:
            print(unspent, amount, leftover)
            if unspent - amount != leftover+self.fee:
                print("line 156")
                return False  # stated leftover is not valid
            else:
                return True  # stated leftover is valid and all previous checks are passed

    def new_block(self, nonce, transaction, previous_hash):
        # creates new block and append them
        transactions = []
        transactions.extend(transaction)  # combine the empty list with with list of new transaction
        block = {
            "index": self.last_block['index']+1,
            "previous_hash": previous_hash,
            "timestamp": time(),
            "nonce": nonce,
            "transactions": transactions,
            "difficulty": self.difficulty
        }
        self.chain.append(block)
        return block

    @staticmethod
    def hash_block(block):  # return the hash of the entire block
        block_string = json.dumps(block, sort_keys=True).encode()
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
            ],
            "difficulty": 1
        }
        self.chain.append(genesis)  # append the pre-determined genesis block to the chain

    @property
    def last_block(self):
        # return the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_nonce):
        # hash of nonce*last nonce in string
        # if hash string starts with 0 * difficulty, return the nonce
        nonce = 0
        while self.nonce_matches_difficulty(last_nonce, nonce) is False:  # (see nonce_matches_difficulty below)
            nonce += 1
        return nonce  # returns this nonce as a nonce of the block

    def nonce_matches_difficulty(self, last_nonce, nonce):  # check if nonce already match difficulty or not
        guess = f'{last_nonce}{nonce}'.encode()  # encode nonce of previous block and current nonce in the iteration
        guess_hash = hashlib.sha256(guess).hexdigest()  # hash them
        return guess_hash[:self.difficulty] == "0"*self.difficulty  # check if the first x character of the hash is 0. x = difficulty level of the block

    def adjust_difficulty(self):  # adjust the difficulty every interval
        if (self.last_block['index'] % self.diff_adjust_interval == 0) and (self.last_block['index'] != 0):
            # difficulty is only adjusted for every x block created. x = difficulty adjustment interval
            pass
        else:
            prev_adjustment = self.chain[-1 - self.diff_adjust_interval]  # the block where difficulty was last adjusted
            avg_time_expected = self.diff_adjust_interval * self.block_generation_interval  # expected time to create all the blocks since last adjustment
            time_taken = self.last_block['timestamp'] - prev_adjustment['timestamp']  # time it takes to create all the blocks since last adjustment
            if avg_time_expected > time_taken:
                self.difficulty += 1  # if the time it takes is lower than the expected time, increase the difficulty
            elif avg_time_expected < time_taken:
                if self.difficulty == 1:
                    # if the difficulty is already at the lowest (difficulty 1), difficulty cannot be lowered anymore
                    pass
                else:
                    self.difficulty -= 1  # if the time it takes is higher than the expected time, lower the difficulty
            else:
                pass  # if the time it takes is equal to the expected time, difficulty stays the same

    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash_block(last_block):
                print(last_block)
                print(block['previous_hash'])
                print(self.hash_block(last_block))
                print('beet')
                return False

            # Check that the Proof of Work is correct
            if not self.nonce_matches_difficulty(last_block['nonce'], block['nonce']):
                print('yeet')
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):  # check if there's a blockchain with higher computational effort than ours in the recognized nodes
        neighbours = self.nodes
        new_chain = None

        # We're looking for chains with higher computational effort than ours
        # computational effort is represented by the cumulative difficulty of that blockchain
        max_diff = self.cumulative_difficulty()

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                chain = response.json()['chain']
                diff = response.json()['cumulative difficulty']

                # Check if the length has higher computational effort and the chain is valid
                if diff > max_diff and self.valid_chain(chain):
                    max_diff = diff
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain with higher computational effort (cumulative difficulty)
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def cumulative_difficulty(self):  # cumulative difficulty of this blockchain
        cum_diff = 0
        for block in self.chain:
            cum_diff += 2 ^ block['difficulty']
        return cum_diff
