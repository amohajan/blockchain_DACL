import random
import time
import logging
import os
import math
import copy
from datetime import datetime
from web3 import Web3

# ---------------------- Logging Configuration ----------------------
LOG_DIRECTORY = './logs/'
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

log_file_name = f"{LOG_DIRECTORY}node_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(filename=log_file_name,
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ---------------------- Blockchain Setup ----------------------
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
contract_address = "0xDA0bab807633f07f013f94DD0E6A4F96F8742B53"

# Load contract ABI (Replace with actual ABI)
contract_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "objectID",
				"type": "string"
			}
		],
		"name": "ACLRevoked",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "objectID",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "operation",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "minTrustThreshold",
				"type": "uint256"
			}
		],
		"name": "ACLUpdated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "reason",
				"type": "string"
			}
		],
		"name": "AccessDenied",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "operation",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "decision",
				"type": "string"
			}
		],
		"name": "AccessRequestLogged",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			}
		],
		"name": "addNode",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "riskFactor",
				"type": "uint256"
			}
		],
		"name": "adjustTrustMetric",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "impactScore",
				"type": "uint256"
			}
		],
		"name": "evaluateRisk",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			}
		],
		"name": "generateAccessPolicy",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "requester",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "targetNode",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "objectID",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "operation",
				"type": "string"
			}
		],
		"name": "getAccessRequest",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "riskFactor",
				"type": "uint256"
			}
		],
		"name": "RiskEvaluated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "newTrustValue",
				"type": "uint256"
			}
		],
		"name": "TrustMetricUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "objectID",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "operation",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "impactScore",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "minTrustThreshold",
				"type": "uint256"
			}
		],
		"name": "updateACL",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			}
		],
		"name": "computeUnauthorizedAccessProbability",
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
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			}
		],
		"name": "getAllACLObjectIDs",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "nodeName",
				"type": "string"
			}
		],
		"name": "getTrustValue",
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
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] # Keep your ABI here
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

sender_address = "0xa1ba22C62C8b73d0777fe0c8be7c4F63dcD08c49"
private_key = "0x69904472dc859c59fd0e95914c3f800c590e293834150b570a61f2024986689a"

# ---------------------- Gas & Transaction Tracking ----------------------
gas_stats = {
    "permission_granted": [],
    "no_permission": [],
    "risk_analysis": [],
    "tm_evaluation": [],
    "tm_below_threshold": [],
    "policy_adjustment": []
}

def track_gas_time(tx_hash, category):
    """Tracks gas usage and transaction time for a given category."""
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    gas_used = tx_receipt.gasUsed
    block = web3.eth.get_block(tx_receipt.blockNumber)
    transaction_time = abs(block.timestamp - time.time())

    gas_stats[category].append((gas_used, transaction_time))

    print(f"✅ {category}: Gas Used: {gas_used}, Time: {transaction_time:.4f}s")
    return gas_used, transaction_time

def get_avg_gas_time(category):
    """Calculates average gas and transaction time for a category."""
    if len(gas_stats[category]) == 0:
        return 0, 0
    avg_gas = sum(g[0] for g in gas_stats[category]) / len(gas_stats[category])
    avg_time = sum(g[1] for g in gas_stats[category]) / len(gas_stats[category])
    return avg_gas, avg_time

# ---------------------- Node Class ----------------------
class Node:
    def __init__(self, name, acl, min_tv, crud_importance):
        self.name = name
        self.trust_value = 100
        self.acl = acl
        self.min_tv = min_tv
        self.crud_importance = crud_importance
        self.data = []

    def add_data(self, new_data):
        self.data.append(new_data)

# ---------------------- Initialize Nodes & ACL ----------------------
nodes = {
    'A': Node('A', {'A': 'C,R,U,D', 'B': 'C,R,U,D', 'C': 'C,R,U,D', 'D': 'C,R,U,D', 'E': 'C,R,U,D', 'F': 'C,R,U,D',
          'G': 'C,R,U,D', 'H': 'C,R,U,D', 'I': 'C,R,U,D', 'J': 'C,R,U,D', 'K': 'C,R,U,D', 'L': 'C,R,U,D',
          'M': 'C,R,U,D', 'N': 'C,R,U,D', 'O': 'C,R,U,D'},
              {'C': 95, 'R': 95, 'U': 95, 'D': 95},
              {'C': 'High', 'R': 'High', 'U': 'High', 'D': 'High'}),

    'B': Node('B', {'A': 'C', 'B': 'C,R,U,D', 'C': 'C,R,U,D', 'E': 'C,R,U,D', 'H': 'R', 'I': 'R', 'J': 'C,R,U,D',
          'K': 'C,R,U,D', 'L': 'C,R,U,D', 'M': 'C,R,U,D', 'N': 'C,R,U,D', 'O': 'C,R,U,D'},
              {'C': 80, 'R': 75, 'U': 80, 'D': 80},
              {'C': 'High', 'R': 'Moderate', 'U': 'High', 'D': 'High'}),

    'C': Node('C', {'A': 'C', 'B': 'C,R,U,D', 'C': 'C,R,U,D', 'F': 'C,R,U,D', 'G': 'C,R,U,D', 'H': 'C,R,U,D',
          'I': 'C,R,U,D'},
              {'C': 80, 'R': 75, 'U': 80, 'D': 80},
              {'C': 'High', 'R': 'Moderate', 'U': 'High', 'D': 'High'}),

    'D': Node('D', {'B': 'C', 'C': 'C,R,U,D', 'D': 'C,R,U,D', 'E': 'C,R,U,D', 'H': 'R', 'I': 'R'},
              {'C': 65, 'R': 60, 'U': 65, 'D': 65},
              {'C': 'Moderate', 'R': 'Low', 'U': 'Low', 'D': 'Moderate'}),

    'E': Node('E', {'B': 'C', 'C': 'C,R', 'D': 'C', 'E': 'C,R,U,D', 'F': 'C', 'J': 'C,R,U,D', 'K': 'C,R,U,D'},
              {'C': 65, 'R': 60, 'U': 65, 'D': 65},
              {'C': 'Moderate', 'R': 'Low', 'U': 'Low', 'D': 'Moderate'}),

    'F': Node('F', {'C': 'C', 'E': 'C', 'F': 'C,R,U,D', 'G': 'C', 'L': 'C', 'M': 'C,R'},
              {'C': 60, 'R': 60, 'U': 60, 'D': 65},
              {'C': 'Moderate', 'R': 'Low', 'U': 'Low', 'D': 'Moderate'}),

    'G': Node('G', {'C': 'R', 'F': 'C', 'G': 'C,R,U,D', 'N': 'C,R', 'O': 'C,R'},
              {'C': 60, 'R': 60, 'U': 60, 'D': 65},
              {'C': 'Moderate', 'R': 'Low', 'U': 'Low', 'D': 'Moderate'}),

    'H': Node('H', {'D': 'R', 'H': 'C,R,U,D', 'I': ''},  # Fixed `None` to `""`
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'I': Node('I', {'D': 'R', 'H': '', 'I': 'C,R,U,D', 'K': 'R', 'L': ''},  # Fixed `None`
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'J': Node('J', {'E': 'R', 'J': 'C,R,U,D', 'K': ''},  # Fixed `None`
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'K': Node('K', {'E': 'R', 'F': '', 'J': '', 'K': 'C,R,U,D', 'M': 'C,R'},  # Fixed `None`
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'L': Node('L', {'F': 'C,R', 'G': 'C,R', 'L': 'C,R,U,D'},
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'M': Node('M', {'F': 'C,R', 'G': 'C,R', 'M': 'C,R,U,D'},
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'N': Node('N', {'G': 'C,R', 'N': 'C,R,U,D'},
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'}),

    'O': Node('O', {'G': 'C,R', 'O': 'C,R,U,D'},
              {'C': 55, 'R': 55, 'U': 60, 'D': 55},
              {'C': 'Low', 'R': 'Low', 'U': 'Low', 'D': 'Low'})
}

acl_table = {node: nodes[node].acl for node in nodes}
minimum_tv_requirements = {node: nodes[node].min_tv for node in nodes}
crud_importance_table = {node: nodes[node].crud_importance for node in nodes}


# ---------------------- CRUD Operations ----------------------
def perform_crud_operation(source_node, target_node, operation):
    """Performs a CRUD operation and tracks gas & transaction time."""
    current_tv = nodes[source_node].trust_value
    category = "no_permission"

    if current_tv < 40:
        logging.warning(f"{operation} denied: {source_node} -> {target_node} | TV too low")
        return

    if check_acl_permission(source_node, target_node, operation):
        required_tv = minimum_tv_requirements[target_node].get(operation, 50)
        if current_tv < required_tv:
            category = "tm_below_threshold"
        else:
            category = "permission_granted"
    else:
        category = "no_permission"
    
    # Simulate blockchain transaction
    tx_hash = contract.functions.getAccessRequest(source_node, target_node, "OBJ", operation).build_transaction({
        'from': sender_address,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(sender_address),
    })
    signed_tx = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Track gas and time
    track_gas_time(tx_hash, category)
    
# ---------------------- ACL Functions ----------------------
def check_acl_permission(source, target, operation):
    """Checks if a source node has permission for an operation on a target node."""
    if source in acl_table and target in acl_table[source]:
        allowed_operations = acl_table[source][target]
        return operation in allowed_operations
    return False

# ---------------------- Risk Analysis & Trust Metric Evaluation ----------------------
def evaluate_trust_metric(source_node, target_node, operation):
    """Evaluates trust metric and tracks gas/time."""
    category = "tm_evaluation"
    
    tx_hash = contract.functions.evaluateRisk(source_node, 10).build_transaction({
        'from': sender_address,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(sender_address),
    })
    signed_tx = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    track_gas_time(tx_hash, category)

# ---------------------- Policy Adjustment ----------------------
def adjust_policy(source_node):
    """Adjusts policy dynamically and tracks gas/time."""
    category = "policy_adjustment"

    tx_hash = contract.functions.generateAccessPolicy(source_node).build_transaction({
        'from': sender_address,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(sender_address),
    })
    signed_tx = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    track_gas_time(tx_hash, category)

# ---------------------- Node Operation Loop ----------------------
def continuous_node_operation():
    iteration = 0
    while True:
        iteration += 1
        print(f"\nIteration {iteration} - Logging to: {log_file_name}")

        source_node = random.choice(list(nodes.keys()))
        target_node = random.choice(list(nodes.keys()))
        operation = random.choice(['C', 'R', 'U', 'D'])

        perform_crud_operation(source_node, target_node, operation)
        evaluate_trust_metric(source_node, target_node, operation)

        if iteration % 5 == 0:
            adjust_policy(source_node)

        if iteration % 10 == 0:
            for category in gas_stats:
                avg_gas, avg_time = get_avg_gas_time(category)
                print(f"📊 Average for {category}: Gas = {avg_gas}, Time = {avg_time:.4f}s")

        time.sleep(30)

# ---------------------- Start Simulation ----------------------
continuous_node_operation()
