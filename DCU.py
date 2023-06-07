# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os

def convert():
    csv_directory = 'csvFolder'

    # iterate over files in
    # that directory
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            f = os.path.join(csv_directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                df1 = pd.read_csv(f)
                html_file = df1.to_html()
                path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                print(f)
                buffer = f[:-3]
                pdf_file = buffer + "pdf"
                pdfkit.from_string(html_file, pdf_file, configuration=config)
                
import csv

def find_missing_services(csv_file):
    services = {}
    devices = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            device = col[0]
            op_sys = col[1]
            services_data = col[2:]  # Services

            devices.append(device)

            for service in services_data:
                if service.strip() != '' or False:
                    services.setdefault(service, []).append(device)

    # List devices missing ALL services
    # for service, missing devices in services.items():
        

    # List devices missing each service
    for service, missing_devices in services.items():
        present_devices = set(missing_devices)
        all_devices = set(devices)
        missing = all_devices - present_devices
        print(f"Missing devices for service '{service}': {', '.join(sorted(missing))}")
        print("\n")


def main():
    convert()
    
    # Usage
    csv_file = input("Enter the CSV file name: ")
    find_missing_services(csv_file)
    
                               
if __name__ == "__main__":
    # execute only if run as a script
    main()
