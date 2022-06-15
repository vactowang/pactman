"""pact test for the Jaeger service client"""

import atexit
import logging
import os
import pytest

from examples.common.test_data.data import *
from examples.common.test_data.expected_response_payload import *
from examples.common.test_data.headers import *
from examples.common.test_data.request_payload import *
from examples.consumer.src.consumer import AdsConsumer
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

PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234

PACT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def ads_consumer() -> AdsConsumer:
    return AdsConsumer("http://{host}:{port}".format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT))


@pytest.fixture(scope="session")
def pact(request):
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
        broker_password=PACT_BROKER_PASSWORD
    )

    pact.start_service()
    atexit.register(pact.stop_service)
    yield pact
    pact.stop_service()
    pact.publish_to_broker = True


def test_jaeger_responds_normally_without_sleep_code(pact, ads_consumer):
    test_pub_app = '59786bc2a43b3a08620026b1'
    test_placement = 'DEFAULT02021'
    expected = expected_served_ads_response(placement_id=test_placement, header_bidding=True)
    device_id = gen_device_id()

    req = jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id, header_bidding=True)
    headers = platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken)

    (
        pact.given("Test Jaeger responds normally without sleep code")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=req, headers=headers)
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        ads = ads_consumer.request_ads(req, headers)
        # assert that there is no sleep code from ads response
        assert ads.sleep_code is None
        pact.verify()


def test_jaeger_responds_normally_without_sleep_code_negative(pact, ads_consumer):
    test_pub_app = '59786bc2a43b3a08620026b1'
    test_placement = '123456'
    expected = expected_served_ads_response(placement_id=test_placement, header_bidding=True)
    device_id = gen_device_id()

    req = jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id, header_bidding=True)
    headers = platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken)

    (
        pact.given("Test Jaeger responds normally without sleep code")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=req, headers=headers)
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        ads = ads_consumer.request_ads(req, headers)
        # assert that there is no sleep code from ads response
        assert ads.sleep_code is None
        pact.verify()


def test_jaeger_responds_normally_with_omsdk_data(pact, ads_consumer):
    test_pub_app = '59786bc2a43b3a08620026b1'
    test_placement = 'DEFAULT02021'
    expected = expected_served_ads_response(placement_id=test_placement, header_bidding=True, omsdk=True)
    device_id = gen_device_id()

    req = jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id, header_bidding=True)
    headers = platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken)

    (
        pact.given("Test Jaeger responds normally without sleep code")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=req, headers=headers)
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        ads = ads_consumer.request_ads(req, headers)
        # assert that there is om data from the ads response
        assert 'OM_SDK_DATA' in ads.ad_markup['templateSettings']['normal_replacements']
        assert ads.ad_markup['viewability']['om']['is_enabled'] is True
        pact.verify()


def test_jaeger_responds_normally_with_omsdk_data_negative(pact, ads_consumer):
    test_pub_app = '59786bc2a43b3a08620026b2'  # not a om enabled pub app
    test_placement = 'DEFAULT02022'
    expected = expected_served_ads_response(placement_id=test_placement, header_bidding=True, omsdk=True)
    device_id = gen_device_id()

    req = jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id, header_bidding=True)
    headers = platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken)

    (
        pact.given("Test Jaeger responds normally without sleep code")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=req, headers=headers)
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        ads = ads_consumer.request_ads(req, headers)
        # assert that there is om data from the ads response
        assert 'OM_SDK_DATA' in ads.ad_markup['templateSettings']['normal_replacements']
        assert ads.ad_markup['viewability']['om']['is_enabled'] is True
        pact.verify()


def test_jaeger_responds_normally_with_skan_data(pact, ads_consumer):
    test_pub_app = '59786bc2a43b3a08620026b2'
    test_placement = 'DEFAULT02022'
    expected = expected_served_ads_response(placement_id=test_placement, skan=True)
    device_id = test_mode_device_id
    network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
    osv = '14.5'
    sdkv = 'Vungle/6.10.0'

    req = jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id, os_version=osv, skadnetwork_ids=network_ids)
    headers = platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_id, sdk_version=sdkv)

    (
        pact.given("Test Jaeger responds normally without sleep code")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=req, headers=headers)
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        ads = ads_consumer.request_ads(req, headers)
        # assert the skan data from the ads response
        assert 'attribution' in ads.ad_markup
        pact.verify()


def test_jaeger_responds_normally_with_skan_data_negative(pact, ads_consumer):
    test_pub_app = '59786bc2a43b3a08620026b2'
    test_placement = 'DEFAULT02022'
    expected = expected_served_ads_response(placement_id=test_placement, skan=True)
    device_id = test_mode_device_id
    network_ids = ['test.ad.nw.001']    # non-matched network id
    osv = '14.5'
    sdkv = 'Vungle/6.10.0'

    req = jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id, os_version=osv, skadnetwork_ids=network_ids)
    headers = platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_id, sdk_version=sdkv)

    (
        pact.given("Test Jaeger responds normally without sleep code")
            .upon_receiving("get ads response from the Jaeger service")
            .with_request("post", "/api/v5/ads", body=req, headers=headers)
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        ads = ads_consumer.request_ads(req, headers)
        # assert the skan data from the ads response
        assert 'attribution' in ads.ad_markup
        pact.verify()


# def test_request_ads_with_non_existing_pub_app(pact, ads_consumer):
#     test_pub_app = '123456'
#     test_placement = 'DEFAULT02021'
#     expected = expected_non_served_ads_response(sleep_code=901, info='publisher not found')
#     device_id = gen_device_id()
#
#     # Define the expected behaviour of the Provider. This determines how the
#     # Pact mock provider will behave. In this case, we expect a 404
#     (
#         pact.given("Test to get the config with a non-existing pub app")
#             .upon_receiving("get ads response from the Jaeger service 2")
#             .with_request("post", "/api/v5/ads", body=jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id),
#                           headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken))
#             .will_respond_with(200, body=Like(expected))
#     )
#
#     with pact:
#         # Perform the actual request
#         ads = ads_consumer.request_ads(test_pub_app, test_placement, device_id=device_id)
#
#         # In this case, the mock Provider will have returned a sleep code
#         assert ads.ad_markup['sleep'] == 901
#         assert ads.ad_markup['info'] == 'publisher not found'
#
#         # Make sure that all interactions defined occurred
#         pact.verify()
#
#
# def test_request_ads_with_non_existing_placement(pact, ads_consumer):
#     test_pub_app = '59786bc2a43b3a08620026b1'
#     test_placement = '123465'
#     expected = expected_non_served_ads_response(sleep_code=902, info='placement not found')
#     device_id = gen_device_id()
#
#     # Define the expected behaviour of the Provider. This determines how the
#     # Pact mock provider will behave. In this case, we expect a 404
#     (
#         pact.given("Test to get the config with a non-existing placement")
#             .upon_receiving("get ads response from the Jaeger service 3")
#             .with_request("post", "/api/v5/ads", body=jaeger_v5_ios(test_pub_app, test_placement, ifa=device_id),
#                           headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_ext_kraken))
#             .will_respond_with(200, body=Like(expected))
#     )
#
#     with pact:
#         # Perform the actual request
#         ads = ads_consumer.request_ads(test_pub_app, test_placement, device_id=device_id)
#
#         # In this case, the mock Provider will have returned a sleep code
#         assert ads.ad_markup['sleep'] == 902
#         assert ads.ad_markup['info'] == 'placement not found'
#
#         # Make sure that all interactions defined occurred
#         pact.verify()
