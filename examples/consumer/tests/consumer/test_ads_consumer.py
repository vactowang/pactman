"""pact test for the Bastion service client"""

import atexit
import logging
import os

import pytest

from examples.common.test_data.data import *
from examples.consumer.src.consumer import AdsConsumer
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
def consumer() -> AdsConsumer:
    return AdsConsumer("http://{host}:{port}".format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT))


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
        Provider("JaegerService"),
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


def test_request_ads_with_valid_pub_app_and_placement(pact, consumer):
    # Define the Matcher; the expected structure and content of the response
    test_pub_app = '59786bc2a43b3a08620026b1'
    test_placement = 'DEFAULT02021'
    expected = expected_served_ads_response(placement_id=test_placement)

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a body which is
    # "Like" the structure defined above. This means the mock provider will
    # return the EXACT content where defined, e.g. UserA for name, and SOME
    # appropriate content e.g. for ip_address.
    (
        pact.given("Test to request ads with a valid pub app")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=jaeger_v5_ios(test_pub_app, test_placement),
                          headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken))
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
        ads = consumer.request_ads(test_pub_app, test_placement)

        # In this case the mock Provider will have returned a valid response
        assert ads.placement_reference_id == test_placement

        # Make sure that all interactions defined occurred
        pact.verify()


def test_request_ads_with_non_existing_pub_app(pact, consumer):
    test_pub_app = '123456'
    test_placement = 'DEFAULT02021'
    expected = expected_non_served_ads_response(sleep_code=901, info='publisher not found')

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a 404
    (
        pact.given("Test to get the config with a non-existing pub app")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=jaeger_v5_ios(test_pub_app, test_placement),
                          headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken))
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
        ads = consumer.request_ads(test_pub_app, test_placement)

        # In this case, the mock Provider will have returned a sleep code
        assert ads.ad_markup['sleep'] == 901
        assert ads.ad_markup['info'] == 'publisher not found'

        # Make sure that all interactions defined occurred
        pact.verify()


def test_request_ads_with_non_existing_placement(pact, consumer):
    test_pub_app = '59786bc2a43b3a08620026b1'
    test_placement = '123465'
    expected = expected_non_served_ads_response(sleep_code=902, info='placement not found')

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a 404
    (
        pact.given("Test to get the config with a non-existing placement")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=jaeger_v5_ios(test_pub_app, test_placement),
                          headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken))
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
        ads = consumer.request_ads(test_pub_app, test_placement)

        # In this case, the mock Provider will have returned a sleep code
        assert ads.ad_markup['sleep'] == 902
        assert ads.ad_markup['info'] == 'placement not found'

        # Make sure that all interactions defined occurred
        pact.verify()
