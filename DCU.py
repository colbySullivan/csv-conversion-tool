# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os
import csv
import sys
import time
import configparser

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

def write_html(file_path, html_buffer, missing):
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
    with open(os.path.join(file_path, html_buffer), 'w') as Func:
        Func.write("<html>\n<head>\n<title> \nDCUP</title>") #change title when needed
        Func.write("\n<meta hr {display: block; height: 1px; border: 0; border-top: 1px solid #ccc; margin: 1em 0; padding: 0;}>")
        Func.write("\n<style> ")
        Func.write("\nh2 {\nfont-family:  Century Gothic;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\np2 {\nfont-family:  Calibri;\n")
        Func.write("\nfont-weight: lighter}")
        Func.write("\n.column { float: left; width: 50%;}")
        Func.write("\n{box-sizing: border-box}")
        Func.write("\n.row:after \n{content: \"\"; \ndisplay: table; \nclear: both;}")
        Func.write("</style>")
        for key_to_lookup in missing:
            if key_to_lookup in set_of_services:
                if not len(key_to_lookup) == 0: #TODO check if this works
                    Func.write("\n</h2> <body><h2>" + config_file['SERVICES'][key_to_lookup] + "</h2><hr>")   # Fill in with whatever needs to be filled
                    if not len(missing[key_to_lookup]) == 0: 
                        Func.write("<div class =\"row\">") 
                        Func.write("<div class=\"column\" >") 
                        Func.write("<p>")
                        j=0
                        for device in missing[key_to_lookup]:
                            #if not device in missing['all'] or key_to_lookup == 'all':
                            if j % 2 == 0:
                                Func.write("\n")
                                Func.write("&bull; ")
                                Func.write(device)
                                Func.write("<br>")
                            j+=1
                        Func.write("</p>")
                        Func.write("</div>") 
                    j=0
                    Func.write("<div class =\"row\">") 
                    Func.write("<div class=\"column\" >") 
                    Func.write("<p2><br>")
                    if not len(missing[key_to_lookup]) == 0: 
                        for device in missing[key_to_lookup]:
                            #if not device in missing['all'] or key_to_lookup == 'all': 
                            if j % 2 == 1:
                                Func.write("\n")
                                Func.write("&bull; ")
                                Func.write(device)
                                Func.write("<br>")
                            j+=1

                Func.write("</p2>")
                Func.write("</div>") #26
                Func.write("</div>") #22
        Func.write("\n</body></html>") #needs to be last line
        Func.close()

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

def convert(processed_count, file_path, process_type):
    """
    Traverses through a given directory and searches 
    for CSV files. For each file they are converted
    into PDF files based on the given process type.

    :param processed_count: counts file conversions
    :param file_path: given path to the CSV folder
    :param process_type: Smart, Abort, or Process
    :return: integer of files processed
    """ 
    #file_path = 'csvFolder'

    #Checks for reprocess and smart
    if process_type == 'reprocess':
        current_files = []
    else:
        current_files = check_duplicates(file_path)

    # iterate over files in the given directory path
    for filename in os.listdir(file_path):
        buffer_filename = filename[:-3]
        if buffer_filename not in current_files:
            if filename.endswith('.csv'): #Ignores pdf files
                f = os.path.join(file_path, filename)
                if os.path.isfile(f): # checking if it is a file
                    print(filename) #Needed print
                    missing = find_missing_services(f)
                    buffer = filename[:-3]
                    html_buffer = buffer + "html"
                    html_location = file_path + "\\" + html_buffer
                    write_html(file_path, html_buffer, missing)
                    create_pdf(f, html_location)
                    processed_count+=1
        elif process_type == 'abort':
            print("A CSV file has already been processed aborting")
            return processed_count
    return processed_count
                

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
        if len(sys.argv) == 3:
            argument1 = sys.argv[1]
            argument2 = sys.argv[2]
        elif len(sys.argv) == 2:
            argument1 = sys.argv[1]
            argument2 = 'smart'
        else:
            raise Exception("\nMissing at least one argument \nArgument 1 is the path to the CSV file \nArgument 2 is optional and is the processing type")
        
        config_file = configparser.ConfigParser()
        config_file.read('config.ini')
        config_file['ARGS']['process'] = argument2
        argument1 = config_file['ARGS']['path']
        argument2 = config_file['ARGS']['process']
        print(config_file['SERVICES']['huntress'])
        #argument1 = create_config()

        convert_counter = 0 #Keeps track of files that have been converted
        tic = time.perf_counter()
        convert_counter = convert(convert_counter, argument1, argument2)
        toc = time.perf_counter()
        print("{}{}{:0.3f}{}".format(convert_counter, ' files have been converted in ', toc - tic, ' seconds'))


if __name__ == '__main__':
    app = CommandLine()