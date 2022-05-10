from typing import Optional

import requests

from examples.common.test_data.headers import *
from examples.common.test_data.request_payload import *


class Config(object):

    def __init__(self, ads_endpoint: str, placement_refer_id: str):
        self.ads_endpoint = ads_endpoint
        self.placement_refer_id = placement_refer_id


class ConfigConsumer(object):

    def __init__(self, base_uri: str):

        self.base_uri = base_uri

    def get_config(self, pub_app_id: str) -> Optional[Config]:

        uri = self.base_uri + "/api/v5/config"
        req = config_v5_ios(pub_app_id)

        r = requests.post(uri, json=req, headers=platform_headers())

        if r.status_code != 200:
            return None

        response_payload = r.json()
        ads_endpoint = response_payload['endpoints']['ads']
        placement_refer_id = response_payload['placements'][0]['reference_id']

        return Config(ads_endpoint, placement_refer_id)


class Ads(object):

    def __init__(self, placement_reference_id: str, ad_markup: dict):
        self.placement_reference_id = placement_reference_id
        self.ad_markup = ad_markup


class AdsConsumer(object):

    def __init__(self, base_uri: str):

        self.base_uri = base_uri

    def request_ads(self, pub_app_id: str, placement_refer_id: str) -> Optional[Ads]:

        uri = self.base_uri + "/api/v5/ads"
        req = jaeger_v5_ios(pub_app_id, placement_refer_id)

        r = requests.post(uri, json=req,
                          headers=platform_headers(src_ip='45.117.100.153', rtb_selector='5fd21d91c80cb9051249a6b1'))

        if r.status_code != 200:
            return None

        response_payload = r.json()
        placement_reference_id = response_payload['ads'][0]['placement_reference_id']
        ad_markup = response_payload['ads'][0]['ad_markup']

        return Ads(placement_reference_id, ad_markup)