#!/bin/bash
set -o pipefail

PACTNAME=$1
PROVIDERVERSION=$2
SERVICE=$3
TEST=$4

echo "Run pytest from SDK"
pytest tests/consumer/test_ads_consumer.py::$TEST --publish-pact $PACTNAME

echo "Run test from SSP"
cd ../provider/
pytest tests/provider/test_ads_provider.py --publish-pact $PACTNAME

echo "Validating against Pact Broker"
pact-verifier \
  --provider-base-url=http://apiqa.vungle.com \
  --provider-app-version $PROVIDERVERSION \
  --pact-url="http://127.0.0.1/pacts/provider/"$SERVICE"Service/consumer/SDK/latest" \
  --pact-broker-username pactbroker \
  --pact-broker-password pactbroker \
  --publish-verification-results \
