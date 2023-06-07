# Data Conversion Utility Script

import pandas as pd
import pdfkit
import os

def addToPDF(html_file, pdf_file, config):
    pdf_directory = 'pdfFolder'
    os.path.join(pdf_directory, filename)
    pdfkit.from_string(html_file, pdf_file, configuration=config)
        # checking if it is a file
        #if os.path.isfile(f):
           

def convert():
    csv_directory = 'csvFolder'
    pdf_directory = 'pdfFolder'

    # iterate over files in
    # that directory
    for filename in os.listdir(csv_directory):
        f = os.path.join(csv_directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            df1 = pd.read_csv(f)
            html_file = df1.to_html()
            path_wkhtmltopdf = r'wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            buffer = f[:-3]
            pdf_file = buffer + "pdf"
            addToPDF(html_file, pdf_file, config)

def main():
    convert()
    
                               
if __name__ == "__main__":
    # execute only if run as a script
    main()