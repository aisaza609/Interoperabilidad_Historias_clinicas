#!/bin/bash
# Script to discover endorsers and channel config
cd /vars

export PEER_TLS_ROOTCERT_FILE=/vars/keyfiles/peerOrganizations/org0.example.com/users/Admin@org0.example.com/tls/ca.crt
export ADMINPRIVATEKEY=/vars/keyfiles/peerOrganizations/org0.example.com/users/Admin@org0.example.com/msp/keystore/priv_sk
export ADMINCERT=/vars/keyfiles/peerOrganizations/org0.example.com/users/Admin@org0.example.com/msp/signcerts/Admin@org0.example.com-cert.pem

discover endorsers --peerTLSCA $PEER_TLS_ROOTCERT_FILE \
  --userKey $ADMINPRIVATEKEY \
  --userCert $ADMINCERT \
  --MSP org0-example-com --channel testchannel \
  --server 172.20.10.9:7002 \
  --chaincode Healthcare | jq '.[0]' | \
  jq 'del(.. | .Identity?)' | jq 'del(.. | .LedgerHeight?)' \
  > /vars/discover/testchannel_Healthcare_endorsers.json

discover config --peerTLSCA $PEER_TLS_ROOTCERT_FILE \
  --userKey $ADMINPRIVATEKEY \
  --userCert $ADMINCERT \
  --MSP org0-example-com --channel testchannel \
  --server 172.20.10.9:7002 > /vars/discover/testchannel_config.json
