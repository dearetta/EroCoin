import random
import string


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
