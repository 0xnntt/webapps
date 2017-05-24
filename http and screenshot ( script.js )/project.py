import os
import glob
import sys
import pprint
from optparse import OptionParser
from url import URL
import threading
from time import sleep
import sys
import glob
import os
import sqlite3
from shutil import copyfile
from screenshot import screenshot
from termcolor import colored

def fetch_url(protocol, hostname, port, useragent, timeout, retries, storage=[]):
    url_obj = URL(protocol,hostname , str(port), useragent, timeout, retries)  # define url object
    url_obj.getdata()
    storage.append(url_obj.result)

def read_first_nline_pop(filename , n):
    v = []
    try:
        g = open(filename,"r")
        all = g.readlines()
        g.close()
        v = all[0:int(n)]
        try:
            g = open(filename,"w")
            print all[int(n):-1]
            g.writelines(all[int(n):-1])
            g.close()
        except Exception as e:
            print "cannot write outfile to ", output
            print e
    except Exception as e:
        print e
        print "cannot read file ", filename

    return v

def fetch_screen(protocol, hostname, port, output, logfile, phantomjs, phantomjs_script, keep, storage):
    b = screenshot(
            protocol=protocol,
            hostname=hostname,
            port=port,
            keep=keep,
            logfile=logfile,
            output=output,
            phantomjs=phantomjs,
            script=phantomjs_script,
            )
    b.capture(storage=storage)

class project:
    """ This class will define every project with its setting"""
    def __init__(self, input_file, output_folder, port, protocol, eachsteps, dbtemplate, threads, useragent, phantomjs, phantomjs_script, save_to_db=False):
        self.input = input_file
        self.output = output_folder
        self.threads = threads
        self.template = dbtemplate
        self.useragent = useragent
        self.eachsteps = eachsteps
        self.protocol = protocol
        self.save_to_db = save_to_db
        self.port = port
        self.name , self.ext = os.path.splitext(os.path.split(input_file)[-1])
        self.dbname = self.name + ".db"
        self.phantomjs = phantomjs
        self.phantomjs_script = phantomjs_script
        self.logfile = os.path.join(self.output, self.name, "logfile.log")
        self.keep = True


    def start(self):

        # 1. create output folder
        try:
            if not os.path.exists(os.path.join(self.output, self.name)):
                os.umask(0000)
                os.mkdir(os.path.join(self.output, self.name))

                # os.chmod( os.path.join(self.output, self.name) , 0777)
                # 2. copy template to project output folder ( output + projectname )
                try:
                    print colored("name: {}, output: {}, dbname: {}".format(self.name, self.output, self.dbname),"red")
                    copyfile(self.template, os.path.join(self.output, self.name, self.dbname))
                except Exception as e:
                    print "cannot copy template file into output folder "
                    print e
                    sys.exit(-1)
                # 3. create backup of input file
                try:
                    copyfile(self.input, self.input + ".backup")
                except Exception as e:
                    print "cannot create backup of input file"
                    print e
                    sys.exit(-1)
                # 4. read files from self.input path and execute each urls
                # all_urls = []  # all urls from input_file
                keep_going = True
                while (keep_going == True):         # main loop for reading and executing urls shots and data
                    # screenshot configuration
                    self.steps_data = []  # at first url headers and content fetched / then screenshot data will be added
                    self.screenshot_thread = 2
                    tmp_screenshot_data =[]

                    #first_slice_data = []
                    first_slice = read_first_nline_pop(self.input, self.eachsteps ) # write new file ( remaining)
                    try:
                        for i in first_slice:
                            b = open(self.input+".done","a")
                            print i
                            b.write(i)
                            b.close()
                    except Exception as e :
                        print colored("cannot write done urls to {}".format(self.input+".done"), 'red')
                        print e
                    if (len(first_slice) == 0):
                        keep_going = False
                    tmp_threads = []
                    screenshot_thread = []
                    for c in first_slice:
                        ps = threading.Thread(target=fetch_screen,
                                              args=(self.protocol,
                                                    c.strip(),
                                                    self.port,
                                                    os.path.join(self.output, self.name),
                                                    self.logfile,
                                                    self.phantomjs,
                                                    self.phantomjs_script,
                                                    self.keep,
                                                    tmp_screenshot_data
                                                    )

                                              )
                        screenshot_thread.append(ps)

                    for i in first_slice:
                        process = threading.Thread(target=fetch_url,
                                                   args=(self.protocol,
                                                         i.strip(),
                                                         self.port,
                                                         self.useragent,
                                                         5,  # timeout
                                                         5,
                                                         self.steps_data)  # retries
                                                   )
                        tmp_threads.append(process)
                    for t in screenshot_thread:
                        try:
                            t.start()
                        except Exception as  e:
                            print e
                            print "cannot start screenshot process"
                    for k in tmp_threads:
                        try:
                            k.start()
                            sleep(1 / self.threads)
                        except Exception as e:
                            print e
                            print "cannot start thread."
                    for r in tmp_threads:
                        r.join(10)
                    for t in screenshot_thread:
                        t.join(10)

                    if(self.save_to_db == True):
                        try:
                            # after this double loops we have a list of n=each_steps length dictionaries
                            for i in self.steps_data:
                                for j in tmp_screenshot_data:
                                    if(i['url'] == j['url']):
                                        i['data']['screenshot'] = j['raw_image']
                                        i['data']['screenshot_date'] = j['date']
                                        #pp = pprint.PrettyPrinter(indent=4)
                                        #pp.pprint(i)
                                        conn = sqlite3.connect(os.path.join(self.output, self.name, self.dbname))
                                        c = conn.cursor()
                                        conn.text_factory = str
                                        c.executemany(
                                        "INSERT INTO urls (protocol,hostname,port,has_ssl,useragent,ctime,date,status_code,status,content,http_header,certificate,screenshot,screenshot_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                            [(i['data']['protocol'],
                                             i['data']['hostname'],
                                             i['data']['port'],
                                             i['data']['has_ssl'],
                                             i['data']['useragent'],
                                             i['data']['ctime'],
                                             i['data']['date'],
                                             i['data']['status_code'],
                                             i['data']['status'],
                                             i['data']['content'],
                                             i['data']['headers'],
                                             i['data']['certificate'],
                                             i['data']['screenshot'],
                                             i['data']['screenshot_date'])
                                             ]
                                        )
                                        conn.commit()
                                        conn.close()
                        except Exception as e:
                            print e
                            print "Cannot INSERT data into {}".format(os.path.join(self.output, self.name, self.dbname))
            else:
                print colored("The output folder should not exist , please remove it using : \nrm -rf {} \nand try again.".format(os.path.join(self.output, self.name)),'red')
                sys.exit(0)
        except Exception as e:
            print e
            print "cannot create phase directory", self.name
