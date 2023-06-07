# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os
import csv

def check_duplicates():
    current_files = [] #list of current pdf files to skip
    csv_directory = 'csvFolder'
    for filename in os.listdir(csv_directory):
        if filename.endswith('.pdf'): #Ignores pdf files
            new_filename = filename[:-3]
            current_files += [new_filename]
    return current_files


def convert(processed_count):
    csv_directory = 'csvFolder'

    # iterate over files in
    # that directory
    current_files = check_duplicates()
    for filename in os.listdir(csv_directory):
        buffer_filename = filename[:-3]
        if buffer_filename not in current_files:
            if filename.endswith('.csv'): #Ignores pdf files
                f = os.path.join(csv_directory, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    df1 = pd.read_csv(f)
                    html_file = df1.to_html() #Converts file to html
                    path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe' #Dependency needed for pdfit
                    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                    print(f) #Debug prints out file name
                    #Formats the csv to pdf
                    buffer = f[:-3]
                    pdf_file = buffer + "pdf"
                    #Utilies the pdfkit API to convert the html to a pdf
                    pdfkit.from_string(html_file, pdf_file, configuration=config)
                    processed_count+=1
    return processed_count
                

def find_missing_services(csv_file):
    services = {}
    devices = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for col in reader:
            device = col[0]
            op_sys = col[1]
            services_data = col[2:]  # Services

            devices.append(device)

            for service in services_data:
                if service.strip() != '' or False:
                    services.setdefault(service, []).append(device)

    # List devices missing each service
    for service, missing_devices in services.items():
        present_devices = set(missing_devices)
        all_devices = set(devices)
        missing = all_devices - present_devices
        print(f"Missing devices for service '{service}': {', '.join(sorted(missing))}")


def main():
    convert_counter = 0 #Keeps track of files that have been converted
    convert_counter = convert(convert_counter)
    print("{}{}".format(convert_counter, ' files have been converted'))
    
    # Usage
    csv_file = input("Enter the CSV file name: ")
    find_missing_services(csv_file)
    
                               
if __name__ == "__main__":
    # execute only if run as a script
    main()
