import random


def config_v5_ios(pub_app_id='59786bc2a43b3a08620026b1', placement_id=None, auto_cached=None, skadnetwork_ids=None,
                  gdpr='opted_in', coppa=None):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.ios-sdk-app.qa",
            "ver": "14f1cf7"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": "Apple",
            "os": "ios",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "h": 2688,
            "model": "x86_64",
            "osv": "12.4",
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 0.60000002384185791,
                        "battery_state": "unknown",
                        "idfa": "4423DD36-2738-46DC-84D1-02A47F95320C",
                        "vduid": "",
                        "battery_level": -1,
                        "locale": "en_US",
                        "connection_type": "wifi",
                        "language": "en",
                        "storage_bytes_available": 228426878976,
                        "idfv": "C8360A3F-81C3-4DC5-99FD-B5B28A161A6D",
                        "battery_saver_enabled": 0,
                        "time_zone": "Asia/Shanghai"
                    }
                }
            },
            "carrier": "",
            "ifa": "V9SHDTQ68ELAHLH7LEFWFWNE9RBZW0H5JJK0",
            "w": 1242,
            "lmt": 0
        },
        "ext": {},
        "request": {},
        "user": {
            "gdpr": {
                "consent_timestamp": 1565346845,
                "consent_status": gdpr,
                "consent_message_version": "publisher_version_v1.0",
                "consent_source": "publisher"
            }
        }
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if auto_cached is not None:
        request_obj.update({
            "is_auto_cached_enforced": auto_cached
        })
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    return data


def gen_device_id(digital=36):
    seed = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    id_str = []
    for i in range(digital):
        id_str.append(random.choice(seed))
    return ''.join(id_str)


def jaeger_v5_ios(pub_app_id='59786bc2a43b3a08620026b1', placement_id=None, gdpr=None,
                  ifa=gen_device_id(), idfv='', header_bidding=False, banner=False, ccpa=None, coppa=None,
                  os_version='13', h=1792, w=828,
                  skadnetwork_ids=None, vision=False, make='Apple', model='iPhone11,8', lmt=0, sound_enabled=0,
                  banner_type='banner_leaderboard', battery_saver_enabled=1, device_connection_type='wifi',
                  ua='Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                     ' Mobile/15E148'):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.ios-sdk-app.qa",
            "ver": "1.0.9"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": make,
            "os": "ios",
            "ua": ua,
            "h": h,
            "w": w,
            "model": model,
            "osv": os_version,
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 0.5625,
                        "battery_state": "unplugged",
                        "idfa": "",
                        "vduid": "",
                        "battery_level": 0.54000002145767231,
                        "locale": "en_US",
                        "connection_type": device_connection_type,
                        "language": "en-US",
                        "storage_bytes_available": 9223372036854775807,
                        "idfv": idfv,
                        "battery_saver_enabled": battery_saver_enabled,
                        "time_zone": "America/Los_Angeles",
                        "sound_enabled": sound_enabled
                    }
                }
            },
            "carrier": "T-Mobile",
            "ifa": ifa,
            "lmt": lmt
        },
        "ext": {},
        "request": {},
        "user": {},
        "badv": [
            "glu.com",
        ],
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if header_bidding:
        request_obj.update({"header_bidding": True})
    if banner:
        request_obj.update({"ad_size": banner_type})
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    if vision:
        vision = {
            "vision": {
                "data_science_cache": "",
                "aggregate": [
                    {
                        "window": 3,
                        "last_viewed_creative_id": "",
                        "total_view_count": 7,
                        "creative_details": [
                            {
                                "view_count": 1,
                                "creative_id": "5fce479352a4d9001688f120",
                                "last_time_viewed": 1629154430
                            }
                        ],
                        "campaign_details": [
                            {
                                "view_count": 3,
                                "campaign_id": "60f82d4c97599e0010813443",
                                "last_time_viewed": 1629154562
                            }
                        ],
                        "advertiser_details": [
                            {
                                "view_count": 3,
                                "advertiser_id": "561941526",
                                "last_time_viewed": 1629154562
                            }
                        ]
                    }
                ]
            }
        }
        data.get("user").update(vision)

    return data