import sys
import json
import base64
import re
import urllib
import urllib2

PAYLOAD    = json.loads(base64.b64decode(sys.argv[1]))
PREFIX_LOG = 'KICKASS - '

def search(query):
    print PREFIX_LOG + ("Running search query: %s" % query)
    response = urllib2.urlopen("http://katproxy.bz/search?q=%s" % urllib.quote_plus(query))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    magnets = re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)
    print PREFIX_LOG + ("Found %d magnet links" % len(magnets))
    return [{"uri": magnet} for magnet in magnets]

def search_episode(imdb_id, tvdb_id, name, season, episode):
    print PREFIX_LOG + 'Seaching for: ' + name + ' (S' + str(season).zfill(2) + 'E' + str(episode).zfill(2) + ')'
    return search("\"%s\" category:tv verified:1 season:%d episode:%d" % (name, season, episode))


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


