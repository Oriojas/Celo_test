from celo_sdk.kit import Kit

kit = Kit('https://alfajores-forno.celo-testnet.org')
_address = "0xBb42716eb3f010921b77e77f1A0c26e7f2D87e0C"
_abi = [
    {
        "inputs": [],
        "name": "ObtenerResultado",
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
        "inputs": [
            {
                "internalType": "uint256",
                "name": "numero1",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "numero2",
                "type": "uint256"
            }
        ],
        "name": "Suma",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    }
]
myContract = kit.w3.eth.contract(address=_address, abi=_abi)

print(myContract.functions.Suma(1, 5).call())
