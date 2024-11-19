#!/bin/bash
# Script to instantiate chaincode
cp $FABRIC_CFG_PATH/core.yaml /vars/core.yaml
cd /vars
export FABRIC_CFG_PATH=/vars

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_ID=cli
export CORE_PEER_ADDRESS=192.168.0.10:7003
export CORE_PEER_TLS_ROOTCERT_FILE=/vars/keyfiles/peerOrganizations/org0.example.com/peers/peer2.org0.example.com/tls/ca.crt
export CORE_PEER_LOCALMSPID=org0-example-com
export CORE_PEER_MSPCONFIGPATH=/vars/keyfiles/peerOrganizations/org0.example.com/users/Admin@org0.example.com/msp
export ORDERER_ADDRESS=192.168.0.10:7007
export ORDERER_TLS_CA=/vars/keyfiles/ordererOrganizations/example.com/orderers/orderer2.example.com/tls/ca.crt

# 1. Fetch the channel configuration
peer channel fetch config config_block.pb -o $ORDERER_ADDRESS \
  --cafile $ORDERER_TLS_CA --tls -c testchannel

# 2. Translate the configuration into json format
configtxlator proto_decode --input config_block.pb --type common.Block \
  | jq .data.data[0].payload.data.config > testchannel_current_config.json

# 3. Translate the current config in json format to protobuf format
configtxlator proto_encode --input testchannel_current_config.json \
  --type common.Config --output config.pb

# 4. Translate the desired config in json format to protobuf format
configtxlator proto_encode --input testchannel_config.json \
  --type common.Config --output modified_config.pb

# 5. Calculate the delta of the current config and desired config
configtxlator compute_update --channel_id testchannel \
  --original config.pb --updated modified_config.pb \
  --output testchannel_update.pb

# 6. Decode the delta of the config to json format
configtxlator proto_decode --input testchannel_update.pb \
  --type common.ConfigUpdate | jq . > testchannel_update.json

# 7. Now wrap of the delta config to fabric envelop block
echo '{"payload":{"header":{"channel_header":{"channel_id":"testchannel", "type":2}},"data":{"config_update":'$(cat testchannel_update.json)'}}}' | jq . > testchannel_update_envelope.json

# 8. Encode the json format into protobuf format
configtxlator proto_encode --input testchannel_update_envelope.json \
  --type common.Envelope --output testchannel_update_envelope.pb

# 9. Need to sign channel update envelop by each org admin
export CORE_PEER_LOCALMSPID=org0-example-com
export CORE_PEER_TLS_ROOTCERT_FILE=/vars/keyfiles/peerOrganizations/org0.example.com/peers/peer2.org0.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/vars/keyfiles/peerOrganizations/org0.example.com/users/Admin@org0.example.com/msp
export CORE_PEER_ADDRESS=192.168.0.10:7003

peer channel signconfigtx -f testchannel_update_envelope.pb

export CORE_PEER_LOCALMSPID=org1-example-com
export CORE_PEER_TLS_ROOTCERT_FILE=/vars/keyfiles/peerOrganizations/org1.example.com/peers/peer1.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/vars/keyfiles/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=192.168.0.10:7004

peer channel signconfigtx -f testchannel_update_envelope.pb

