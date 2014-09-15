import sys
import json
import base64
import re
import urllib
import urllib2

import sys
import json
import base64
import re
import urllib
import urllib2

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

def search(query):
    response = urllib2.urlopen("http://katproxy.bz/search/?q=%s" % urllib.quote_plus(query))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

def search_episode(imdb_id, tvdb_id, name, season, episode):
    return search("%s S%02dE%02d" % (name, season, episode))


def search_movie(imdb_id, name, year):
    response = urllib2.urlopen("http://katproxy.bz/usearch/" + name + "%20category:movies/")
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)

