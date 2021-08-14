from brownie import *
from itertools import count
from click import style
from eth_utils import decode_hex
from time import sleep
import json

from git import Repo

PATH_OF_GIT_REPO = r'/root/hacker-chat/.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'update data'

start_block = 12997793
hacker = '0xC8a65Fadf0e0dDAf421F28FEAb69Bf6E2E589963'

network.connect('mainnet')

messages = []

def get_message(tx):
    try:
        return decode_hex(tx.input).decode('utf-8')
    except UnicodeDecodeError:
        return style('(unintelligible)', dim=True)


def git_push():
            try:
                repo = Repo(PATH_OF_GIT_REPO)
                repo.index.add("data.json")
                repo.index.commit(COMMIT_MESSAGE)
                origin = repo.remote(name='origin')
                origin.push()
            except:
                print('Some error occured while pushing the code')

for n in count(start_block):
    while n > web3.eth.block_number:
        sleep(1)

    if n % 100 == 0 and n < web3.eth.block_number:
        print(style(f'{web3.eth.block_number - n:,d} blocks remaining', dim=True))
    try:
        block = web3.eth.get_block(n, True)
    except Exception:
        pass
    # print(block)
    
    for tx in block.transactions:
        if hacker not in [tx['from'], tx.to]:
            continue
        message = get_message(tx)
        
        if message == '' or message is None: 
            print('no message')
            continue
        else:
            msg = { "hash": tx["hash"].hex(), "timestamp": block['timestamp'], "address": tx['from'], "message": message, "blockHash": tx['blockHash'].hex(), "blockNumber": tx['blockNumber'] }
            # print(tx)
            messages.append(msg)
            
            
            json_string = json.dumps(messages)
            f = open("data.json", "w")
            f.write(json_string)
            f.close()

