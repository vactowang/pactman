#!/bin/bash
set -o pipefail

# Now run the tests
pytest tests --run-broker True --publish-pact 1