import subprocess
import json
import os
from constants import *
from pprint import pprint

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

from web3.gas_strategies.time_based import slow_gas_price_strategy
from web3 import Web3, middleware, Account
from web3.middleware import geth_poa_middleware


# connect to web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER', 'http://localhost:8545')))

# allow POA middleware
# https://web3py.readthedocs.io/en/stable/middleware.html#:~:text=Web3%20manages%20layers%20of%20middlewares,are%20available%20for%20optional%20use.

#geth-alltools-windows-amd64-1.9.23-8c2f2715
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#set the gas price from the api
w3.eth.setGasPriceStrategy(slow_gas_price_strategy)


# create the mnemonic
mnemonic = os.getenv("MNEMONIC", "rose because area chef save song year rich police festival east joy")
def wallet(coin=BTC, mnemonic=mnemonic, depth=3):


    command = f"./derive -g --mnemonic='{mnemonic}' --coin={coin} --numderive={depth} --format=json"

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    return keys

# function for private key
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether")
        # gas estimate from web3.py
        gas_estimate = w3.eth.estimateGas({"to": to, "from": account.address, "amount": value})

        return {
            "to": to,
            "from": account.address,
            "value": value,
            "gas": gas_estimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce" : w3.eth.getTransactionCount(account.address),

        }
    
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


def send_tx(coin, account, to, amount):
    if coin == ETH:
        send_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(send_tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)
        
    if coin == BTCTEST:
        send_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(send_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)

coins = {
    ETH: wallet(coin=ETH),
    BTCTEST: wallet(coin=BTCTEST),
}

pprint(coins)

        


