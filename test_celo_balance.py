from celo_sdk.kit import Kit

kit = Kit('https://alfajores-forno.celo-testnet.org')

balance = kit.w3.eth.getBalance("0x5027323B073841Dfb6481F2a2AFf38c1f393B9fb")
print(balance)