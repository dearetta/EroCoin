from blockchain import Blockchain
from wallet import Wallet
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from ecdsa import SigningKey, NIST256p

app = Flask(__name__)

blockchain = Blockchain()  # a new instance of 'blockchain' object from Blockchain class
blockchain.initiate_genesis_block()  # generate a genesis block on startup
wallet = Wallet()  # a new instance of 'wallet' object from Wallet class


@app.route('/wallet/create', methods=['GET'])
def wallet_create():  # create a new wallet for this node (see wallet.py for details)
    private, public = wallet.generate_pairs()  # (see wallet.py for details)
    response = {
        "private": private,
        "public": public
    }
    return jsonify(response), 200  # return private key and public key as json to display, success code 200


@app.route('/mine/empty', methods=['GET'])
def mine_empty_block():  # mine an empty block that rewards the miner with Erocoin
    last_block = blockchain.last_block
    last_nonce = last_block['nonce']  # last nonce to solve for
    miner = wallet.public_decode  # public address from the wallet of the miner
    id = get_transact_id("None", blockchain.reward, miner)  # (see get_transact_id in blockchain.py for more detail)
    private_key = SigningKey.from_string(wallet.private, curve=NIST256p)  # private key from the wallet of the miner
    signed_id = private_key.sign(id.encode()).hex()  # use private key and transaction id to create signature
    valid_transact = blockchain.new_reward(id, miner, signed_id)  # (see blockchain.py for more detail)
    if not valid_transact:
        return 'Your values are invalid/has been tampered!', 403  # if transaction is not valid return 403 error
    nonce = blockchain.proof_of_work(last_nonce)  # solve for nonce using last nonce (see proof_of_work in blockchain.py for more detail)
    print(last_block)  # debug statement
    previous_hash = blockchain.hash_block(last_block)  # hashes the entire last block (see hash_block in blockchain.py for more detail)
    print(previous_hash)  # debug statement
    transactions = [valid_transact]  # add the new transaction to the list of transactions in the block
    response = blockchain.new_block(nonce, transactions, previous_hash)  # (see blockchain.py for more detail)
    return jsonify(response), 201  # display the response as json, success code 201


@app.route('/mine/mempool', methods=['GET'])
def mine_mempool_block():
    # mine the existing mempool (uncofirmed transactions) in this node to add them in the blockchain
    length = len(blockchain.mempool)
    transactions = []
    # maximum size of a block is two transfer-type transactions (and with fees attached to each transaction the
    # maximum transactions in a block is 4)
    if length < 2 and length != 0:
        # if the length is 1, only mine the only transaction in the mempool
        transactions.append(blockchain.mempool[0])
    elif length >= 2:
        # if the length is bigger than 2 (max), only mine the first two transactions
        transactions.append(blockchain.mempool[0])
        transactions.append(blockchain.mempool[1])
    else:
        # if mempool is empty, return error
        return "No available transactions in the Mempool to mine!", 404

    # Proof-of-work
    last_block = blockchain.last_block
    last_nonce = last_block['nonce']
    nonce = blockchain.proof_of_work(last_nonce)  # solve for nonce using last nonce (see proof_of_work in blockchain.py for more detail)

    # Create a new fee payment for the miner
    miner = wallet.public_decode
    private_key = SigningKey.from_string(wallet.private, curve=NIST256p)
    fees = []
    for i in range(0, len(transactions)):  # for every transaction added from the mempool, reward the miner
        id = get_transact_id("None", blockchain.fee, miner)  # transaction id
        signed_id = private_key.sign(id.encode()).hex()  # signature of miner
        valid_transact = blockchain.new_fee(id, miner, signed_id)
        if not valid_transact:
            return 'Your values are invalid/has been tampered!', 403  # if fee is not valid, error code 403
        else:
            fees.append(valid_transact)  # add the fee-type transaction to the list of fees
        blockchain.mempool.pop(i)  # remove this transaction from the mempool as it has already been confirmed

    # Create a new block of existing transactions
    transactions.extend(fees)  # combine the transfer-type transactions with fee-type transactions into the same transaction list of the same block
    previous_hash = blockchain.hash_block(last_block)
    response = blockchain.new_block(nonce, transactions, previous_hash)  # add the new block to the chain
    return jsonify(response, 201)  # display block as json, success code 201


@app.route('/wallet/balance', methods=['GET'])
def wallet_get_balance():
    # Get a virtual balance from your past TxOuts (see current_balance in blockchain.py)
    pass


@app.route('/wallet/transfer', methods=['POST'])
def create_transfer():
    # Sample POST Request
    # {
    #     "recipient": "2ef97fbb2df87d662ce5b2ef13ecfe5023986063ecdb512692a128ca31f147e247735a639b15a9192ea4c429301b3a3aa097e13b34f3324b5e837ae79edad8b3",
    #     "amount": 3
    # }
    values = request.get_json()  # get the json as a dictionary
    required = ['recipient', 'amount']  # these key-value pairs are required in the json
    if not all(k in values for k in required):
        return 'Missing values', 400  # if those values are not found, error code 400
    sender = wallet.public_decode  # get the sender's public key from the wallet as the sender address (sender is this node)
    id = get_transact_id(sender, values['amount'], values['recipient'])  # create transaction id
    private_key = SigningKey.from_string(wallet.private, curve=NIST256p)  # get the private key of the sender
    signed_id = private_key.sign(id.encode()).hex()  # create signature from the sender's private key
    response = blockchain.new_transfer(id, sender, values['recipient'], values['amount'], signed_id)  # new transfer-type type transaction is added to the mempool
    if response == 403:
        return 'Your values are invalid/has been tampered!', 403  # transaction is not valid!
    else:
        return jsonify(response), 201  # transaction is valid, display new transaction as json, success code 201


def get_transact_id(sender, amount, recipient):  # get transaction id by hashing arguments
    dk = hashlib.sha256()  # new empty sha256 hash
    bamount = str(amount).encode()  # transform amount to string then encode it
    dk.update(bamount)  # hash the encoded amount, add it to the empty hash
    dk.update(sender.encode())  # hash the encoded sender, add it to the empty hash
    dk.update(recipient.encode())  # hash the encoded recipient, add it to the empty hash
    return dk.hexdigest()  # return the hash as a string as transaction id


@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'cumulative difficulty': blockchain.cumulative_difficulty()
    }
    return jsonify(response), 200  # display the current blockchain of this node as a json, success code 200


@app.route('/mempool', methods=['GET'])
def get_mempool():
    response = {
        'mempool': blockchain.mempool,
        'length': len(blockchain.mempool)
    }
    return jsonify(response), 200  # display the current mempool of this node as a json, success code 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():  # register a new node within the blockchain
    # Sample POST Request
    # {
    #     "nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
    # }
    values = request.get_json()

    nodes = values.get('nodes')  # get the list
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400  # if list is empty, return 400 error

    for node in nodes:
        blockchain.register_node(node)  # register all the nodes in the list

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201  # return the response as a json, code 201 success


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()  # see resolve_conflicts in blockchain.py for detail

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
