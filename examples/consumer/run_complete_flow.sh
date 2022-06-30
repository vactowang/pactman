#!/bin/bash
set -o pipefail

CONSUMER_VERSION=$1
PROVIDER_VERSION=$2
PROVIDER_NAME=$3
TEST=$4

echo "Run pytest from SDK"
pytest tests/consumer/test_ads_consumer.py::$TEST --publish-pact $CONSUMER_VERSION

echo "Run test from SSP"
cd ../provider/
pytest tests/provider/test_ads_provider.py --publish-pact $CONSUMER_VERSION

echo "Validating against Pact Broker"
pact-verifier \
  --provider-base-url=https://adex.ads-qa.vungle.com \
  --provider-app-version $PROVIDER_VERSION \
  --pact-url="http://127.0.0.1/pacts/provider/"$PROVIDER_NAME"Service/consumer/SDK/latest" \
  --pact-broker-username pactbroker \
  --pact-broker-password pactbroker \
  --publish-verification-results \
