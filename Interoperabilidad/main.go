/*
Copyright Cristian Valencia All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

		 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"bytes"
	"fmt"
	"strconv"
	"unicode"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
	"github.com/montanaflynn/stats"
)

var wd float64 = 0.0
var wd2 float64 = 0.0
var coffeeType string = ""

// PlatformChaincode BlockChain Traceability Network Chaincode implementation
type PlatformChaincode struct {
}

// Init Chaincode initialization
func (t *PlatformChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("Init method gets called")
	var A, T string        // Entities
	var Aval, Tval float64 // Asset holdings
	var wngt, wng string   //warning variable
	var err error

	_, args := stub.GetFunctionAndParameters()
	if len(args) != 0 {
		return shim.Error("Incorrect number of arguments. Expecting name of the entity to query")
	}

	//coffeeType = args[0]

	A = "IPSID"
	Aval = 15.0
	err = stub.PutState(A, []byte(strconv.FormatFloat(Aval, 'E', -1, 64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	A = "IPSNAME"
	Aval = 55.0
	err = stub.PutState(A, []byte(strconv.FormatFloat(Aval, 'E', -1, 64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)
}

// Invoke all methods
func (t *PlatformChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("Invoke method gets called")
	function, args := stub.GetFunctionAndParameters()
	if function == "invoke" {
		// Make comparisons on the accelerometer values
		return t.invoke(stub, args)
	} else if function == "query" {
		// the old "Query" is now implemtned in invoke
		return t.query(stub, args)
	} else if function == "history" {
		// Query the history of modifications on an entity
		return t.queryhistory(stub, args)
	}

	return shim.Error("Invalid invoke function name. Expecting \"invoke\" \"delete\" \"query\"")
}

// Transaction - Agregar condicional para revisar si hay texto en el numero
func (t *PlatformChaincode) invoke(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	fmt.Println("invoke method gets called")
	var A, S string  // Entities
	var Anew float64 // Difference value
	var err error
	var wngt string   //warning variable
	var reliat string //reliability variable
	var letter bool

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	A = args[0]
	S = args[1]

	letter = false
	for _, r := range S {
		if unicode.IsDigit(r) || string(r) == "." || string(r) == "," {
			letter = false
		} else {
			letter = true
			break
		}
	}

	if !letter {
		Anew, err = strconv.ParseFloat(S, 64)
	} else {
		wd = wd + 1.0
		Avalbytes, _ := stub.GetState(A)
		Anew, err = strconv.ParseFloat(string(Avalbytes), 64)
		wngt = A + "_errors"
		err = stub.PutState(wngt, []byte(S))
		if err != nil {
			return shim.Error(err.Error())
		}
	}

	// Write the state to the ledger
	err = stub.PutState(A, []byte(strconv.FormatFloat(Anew, 'E', -1, 64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)
}

// query callback representing the query of a chaincode
func (t *PlatformChaincode) query(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	fmt.Println("query method gets called")
	var A string // Entities
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the entity to query")
	}

	A = args[0]

	// Get the state from the ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	if Avalbytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	jsonResp := "{\"Name\":\"" + A + "\",\"Amount\":\"" + string(Avalbytes) + "\"}"
	fmt.Printf("Query Response:%s\n", jsonResp)
	return shim.Success(Avalbytes)
}

// query callback representing the query history of a chaincode entity
func (t *PlatformChaincode) queryhistory(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	fmt.Println("query method gets called")
	var A string // Entities
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to query")
	}

	A = args[0]

	// Get the history of states from the ledger
	historyIter, err := stub.GetHistoryForKey(A)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get history state for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	// buffer is a JSON array containing historic values for the number
	var buffer bytes.Buffer
	buffer.WriteString("[")

	bArrayMemberAlreadyWritten := false
	for historyIter.HasNext() {
		response, err := historyIter.Next()
		if err != nil {
			return shim.Error(err.Error())
		}
		// Add a comma before array members, suppress it for the first array member
		if bArrayMemberAlreadyWritten == true {
			buffer.WriteString(",")
		}
		//buffer.WriteString("{\"TxId\":")
		//buffer.WriteString("\"")
		//buffer.WriteString(response.TxId)
		//buffer.WriteString("\"")

		buffer.WriteString("\"Value\":")
		// if it was a delete operation on given key, then we need to set the
		//corresponding value null. Else, we will write the response.Value
		//as-is (as the Value itself a JSON marble)
		if response.IsDelete {
			buffer.WriteString("null")
		} else {
			buffer.WriteString(string(response.Value))
		}

		buffer.WriteString("}")
		bArrayMemberAlreadyWritten = true
	}
	if !bArrayMemberAlreadyWritten {
		buffer.WriteString("No record found")
	}
	buffer.WriteString("]")

	fmt.Printf("- getAllTransactionForNumber returning:\n%s\n", buffer.String())

	return shim.Success(buffer.Bytes())
}

func main() {
	err := shim.Start(new(PlatformChaincode))
	if err != nil {
		fmt.Printf("Error starting platform chaincode: %s", err)
	}
}
