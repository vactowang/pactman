from pact import Format, EachLike


def expected_served_config_response():
    data = {
        "endpoints": {
            "new": "https://apiqa.vungle.com/api/v5/new",
            "ads": "https://apiqa.vungle.com/api/v5/ads",
            "will_play_ad": "https://apiqa.vungle.com/api/v5/will_play_ad",
            "report_ad": "https://apiqa.vungle.com/api/v5/report_ad",
            "log": "http://logs-apiqa.vungle.io/sdk",
            "ri": "https://events-ext-qa.api.vungle.com/api/v5/ri",
            "cache_bust": "https://events-ext-qa.api.vungle.com/api/v5/cache_bust",
            "sdk_bi": "https://events-ext-qa.api.vungle.com/api/v5/sdk_bi"
        },
        "placements": [
            {
                "id": "5f68be4ed5ba35022aeace75",
                "reference_id": "DEFAULT02024",
                "is_auto_cached": True,
                "is_incentivized": True,
                "supported_template_types": [
                    "fullscreen"
                ],
                "supported_ad_formats": [
                    "vungle_mraid",
                    "third_party",
                    "third_party_playable"
                ],
                "header_bidding": True
            },
            {
                "id": "5f6a468cd5ba35022aeace76",
                "reference_id": "AREYOUS82694",
                "is_auto_cached": False,
                "is_incentivized": True,
                "supported_template_types": [
                    "fullscreen"
                ],
                "supported_ad_formats": [
                    "vungle_mraid",
                    "third_party",
                    "third_party_playable"
                ]
            },
            {
                "id": "6038c3923f32a974dcad4942",
                "reference_id": "DEFAULT020241",
                "is_auto_cached": True,
                "is_incentivized": True,
                "supported_template_types": [
                    "fullscreen"
                ],
                "supported_ad_formats": [
                    "vungle_mraid",
                    "third_party",
                    "third_party_playable"
                ],
                "header_bidding": True
            }
        ],
        "config": {
            "refresh_time": 86400000
        },
        "will_play_ad": {
            "enabled": False,
            "request_timeout": 300
        },
        "playback": {
            "buffer_timeout": 500
        },
        "viewability": {
            "moat": True,
            "om": True
        },
        "exception_reporting": True,
        "logging": {
            "enabled": False
        },
        "crash_report": {
            "max_send_amount": 0,
            "enabled": False,
            "collect_filter": "*.vungle.com"
        },
        "vduid": "",
        "gdpr": {
            "is_country_data_protected": False,
            "consent_title": "Personalized Ads",
            "consent_message": "Ads are personalized. Denying would disable it",
            "consent_message_version": "0.0",
            "button_accept": "Accept",
            "button_deny": "Deny"
        },
        "ri": {
            "enabled": False
        },
        "vision": {
            "enabled": False,
            "aggregation_filters": [
                "creative_details",
                "campaign_details",
                "advertiser_details"
            ],
            "aggregation_time_windows": [
                1,
                45
            ],
            "view_limit": {
                "device": 1000,
                "wifi": 100,
                "mobile": 50
            }
        },
        "session": {
            "enabled": True,
            "timeout": 900,
            "limit": 0
        },
        "skadnetwork": {},
        "cache_bust": {
            "enabled": True,
            "interval": 3600
        },
        "ad_load_optimization": {
            "enabled": False
        }
    }
    
    return data


def expected_served_ads_response(placement_id=None, header_bidding=False, omsdk=False, skan=False):
    data = {
        "ads": [
            {
                "placement_reference_id": placement_id,
                "ad_markup": {
                    "id": "string",
                    "campaign": "string",
                    "app_id": "string",
                    "expiry": Format().integer,
                    "tpat": {
                        "moat": {
                            "is_enabled": True,
                            "extra_vast": "string"
                        },
                        "clickUrl": EachLike('string'),
                        "checkpoint.0": EachLike('string'),
                        "checkpoint.25": EachLike('string'),
                        "checkpoint.50": EachLike('string'),
                        "checkpoint.75": EachLike('string'),
                        "checkpoint.100": EachLike('string'),
                        "postroll.view": EachLike('string'),
                        "postroll.click": EachLike('string'),
                        "video.close": EachLike('string'),
                        "video.unmute": EachLike('string'),
                        "video.mute": EachLike('string')
                    },
                    "delay": Format().integer,
                    "showClose": Format().integer,
                    "showCloseIncentivized": Format().integer,
                    "countdown": Format().integer,
                    "url": "string",
                    "videoWidth": Format().integer,
                    "videoHeight": Format().integer,
                    "callToActionUrl": "string",
                    "adType": "string",
                    "templateURL": "string",
                    "templateSettings": {
                        "normal_replacements": {
                            "SK_FSC": "string",
                            "CTA_BUTTON_BACKGROUND": "string",
                            "INCENTIVIZED_BODY_TEXT": "string",
                            "CTA_BUTTON_URL": "string",
                            "SK_ASOI_AGGRESSIVE": "string",
                            "SK_ASOI_COMPLETE": "string",
                            "SK_SKDT": "string",
                            "FULL_CTA": "string",
                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "string",
                            "ACTION_TRACKING": "string",
                            "VIDEO_PROGRESS_BAR": "string",
                            "PRIVACY_BODY_TEXT": "string",
                            "VUNGLE_PRIVACY_URL": "string",
                            "PRIVACY_CLOSE_TEXT": "string",
                            "START_MUTED": "string",
                            "FULL_CTA_OPTION": "string",
                            "INCENTIVIZED_TITLE_TEXT": "string",
                            "INCENTIVIZED_CLOSE_TEXT": "string",
                            "PRIVACY_CONTINUE_TEXT": "string",
                            "AUTO_LOCALIZE": "string",
                            "INCENTIVIZED_CONTINUE_TEXT": "string",
                            "SK_CTA_ONLY": "string"
                        },
                        "cacheable_replacements": {
                            "MAIN_VIDEO": {
                                "url": "string",
                                "extension": "string"
                            }
                        }
                    },
                    "templateId": "string",
                    "template_type": "string",
                    "ad_market_id": "string",
                    "ad_token": "string",
                    "requires_sideloading": True,
                    "timestamp": Format().integer
                }
            }
        ]
    }

    if header_bidding:
        data.get('ads')[0].get('ad_markup').update(bid_token="string")

    if omsdk:
        data.get('ads')[0].get('ad_markup').get('templateSettings').get('normal_replacements')\
            .update(OM_SDK_DATA="string")
        data.get('ads')[0].get('ad_markup').update(viewability={
            "om": {
                "is_enabled": True,
                "extra_vast": "string"
            }
        })

    if skan:
        data.get('ads')[0].get('ad_markup').update(attribution={
            "method": "string",
            "skadnetwork": {
                "version": "string",
                "storekit": {
                    "fidelity_type": Format().integer,
                    "version": "string",
                    "ad_network_id": "string",
                    "source_app_id": Format().integer,
                    "itunes_item_id": Format().integer,
                    "signature": "string",
                    "campaign_id": Format().integer,
                    "nonce": Format().uuid,
                    "timestamp": Format().integer
                },
                "viewthrough": {
                    "ad_type": "string",
                    "ad_description": "string",
                    "ad_purchaser_name": "string",
                    "fidelity_type": Format().integer,
                    "version": "string",
                    "ad_network_id": "string",
                    "source_app_id": Format().integer,
                    "itunes_item_id": Format().integer,
                    "signature": "string",
                    "campaign_id": Format().integer,
                    "nonce": Format().uuid,
                    "timestamp": Format().integer
                }
            }
        })

    return data


def expected_non_served_ads_response(sleep_code=None, info=None):

    data = {
        "ads": [
            {
                "placement_reference_id": "DEFAULT02021",
                "ad_markup": {
                    "id": "",
                    "campaign": None,
                    "app_id": None,
                    "sleep": sleep_code,
                    "info": info,
                    "delay": 0,
                    "showClose": 0,
                    "showCloseIncentivized": 0,
                    "countdown": 0,
                    "url": "",
                    "videoWidth": 0,
                    "videoHeight": 0,
                    "requires_sideloading": False
                }
            }
        ]
    }

    return data