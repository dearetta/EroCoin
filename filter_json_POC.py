import random
import string
import json
import hashlib

def new_transfer(sender):
    # create new transfer-type transaction

    chain = [
        {
            "index": 1,
            "previous_hash": "somestrings",
            "timestamp": 1584941533,
            "nonce": 19,
            "transactions": [
                {
                    "id": 1,
                    "timestamp": 1584941510,
                    "type": "reward",
                    "sender": "None",
                    "unspent": 69,
                    "recipient": "Astolfo",
                    "Amount": 69,
                    "Leftover": 0
                },
                {
                    "id": 2,
                    "timestamp": 1584941521,
                    "type": "reward",
                    "sender": "None",
                    "unspent": 69,
                    "recipient": "Jeanne",
                    "Amount": 69,
                    "Leftover": 0
                }
            ]
        },
        {
            "index": 2,
            "previous_hash": "somestrings",
            "timestamp": 1584941569,
            "nonce": 21,
            "transactions": [
                {
                    "id": 3,
                    "timestamp": 1584941552,
                    "type": "reward",
                    "sender": "None",
                    "unspent": 69,
                    "recipient": "Mordred",
                    "Amount": 69,
                    "Leftover": 0
                },
                {
                    "id": 4,
                    "timestamp": 1584941562,
                    "type": "transfer",
                    "sender": "Mordred",
                    "unspent": 69,
                    "recipient": "Astolfo",
                    "Amount": 30,
                    "Leftover": 38
                }
            ]
        },
        {
            "index": 3,
            "previous_hash": "somestrings",
            "timestamp": 1584941900,
            "nonce": 1,
            "transactions": [
                {
                    "id": 5,
                    "timestamp": 1584941600,
                    "type": "reward",
                    "sender": "None",
                    "unspent": 69,
                    "recipient": "Astolfo",
                    "Amount": 69,
                    "Leftover": 0
                },
                {
                    "id": 6,
                    "timestamp": 1584941605,
                    "type": "transfer",
                    "sender": "Astolfo",
                    "unspent": 129,
                    "recipient": "Jeanne",
                    "Amount": 10,
                    "Leftover": 118
                }
            ]
        },
        {
            "index": 4,
            "previous_hash": "somestrings",
            "timestamp": 1584941902,
            "nonce": 1,
            "transactions": [
                {
                    "id": 7,
                    "timestamp": 1584941652,
                    "type": "reward",
                    "sender": "None",
                    "unspent": 69,
                    "recipient": "Astolfo",
                    "Amount": 69,
                    "Leftover": 0
                },
                {
                    "id": 8,
                    "timestamp": 1584941689,
                    "type": "reward",
                    "sender": "None",
                    "unspent": 69,
                    "recipient": "Astolfo",
                    "Amount": 69,
                    "Leftover": 0
                }
            ]
        }
    ]

    new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
    unspent = 0
    recip_latest_time = 0
    send_latest_time = 0
    recip_dict = {}
    sender_dict = {}
    TxOuts = ""
    for block in chain:
        transactions = block['transactions']
        for transaction in transactions:
            if transaction['sender'] == sender:
                sender_dict = transaction
                unspent = transaction['Leftover']
            elif transaction['recipient'] == sender:
                recip_dict = transaction
                unspent += transaction['Amount']
            else:
                pass
    return unspent


print(new_transfer("Astolfo"))

arr = [1,2,3,4,5,6,7,8,9]
v = []
for i in arr:
    v.append('1')
print(v)


def hash_block(block):
    block_string = json.dumps(block).encode()
    print(block_string)
    return hashlib.sha256(block_string).hexdigest()

last_block = {'difficulty': 1, 'index': 0, 'nonce': 69, 'previous_hash': '8132eb35f965fe190a9e903b1c392909579a816d9bcf18dfda3e942ed39be2d7', 'timestamp': 1585056323.1808214, 'transactions': [{'amount':
0, 'id': 'Corvus_Rex', 'leftover': 0, 'recipient': 'None', 'sender': 'None', 'signature': 'Yeet', 'timestamp': 0, 'type': 'genesis', 'unspent': 1}]}
hash = hash_block(last_block)
print(hash)
