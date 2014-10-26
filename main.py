import base64
import hashlib
import json
import os
import sys
import urllib
import xbmcaddon

from pulsar import provider

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
        response = provider.GET(url, params={"q": query})
        data = response.data
        if response.headers.get("Content-Encoding", "") == "gzip":
            import zlib
            data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
        f = open(cache_file, 'w')
        f.write(data)
        f.close()

    return provider.extract_magnets(data)

def search_episode(episode):
    print PREFIX_LOG + 'Seaching for: %(title)s (S%(season)02dE%(episode)02d)' % episode
    return search("\"%(title)s\" category:tv verified:1 season:S%(season)02d episode:%(episode)02d" % episode)

def search_movie(movie):
    print PREFIX_LOG + 'Seaching for: %(title)s %(year)d' % movie
    return search("\"%(title)s\" %(year)d category:movies" % movie)

provider.register(search, search_movie, search_episode)
