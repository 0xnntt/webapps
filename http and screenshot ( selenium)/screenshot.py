import os
import random
import subprocess
import time
import platform
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class screenshot:
    def __init__(self, hostname, output, protocol, port, logfile, useragent_abr, keep=False):
        self.hostname = hostname
        self.logfile = logfile
        self.useragent_abr = useragent_abr
        self.output = output  # output folder that image should save in it
        self.protocol = protocol
        self.port = port
        self.abs_path = ""  # absolute path
        self.data = ''
        self.date = ''
        self.log = ""
        self.keep = keep
        self.image = ""
        self.useragent_raw = ""
        self.useragent_strings = {
            'desktop': [
                "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/37.0",  # firefox
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)"],  # IE
            'mobile': [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
                # Iphone
                "Mozilla/5.0 (Linux; Android 4.3; SM-N900V Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.92 Mobile Safari/537.36"]
        # Note 3
        }

    def capture(self, storage):

        """
         this function capture screenshot and store image file into self.data
        """
        # capture date ( for e.g 20161212 )
        #self.date = time.strftime("%Y%m%d_%H%M", time.localtime())
        self.date = time.time()
        # make output filename
        self.abs_path = os.path.join(self.output, "screenshots", "{}_{}_{}.png".format(self.protocol, self.hostname, self.date))
        # print self.abs_path
        # try to capture file
        try:
            # custom capabalities like useragent in phantomjs
            options = dict(DesiredCapabilities.PHANTOMJS)
            self.useragent_raw = random.choice(self.useragent_strings[self.useragent_abr])
            options['phantomjs.page.settings.userAgent']=(self.useragent_raw)
            driver = webdriver.PhantomJS(desired_capabilities=options)
            driver.get("{}://{}:{}/".format(self.protocol, self.hostname, self.port))
            driver.save_screenshot(self.abs_path)
            self.image = driver.get_screenshot_as_png()
            driver.quit()
            # sleep to be sure that result saved successfully

            # read image file as byte and store in self.data
            try:
                if os.path.exists(self.abs_path):
                    self.log = "[+] Screenshot successfully saved in {}. \n".format(self.abs_path)
                    # example : ['https://ww.google.com:8800/', imagedata, "20151205"]
                    storage.append(
                        {'url':"{}://{}:{}/".format(self.protocol,self.hostname, self.port),
                         'image_path': self.abs_path,
                         'date': self.date}
                    )      # add data to storgae that provided by user ( because of using thread , using this technique we can read thread data)
                    print colored(self.log, 'green')
                self.data = [("{}://{}:/".format(self.protocol, self.hostname, self.port), self.image, self.date)]
                if(self.keep != True):
                    os.remove(self.abs_path)   # uncomment if you want to
                    self.log += "[+] {} removed successfully .\n".format(self.abs_path)
                    print colored(self.log, 'green')
            except Exception as e:
                print colored(e,'red')
                self.log = '[-] no image saved in {}'.format(self.abs_path)
                print colored(self.log, 'red')
                self.data = [(self.hostname, "NA", self.date)]
        except Exception as e:
            self.log = "[-] Cannot Start Process on {} because {}\n".format(self.hostname, e)
            print colored(self.log, 'red')
        try:
            f = open(self.logfile,"a")
            f.write(self.log+"\n")
            f.close()
        except Exception as e:
            print colored(e, 'red')
            print colored("[-] cannot open logfile: {}".format(self.logfile), 'red')


#o = screenshot("www.gmail.com", "/root/Desktop/url_information_gathering/lib/", "https", "443","/usr/local/bin/phantomjs", "/root/Desktop/url_information_gathering/lib/screen.js", keep=True  ,logfile= "/root/Desktop/url_information_gathering/lib/logfile.txt")
#o.capture()
