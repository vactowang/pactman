#!/bin/bash
set -o pipefail

VERSION=$1
SERVICE=$2

echo "Validating against Pact Broker"
pact-verifier \
  --provider-base-url=http://apiqa.vungle.com \
  --provider-app-version $VERSION \
  --pact-url="http://127.0.0.1/pacts/provider/"$SERVICE"Service/consumer/SDK/latest" \
  --pact-broker-username pactbroker \
  --pact-broker-password pactbroker \
  --publish-verification-results \
