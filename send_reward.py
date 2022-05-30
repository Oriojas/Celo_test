import json
from celo_sdk.kit import Kit

with open("config.json", "r", encoding="utf-8") as file:
    SECRETS_FILE = json.load(file)
SECRET_KEY = SECRETS_FILE["SECRET_KEY"]

kit = Kit('https://alfajores-forno.celo-testnet.org')
_address = "0xB706B78F296Ed29305d0671b5cE49c886Af648a1"
_abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_limit",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_getReward",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "getHumidity",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getReward",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "limit",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "sender",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "state",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


class SendReward:

    def __init__(self):
        self.myContract = kit.w3.eth.contract(address=_address, abi=_abi)

    def send_hum_value(self, humidity):
        state = self.myContract.functions.getHumidity(humidity).call()

        return state

    def get_balance(self):
        send_address = self.myContract.functions.sender().call()
        wei_balance = kit.w3.eth.getBalance(send_address)
        balance = kit.w3.fromWei(wei_balance, 'ether')

        return balance

    def send_reward(self, reward, now_state, now_balance):
        send_address = self.myContract.functions.sender().call()
        get_address = self.myContract.functions.getReward().call()

        if now_state & reward < now_balance:
            nonce = kit.w3.eth.getTransactionCount(send_address)

            tx = {
                'nonce': nonce,
                'to': get_address,
                'value': kit.w3.toWei(reward, 'ether'),
                'gas': 2000000,
                'gasPrice': kit.w3.toWei('50', 'gwei'),
            }

            signed_tx = kit.w3.eth.account.signTransaction(tx, SECRET_KEY)
            tx_hash = kit.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            balance = kit.w3.eth.getBalance(send_address) - reward

        else:
            print(f"the reward ({reward}) is greater than the balance ({now_balance})")
            wei_balance = kit.w3.eth.getBalance(send_address)
            balance = kit.w3.fromWei(wei_balance, 'ether')
            tx_hash = None

        return balance, tx_hash
