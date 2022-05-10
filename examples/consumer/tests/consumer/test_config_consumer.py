"""pact test for the Bastion service client"""

import atexit
import logging
import os

import pytest

from examples.consumer.src.consumer import ConfigConsumer
from examples.common.test_data.headers import *
from examples.common.test_data.request_payload import *
from examples.common.test_data.expected_response_payload import *
from pact import Consumer, Like, Provider

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# If publishing the Pact(s), they will be submitted to the Pact Broker here.
# For the purposes of this example, the broker is started up as a fixture defined
# in conftest.py. For normal usage this would be self-hosted or using Pactflow.

# pact broker
PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "pactbroker"
PACT_BROKER_PASSWORD = "pactbroker"

# pactflow
# PACT_BROKER_URL = "https://ssptest.pactflow.io/"
# PACT_BROKER_TOKEN = "_cmJAJb1Zos1DkcTUivTMw"

# Define where to run the mock server, for the consumer to connect to. These
# are the defaults so may be omitted
PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234

# Where to output the JSON Pact files created by any tests
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def consumer() -> ConfigConsumer:
    return ConfigConsumer("http://{host}:{port}".format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT))


@pytest.fixture(scope="session")
def pact(request):
    """Setup a Pact Consumer, which provides the Provider mock service. This
    will generate and optionally publish Pacts to the Pact Broker"""

    # When publishing a Pact to the Pact Broker, a version number of the Consumer
    # is required, to be able to construct the compatability matrix between the
    # Consumer versions and Provider versions
    version = request.config.getoption("--publish-pact")
    publish = True if version else False

    pact = Consumer("SDK", version=version).has_pact_with(
        Provider("BastionService"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
        publish_to_broker=publish,
        broker_base_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
        # broker_token=PACT_BROKER_TOKEN,
    )

    pact.start_service()

    # Make sure the Pact mocked provider is stopped when we finish, otherwise
    # port 1234 may become blocked
    atexit.register(pact.stop_service)

    yield pact

    # This will stop the Pact mock server, and if publish is True, submit Pacts
    # to the Pact Broker
    pact.stop_service()

    # Given we have cleanly stopped the service, we do not want to re-submit the
    # Pacts to the Pact Broker again atexit, since the Broker may no longer be
    # available if it has been started using the --run-broker option, as it will
    # have been torn down at that point
    pact.publish_to_broker = False


def test_get_config_with_valid_pub_app(pact, consumer):
    # Define the Matcher; the expected structure and content of the response
    expected = expected_served_config_response()
    test_pub_app = '59786bc2a43b3a08620026b4'

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a body which is
    # "Like" the structure defined above. This means the mock provider will
    # return the EXACT content where defined, e.g. UserA for name, and SOME
    # appropriate content e.g. for ip_address.
    (
        pact.given("Test to get the config with a valid pub app")
            .upon_receiving("get pub config from the Bastion service")
            .with_request("post", "/api/v5/config", body=config_v5_ios(test_pub_app),
                          headers=platform_headers())
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
        config = consumer.get_config(test_pub_app)

        # In this case the mock Provider will have returned a valid response
        assert config.ads_endpoint == "https://apiqa.vungle.com/api/v5/ads"
        assert config.placement_refer_id == 'DEFAULT02024'

        # Make sure that all interactions defined occurred
        pact.verify()


def test_get_config_with_non_existing_pub_app(pact, consumer):
    test_pub_app = '123456'

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a 404
    (
        pact.given("Test to get the config with a non-existing pub app")
            .upon_receiving("get pub config from the Bastion service")
            .with_request("post", "/api/v5/config", body=config_v5_ios(test_pub_app),
                          headers=platform_headers())
            .will_respond_with(400)
    )

    with pact:
        # Perform the actual request
        config = consumer.get_config(test_pub_app)

        # In this case, the mock Provider will have returned a 404 so the
        # consumer will have returned None
        assert config is None

        # Make sure that all interactions defined occurred
        pact.verify()
