def platform_headers(sdk_version='Vungle/6.11.0', src_ip='45.117.100.153', vungle_version='5.8', debug=None,
                     rtb_selector=None, experiment=None, override_bid_ext=None, override_bid_price=None,
                     override_bid_adomain=None, omid=None,
                     accept_encoding=None, content_encoding=None, is_hb=False):
    headers = {
        'Accept': "application/json",
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'user-agent': sdk_version,
        'X-Forwarded-For': src_ip,
        'X-VUNGLE-BUNDLE-ID': 'com.outfit7.mytalkingtomfree',
        'X-VUNGLE-LANGUAGE': 'ru',
        'X-VUNGLE-TIMEZONE': 'Asia/Shanghai',
        'Vungle-Version': vungle_version
    }

    if debug is not None:
        headers['Vungle-explain'] = debug

    if rtb_selector is not None:
        headers['X-Vungle-RTB-ID'] = rtb_selector

    if experiment is not None:
        headers['X-Vungle-Experiment-Bucket'] = experiment

    if override_bid_ext is not None:
        headers['X-Vungle-Override-Bid-Ext'] = override_bid_ext

    if override_bid_price is not None:
        headers['X-Vungle-Override-Bid-Price'] = override_bid_price

    if override_bid_adomain is not None:
        headers['X-Vungle-Override-Bid-Adomain'] = override_bid_adomain

    if omid is not None:
        headers['X-Vungle-Omid'] = omid

    if accept_encoding is not None:
        headers['Accept-Encoding'] = accept_encoding

    if content_encoding is not None:
        headers['Content-Encoding'] = content_encoding

    if is_hb:
        headers['user-agent'] = sdk_version + ';' + is_hb

    return headers