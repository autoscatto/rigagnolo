from BeautifulSoup import BeautifulSoup
import urllib2
import sys, os, hashlib, StringIO
import bencode

SEARCH_URL = "http://torrentz.eu/%s"
def main():
    """ 
        it looks for trackers for specified file as the first argument
        
        for each tracker found prints a line to std output.
        If it encounters an error it will print a short description on std error, and exits with exit status 1.
    """
    try:
        torrent_file = open(sys.argv[1], "rb")
    except:
        print >> sys.stderr,"Error on file oepning"
        sys.exit(1)
    try:
        metainfo = bencode.bdecode(torrent_file.read())
        torrent_file.close()
        hasha= hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest()  
        print "HASH found: %s"%hasha  
    except:
        print >> sys.stderr,"Error on .torrent parsing"
        sys.exit(1)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    u =urllib2.Request(SEARCH_URL%hasha,"",{ 'User-Agent' : user_agent} )
    response = urllib2.urlopen(u)
    if response.code is not 200:
        print >> sys.stderr,"Error on web request"
        sys.exit(1)
    html = response.read()
    if html is None or html is '':
        print >> sys.stderr,"Error on response"
        sys.exit(1)
    soup = BeautifulSoup(html)
    trackers_div = soup.find('div',{"class":'trackers'})
    if trackers_div is None:
        # 0 trackers found
        sys.exit(0)
    dt=trackers_div.findAll('dt')
    trackers=[]
    for d in dt:
        trackers.append(d.find(text=True))
    print "\n".join(trackers)
    sys.exit(0)
    
if __name__ == "__main__":
    main()
