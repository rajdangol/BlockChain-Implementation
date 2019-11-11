import datetime
import hashlib
import json
from flask import Flask, jsonify

# Build the blockchain
class Blockchain:
    def __init__(self):
        self.chain = []

        # create a genensis block (the first block of the block chain)
        self.create_block(proof = 1, prevHash = '0')
    
    def create_block(self, proof, prevHash):
        # this function will execute right after a block is mined, so we need proof of work and previous hash
        block = {'index' : len(self.chain) + 1, 
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : prevHash }
        
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    

    #  proof of work - number or piece of data needed in order to mine a new block
    #  hard to find and easy to verify
    
    def get_proof_of_work(self, prevProof):
        newProof = 1
        isValidProof = False
        while isValidProof is False:
            # difference of sqauares is a simple assymetrical operation
            hashOperation = hashlib.sha256(str(newProof**2 - prevProof**2).encode()).hexdigest()
            # check for four leading zeroes
            if hashOperation[:4] == '0000':
                isValidProof = True
            else:
                newProof += 1
        return newProof

    def hash(self, block):
        enocodedBlock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(enocodedBlock).hexdigest()

    def is_chain_valid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if (block['previous_hash'] != self.hash(previousBlock)):
                return False
            previousProof = previousBlock['previous_hash']
            proof = block['previous_hash']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            previousBlock = block
            blockIndex += 1
        return True


# Mine Block

# Create a Flask web application
app = Flask(__name__)

# Create a blockchain
blockchain = Blockchain()

# Mining new Block
@app.route('/mine', methods=['GET'])
def mine_block():
    previousBlock = blockchain.get_previous_block()
    previousProof = previousBlock['proof']
    proof = blockchain.get_proof_of_work(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.create_block(proof, previousHash)
    response = {'message' : 'Congrats',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200

# Getting the full chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200

# Run the app
app.run(host = '0.0.0.0', port = 5000)