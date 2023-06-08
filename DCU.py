# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os
import csv
import sys

def check_duplicates():
    """
    Traverses through given CSV file and puts all
    PDF files into a list so that they can be compared
    in convert()

    :return: list of PDF files without their extension type
    """ 
    current_files = [] #list of current pdf files to skip
    csv_directory = 'csvFolder'
    for filename in os.listdir(csv_directory):
        if filename.endswith('.pdf'): #Ignores pdf files
            new_filename = filename[:-3]
            current_files += [new_filename]
    return current_files


def create_html(f):
    """
    Takes in a CSV file and converts it into
    an HTML file

    :param f: current csv file
    :return: converted html file
    """ 
    df1 = pd.read_csv(f)
    return df1.to_html() #Converts file to html
    #TODO we can edit the html here

def create_pdf(current_file, html_file):
    """
    Takes in an HTML file and converts it into
    a PDF file

    :param current_file: string name of CSV file
    :param html_file: current HTML file
    """ 
    print(current_file)
    path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe' #Dependency needed for pdfkit
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    #Formats the csv to pdf
    buffer = current_file[:-3]
    pdf_file = buffer + "pdf"
    pdfkit.from_string(html_file, pdf_file, configuration=config)  #Utilizes the pdfkit API to convert the html to a pdf


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
        current_files = check_duplicates()

    # iterate over files in the given directory path
    for filename in os.listdir(file_path):
        buffer_filename = filename[:-3]
        if buffer_filename not in current_files:
            if filename.endswith('.csv'): #Ignores pdf files
                f = os.path.join(file_path, filename)
                if os.path.isfile(f): # checking if it is a file
                    html_file = create_html(f)
                    create_pdf(f, html_file)
                    processed_count+=1
        elif process_type == 'abort':
            print("abort")
            return processed_count
    return processed_count
                

def find_missing_services(csv_file):
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
    for service, missing_devices in services.items():
        present_devices = set(missing_devices)
        all_devices = set(devices)
        missing = all_devices - present_devices
        print(f"Missing devices for service '{service}': {', '.join(sorted(missing))}")
    
                               
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
        convert_counter = 0 #Keeps track of files that have been converted
        convert_counter = convert(convert_counter, argument1, argument2)
        print("{}{}".format(convert_counter, ' files have been converted'))
    
    # Usage
    csv_file = input("Enter the CSV file name: ")
    find_missing_services(csv_file) 


if __name__ == '__main__':
    app = CommandLine()