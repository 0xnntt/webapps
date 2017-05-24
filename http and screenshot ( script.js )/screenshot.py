import os
import subprocess
import time
import platform
from termcolor import colored

class screenshot:
    def __init__(self, hostname, output, protocol, port, logfile, phantomjs, script, keep=False):
        self.hostname = hostname
        self.logfile = logfile
        self.phantomjs_path = phantomjs
        self.script = script
        self.phantomjs_options = "--ignore-ssl-errors=true"
        self.output = output  # output folder that image should save in it
        self.protocol = protocol
        self.port = port
        self.abs_path = ""  # absolute path
        self.data = ''
        self.date = ''
        self.log = ""
        self.keep = keep
        self.image = ""

    def capture(self, storage):

        """
         this function capture screenshot and store image file into self.data
        """
        # capture date ( for e.g 20161212 )
        self.date = time.strftime("%Y%m%d_%H%M", time.localtime())
        # make output filename
        self.abs_path = os.path.join(self.output, "{}_{}_{}.png".format(self.protocol, self.hostname, self.date))
        # print self.abs_path
        # try to capture file
        try:
            # create no windows
            command = [ self.phantomjs_path, self.phantomjs_options, self.script,
                       "{}://{}:{}/".format(self.protocol, self.hostname, str(self.port)), self.abs_path]

            print colored(command, 'green')

            if(platform.system() == 'Windows'):
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call(command, startupinfo=si)
            elif(platform.system()=="Linux"):
                subprocess.call(command)
            else:
                print "Unknown OS"

            # sleep to be sure that result saved successfully
            time.sleep(5)

            # read image file as byte and store in self.data
            try:
                v = open(self.abs_path, 'rb')
                dt = v.read()
                v.close()
                if(len(dt) != 0):
                    self.log = "[+] Screenshot successfully saved in {}. \n".format(self.abs_path)
                    # example : ['https://ww.google.com:8800/', imagedata, "20151205"]
                    storage.append(
                        {'url':"{}://{}:{}/".format(self.protocol,self.hostname, self.port),
                         'raw_image':dt,
                         'date': self.date}
                    )      # add data to storgae that provided by user ( because of using thread , using this technique we can read thread data)
                    print colored(self.log, 'green')
                self.data = [("{}://{}:/".format(self.protocol, self.hostname, self.port), dt, self.date)]
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