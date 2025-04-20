import pandas as pd
import numpy as np
import json
import os
import subprocess
import uuid

df = pd.read_csv("../data/reputation_scores.csv")
df = df.sort_values("Reputation", ascending=False).drop_duplicates("Vehicle_ID")
mcn_set = df.head(4).copy()
proposer = mcn_set.iloc[0]
validators = mcn_set.iloc[1:]

votes = []
for _, row in validators.iterrows():
    vote = np.random.rand() < row["SoB"]
    votes.append((row["Vehicle_ID"], vote))

approvals = [v[0] for v in votes if v[1]]
consensus = len(approvals) >= 2

if consensus:
    block_id = f"BLOCK-{uuid.uuid4()}"
    proposer_id = proposer["Vehicle_ID"]

    os.environ['CORE_PEER_LOCALMSPID'] = "Org1MSP"
    os.environ['CORE_PEER_TLS_ENABLED'] = "true"
    os.environ['CORE_PEER_TLS_ROOTCERT_FILE'] = os.path.abspath(
        "../../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
    )
    os.environ['CORE_PEER_MSPCONFIGPATH'] = os.path.abspath(
        "../../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
    )
    os.environ['CORE_PEER_ADDRESS'] = "localhost:7051"

    cmd = [
        "peer", "chaincode", "invoke",
        "-o", "localhost:7050",
        "--ordererTLSHostnameOverride", "orderer.example.com",
        "--tls", "--cafile",
        os.path.abspath("../../fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"),
        "-C", "vehiclepbft",
        "-n", "vehiclecc",
        "-c", json.dumps({
            "function": "SubmitBlock",
            "Args": [proposer_id, json.dumps(approvals), block_id]
        })
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print("✔️ Block committed. Block ID:", block_id)
    print(result.stdout)
else:
    print("❌ Consensus failed. Block not submitted.")
