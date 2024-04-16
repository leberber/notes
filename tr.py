import requests
def get_latest_mint_transactions(num_transactions):
    # Construct the URL for the Solana RPC endpoint
    url = "https://api.mainnet-beta.solana.com"

    # Construct the request data for getConfirmedSignaturesForAddress2 RPC method
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [
            "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # Token program ID
            {
                "limit": num_transactions
            }
        ]
    }

    # Send a POST request to the Solana RPC endpoint
    response = requests.post(url, json=request_data, headers={"Content-Type": "application/json"})
    response_data = response.json()

    # Parse the response to extract transaction signatures
    mint_transactions = []
    if "result" in response_data:
        for result in response_data["result"]:
            mint_transactions.append(result["signature"])
    else:
        print("Error:", response_data["error"])
    
    return mint_transactions

# Specify the number of latest mint transactions to retrieve
num_transactions = 10

# Get the latest mint transactions
latest_mint_transactions = get_latest_mint_transactions(num_transactions)
latest_mint_transactions








import json
import requests

# Replace with the actual transaction signature
transaction_signature = "65NMhKLbPvT2i1kBDgzsRhTMJcFFvBGspYYsKuuBE1uDMxECy4XpV4wpEtfQw68jXCSNnpBj2s5V1XGNUFCGcpvi"

# Prepare the request data
url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}
data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTransaction",
    "params": [transaction_signature, {"encoding":"jsonParsed", "maxSupportedTransactionVersion": 0}],
}

# Send the POST request
response = requests.post(url, headers=headers, json=data)

# Check for successful response
if response.status_code == 200:
    # Parse the JSON response and prettify it for better readability
    response_data = json.loads(response.text)
    print(json.dumps(response_data, indent=4))  # Indent for better formatting
else:
    print(f"Error: {response.status_code}")
    print(response.json())














import requests

def get_swaps_for_meme_coin(meme_coin_token_address, num_swaps):
    # Construct the URL for the Solana RPC endpoint
    url = "https://api.mainnet-beta.solana.com"

    # Construct the request data for getSignaturesForAddress RPC method
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            meme_coin_token_address,
            {
                "limit": num_swaps
            }
        ]
    }

    # Send a POST request to the Solana RPC endpoint
    response = requests.post(url, json=request_data, headers={"Content-Type": "application/json"})
    response_data = response.json()

    # Parse the response to extract transaction signatures
    if "result" in response_data:
        signatures = [signature["signature"] for signature in response_data["result"]]
        return signatures, response_data["result"]
    else:
        print("Error:", response_data["error"])
        return None

# Specify the meme coin token address
meme_coin_token_address = "A9ENr7uXH5ydnBDTvxvCmQT1J2nxS63pv9VK7KL1BRSM"

# Specify the number of swaps to list
num_swaps = 10

# Get recent swaps related to the meme coin
swaps, d =  get_swaps_for_meme_coin(meme_coin_token_address, num_swaps)
if swaps:
    print("Recent swaps related to the meme coin:")
    for swap in swaps:
        print(swap)





# curl https://api.devnet.solana.com -X POST -H "Content-Type: application/json" -d '
#                                   {
#                                     "jsonrpc": "2.0",
#                                     "id": 1,
#                                     "method": "getTransaction",
#                                     "params": [
#                                       "2YHDUWRRh4jwaAqSPJqCiu97FTy6Pu2C6XGbAzsaBbyjQeXW11z
# hhF3DJHt4vDFHVND1ybdSHf6E5FxbjFXZP4gQ",
#                                       "jsonParsed"
#                                     ]
#                                   }
#                                 ' | python3 -m json.tool
d = {
    "jsonrpc": "2.0",
    "result": {
        "blockTime": 1647001173,
        "meta": {
            "err":'null',
            "fee": 5000,
            "innerInstructions": [],
            "logMessages": [
                "Program 11111111111111111111111111111111 invoke [1]",
                "Program 11111111111111111111111111111111 success"
            ],
            "postBalances": [
                23932341357,
                110000000,
                1
            ],
            "postTokenBalances": [],
            "preBalances": [
                23942346357,
                100000000,
                1
            ],
            "preTokenBalances": [],
            "rewards": [],
            "status": {
                "Ok": 'null',
            }
        },
        "slot": 120237987,
        "transaction": {
            "message": {
                "accountKeys": [
                    {
                        "pubkey": "4SnSuUtJGKvk2GYpBwmEsWG53zTurVM8yXGsoiZQyMJn",
                        "signer": True,
                        "writable": True
                    },
                    {
                        "pubkey": "4AUt2JyjzJYVhWkjKugXmzhWizpb4SpLHBtL2fuqPskU",
                        "signer": False,
                        "writable": True
                    },
                    {
                        "pubkey": "11111111111111111111111111111111",
                        "signer": False,
                        "writable": False
                    }
                ],
                "instructions": [
                    {
                        "parsed": {
                            "info": {
                                "destination": "4AUt2JyjzJYVhWkjKugXmzhWizpb4SpLHBtL2fuqPskU",
                                "lamports": 10000000,
                                "source": "4SnSuUtJGKvk2GYpBwmEsWG53zTurVM8yXGsoiZQyMJn"
                            },
                            "type": "transfer"
                        },
                        "program": "system",
                        "programId": "11111111111111111111111111111111"
                    }
                ],
                "recentBlockhash": "3zny2xt5wimev9Jry3TiAyK8yA2pMMcGvsPWpFN5HiL6"
            },
            "signatures": [
                "2YHDUWRRh4jwaAqSPJqCiu97FTy6Pu2C6XGbAzsaBbyjQeXW11zhhF3DJHt4vDFHVND1ybdSHf6E5FxbjFXZP4gQ"
            ]
        }
    },
    "id": 1
}




d['result']['transaction']['message']['instructions'][0]['parsed']
