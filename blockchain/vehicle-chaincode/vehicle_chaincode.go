package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

type VehicleRecord struct {
	Speed      float64 `json:"Speed"`
	PositionX  float64 `json:"Position_X"`
	PositionY  float64 `json:"Position_Y"`
	Cluster    int     `json:"Cluster"`
}

type Vehicle struct {
	VehicleID string          `json:"VehicleID"`
	Records   []VehicleRecord `json:"Records"`
}

// InitLedger initializes the ledger with sample data
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	return nil
}

// SubmitVehicleData submits vehicle data to the ledger
func (s *SmartContract) SubmitVehicleData(ctx contractapi.TransactionContextInterface, vehicleID string, recordsJSON string) error {
	var records []VehicleRecord
	err := json.Unmarshal([]byte(recordsJSON), &records)
	if err != nil {
		return fmt.Errorf("failed to unmarshal records: %v", err)
	}

	vehicle := Vehicle{
		VehicleID: vehicleID,
		Records:   records,
	}

	vehicleJSON, err := json.Marshal(vehicle)
	if err != nil {
		return fmt.Errorf("failed to marshal vehicle: %v", err)
	}

	return ctx.GetStub().PutState(vehicleID, vehicleJSON)
}

// QueryVehicle retrieves vehicle data by ID
func (s *SmartContract) QueryVehicle(ctx contractapi.TransactionContextInterface, vehicleID string) (*Vehicle, error) {
	vehicleJSON, err := ctx.GetStub().GetState(vehicleID)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if vehicleJSON == nil {
		return nil, fmt.Errorf("vehicle %s does not exist", vehicleID)
	}

	var vehicle Vehicle
	err = json.Unmarshal(vehicleJSON, &vehicle)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal vehicle: %v", err)
	}

	return &vehicle, nil
}

// QueryAllVehicles retrieves all vehicle data
func (s *SmartContract) QueryAllVehicles(ctx contractapi.TransactionContextInterface) ([]*Vehicle, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var vehicles []*Vehicle
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var vehicle Vehicle
		err = json.Unmarshal(queryResponse.Value, &vehicle)
		if err != nil {
			return nil, err
		}
		vehicles = append(vehicles, &vehicle)
	}

	return vehicles, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		fmt.Printf("Error creating vehicle chaincode: %v\n", err)
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting vehicle chaincode: %v\n", err)
	}
}
