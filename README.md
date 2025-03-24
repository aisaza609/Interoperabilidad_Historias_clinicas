# Descripción del Proyecto

En Colombia, el sistema de salud enfrenta desafíos significativos en la continuidad de la atención médica, especialmente en zonas rurales donde la infraestructura y el personal son limitados. Los pacientes que requieren atención especializada suelen ser trasladados a hospitales de mayor nivel, ubicados en zonas urbanas, lo que incrementa los tiempos de espera y pone en riesgo su salud debido a la falta de interoperabilidad en la información clínica entre instituciones.

Nuestro proyecto propone una solución basada en tecnología blockchain para mejorar la interoperabilidad de Historias Clínicas Electrónicas (HCE) entre hospitales y clínicas en Colombia. Con esta red blockchain, se garantiza que la historia clínica de cada paciente esté disponible en tiempo real, accesible de forma segura y sin duplicación, independientemente de la ubicación geográfica de las instituciones de salud. La solución incluye un sistema de recomendación que, a partir del análisis de datos, sugiere el hospital más adecuado según el estado de salud del paciente, su EPS y el servicio hospitalario que requiere, asegurando una atención continua y de calidad.

Esta plataforma no solo optimiza los traslados y la asignación de recursos médicos, sino que también reduce errores y mejora la seguridad en el manejo de información clínica, ofreciendo una solución escalable y adaptable a las necesidades del sistema de salud colombiano.

# Arquitectura de la Solución

La solución propuesta se basa en una red **blockchain** que permite la interoperabilidad entre diferentes hospitales y clínicas en Colombia, asegurando que la información clínica de los pacientes esté disponible en tiempo real y de manera segura. Esta red blockchain está diseñada para almacenar y compartir las Historias Clínicas Electrónicas (HCE) de los pacientes entre instituciones de salud de distintos niveles de atención.

Para validar la funcionalidad y efectividad de la solución, se ha implementado una **simulación** utilizando datos de **3 hospitales** con diferentes niveles de atención. La arquitectura de la solución incluye los siguientes componentes clave:

1. **Red Blockchain para Interoperabilidad**:
   - **Propósito**: Facilitar el intercambio de HCE entre hospitales y clínicas de forma segura y descentralizada.
   - **Funcionamiento**: Cada registro de paciente en la red es único y no puede ser alterado, garantizando la integridad de la información.
   - **Protocolos de Consenso**: La red utiliza protocolos de consenso para validar la autenticidad de los datos, asegurando que solo entidades autorizadas (IPS, EPS y otros actores del sistema de salud) puedan acceder y actualizar la información.

2. **Simulación de los 3 Hospitales**:
   - **Distribución por Niveles de Atención**: Los hospitales simulados representan distintos niveles de atención (niveles 1, 2 y 3), lo cual permite observar el flujo y manejo de pacientes de acuerdo con la gravedad de sus condiciones y la disponibilidad de recursos.
   - **Datos Utilizados**: La simulación emplea datos reales obtenidos de fuentes de datos abiertos y del **Registro Especial de Prestadores de Servicios de Salud (REPS)** de MinSalud, lo cual permite asignar correctamente el nivel hospitalario y evaluar la interoperabilidad de la red blockchain.
   - **Interacción en la Red**: A través de la simulación, los hospitales pueden intercambiar información sobre el estado de salud del paciente y su historia clínica. Si un hospital de nivel 1 recibe a un paciente en estado crítico, el sistema de recomendación sugiere el traslado a un hospital de mayor nivel que cuente con los recursos y servicios necesarios.

3. **Sistema de Recomendación en Tiempo Real**:
   - **Propósito**: Evaluar en tiempo real el estado de cada paciente y sugerir el hospital más adecuado para su traslado, tomando en cuenta factores como su estado de salud, el tipo de atención requerida y su EPS.
   - **Métodos y Métricas**: Basado en reglas preestablecidas y datos históricos, el sistema de recomendación calcula el nivel de atención necesario y selecciona el hospital que cumple con esos requisitos, priorizando aquellos en estado crítico. Las métricas clave incluyen precisión en la asignación del hospital adecuado y tiempos estimados de traslado, mejorando la respuesta en la atención médica.
   - **Impacto**: Este sistema optimiza los traslados y reduce los tiempos de espera, asegurando que cada paciente reciba la atención correcta en el hospital que cuenta con los recursos necesarios para su condición, mejorando así la continuidad y calidad de la atención en el sistema de salud.

4. **Módulo de Seguridad y Autenticación**:
   - **Acceso Controlado**: La red blockchain emplea un sistema de autenticación robusto, donde solo instituciones verificadas pueden acceder a las HCE, con información sacada de datos de MinSalud y disponible en el archivo `Datasets externos/Prestadores_Reps.csv` en GitHub.
   - **Protección de Datos**: La blockchain protege los datos del paciente contra modificaciones no autorizadas, reduciendo el riesgo de pérdida de información durante los traslados.

# Dataset Usados y Preparacion de los Datos

## Datasets Utilizados

A continuación, se detallan los datasets utilizados hasta el momento en este proyecto:

- [Morbilidad por EAPB 2021 - ESE Hospital San Rafael Itagüí, Antioquia](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Morbilidad-por-EAPB-2021/echz-i3bm/data_preview): Este dataset corresponde a los datos del Hospital San Rafael en Itagüí, Antioquia, del año 2021. Fue empleado para el análisis descriptivo de traslados en el archivo [`Analisis_Descriptivo_de_Traslados_en_los_Hospitales.ipynb`](Analisis_Descriptivo_de_Traslados_en_los_Hospitales.ipynb).

- [Remisiones de pacientes - Empresa Social del Estado Pasto Salud](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Remisiones-de-pacientes/emmz-uf6m/about_data): Este dataset pertenece a la Empresa Social del Estado Pasto Salud y también se usó en el análisis descriptivo de traslados.

### Normalización de los Datasets

Para garantizar una interoperabilidad eficiente y homogénea, se realizó un proceso de normalización en los datasets de cada hospital, asegurando que todos contaran con las mismas columnas. También se asignaron servicios específicos a cada caso, y dependiendo del nivel de atención, se verificó si había necesidad de traslado según el código diagnóstico.

Se priorizó la normalización de tres hospitales, seleccionados para representar cada nivel de atención. Los datasets específicos y el proceso de normalización aplicado en cada uno están descritos a continuación:

1. **Hospital Departamental San Antonio, Pitalito** (Nivel 2):
   - Dataset: [Morbilidad urgencias - Hospital Pitalito](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Morbilidad-urgencias-Hospital-Pitalito/ekrt-9aay/about_data)
   - Proceso de normalización: Disponible en [`Normalizacion_Dataset_pitalito__Hospitalarios.ipynb`](Normalizacion_Dataset_pitalito__Hospitalarios.ipynb).

2. **Empresa Social del Estado Pasto Salud** (Nivel 1):
   - Dataset resultante del análisis descriptivo: [`Dataset de datos abiertos/Hospital_Pasto_v1.xlsx`](Dataset%20de%20datos%20abiertos/Hospital_Pasto_v1.xlsx).
   - Proceso de normalización: Disponible en [`Normalizacion_Dataset_Pasto.ipynb`](Normalizacion_Dataset_Pasto.ipynb).

3. **Hospital Universitario Hernando Moncaleano Perdomo, Neiva** (Nivel 3):
   - Dataset: [Perfil de morbilidad](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Perfil-de-morbilidad/5c4n-qdbv/about_data)
   - Proceso de normalización: Disponible en [`Normalizacion_Dataset_Neiva.ipynb`](Normalizacion_Dataset_Neiva.ipynb).

### Acceso a los Datasets en Google Drive

Los datasets cargados y utilizados en el código están disponibles en la siguiente carpeta de Google Drive: [Carpeta de Datasets en Drive](https://drive.google.com/drive/folders/1g_g7nNmjAK4MWKhcBxZKm9-tgX4TQUld?usp=drive_link).
**AVANCE**: La información ha sido normalizada para su envío en la blockchain, facilitando la interoperabilidad. Se evaluó el nivel hospitalario, el servicio requerido y la necesidad de traslado, asegurando la adecuada referencia de pacientes en la red. los demas datasets no han sido normalizados debido a que Hyperleger Fabric debe garantizar la interoperabilidad,sin importar el formato de los datos, asi podemos observar los dos escenarios cuando los formatos de dos instituciones no son compatibles.

# Red blockchain
En el archivo interoperabilidad.zip esta la red blockchain montada para ejecutarla se deben realizar los siguientes pasos:
1. Descargar Docker desktop cualquier version
2. Descargar go 1.21.6 https://go.dev/dl/
3. Una vez instalados los servicios vamos a la carpeta, verificamos que no este la carpeta vars, si esta, la eliminamos. En la carpeta go donde esta el contrato inteligente verificamos que solo se encuentre el archivo de origen go si hay mas debemos eliminarlos. Estos archivos se borran ya que son del anterior despliegue y genera conflictos al mantenerlos.
4. El primer paso a seguir para desplegar la red en nustro ordenador es: en el terminal con la carpeta donde esta el contrato inteligente, por ejemplo: "C:\Users\Asus\Documents\GitHub\Datos_a_la_U_grupo_2\Interoperabilidad\Hyperledger\ChainCodes\Healthcare\go"
corremos los siguientes codigos para la implementacion del contrato inteligente:
         go mod init main.go
         go mod tiny
         go build main.go
5. Despues de esto corremos el archivo main.py y nos pedira importar diferentes librerias, una vez hecho esto en esa carpeta corremos el codigo ./minifab cleanup para hacer una limpieza una vez hecho esto procederemos a correr el archivo main.py y demorara unos minutos en desplegar la red.
6. Finalmente, una vez la red desplegada corremos el archivo senttransaction donde nos aparecera una "Guia" de como ejecutar las transacciones, un ejemplo de resgitro de paciente es el siguiente: python SentTransaction.py -rp 15155121 danilo 789, "python SentTransaction.py" se mantiene lo unico que cambia es el -c, -sispro, etc, dependiendo de lo que queramos hacer.

# Minifabric, instrucciones de Instalación y Ejecución.
La red fue montada en una máquina virtual utilizando Ubuntu 24.04.1 LTS como sistema operativo.En este proyecto, Docker se utiliza para crear y gestionar un entorno de contenedores que permita desplegar la red blockchain de forma aislada y replicable. Esto asegura que todos los componentes necesarios se ejecuten en un entorno controlado, independientemente de las configuraciones individuales del sistema anfitrión. A continuación se detallan los pasos para replicar el entorno de instalación en este sistema linux.
1. Ingrese al terminal del ordenador e ingrese los siguientes comandos:
   
-**1.1 Actualizar los paquetes del sistema:**
   <pre>
   apt update
   apt upgrade -y
   </pre>
-**1.2 Instalar paquetes necesarios:** Docker requiere algunas dependencias adicionales, como apt-transport-https, ca-certificates, y curl. Estas permiten descargar paquetes de repositorios seguros y gestionar conexiones HTTPS:
   <pre>
   apt install apt-transport-https ca-certificates curl software-properties-common -y
   </pre>
-**1.3 Agregar la clave GPG de Docker:** Esto permite que el sistema confíe en los paquetes de Docker que se van a instalar.
  <pre>curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 
  </pre>
-**1.4 Agregar el repositorio de Docker:** Este paso configura el repositorio de Docker para que se pueda instalar la versión más reciente.
   <pre>
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   </pre>
   -**1.5 Actualizar los paquetes nuevamente:** Después de agregar el repositorio, actualiza la lista de paquetes.
   <pre>
   apt update
   </pre>
   -**1.6 Instalar Docker:** Ahora, instala Docker y Docker Compose para gestionar los contenedores en los que se ejecutará la red blockchain.
   <pre>
   apt install docker-ce docker-ce-cli containerd.io -y```
   </pre>
   **1.7 Verificar la instalación de Docker:** Para comprobar que Docker se instaló correctamente, ejecuta:
   <pre>
   docker --version
   </pre>

   -**1.8 (opcional) Permitir que Docker se ejecute sin sudo:** Este paso permite ejecutar Docker sin usar sudo cada vez. Para hacerlo, agrega tu usuario al grupo de Docker:
   <pre>
   usermod -aG docker $USER```
   </pre>
##NOTA: Después de ejecutar este comando, cierra sesión o reinicia la máquina para que el cambio surta efecto.

Instalacion de Docker Compose 
   -**1.9 Descargar Docker Compose:** Permite gestionar y coordinar múltiples contenedores Docker, facilitando el despliegue de entornos complejos como nuestra red blockchain en un solo paso.
<pre>
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
</pre>

   -**1.10 Dar permisos de ejecución:** Permite que Docker Compose se ejecute como programa.
<pre>   
sudo chmod +x /usr/local/bin/docker-compose
</pre>
   
   -**1.11 Verificacion final:** Para asegurarte de que Docker y Docker Compose funcionan correctamente:
   <pre>
   docker --version
   docker-compose --version
   </pre>

2. Una vez verificados los anteriores requisitos detallaremos la creacion de una red Hyperledger Fabric (HLF) usando Minifabric. La utilizaremos para construir una red HLF con dos canales de aplicación, tres organizaciones y dos nodos ordenadores. Se emplea Docker y Docker Compose para gestionar los contenedores de HLF y sus componentes.

   -**2.1 Definiremos las 3 redes de la siguiente manera:** nuevamente abriremos o en el mismo terminal que tenemos abierto usaremos 3 directorios org1, org2 y org3.Una red se define usando el spec.yamlarchivo . Es muy recomendable descargar el archivo de [plantilla del repositorio de Github de Minifabric](https://github.com/hyperledger-labs/minifabric/blob/main/spec.yaml) y editarlo de la siguiente manera:
   **cat ./org1/spec.yaml**
<pre>
fabric:
  cas:
  - "ca1.org1.example.com"
  peers: 
  - "peer1.org1.example.com"
  - "peer2.org1.example.com"
  orderers:
  - "orderer1.example.com"
  settings:
    ca:
      FABRIC_LOGGING_SPEC: DEBUG
    peer:
      FABRIC_LOGGING_SPEC: DEBUG
    orderer:
      FABRIC_LOGGING_SPEC: DEBUG
  netname: "network1"
</pre>

  
   **cat ./org2/spec.yaml**
   <pre>
fabric:
  cas:
  - "ca1.org2.example.com"
  peers: 
  - "peer1.org2.example.com"
  - "peer2.org2.example.com"
  settings:
    ca:
      FABRIC_LOGGING_SPEC: DEBUG
    peer:
      FABRIC_LOGGING_SPEC: DEBUG
  netname: "network2"
  </pre>
   **cat ./org3/spec.yaml**
   <pre>
fabric:
  cas:
  - "ca1.org3.example.com"
  peers: 
  - "peer1.org3.example.com"
  - "peer2.org3.example.com"
  orderers:
  - "orderer2.example.com"
  settings:
    ca:
      FABRIC_LOGGING_SPEC: DEBUG
    peer:
      FABRIC_LOGGING_SPEC: DEBUG
    orderer:
      FABRIC_LOGGING_SPEC: DEBUG
  netname: "network3"
  </pre>
Hay que asegurarse de configurar 3 nombres de red diferentes
**Lanzamiento de la red 1 y 2**

Desde el directorio: ```cd org1```
<pre>
minifab netup -e 7100 -o org1.example.com -i 2.2 -l nodo -s Couchdb
minifab crear,unir -c channell1
minifab install, approve, commit -n simple -l nodo -v 1.0 -p ' "init", "a", "200", "b", "300" '
</pre>
Desde el directorio: ``cd ../org3``
<pre>
minifab netup -e 7300 -o org3.example.com -i 2.2 -l nodo -s couchdb
minifab create,join -c channel2
minifab install,approve,commit -n simple -l nodo -v 1.0 -p '"init", "a", "200", "b", "300"'
</pre>
**Red de lanzamiento 2**

Desde el directorio ``cd ../org2`` 
<pre>
minifab netup -e 7200 -o org2.example.com -i 2.2 -l nodo -s couchdb
</pre>
**Unirse a Network2 a los canales**

Desde el directorio ``cd ../org1`` 
<pre>
cp ../org2/vars/JoinRequest_org2-example-com.json ./vars/NewOrgJoinRequest.json
minifab orgjoin,profilegen
</pre>

Desde el directorio ``cd ../org3`` 
<pre>
cp ../org2/vars/JoinRequest_org2-example-com.json ./vars/NewOrgJoinRequest.json``
minifab orgjoin,profilegen
</pre>
**Unir pares de Org2 a los canales**

Desde el directorio``cd ../org2``
<pre>
cp ../org1/vars/profiles/endpoints.yaml vars
minifab nodeimport,join -c channel1
</pre>
<pre>
cp ../org3/vars/profiles/endpoints.yaml vars
minifab nodeimport,join -c channel2
</pre>
**Instalar Chaincode en Org2**
<pre>
minifab install,approve -n simple -v 1.0 -p ' "init", "a", "200", "b", "300" ' -c channel1``
</pre>
Desde el directorio ``cd ../org1``
<pre>
   minifab approve,discover,commit
</pre>
Desde el diretorio ``cd ../org3``
<pre>
   minifab approve,discover,commit
</pre>

**Resultado esperado**
**Si no se ve el resultado se debe lanzar de nuevo la red.** 
<pre>
network3
ca1.org3.example.com
orderer2.example.com
peer2.org3.example.com
peer1.org3.example.com
peer2.org3.example.com.couchdb
peer1.org3.example.com.couchdb
network2
ca1.org2.example.com
peer2.org2.example.com
peer1.org2.example.com
peer2.org2.example.com.couchdb
peer1.org2.example.com.couchdb
network1
ca1.org1.example.com
orderer1.example.com
peer2.org1.example.com
peer1.org1.example.com
peer2.org1.example.com.couchdb
peer1.org1.example.com.couchdb
</pre>






