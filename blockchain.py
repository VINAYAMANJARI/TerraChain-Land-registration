import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data='Genesis Block', previous_hash='0')

    def create_block(self, data, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': data,
            'previous_hash': previous_hash,
            'hash': self.hash_block(data, previous_hash)
        }
        self.chain.append(block)
        return block

    def hash_block(self, data, previous_hash):
        block_string = json.dumps({'data': data, 'previous_hash': previous_hash}, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data):
        previous_block = self.chain[-1]
        previous_hash = previous_block['hash']
        return self.create_block(data, previous_hash)

    def get_chain(self):
        return self.chain
