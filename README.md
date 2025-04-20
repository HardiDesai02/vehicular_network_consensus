# Vehicle Data Consensus with Hyperledger Fabric

This project implements a blockchain-based consensus mechanism for vehicle data using Hyperledger Fabric. The network includes two organizations (Org1 and Org2) and an orderer, with a chaincode (consensus) that manages vehicle data (speed, position, cluster). Data is parsed from a CSV file, submitted to the blockchain, and queried to verify consensus across peers. A `SelectNode` function allows post-consensus decision-making, such as selecting a node for further processing.

## Prerequisites

- **Operating System:** Ubuntu 20.04 or later (Linux recommended)
- **Docker:** Version 20.10 or higher
- **Docker Compose:** Version 1.29 or higher
- **Git:** For cloning repositories
- **Go:** Version 1.18 or higher (for chaincode development)
- **Python:** Version 3.8 or higher (for data parsing and submission scripts)

## Project Setup

### Step 1: Clone Hyperledger Fabric
```bash
mkdir -p ~/Desktop/Blockchain
cd ~/Desktop/Blockchain
git clone https://github.com/hyperledger/fabric-samples.git
```

### Step 2: Clone Project Repository
```bash
cd ~/Desktop/Blockchain
git clone https://github.com/HardiDesai02/vehicular_network_consensus.git
```

### Step 3: Set Up Fabric Network
```bash
cd ~/Desktop/Blockchain/fabric-samples/test-network

# Create the channel (mychannel)
./network.sh down
./network.sh up createChannel -c mychannel -ca

# If the channel already exists
./network.sh up -ca
```

Verify containers:
```bash
docker ps
```
Expected:
- orderer.example.com
- peer0.org1.example.com
- peer0.org2.example.com

### Step 4: Join Peers to Channel
Join Org1:
```bash
docker exec -it peer0.org1.example.com bash
peer channel join -b /opt/gopath/src/github.com/hyperledger/fabric/peer/mychannel.block
exit
```
Join Org2:
```bash
docker exec -it peer0.org2.example.com bash
peer channel join -b /opt/gopath/src/github.com/hyperledger/fabric/peer/mychannel.block
exit
```


## Chaincode Deployment

### Step 1: Package Chaincode

Package the consensus chaincode:
```bash
cd ~/Desktop/Blockchain/fabric-samples/test-network
peer lifecycle chaincode package consensus.tar.gz \
  --path ~/Desktop/Blockchain/smart_contract \
  --lang golang \
  --label consensus_1
```
### Step 2: Install Chaincode on Peers

#### Org1

Set environment variables:
```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_TLS_ENABLED=true
```
Install chaincode:
```bash
peer lifecycle chaincode install consensus.tar.gz
```
Verify installation:
```bash
peer lifecycle chaincode queryinstalled
```
Expected output:
```plain
Installed chaincodes on peer:
Package ID: consensus_1:<hash>, Label: consensus_1
```
Note the Package ID (e.g., consensus_1:8797f0f08161b8a26f4f4ddb32617d034d74a343017e05afed8c525c3cb391e4).

#### Org2

Set environment variables:
```bash
export CORE_PEER_LOCALMSPID="Org2MSP"
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_TLS_ENABLED=true
```
Install chaincode:
```bash
peer lifecycle chaincode install consensus.tar.gz
```
Verify:
```bash
peer lifecycle chaincode queryinstalled
```
### Step 3: Approve Chaincode

#### Org1

Set environment:
```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_TLS_ENABLED=true
```
Approve:
```bash
peer lifecycle chaincode approveformyorg \
  --orderer localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --channelID mychannel \
  --name consensus \
  --version 1.0 \
  --package-id consensus_1:<hash-from-queryinstalled> \
  --sequence 1 \
  --tls \
  --cafile $HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
```
Check commit readiness:
```bash
peer lifecycle chaincode checkcommitreadiness \
  --channelID mychannel \
  --name consensus \
  --version 1.0 \
  --sequence 1 \
  --output json
```
Expected:
```json
{
  "approvals": {
    "Org1MSP": true
  }
}
```
### Org2

Set environment:
```bash
export CORE_PEER_LOCALMSPID="Org2MSP"
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_TLS_ENABLED=true
```
Approve:
```bash
peer lifecycle chaincode approveformyorg \
  --orderer localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --channelID mychannel \
  --name consensus \
  --version 1.0 \
  --package-id consensus_1:<hash-from-queryinstalled> \
  --sequence 1 \
  --tls \
  --cafile $HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
```
Verify readiness:
```bash
peer lifecycle chaincode checkcommitreadiness \
  --channelID mychannel \
  --name consensus \
  --version 1.0 \
  --sequence 1 \
  --output json
```
Expected:
```json
{
  "approvals": {
    "Org1MSP": true,
    "Org2MSP": true
  }
}
```
### Step 4: Commit Chaincode

Using Org1’s environment:
```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_TLS_ENABLED=true
```
Commit:
```bash
peer lifecycle chaincode commit \
  --orderer localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --channelID mychannel \
  --name consensus \
  --version 1.0 \
  --sequence 1 \
  --tls \
  --cafile $HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles $HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt \
  --peerAddresses localhost:9051 \
  --tlsRootCertFiles $HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
```
Verify:
```bash
peer lifecycle chaincode querycommitted --channelID mychannel --name consensus
```
Expected:
```plain
Committed chaincode definition for chaincode 'consensus' on channel 'mychannel':
Version: 1.0, Sequence: 1, Endorsement Plugin: escc, Validation Plugin: vscc, Approvals: [Org1MSP: true, Org2MSP: true]
```
## Process Vehicle Data

### Step 1: Parse Vehicle Data

Convert clustered_vehicles.csv to vehicle_data.json:
```bash
cd ~/Desktop/Blockchain
python3 parse_vehicle_data.py
```
Verify:
```bash
cat vehicle_data.json | head -n 20
```
### Step 2: Submit Vehicle Data

Submit data to the blockchain:
```bash
python3 submit_vehicle_data.py
```
Expected:
```plain
Loaded 100 vehicles from vehicle_data.json
Submitting data for veh1.0...
Success: veh1.0 submitted...
...
Finished submitting vehicle data.
```
### Step 3: Query Vehicle Data

Query the ledger to verify data:
```bash
python3 query_vehicle_data.py
```
Expected:
```plain
Query Result: [
  {
    "VehicleID": "veh1.99",
    "Records": [
      {"Speed": 0, "Position_X": 5.1, "Position_Y": -1.6, "Cluster": 2},
      ...
    ]
  },
  ...
]
Found 100 vehicles:
VehicleID: veh1.0, Records: 39
...
```
## Verify Consensus

Consensus is achieved when both peers (Org1 and Org2) have identical ledger states, ensuring all vehicle data is consistently stored.

### Step 1: Query Both Peers

#### Org1:
```bash
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_TLS_ENABLED=true
peer chaincode query -C mychannel -n consensus -c '{"function":"QueryAllVehicles","Args":[]}' > ~/Desktop/Blockchain/org1_query.json
```
#### Org2:
```bash
export CORE_PEER_LOCALMSPID="Org2MSP"
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_TLS_ENABLED=true
peer chaincode query -C mychannel -n consensus -c '{"function":"QueryAllVehicles","Args":[]}' > ~/Desktop/Blockchain/org2_query.json
```
Compare:
```bash
diff ~/Desktop/Blockchain/org1_query.json ~/Desktop/Blockchain/org2_query.json
```




No output: Consensus achieved (identical ledger states).

### Step 2: Check Commit Hashes
```bash
docker logs peer0.org1.example.com | grep "commitHash" | tail -n 1
docker logs peer0.org2.example.com | grep "commitHash" | tail -n 1
```




Same hash: Confirms consensus at the block level (e.g., block 26).

## Invoke SelectNode

After consensus is verified, invoke the SelectNode function to select a node (e.g., node1) for additional consensus logic, such as designating a leader or coordinator based on vehicle data:
```bash
peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile ~/Desktop/Blockchain/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem \
  -C mychannel \
  -n consensus \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles ~/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt \
  --peerAddresses localhost:9051 \
  --tlsRootCertFiles ~/Desktop/Blockchain/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
  -c '{"Args":["SelectNode", "node1"]}'
```
Expected:
```plain
INFO [chaincodeCmd] chaincodeInvokeOrQuery -> Chaincode invoke successful. result: status:200
```
## Shutdown

Clean up the network:
```bash
cd ~/Desktop/Blockchain/fabric-samples/test-network
./network.sh down
```
