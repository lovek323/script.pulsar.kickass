import base64
import hashlib
import json
import os
import re
import sys
import urllib
import urllib2
import xbmcaddon

PAYLOAD      = json.loads(base64.b64decode(sys.argv[1]))
PREFIX_LOG   = 'KICKASS - '
__addon__    = xbmcaddon.Addon(str(sys.argv[0]))
cache_prefix = xbmc.translatePath('special://temp') + __addon__.getAddonInfo('name').lower().replace(' ','_') + '_cache_'

def search(query):
    print PREFIX_LOG + ("Running search query: %s" % query)
    url = "http://katproxy.bz/usearch/%s" % query
    m = hashlib.md5()
    m.update(url)
    url_hash = m.hexdigest()
    cache_file = cache_prefix + url_hash
    print PREFIX_LOG + ("Cache file: %s" % cache_file)
    if (os.path.isfile(cache_file)):
        print PREFIX_LOG + "Pulling from cache"
        f = open(cache_file, 'r')
        data = f.read()
        f.close()
    else:
        print PREFIX_LOG + ("Requesting: %s" % url)
        response = urllib2.urlopen(url)
        data = response.read()
        if response.headers.get("Content-Encoding", "") == "gzip":
            import zlib
            data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
        f = open(cache_file, 'w')
        f.write(data)
        f.close()
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
