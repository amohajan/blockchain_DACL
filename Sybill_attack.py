import random
import time
import logging
import os
from datetime import datetime
from web3 import Web3

# ---------------------- Logging Configuration ----------------------
LOG_DIRECTORY = './logs/'
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

log_file_name = f"{LOG_DIRECTORY}sybil_attack_15_nodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
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

# ---------------------- Initialize Nodes ----------------------
class Node:
    def __init__(self, name, acl, min_tv, crud_importance):
        self.name = name
        self.trust_value = 100
        self.acl = acl
        self.min_tv = min_tv
        self.crud_importance = crud_importance
        self.data = []

    def decrease_trust(self, penalty):
        self.trust_value = max(0, self.trust_value - penalty)

# Define the nodes with ACL, minimum trust, and CRUD importance
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

# ---------------------- Define Sybil Attackers ----------------------
sybil_nodes = random.sample(list(nodes.keys()), 3)  # Select 3 random Sybil nodes
print(f"🚨 Sybil Attackers Identified: {sybil_nodes}")

# ---------------------- Sybil Attack Simulation ----------------------
def perform_sybil_attack():
    for iteration in range(1, 6):  # Run for 5 iterations
        print(f"\n🛠 Iteration {iteration}: System Running...\n")
        logging.info(f"Iteration {iteration}: System Running...")

        print("\n🔴 Initiating Sybil Attack 🔴\n")
        logging.info("🔴 Initiating Sybil Attack 🔴")

        for attacker in sybil_nodes:
            target = random.choice(list(nodes.keys()))  # Select random target node
            operation = random.choice(['C', 'R', 'U', 'D'])  # Random operation
            
            # Check ACL restrictions
            if target in nodes[attacker].acl:
                print(f"✅ {attacker} SUCCESSFULLY executed {operation} on {target} (Unauthorized!)")
                logging.warning(f"{attacker} SUCCESSFULLY executed {operation} on {target} (Unauthorized!)")
                nodes[attacker].decrease_trust(10)  # Unauthorized actions decrease trust
            else:
                print(f"🚫 {attacker} was DENIED {operation} on {target}. ACL Restriction!")
                logging.info(f"{attacker} was DENIED {operation} on {target}. ACL Restriction!")
                
                # Perform risk evaluation
                risk_factor = random.randint(10, 20)
                if risk_factor > 15:
                    print(f"❌ HIGH RISK: {attacker} denied {operation} on {target}.")
                    print(f"🚨 {attacker} detected & denied access due to high risk!")
                    logging.warning(f"{attacker} detected & denied access due to high risk!")
                    nodes[attacker].decrease_trust(15)  # Higher penalty for high-risk actions

        # Revoke all access for Sybil nodes below trust threshold
        for attacker in sybil_nodes:
            if nodes[attacker].trust_value < 40:
                nodes[attacker].acl = {}  # Remove all permissions
                print(f"🔒 {attacker} has lost ALL ACCESS due to repeated attacks!")
                logging.critical(f"{attacker} has lost ALL ACCESS due to repeated attacks!")

        time.sleep(2)

# Run attack simulation
perform_sybil_attack()

# ---------------------- Display Final Trust Values ----------------------
print("\n📊 System Monitoring: Final Trust Values\n")
logging.info("📊 System Monitoring: Final Trust Values")

for node in nodes.keys():
    status = "Sybil" if node in sybil_nodes else "Legitimate"
    print(f"  🔹 {node}: TV = {nodes[node].trust_value} ({status})")
    logging.info(f"{node}: TV = {nodes[node].trust_value} ({status})")
