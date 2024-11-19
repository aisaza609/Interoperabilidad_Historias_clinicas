package main

// Importamos los paquetes necesarios
import (
	"bytes"                            // Para manejar buffers de bytes
	"fmt"                              // Para imprimir mensajes en la consola
	"strconv"                          // Para convertir valores a diferentes tipos
	"github.com/hyperledger/fabric/core/chaincode/shim" // Interfaz shim para el chaincode
	pb "github.com/hyperledger/fabric/protos/peer"      // Protocolo peer para responder a las solicitudes
)

// Definimos la estructura principal del contrato inteligente
// Esta estructura se utiliza para agrupar los métodos que serán parte del contrato
type HealthcareChaincode struct{}

// Init se ejecuta una sola vez cuando el contrato se despliega en la red
// En este caso, solo imprimimos un mensaje para confirmar la inicialización
func (t *HealthcareChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("Inicializando el contrato de atención médica")
	// Retorna éxito, indicando que la inicialización fue exitosa
	return shim.Success(nil)
}

// Invoke es la función principal que maneja las solicitudes entrantes
// Según el nombre de la función solicitada, redirige a métodos específicos
func (t *HealthcareChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	// Obtenemos el nombre de la función y los argumentos de la solicitud
	function, args := stub.GetFunctionAndParameters()

	// Redirigimos la llamada a diferentes funciones según el nombre recibido
	switch function {
	case "registerIPS":
		return t.registerIPS(stub, args)
	case "registerPatient":
		return t.registerPatient(stub, args)
	case "queryPatient":
		return t.queryPatient(stub, args)
	case "updatePatient":
		return t.updatePatient(stub, args)
	case "getPatientHistory":
		return t.getPatientHistory(stub, args)
	default:
		return shim.Error("Función no reconocida")
	}
}

// Función principal que inicia el contrato inteligente en la red
func main() {
	// Iniciamos el contrato creando una nueva instancia de HealthcareChaincode
	err := shim.Start(new(HealthcareChaincode))
	if err != nil {
		// Si hay un error al iniciar, se imprime un mensaje de error
		fmt.Printf("Error al iniciar el contrato: %s", err)
	}
}

// registerIPS registra una nueva IPS en el ledger
func (t *HealthcareChaincode) registerIPS(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// Verificamos que se recibieron exactamente 2 argumentos: ID de la IPS y nombre
	if len(args) != 2 {
		return shim.Error("Número incorrecto de argumentos. Se requieren 2: ID de la IPS y nombre")
	}

	// Asignamos los argumentos a variables descriptivas
	ipsID := args[0]  // Primer argumento: ID de la IPS
	ipsName := args[1]  // Segundo argumento: Nombre de la IPS

	// Verificamos si la IPS ya está registrada
	ipsAsBytes, err := stub.GetState(ipsID)
	if err != nil {
		return shim.Error("Error al verificar el estado de la IPS: " + err.Error())
	}
	if ipsAsBytes != nil {
		return shim.Error("La IPS ya está registrada")
	}

	// Guardamos el nombre de la IPS asociado al ID
	err = stub.PutState(ipsID, []byte(ipsName))
	if err != nil {
		return shim.Error("Error al registrar la IPS: " + err.Error())
	}

	// Retornamos un mensaje de éxito si todo salió bien
	return shim.Success([]byte("IPS registrada exitosamente"))
}

// registerPatient registra un nuevo paciente en el ledger y lo asocia con una IPS
func (t *HealthcareChaincode) registerPatient(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// Verificamos que se recibieron 3 argumentos: ID del paciente, nombre y ID de la IPS
	if len(args) != 3 {
		return shim.Error("Número incorrecto de argumentos. Se requieren 3: ID del paciente, nombre y ID de la IPS")
	}

	// Asignamos los argumentos a variables descriptivas
	patientID := args[0]  // ID del paciente
	patientName := args[1]  // Nombre del paciente
	ipsID := args[2]  // ID de la IPS asociada

	// Verificamos si el paciente ya está registrado
	patientAsBytes, err := stub.GetState(patientID)
	if err != nil {
		return shim.Error("Error al verificar el estado del paciente: " + err.Error())
	}
	if patientAsBytes != nil {
		return shim.Error("El paciente ya está registrado")
	}

	// Verificamos que la IPS asociada exista
	ipsAsBytes, err := stub.GetState(ipsID)
	if err != nil {
		return shim.Error("Error al verificar el estado de la IPS: " + err.Error())
	}
	if ipsAsBytes == nil {
		return shim.Error("La IPS asociada no existe")
	}

	// Creamos un JSON para representar al paciente con sus datos
	patientData := fmt.Sprintf("{\"Nombre\":\"%s\", \"IPS\":\"%s\"}", patientName, ipsID)

	// Guardamos los datos del paciente en el ledger
	err = stub.PutState(patientID, []byte(patientData))
	if err != nil {
		return shim.Error("Error al registrar el paciente: " + err.Error())
	}

	// Retornamos un mensaje de éxito si todo salió bien
	return shim.Success([]byte("Paciente registrado exitosamente"))
}

// queryPatient consulta los datos de un paciente por su ID
func (t *HealthcareChaincode) queryPatient(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// Verificamos que se reciba 1 argumento: el ID del paciente
	if len(args) != 1 {
		return shim.Error("Número incorrecto de argumentos. Se requiere 1: ID del paciente")
	}

	patientID := args[0]  // ID del paciente

	// Obtenemos los datos del paciente desde el ledger
	patientAsBytes, err := stub.GetState(patientID)
	if err != nil {
		return shim.Error("Error al consultar el paciente: " + err.Error())
	}
	if patientAsBytes == nil {
		return shim.Error("El paciente no está registrado")
	}

	// Retornamos los datos del paciente
	return shim.Success(patientAsBytes)
}

// updatePatient actualiza los datos de un paciente existente en el ledger
func (t *HealthcareChaincode) updatePatient(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// Verificamos que se reciban 2 argumentos: ID del paciente y nuevos datos
	if len(args) != 2 {
		return shim.Error("Número incorrecto de argumentos. Se requieren 2: ID del paciente y nuevos datos")
	}

	patientID := args[0]         // ID del paciente
	newData := args[1]           // Nuevos datos en formato JSON o cadena de texto

	// Verificamos si el paciente ya está registrado
	patientAsBytes, err := stub.GetState(patientID)
	if err != nil {
		return shim.Error("Error al verificar el estado del paciente: " + err.Error())
	}
	if patientAsBytes == nil {
		return shim.Error("El paciente no está registrado")
	}

	// Actualizamos los datos del paciente en el ledger
	err = stub.PutState(patientID, []byte(newData))
	if err != nil {
		return shim.Error("Error al actualizar el paciente: " + err.Error())
	}

	// Retornamos un mensaje de éxito si todo salió bien
	return shim.Success([]byte("Datos del paciente actualizados exitosamente"))
}

// getPatientHistory obtiene el historial de cambios de un paciente
func (t *HealthcareChaincode) getPatientHistory(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// Verificamos que se reciba 1 argumento: ID del paciente
	if len(args) != 1 {
		return shim.Error("Número incorrecto de argumentos. Se requiere 1: ID del paciente")
	}

	patientID := args[0]  // ID del paciente

	// Obtenemos el historial de cambios de la clave del paciente
	resultsIterator, err := stub.GetHistoryForKey(patientID)
	if err != nil {
		return shim.Error("Error al obtener el historial del paciente: " + err.Error())
	}
	defer resultsIterator.Close()

	// Construimos el historial en un buffer de bytes
	var historyBuffer bytes.Buffer
	historyBuffer.WriteString("[")

	bArrayMemberAlreadyWritten := false
	for resultsIterator.HasNext() {
		response, err := resultsIterator.Next()
		if err != nil {
			return shim.Error("Error al leer el historial: " + err.Error())
		}

		// Agregamos una coma entre miembros del arreglo JSON
		if bArrayMemberAlreadyWritten == true {
			historyBuffer.WriteString(",")
		}
		historyBuffer.WriteString("{\"TxId\":\"")
		historyBuffer.WriteString(response.TxId)
		historyBuffer.WriteString("\", \"Value\":\"")
		historyBuffer.WriteString(string(response.Value))
		historyBuffer.WriteString("\"}")
		bArrayMemberAlreadyWritten = true
	}
	historyBuffer.WriteString("]")

	// Retornamos el historial de cambios como JSON
	return shim.Success(historyBuffer.Bytes())
}
