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

# ---------------------- Dynamic Node Generation ----------------------
def generate_nodes(num_nodes):
    """Dynamically generate nodes with randomized ACL and Trust Metrics."""
    nodes = {}
    crud_importance_levels = ['High', 'Moderate', 'Low']
    
    for i in range(num_nodes):
        node_name = f"N{i}"
        
        # Generate random ACL (each node can access 20% of other nodes)
        acl = {}
        accessible_nodes = random.sample(range(num_nodes), max(1, num_nodes // 5))
        for target in accessible_nodes:
            if target != i:
                acl[f"N{target}"] = random.sample(['C', 'R', 'U', 'D'], random.randint(1, 4))

        # Assign minimum Trust Metrics randomly
        min_tv = {op: random.randint(50, 100) for op in ['C', 'R', 'U', 'D']}
        
        # Assign CRUD importance levels randomly
        crud_importance = {op: random.choice(crud_importance_levels) for op in ['C', 'R', 'U', 'D']}
        
        nodes[node_name] = Node(node_name, acl, min_tv, crud_importance)
    
    return nodes

# ---------------------- ACL Functions ----------------------
def check_acl_permission(source, target, operation):
    return target in nodes[source].acl and operation in nodes[source].acl[target]

def revoke_all_access(node_name):
    nodes[node_name].acl = {}
    logging.warning(f"Revoked all ACL entries for {node_name} due to TV < 40%")

# ---------------------- CRUD Operations ----------------------
def perform_crud_operation(source_node, target_node, operation):
    """Performs a CRUD operation and tracks gas & transaction time."""
    current_tv = nodes[source_node].trust_value
    category = "no_permission"

    if current_tv < 40:
        logging.warning(f"{operation} denied: {source_node} -> {target_node} | TV too low")
        return

    if check_acl_permission(source_node, target_node, operation):
        required_tv = nodes[target_node].min_tv[operation]
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

    track_gas_time(tx_hash, category)

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

# ---------------------- Run Simulation for Different Node Sizes ----------------------
def run_simulation(num_nodes):
    global nodes
    nodes = generate_nodes(num_nodes)

    print(f"\n🔹 Running Simulation for {num_nodes} Nodes 🔹\n")

    for iteration in range(100):  # Run for 100 iterations per simulation
        source_node = random.choice(list(nodes.keys()))
        target_node = random.choice(list(nodes.keys()))
        operation = random.choice(['C', 'R', 'U', 'D'])

        perform_crud_operation(source_node, target_node, operation)
        evaluate_trust_metric(source_node, target_node, operation)

        if iteration % 10 == 0:
            adjust_policy(source_node)

for size in [10, 50, 100, 500, 1000]:
    run_simulation(size)
