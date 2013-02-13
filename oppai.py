# -*- coding: utf-8 -*-
import os
import json
import hashlib
import re
import urllib

APP_ID = '17C9833049FC22871BCA2D3CCE54885DDD07CDBC'
API_URI = 'http://api.bing.net/json.aspx'
OUT_DIR = './data'

if __name__ == '__main__':
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    page_count = 0
    dl_count = 0

    while True:
        params = {
                "AppId": APP_ID,
                "Version": 2.2,
                "Market": "ja-JP",
                "Sources": "Image",
                "Image.Count": 50,
                "Image.Offset":page_count * 50,
                "Adult": "off",
                "Query": "おっぱい"
                }

        url = API_URI + "?" + urllib.urlencode(params)
        data = json.load(urllib.urlopen(url))

        for entry in data["SearchResponse"]["Image"]["Results"]:
            media_url = entry["MediaUrl"].encode('utf-8')

            if not re.search("\.jpe?g$", media_url):
                continue

            filename = hashlib.md5(media_url).hexdigest() + ".jpg"
            filepath = "%s/%s" % (OUT_DIR, filename)

            if os.path.exists(filepath):
                continue

            print "%s : Download... %s" % (dl_count, filepath)

            image = urllib.urlretrieve(media_url, filepath)

            if not re.search("^image\/.+", image[1]["Content-Type"]):
                os.remove(filepath)

            dl_count += 1
            page_count += 1
