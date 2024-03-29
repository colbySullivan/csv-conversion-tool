# Data Conversion Utility Script

import pdfkit
import os
import csv
import sys
import time
import configparser
import getopt
import multiprocessing
from multiprocessing import Manager, Pool

def check_duplicates(file_path):
    """
    Traverses through given CSV file and puts all
    PDF files into a list so that they can be compared
    in convert()

    :return: list of PDF files without their extension type
    """ 
    current_files = [] #list of current pdf files to skip
    for filename in os.listdir(file_path):
        if filename.endswith('.pdf'): #Ignores pdf files
            new_filename = filename[:-3]
            current_files += [new_filename]
    return current_files     
    
def create_missing_dict(missing, set_of_services):
    """
    Finds the total number of services and 
    returns the devices that are missing that
    number of services

    :param missing: dict of services
    :param set_of_services: services for current client
    :return: set of devices missing all services
    """ 
    number_of_serverices = 0 #Total number of services
    for services in missing:
        if services in set_of_services:
            number_of_serverices+=1

    #Creates a list of devices that are missing all the services       
    set_of_all = [] #Set of devices with all services
    if number_of_serverices > 1:
        frequency = {}
        for service in set_of_services:
            if service in missing:
                for device in missing[service]:
                    if device in frequency:
                        frequency[device] += 1
                    else:
                        frequency[device] = 1
        for names in frequency:
            if frequency[names] == number_of_serverices:
                set_of_all += [names]
    return set_of_all

def write_html(file_path, html_buffer, missing, f, html_location):
    """
    Takes in a CSV file and converts it into
    an HTML file

    :param file_path: current csv file
    :param html_buffer: current csv file
    :param missing: dict were key is service and value is list of devices missing
    """ 
    config_file = configparser.ConfigParser()
    config_file.read('config.ini')

    #Add new services to this set and in the switch def
    set_of_services = {'huntress', 'sentinelone', 'cybercns-sec-vm', 'cb-cloud', 'sophos'} 
    missing['all'] = create_missing_dict(missing, set_of_services) #Set of devices missing all

    if not len(missing['all']) == 0:
        set_of_services.add('all')
    para_num = 0
    with open(os.path.join(file_path, html_buffer), 'w') as Func:
        Func.write("<html>\n<head>\n<title> \nDCUP</title>") #change title when needed
        Func.write("\n<meta hr {display: block; height: 1px; border: 0; border-top: 1px solid #ccc; margin: 1em 0; padding: 0;}>")
        Func.write("\n<style> ")
        Func.write("\nh2 {\nfont-family:  Century Gothic;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np1 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np2 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np3 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np4 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np5 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\n.column { float: left; width: 50%;}")
        Func.write("\n{box-sizing: border-box}")
        Func.write("\n.row:after \n{content: \"\"; \ndisplay: table; \nclear: both;}")
        Func.write("</style>")
        for key_to_lookup in missing:
            if key_to_lookup in set_of_services:
                if not len(key_to_lookup) == 0:
                    Func.write("\n</h2> <body><h2>" + config_file['SERVICES'][key_to_lookup] + "</h2><hr>\n")
                    if not len(missing[key_to_lookup]) == 0: 
                        Func.write("<div class =\"row\">") 
                        Func.write("<div class=\"column\" >") 
                        Func.write("<ul type = &bull>")
                        para_num = para_num + 1
                        Func.write("\n<p" + str(para_num) + ">")
                        j=0
                        for device in missing[key_to_lookup]:
                            #if not device in missing['all'] or key_to_lookup == 'all':
                            if j % 2 == 0:
                                Func.write("\n")
                                Func.write("<li>")
                                Func.write(device)
                            j+=1
                        Func.write("</p" + str(para_num) + ">")
                        Func.write("</div>") 
                        Func.write("</ul>")
                    j=0
                    Func.write("<div class =\"row\">") 
                    Func.write("<div class=\"column\" >") 
                    Func.write("<ul type = &bull>")
                    Func.write("<p" + str(para_num)  + ">")
                    if not len(missing[key_to_lookup]) == 0: 
                        for device in missing[key_to_lookup]:
                            #if not device in missing['all'] or key_to_lookup == 'all': 
                            if j % 2 == 1:
                                Func.write("\n")
                                Func.write("<li>")
                                Func.write(device)
                            j+=1
                Func.write("</ul>")
                Func.write("<p" + str(para_num) + ">")
                Func.write("</div>") #26
                Func.write("</div>") #22
        Func.write("\n</body></html>") #needs to be last line
        Func.close()
        create_pdf(f, html_location)

def create_pdf(current_file, html_location):
    """
    Takes in an HTML file and converts it into
    a PDF file

    :param current_file: string name of CSV file
    :param html_file: current HTML file
    """ 
    path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe' #Dependency needed for pdfkit
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    #Formats the csv to pdf
    buffer = current_file[:-3]
    pdf_file = buffer + "pdf"
    pdfkit.from_file(html_location, pdf_file, configuration=config)  #Utilizes the pdfkit API to convert the html to a pdf
    os.remove(html_location)

def convert(processed_count, file_path, process_type, shared_list, shared_int):
    """
    Traverses through a given directory and searches 
    for CSV files. For each file they are converted
    into PDF files based on the given process type.

    :param processed_count: counts file conversions
    :param file_path: given path to the CSV folder
    :param process_type: Smart, Abort, or Process
    :return: integer of files processed
    """ 

    #Checks for reprocess and smart
    if process_type == 'reprocess':
        current_files = []
    else:
        current_files = check_duplicates(file_path)

    # iterate over files in the given directory path
    for filename in os.listdir(file_path):
        buffer_filename = filename[:-3]
        if not buffer_filename in shared_list:
            shared_list += [buffer_filename]
            if buffer_filename not in current_files:
                if filename.endswith('.csv'): #Ignores pdf files
                    f = os.path.join(file_path, filename)
                    if os.path.isfile(f): # checking if it is a file
                        buffer = filename[:-3]
                        html_buffer = buffer + "html"
                        html_location = file_path + "\\" + html_buffer
                        print(filename) #Needed print
                        missing = find_missing_services(f)
                        write_html(file_path, html_buffer, missing, f, html_location)
                        shared_int.value +=1
            elif process_type == 'abort':
                print("A CSV file has already been processed aborting")
                

def find_missing_services(csv_file):
    """
    Traverses through a given CSV file and creates a
    dict where the service is the key and the missing
    devices are the value.

    :param processed_count: CSV file contain client devices
    :return: dict from CSV file
    """ 
    services = {}
    devices = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            device = row[0]
            services_data = row[1:]  # Remaining elements on the line

            devices.append(device)

            for service in services_data:
                if service.strip() != '':
                    services.setdefault(service, []).append(device)

    # List devices missing each service
    dict_missing = {}
    for service, missing_devices in services.items():
        present_devices = set(missing_devices)
        all_devices = set(devices)
        missing = all_devices - present_devices
        dict_missing[service] = missing
    return dict_missing
    
class CommandLine:
    def __init__(self):
        config_file = configparser.ConfigParser()
        config_file.read('config.ini')
        file_path = config_file['ARGS']['path']
        process_type = config_file['ARGS']['process']
        process_count = config_file['ARGS']['process_count']
        argv = sys.argv[1:]
        try:
            opts, arg = getopt.getopt(argv, "hf:p:c:", 
                                    ["file_path=",
                                        "process_type=",
                                        "process_count=",
                                        "help"])
        except:
            with open('usage.txt', 'r') as fin:
                    print(fin.read())
            #raise IOError("Argument dependency not met")
            sys.exit()
    
        for opt, arg in opts:
            if opt in ['-f', '--file_path']:
                file_path = arg
            elif opt in ['-p', '--process_type']:
                process_type = arg
            elif opt in ['-c', '--process_count']:
                process_count = arg
            elif opt in ['-h', '--help']:
                with open('usage.txt', 'r') as fin:
                    print(fin.read())
                sys.exit()
        convert_counter = 0 #Keeps track of files that have been converted
        shared_list = []
        manager = Manager()
        shared_list = manager.list()
        shared_int = manager.Value('i', 0)
        process_number = [multiprocessing.Process(target=convert, args=(convert_counter, file_path, process_type, shared_list, shared_int)) for x in range(int(process_count))]
        for p in process_number:
            p.start()
        tic = time.perf_counter()
        
        for p in process_number:
            p.join()
            
        toc = time.perf_counter()
        print("{}{}{:0.3f}{}".format(shared_int.value, ' files have been converted in ', toc - tic, ' seconds'))


if __name__ == '__main__':
    app = CommandLine()