from blockchain import Blockchain
from wallet import Wallet
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from ecdsa import SigningKey, NIST256p

app = Flask(__name__)

blockchain = Blockchain()
blockchain.initiate_genesis_block()
wallet = Wallet()


@app.route('/wallet/create', methods=['GET'])
def wallet_create():
    private, public = wallet.generate_pairs()
    response = {
        "private": private,
        "public": public
    }
    return jsonify(response), 200


@app.route('/mine/empty', methods=['GET'])
def mine_empty_block():
    last_block = blockchain.last_block
    last_nonce = last_block['nonce']
    miner = wallet.public_hex
    id = get_transact_id("None", blockchain.reward, miner)
    private_key = SigningKey.from_string(wallet.private, curve=NIST256p)
    signed_id = private_key.sign(id.encode()).hex()
    valid_transact = blockchain.new_reward(id, miner, signed_id)
    if not valid_transact:
        return 'Your values are invalid/has been tampered!', 403
    else:
        pass
    nonce = blockchain.proof_of_work(last_nonce)
    previous_hash = blockchain.hash_block(last_block)
    transactions = [valid_transact]
    response = blockchain.new_block(nonce, transactions, previous_hash)
    return jsonify(response), 201


@app.route('/mine/mempool', methods=['GET'])
def mine_mempool_block():
    length = len(blockchain.mempool)
    transactions = []
    if length < 2 and length != 0:
        transactions.append(blockchain.mempool[0])
    elif length >= 2:
        transactions.append(blockchain.mempool[0])
        transactions.append(blockchain.mempool[1])
    else:
        return "No available transactions in the Mempool to mine!", 404

    # Proof-of-work
    last_block = blockchain.last_block
    last_nonce = last_block['nonce']
    nonce = blockchain.proof_of_work(last_nonce)

    # Create a new fee payment for the miner
    miner = wallet.public_hex
    private_key = SigningKey.from_string(wallet.private, curve=NIST256p)
    fees = []
    for i in range(0, len(transactions)):
        id = get_transact_id("None", blockchain.fee, miner)
        signed_id = private_key.sign(id.encode()).hex()
        valid_transact = blockchain.new_fee(id, miner, signed_id)
        if not valid_transact:
            return 'Your values are invalid/has been tampered!', 403
        else:
            fees.append(valid_transact)
        blockchain.mempool.pop(i)

    # Create a new block of existing transactions
    transactions.extend(fees)
    previous_hash = blockchain.hash_block(last_block)
    response = blockchain.new_block(nonce, transactions, previous_hash)
    return jsonify(response, 201)


@app.route('/wallet/balance', methods=['GET'])
def wallet_get_balance():
    # Get a virtual balance from your past TxOuts
    pass


@app.route('/wallet/transfer', methods=['POST'])
def create_transfer():
    values = request.get_json()
    required = ['recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    sender = wallet.public_hex
    id = get_transact_id(sender, values['amount'], values['recipient'])
    private_key = SigningKey.from_string(wallet.private, curve=NIST256p)
    signed_id = private_key.sign(id.encode()).hex()
    response = blockchain.new_transfer(id, sender, values['recipient'], values['amount'], signed_id)
    if response == 403:
        return 'Your values are invalid/has been tampered!', 403
    else:
        return jsonify(response), 201


def get_transact_id(sender, amount, recipient):
    dk = hashlib.sha256()
    bamount = str(amount).encode()
    dk.update(bamount)
    dk.update(sender.encode())
    dk.update(recipient.encode())
    return dk.hexdigest()


@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mempool', methods=['GET'])
def get_mempool():
    response = {
        'mempool': blockchain.mempool,
        'length': len(blockchain.mempool)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
