"""pact test for the real Jaeger service provider"""

import logging

import pytest

from pact import Verifier

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# pact broker
PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "pactbroker"
PACT_BROKER_PASSWORD = "pactbroker"


PROVIDER_HOST = "apiqa.vungle.com"
PROVIDER_PORT = 80
PROVIDER_URL = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"


@pytest.fixture
def broker_opts():
    return {
        "broker_username": PACT_BROKER_USERNAME,
        "broker_password": PACT_BROKER_PASSWORD,
        "broker_url": PACT_BROKER_URL,
        "publish_version": "v1.216.0",
        "publish_verification_results": True,
    }


def test_jaeger_service_provider_against_broker(broker_opts):
    verifier = Verifier(provider="JaegerService", provider_base_url=PROVIDER_URL)

    success, logs = verifier.verify_with_broker(
        **broker_opts,
        verbose=True,
        enable_pending=False,
    )

    assert success == 0
