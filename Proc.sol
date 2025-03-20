// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract EnhancedAccessControl {
    
    struct TrustMetrics {
        uint256 value; // Trust Metric (TV)
    }

    struct ACL {
        string objectID;
        string operation;
        uint256 impactScore; // 0.9 (High), 0.5 (Moderate), 0.2 (Low)
        uint256 minTrustThreshold;
    }

    struct Node {
        string nodeName;
        TrustMetrics trustMetrics;
        mapping(string => ACL) aclEntries; // ACL entries for objects
        bool exists;
    }

    mapping(string => Node) private nodes;
    mapping(string => uint256) private unauthorizedRequests; // Track unauthorized requests per node
    mapping(string => uint256) private totalRequests; // Track total requests per node
    mapping(string => string[]) private nodeACLObjects;  // Store objectIDs for each node

    address public owner;

    event AccessRequestLogged(string indexed nodeName, string operation, string decision);
    event TrustMetricUpdated(string indexed nodeName, uint256 newTrustValue);
    event ACLUpdated(string indexed nodeName, string objectID, string operation, uint256 minTrustThreshold);
    event AccessDenied(string indexed nodeName, string reason);
    event RiskEvaluated(string indexed nodeName, uint256 riskFactor);
    event ACLRevoked(string indexed nodeName, string objectID);

    modifier onlyExistingNode(string memory nodeName) {
        require(nodes[nodeName].exists, "Node does not exist");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // Add a new node with an initial Trust Value of 100
    function addNode(string memory nodeName) public {
        require(!nodes[nodeName].exists, "Node already exists");
        nodes[nodeName].trustMetrics.value = 100;
        nodes[nodeName].exists = true;
    }

    // Update ACL permissions for a node
    function updateACL(string memory nodeName, string memory objectID, string memory operation, uint256 impactScore, uint256 minTrustThreshold) 
        public onlyExistingNode(nodeName) 
    {
        nodes[nodeName].aclEntries[objectID] = ACL(objectID, operation, impactScore, minTrustThreshold);
        nodeACLObjects[nodeName].push(objectID);  // Track object ID
        emit ACLUpdated(nodeName, objectID, operation, minTrustThreshold);
    }

    // Get all ACL object IDs for a node
    function getAllACLObjectIDs(string memory nodeName) public view onlyExistingNode(nodeName) returns (string[] memory) {
        return nodeACLObjects[nodeName];
    }

    // Get Trust Value of a node
    function getTrustValue(string memory nodeName) public view onlyExistingNode(nodeName) returns (uint256) {
        return nodes[nodeName].trustMetrics.value;
    }

    // Adjust Trust Value based on Risk Factor
    function adjustTrustMetric(string memory nodeName, uint256 riskFactor) public onlyExistingNode(nodeName) {
        uint256 reduction = (nodes[nodeName].trustMetrics.value * riskFactor) / 100;

        if (reduction > nodes[nodeName].trustMetrics.value) {
            nodes[nodeName].trustMetrics.value = 0;
        } else {
            nodes[nodeName].trustMetrics.value -= reduction;
        }

        emit TrustMetricUpdated(nodeName, nodes[nodeName].trustMetrics.value);
    }

    // Compute Probability of Unauthorized Access Request
    function computeUnauthorizedAccessProbability(string memory nodeName) public view onlyExistingNode(nodeName) returns (uint256) {
        uint256 totalOps = totalRequests[nodeName]; 
        uint256 failedOps = unauthorizedRequests[nodeName]; 

        if (totalOps == 0) return 0;

        uint256 pN = (failedOps * 100) / totalOps; // Convert probability into percentage

        return pN;
    }

    // Evaluate Risk Based on Unauthorized Requests & Impact Level
    function evaluateRisk(string memory nodeName, uint256 impactScore) 
        public onlyExistingNode(nodeName) returns (uint256)
    {
        uint256 pN = computeUnauthorizedAccessProbability(nodeName);
        uint256 riskFactor = (pN * impactScore) / 100; // Applying impact level factor

        emit RiskEvaluated(nodeName, riskFactor);
        return riskFactor;
    }

    // Handle Access Request
    function getAccessRequest(string memory requester, string memory targetNode, string memory objectID, string memory operation) 
        public onlyExistingNode(requester) onlyExistingNode(targetNode) 
    {
        totalRequests[requester] += 1;

        ACL memory aclEntry = nodes[targetNode].aclEntries[objectID];

        if (keccak256(abi.encodePacked(aclEntry.operation)) == keccak256(abi.encodePacked(operation))) {
            uint256 requesterTrust = nodes[requester].trustMetrics.value;
            
            if (requesterTrust >= aclEntry.minTrustThreshold) {
                emit AccessRequestLogged(requester, operation, "GRANTED");
            } else {
                emit AccessDenied(requester, "Low Trust Value");
                unauthorizedRequests[requester] += 1;
                uint256 riskFactor = evaluateRisk(requester, aclEntry.impactScore);
                adjustTrustMetric(requester, riskFactor);
            }
        } else {
            emit AccessDenied(requester, "Insufficient Permissions");
            unauthorizedRequests[requester] += 1;
            uint256 riskFactor = evaluateRisk(requester, aclEntry.impactScore);
            adjustTrustMetric(requester, riskFactor);
        }
    }

    // Generate Access Policy if Trust Value Drops Below 40%
    function generateAccessPolicy(string memory nodeName) public onlyExistingNode(nodeName) {
        if (nodes[nodeName].trustMetrics.value < 40) {
            string[] memory objectIDs = getAllACLObjectIDs(nodeName);
            
            for (uint256 i = 0; i < objectIDs.length; i++) {
                delete nodes[nodeName].aclEntries[objectIDs[i]];
                emit ACLRevoked(nodeName, objectIDs[i]);
            }

            emit AccessDenied(nodeName, "Access Revoked Due to Low Trust");
        }
    }
}
