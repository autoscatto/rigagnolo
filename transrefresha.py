import transmissionrpc
from BeautifulSoup import BeautifulSoup
import urllib2
from multiprocessing import Pool, Event

TRANSMISSION_IP = "127.0.0.1"
SEARCH_URL = "http://torrentz.eu/%s"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
PNUMBER = 8

def initializer(terminating_):
    global terminating
    terminating = terminating_


def tradder(h):
    try:
        if not terminating.is_set():
            try:
                hashstring, ttrackers, tid = h
                u = urllib2.Request(SEARCH_URL % hashstring, "", {'User-Agent': user_agent})
                response = urllib2.urlopen(u)
                soup = BeautifulSoup(response.read())
                trackers_div = soup.find('div', {"class": 'trackers'})
                trackers = [b['announce'] for b in ttrackers]
                if trackers_div:
                    uu = []
                    for d in trackers_div.findAll('dt'):
                        tl = d.find(text=True)
                        if tl not in trackers:
                            uu.append(tl)
                    return tid, uu
                return None, []
            except Exception as e:
                    print e
        else:
            print "Ok, stahp"
    except KeyboardInterrupt:
        terminating.set()


if __name__ == "__main__":
    tc = transmissionrpc.Client(address=TRANSMISSION_IP)
    torrents = tc.get_torrents()
    terminating = Event()
    try:
        #print torrents
        pool = Pool(PNUMBER, initializer=initializer, initargs=(terminating, ))
        hh = [(h.hashString, h.trackers, h.id) for h in torrents]
        resulti = pool.map(tradder, hh)
        for tid, tlist in resulti:
            #print tid
            if len(tlist) > 0:
                ts = tc.get_torrent(tid)
                print "Adds %s to '%s'" % (str(tlist).translate(None, "'"), str(ts))
                tc.change_torrent([tid], trackerAdd=tlist)
        pool.close()
    except KeyboardInterrupt:
        print "################ Caught KeyboardInterrupt, terminating workers #####################"
        pool.terminate()
        pool.join()

