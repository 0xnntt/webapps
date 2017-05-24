from project import  project
from optparse import   OptionParser
parser = OptionParser()
parser.add_option("-u","--useragent",dest="useragent",help="Specify user agent for sending request. default=desktop  :desktop|mobile " ,default="desktop")
parser.add_option("-p","--protocol",dest="protocol",help="Protocol (default=http): http | https ", default="http")
parser.add_option("-P","--port-number",dest="port",help="Port Number (default=80) ", default=80)
parser.add_option("-t","--threads",dest="threads",help="Number of Threads (default = 10): 10", default=10)
parser.add_option("-e","--each-step",dest="each_step",help="Number of URLs program should picks in every request (default=10) ",default=10)
parser.add_option("-i","--input-file",dest="input_file",help="Input .txt file .")
parser.add_option("-o","--output-folder",dest="output_folder",help="Output folder where files should be saved (default=output)",default="output")
parser.add_option("-T","--template",dest="template",help="sqlite3 database template for storing files there (default=db.db)" , default="db.db")
(options, args) = parser.parse_args()



b = [options.input_file, options.output_folder, options.port, options.protocol, options.each_step, options.template, options.threads, options.useragent]
if __name__ == "__main__":
    args_validate = 1
    for i in b:
        if(len(str(i)) == 0):
            print "use -h or --help for help"
        else:
            args_validate += 1
    if (args_validate) == 9:
        v = project(options.input_file,
                    options.output_folder,
                    options.port,
                    options.protocol,
                    options.each_step,
                    options.template,
                    options.threads,
                    options.useragent,
                    )
        v.save_to_db = True
        v.start()
