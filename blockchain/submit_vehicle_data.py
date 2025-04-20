# submit_vehicle_data.py
import json
import subprocess
import os

# Set environment variables for Org1
os.environ['CORE_PEER_LOCALMSPID'] = "Org1MSP"
os.environ['CORE_PEER_TLS_ENABLED'] = "true"
os.environ['CORE_PEER_TLS_ROOTCERT_FILE'] = os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
os.environ['CORE_PEER_MSPCONFIGPATH'] = os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp")
os.environ['CORE_PEER_ADDRESS'] = "localhost:7051"

# Load vehicle data
try:
    with open('vehicle_data.json', 'r') as f:
        vehicle_data = json.load(f)
    print(f"Loaded {len(vehicle_data)} vehicles from vehicle_data.json")
except FileNotFoundError:
    print("Error: vehicle_data.json not found. Run parse_vehicle_data.py first.")
    exit(1)

# Submit each vehicle's data
for vehicle in vehicle_data:
    vehicle_id = vehicle['VehicleID']
    records_json = json.dumps(vehicle['Records']).replace('"', '\\"')  # Escape quotes for CLI
    
    cmd = [
        "peer", "chaincode", "invoke",
        "-o", "localhost:7050",
        "--ordererTLSHostnameOverride", "orderer.example.com",
        "--tls",
        "--cafile", os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"),
        "-C", "vehiclechannel",
        "-n", "vehiclecc",
        "--peerAddresses", "localhost:7051",
        "--tlsRootCertFiles", os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"),
        "--peerAddresses", "localhost:9051",
        "--tlsRootCertFiles", os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"),
        "-c", f'{{"function":"SubmitVehicleData","Args":["{vehicle_id}","{records_json}"]}}'
    ]
    
    print(f"Submitting data for {vehicle_id}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"Success: {vehicle_id} submitted. Response: {result.stdout}")
        else:
            print(f"Error submitting {vehicle_id}: {result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"Error: Submission for {vehicle_id} timed out.")
    except Exception as e:
        print(f"Error submitting {vehicle_id}: {str(e)}")

print("Finished submitting vehicle data.")
