# query_vehicle_data.py
import subprocess
import os
import json

# Set environment variables for Org1
os.environ['CORE_PEER_LOCALMSPID'] = "Org1MSP"
os.environ['CORE_PEER_TLS_ENABLED'] = "true"
os.environ['CORE_PEER_TLS_ROOTCERT_FILE'] = os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
os.environ['CORE_PEER_MSPCONFIGPATH'] = os.path.join(os.getcwd(), "../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp")
os.environ['CORE_PEER_ADDRESS'] = "localhost:7051"

# Query all vehicles
cmd = [
    "peer", "chaincode", "query",
    "-C", "vehiclechannel",
    "-n", "vehiclecc",
    "-c", '{"function":"QueryAllVehicles","Args":[]}'
]

print("Executing query...")
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        if result.stdout.strip():
            try:
                result_data = json.loads(result.stdout)
                print("Query Result:", json.dumps(result_data, indent=2))
                print(f"Found {len(result_data)} vehicles:")
                for vehicle in result_data:
                    print(f"VehicleID: {vehicle['VehicleID']}, Records: {len(vehicle['Records'])}")
            except json.JSONDecodeError:
                print("Error: Query result is not valid JSON:", result.stdout)
        else:
            print("Query Result: No data found in the ledger.")
    else:
        print("Query Failed with Error:", result.stderr)
except subprocess.TimeoutExpired:
    print("Error: Query timed out.")
except Exception as e:
    print(f"Error executing query: {str(e)}")
