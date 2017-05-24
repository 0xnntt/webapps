import mechanize
import cookielib
import time
import sys

# author : 0xnnt
# date : May 2012
# this little script simulate a browser and open bing.com and search with ip directive and return the results. ( with no exception handling ) 
# requirements :
# pip install mechanize
# pip install cookielib


# list of IP addresses
#ips = ["4.2.2.4","199.99.99.99"]

#print sys.argv
#usage: python-bing.py  ip1,ip2,ip3   number_of_pages_to_parse_from_bing
#usage: python-bing.py 192.168.10.10,172.10.10.10,150.50.50.50 5

ips = sys.argv[1].split(',')
page_numbers = sys.argv[2]


def site_counter(string):   #return count of websites returned by bing
    count = string.split('<span class="sb_count">')[1]
    count = count.split(" results</span>")[0]
    return count
    
def check_empty_result(string):      #check a reverse ip lookup html and see if there is no website on it
    if(string.count("No results found for ") >= 1):
        return "Empty"
    else:
        return "NotEmpty"


def get_url(url):
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)


    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    r = br.open(url)
    result = r.read()
    br.close()
    return result
    
    
def extract_websites(string):       # return list of websites from a saved html bing file
    v = string.split("<cite>")
    v.pop(0)
    sites = []
    for i in v:
        sites.append(i.split("</cite>")[0].replace("<strong>","").replace("</strong>",""))
    return sites

# Browser

for j in ips:
    all_sites = []
    try:
        counter = 1
        print counter," SET !!!"
        print "https://www.bing.com/search?q=ip:"+j+"&first="+str(counter)
        s = get_url("https://www.bing.com/search?q=ip:"+j+"&first="+str(counter))
        #for i in  extract_websites(s):
        #    print i
        for i in extract_websites(s):
               all_sites.append(i)
               print i
        for k in  range(int(page_numbers)):
            start = str(k*10+1)
            print "https://www.bing.com/search?q=ip:"+j+"&first="+start
            ss = get_url("https://www.bing.com/search?q=ip:"+j+"&first="+start)
            time.sleep(3)
            for k in extract_websites(ss):
                print k
                all_sites.append(k)
        """k = open(j+".html","w")
        k.write(html)
        k.close()"""
        clean = []
        for l in all_sites:
            if (l.count("https://")>=1):
                l = l.replace("https://","")
            elif(l.count("http://")>=1):
                l = l.replace("http://","")
            clean.append(l.split("/")[0])
        print "============================================result========================================="
        z = open(j+".txt","w")
        for v in set(clean):
            print v
            z.write(v+"\n")
        z.close()
    except IOError as e:
        print j,"Cannot done !!!","I/O error({0}): {1}".format(e.errno, e.strerror)
    #ips.pop(ips.index(j))
    #v =open("remainds.txt","w").writelines(ips)
    #v.close()
    time.sleep(3)
    
