# Multi-Blockchain Wallet in Python

## Rich Ripley
### 11/11/2020

![crypto wallet](https://camo.githubusercontent.com/6b238516fa8f3dfb4d3af8ef9828ffc1b614b242f22a4b2adc39ab6c97dcafa8/68747470733a2f2f7777772e656c657638636f6e2e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031392f30322f446f2d492d6e6565642d612d63727970746f63757272656e63792d77616c6c65742e6a7067)

---

# Objective: send BTCTEST/ETH transactions using Python

## Dependencies:

 - PHP must be installed on your operating system (any version, 5 or 7). Don't worry, you will not need to know any PHP.

 - You will need to clone the hd-wallet-derive tool.

 - bit Python Bitcoin library.

 - web3.py Python Ethereum library.
 
## Project set-up:

 - Create a project directory called wallet and cd into it.

 - Clone the hd-wallet-derive tool into this folder and install it using the instructions on its README.md.

 - Create a symlink called derive for the hd-wallet-derive/hd-wallet-derive.php script into the top level project directory like so: ln -s hd-wallet-derive/hd-wallet-derive.php derive 

    - This will clean up the command needed to run the script in our code, as we can call ./derive instead of ./hd-wallet-derive/hd-wallet-derive.php.

 - Test that you can run the ./derive script properly.

 - Create a file called wallet.py -- this will be your universal wallet script (see wallet.py file for code).
 
## Setup constants

 - In a separate file, constants.py, set the following constants:

    BTC = 'btc'
    
    ETH = 'eth'
    
    BTCTEST = 'btc-test'

 - In wallet.py, import all constants: from constants import *

 - Use these anytime you reference these strings, both in function calls, and in setting object keys.

## Generate a Mnemonic

 - Generate a new 12 word mnemonic using hd-wallet-derive or by using this [tool](https://iancoleman.io/bip39/).

 - Set this mnemonic as an environment variable, and include the one you generated as a fallback using: mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here')

## Linking the transaction signing libraries

Now, we need to use bit and web3.py to leverage the keys we've got in the coins object. You will need to create three more functions:

 - priv_key_to_account -- this will convert the privkey string in a child key to an account object that bit or web3.py can use to transact. This function needs the following parameters:

    - coin -- the coin type (defined in constants.py).
    - priv_key -- the privkey string will be passed through here.
    - You will need to check the coin, then return one of the following functions based on the library:

- For ETH, return Account.privateKeyToAccount(priv_key)
    - This function returns an account object from the private key string. You can read more about this object [here](https://web3js.readthedocs.io/en/v1.2.0/web3-eth-accounts.html#privatekeytoaccount).
- For BTCTEST, return PrivateKeyTestnet(priv_key)
- This is a function from the bit libarary that converts the private key string into a WIF (Wallet Import Format) object. WIF is a special format bitcoin uses to designate the types of keys it generates.
    - You can read more about this function [here](https://ofek.dev/bit/dev/api.html).
- create_tx -- this will create the raw, unsigned transaction that contains all metadata needed to transact. This function needs the following parameters:
    - coin -- the coin type (defined in constants.py).
    - account -- the account object from priv_key_to_account.
    - to -- the recipient address.
    - amount -- the amount of the coin to send.
- For ETH, return an object containing to, from, value, gas, gasPrice, nonce, and chainID. Make sure to calculate all of these values properly using web3.py!
- For BTCTEST, return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
- send_tx -- this will call create_tx, sign the transaction, then send it to the designated network.-- This function needs the following parameters:

    - coin -- the coin type (defined in constants.py).
    - account -- the account object from priv_key_to_account.
    - to -- the recipient address.
    - amount -- the amount of the coin to send.
    
You will need to check the coin, then return one of the following functions based on the library:

- For ETH, return an object containing to, from, value, gas, gasPrice, nonce, and chainID. Make sure to calculate all of these values properly using web3.py!
- For BTCTEST, return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
- send_tx -- this will call create_tx, sign the transaction, then send it to the designated network. This function needs the following parameters:

    - coin -- the coin type (defined in constants.py).
    - account -- the account object from priv_key_to_account.
    - to -- the recipient address.
    - amount -- the amount of the coin to send.
    
    You may notice these are the exact same parameters as create_tx. send_tx will call create_tx, so it needs all of this information available.

    You will need to check the coin, then create a raw_tx object by calling create_tx. Then, you will need to sign the raw_tx using bit or web3.py (hint: the account objects have a sign transaction function within).

    Once you've signed the transaction, you will need to send it to the designated blockchain network.

    - For ETH, return w3.eth.sendRawTransaction(signed.rawTransaction)
    - For BTCTEST, return NetworkAPI.broadcast_tx_testnet(signed)

## Send some transactions!

Now, you should be able to fund these wallets using testnet faucets. Open up a new terminal window inside of wallet, then run python. Within the Python shell, run from wallet import * -- you can now access the functions interactively, and you should see something like this:![screenshot2](https://user-images.githubusercontent.com/65874272/98889437-2ebfab80-2457-11eb-8be3-35f9a767dc62.png)

You'll need to set the account with priv_key_to_account and use send_tx to send transactions.

### Bitcoin Testnet transaction

Fund a BTCTEST address using this [testnet faucet](https://testnet-faucet.mempool.co).

Use a [block explorer](https://tbtc.bitaps.com) to watch transactions on the address.

Send a transaction to another testnet address (either one of your own, or the faucet's).

Screenshot the confirmation of the transaction like so:
![Screenshot1](https://user-images.githubusercontent.com/65874272/98888870-084d4080-2456-11eb-8b54-6d4b028c85c3.png)

## Ganashe Ethereum transaction

Open up Ganashe and activate your ethereum accounts.

Set the private key and call the send_tx function just like with btc-test.

Pick a different address to be the recipient, and in the send_tx function, include how much ETH to send (should be 1 or more, I picked 5). Output should look like this in python terminal: ![screenshot3](https://user-images.githubusercontent.com/65874272/98889857-fa98ba80-2457-11eb-81a6-734f5586e690.png)

Check Ganashe "transactions" tab and verify transaction went through. Click on the transaction to verify, should look like this: ![screenshot4](https://user-images.githubusercontent.com/65874272/98889987-3cc1fc00-2458-11eb-901e-a0b83e04256d.png)

**Congratulations - you've just successfully sent crypto transactions via Python!**

