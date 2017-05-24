# import mechanize
# import cookielib

import ssl
import time
import requests
import random
from termcolor import colored


# some common user agent   mobile ( iphone and android)  , desktop ( IE and firefox)


class URL:
    """ This class will gather information about a single URL like : https://www.google.com:80/"""
    def __init__(self, protocol, hostname, port, useragent, timeout, retries):
        # setting initial variables
        self.protocol = protocol
        self.hostname = hostname
        self.port = int(port)
        self.timeout = timeout
        self.retries = retries
        self.response = ""
        self.status_code = 0
        self.content = ""
        self.headers = ""
        self.status = ""
        self.result = ""
        self.ctime = time.ctime()
        self.date = time.strftime("%Y%m%d_%H%M", time.localtime())
        self.useragent_abr = useragent

        self.useragent_strings = {
            'desktop':[
                "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/37.0",  # firefox
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)"  ], # IE
            'mobile': [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25", # Iphone
                "Mozilla/5.0 (Linux; Android 4.3; SM-N900V Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.92 Mobile Safari/537.36" ] # Note 3
        }
        # set user agent according to input
        self.useragent = {'User-Agent': random.choice(self.useragent_strings[self.useragent_abr])}
        self.date = time.strftime("%Y%m%d_%H%M", time.localtime())
        self.has_ssl = False
        if (self.protocol.lower() == "https"):
            self.has_ssl = True
    def getdata(self):
        # this method will get information from url
        try:
            # ignore SSL
            session = requests.Session()

            # simulate retries for accurate result
            session.mount("http://", requests.adapters.HTTPAdapter(max_retries=self.retries))
            session.mount("https://", requests.adapters.HTTPAdapter(max_retries=self.retries))
            self.response = session.get(url="{}://{}:{}/".format(self.protocol, self.hostname, self.port),
                                        verify=False,
                                        headers=self.useragent,
                                        timeout=self.timeout)
            self.status_code = int(self.response.status_code)
            self.content = self.response.content
            for j in self.response.headers:
                self.headers += "{} : {}\n".format(j,self.response.headers[j])

        except Exception as e:
            print "Error occurred when trying to get data from url {}://{}:{}/ ".format(self.protocol, self.hostname, self.port)
            self.status_code = -1
            self.content = "Error"
            self.headers = "Error"
            print colored(type(e),'green')

        if(self.has_ssl):
            self.certificate = ssl.get_server_certificate((self.hostname, self.port ))
        else:
            self.certificate = "Haven't HTTPS."

        # this variable indicate whether this url has been fetched successfully or not
        if self.status_code  == -1:
            self.status = "Failed"
        elif self.status_code == 0:
            self.status = "Nothing tried"
        else:
            self.status = "OK"

        self.result = {
            'url':"{}://{}:{}/".format(self.protocol, self.hostname, self.port),
            'data':
                dict(protocol=self.protocol,
                hostname=self.hostname,
                port=self.port,
                has_ssl=self.has_ssl,
                useragent=self.useragent_abr,
                ctime=self.ctime,
                date=self.date,
                status_code=self.status_code,
                status=self.status,
                content=self.content,
                headers=self.headers,
                certificate=self.certificate )
        }
#s = URL('https','www.google.com',443,'mobile',5,5)
#s.getdata()
#print s.result